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

    merged_bars_path = out / "variant_option_bars.parquet"
    pl.concat([base_bars, ext_bars.lazy()], how="vertical_relaxed").sink_parquet(
        merged_bars_path,
        compression="zstd",
        maintain_order=False,
    )

    merged_bars = pl.scan_parquet(merged_bars_path)
    dup = (
        merged_bars
        .group_by(["variant_id", "target_expiry", "timestamp", "strike"])
        .len()
        .filter(pl.col("len") > 1)
        .select(pl.len())
        .collect(streaming=True)
        .item()
    )
    if int(dup) != 0:
        raise RuntimeError(f"Merged option bars contain duplicate observation groups: {dup}")

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
        "combined_bar_variant_cycle_cells": bar_cell_counts.height,
        "combined_unique_expiries": len(covered_expiries),
        "missing_expiries": sorted(set(baseline_expiries) - set(covered_expiries)),
        "unexpected_expiries": sorted(set(covered_expiries) - set(baseline_expiries)),
        "external_target_expiries": sorted(TARGETS),
        "external_cycle_cells": ext_cycle.height,
        "external_bar_rows": ext_bars.height,
        "overlap_cycle_cells": overlap_cycle,
        "duplicate_bar_groups": int(dup),
    }
    if coverage["combined_cycle_cells"] != coverage["base_cycle_cells"] + 224 * len(TARGETS):
        raise RuntimeError(f"Combined cycle manifest coverage failed: {coverage}")
    if coverage["combined_bar_variant_cycle_cells"] != coverage["combined_cycle_cells"]:
        raise RuntimeError(f"Combined bar coverage failed: {coverage}")
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
