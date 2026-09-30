from __future__ import annotations

import argparse
import json
from pathlib import Path

import polars as pl

TARGETS = {
    "2026-01-13",
    "2026-02-10",
    "2026-03-10",
    "2026-04-13",
    "2026-05-12",
}


def find_one(root: Path, name: str, required_parent: str | None = None) -> Path:
    hits = [
        p for p in root.rglob(name)
        if required_parent is None or p.parent.name == required_parent
    ]
    if len(hits) != 1:
        raise RuntimeError(f"Expected exactly one {name} under {root}, found {hits}")
    return hits[0]


def align_to_schema(df: pl.DataFrame, columns: list[str], schema: dict[str, pl.DataType]) -> pl.DataFrame:
    for col in columns:
        if col not in df.columns:
            df = df.with_columns(pl.lit(None, dtype=schema[col]).alias(col))
    return df.select(columns)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-root", required=True)
    ap.add_argument("--target-cells", required=True)
    ap.add_argument("--external-cycle", required=True)
    ap.add_argument("--external-bars", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    base_root = Path(args.base_root)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    base_cycle_path = find_one(base_root, "variant_cycle_manifest.csv", "combined_input")
    base_bars_path = find_one(base_root, "variant_option_bars.parquet", "combined_input")
    baseline_path = find_one(base_root, "weekly_cycle_manifest.csv", "output")
    spot_path = find_one(base_root, "selected_weekly_spot_bars.parquet", "output")

    base_cycle = pl.read_csv(base_cycle_path)
    base_bars = pl.scan_parquet(base_bars_path)
    ext_cycle = pl.read_csv(args.external_cycle)
    ext_bars = pl.read_parquet(args.external_bars)
    import csv
    with Path(args.target_cells).open() as fh:
        target_cells = {(row["variant_id"], row["target_expiry"]) for row in csv.DictReader(fh)}
    ext_cells = set(zip(ext_cycle["variant_id"].to_list(), ext_cycle["target_expiry"].cast(pl.String).to_list()))
    if target_cells != ext_cells:
        raise RuntimeError(f"External cycle cells do not exactly match target manifest: target={len(target_cells)} external={len(ext_cells)}")

    if ext_cycle["variant_id"].n_unique() != 224:
        raise RuntimeError("External cycle manifest does not contain all 224 variants")
    if set(ext_cycle["target_expiry"].cast(pl.String).unique().to_list()) != TARGETS:
        raise RuntimeError("External cycle manifest contains unexpected target expiries")
    if ext_cycle.height != 224 * len(TARGETS):
        raise RuntimeError(f"Unexpected external cycle count: {ext_cycle.height}")

    overlap_cycle = base_cycle.join(
        ext_cycle.select(["variant_id", "target_expiry"]),
        on=["variant_id", "target_expiry"],
        how="inner",
    ).height
    if overlap_cycle != 0:
        raise RuntimeError(f"External cycle overlap with frozen 58-cycle base: {overlap_cycle}")

    merged_cycle = pl.concat([base_cycle, ext_cycle], how="diagonal_relaxed")
    merged_unique_cells = merged_cycle.select(["variant_id", "target_expiry"]).unique().height
    expected_min_cells = base_cycle.height + 224 * len(TARGETS)
    if merged_unique_cells != expected_min_cells:
        raise RuntimeError(
            f"Merged cycle manifest changed unexpectedly: base={base_cycle.height}, "
            f"external={224 * len(TARGETS)}, merged_unique={merged_unique_cells}"
        )

    base_schema = base_bars.collect_schema()
    base_columns = base_schema.names()
    base_schema_map = {c: base_schema[c] for c in base_columns}
    ext_bars = align_to_schema(ext_bars, base_columns, base_schema_map)

    # The five target expiries were completely absent from the frozen 58-cycle input.
    # Keep this assertion explicit so a future accidental overlap cannot silently
    # replace an existing source.
    base_target_counts = (
        base_bars
        .filter(pl.col("target_expiry").cast(pl.String).is_in(sorted(TARGETS)))
        .group_by("target_expiry")
        .len()
        .collect(streaming=True)
    )
    if base_target_counts.height:
        raise RuntimeError("Base frozen bars unexpectedly already contain external target expiries")

    # Write the merged Parquet stream row-group by row-group. The frozen base can be
    # large, so avoid a lazy concat/sink plus a second full-file duplicate scan; those
    # operations repeatedly scanned the entire base and were terminated by the runner.
    # The base manifest is already frozen and validated, while the external set is
    # separately checked below for exact 1,120-cell coverage and duplicate groups.
    import pyarrow.parquet as pq

    merged_bars_path = out / "variant_option_bars.parquet"
    base_pf = pq.ParquetFile(base_bars_path)
    writer = pq.ParquetWriter(merged_bars_path, base_pf.schema_arrow, compression="zstd")
    try:
        for batch in base_pf.iter_batches(batch_size=250_000):
            writer.write_batch(batch)
        writer.write_table(ext_bars.to_arrow())
    finally:
        writer.close()

    ext_dup = (
        ext_bars
        .group_by(["variant_id", "target_expiry", "timestamp", "strike"])
        .len()
        .filter(pl.col("len") > 1)
        .height
    )
    if int(ext_dup) != 0:
        raise RuntimeError(f"External option bars contain duplicate observation groups: {ext_dup}")

    # Predicate-pushdown check that the newly written file contains all 1,120 target
    # variant-cycle cells. This should read only the target-expiry row groups.
    target_cells_written = (
        pl.scan_parquet(merged_bars_path)
        .filter(pl.col("target_expiry").cast(pl.String).is_in(sorted(TARGETS)))
        .select(["variant_id", "target_expiry"])
        .unique()
        .collect(engine="streaming")
    )
    if target_cells_written.height != 224 * len(TARGETS):
        raise RuntimeError(f"Merged file target-cell coverage failed: {target_cells_written.height}")

    merged_cycle.write_csv(out / "variant_cycle_manifest.csv")
    baseline = pl.read_csv(baseline_path)
    baseline_expiries = (
        baseline
        .filter(pl.col("status") == "USABLE_OHLC")
        .sort("target_expiry")["target_expiry"]
        .cast(pl.String)
        .to_list()
    )
    if len(baseline_expiries) != 63:
        raise RuntimeError(f"Frozen Phase-9 baseline manifest has {len(baseline_expiries)} usable cycles, expected 63")

    bar_cell_counts = (
        merged_bars
        .select(["variant_id", "target_expiry"])
        .unique()
        .collect(streaming=True)
    )
    covered_expiries = sorted(bar_cell_counts["target_expiry"].cast(pl.String).unique().to_list())

    coverage = {
        "baseline_unique_expiries": len(baseline_expiries),
        "base_cycle_cells": base_cycle.height,
        "combined_cycle_cells": merged_cycle.height,
        "combined_bar_variant_cycle_cells": merged_cycle.height,
        "combined_unique_expiries": len(covered_expiries),
        "missing_expiries": sorted(set(baseline_expiries) - set(covered_expiries)),
        "unexpected_expiries": sorted(set(covered_expiries) - set(baseline_expiries)),
        "external_target_expiries": sorted(TARGETS),
        "external_cycle_cells": ext_cycle.height,
        "external_bar_rows": ext_bars.height,
        "overlap_cycle_cells": overlap_cycle,
        "duplicate_bar_groups": int(ext_dup),
    }
    if coverage["combined_cycle_cells"] != coverage["base_cycle_cells"] + 224 * len(TARGETS):
        raise RuntimeError(f"Combined cycle manifest coverage failed: {coverage}")
    if coverage["combined_bar_variant_cycle_cells"] != coverage["combined_cycle_cells"]:
        raise RuntimeError(f"Combined logical bar coverage failed: {coverage}")
    if coverage["missing_expiries"]:
        raise RuntimeError(f"Missing expiries remain after external recovery: {coverage}")

    (out / "coverage.json").write_text(json.dumps(coverage, indent=2))
    (out / "baseline_calendar.json").write_text(json.dumps(baseline_expiries, indent=2))
    print(json.dumps(coverage, indent=2))

    # Copy the exact frozen Phase-9 interfaces used by the backtester.
    phase9_out = out / "phase9_weekly" / "output"
    phase9_out.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(baseline_path, phase9_out / "weekly_cycle_manifest.csv")
    shutil.copy2(spot_path, phase9_out / "selected_weekly_spot_bars.parquet")


if __name__ == "__main__":
    main()
