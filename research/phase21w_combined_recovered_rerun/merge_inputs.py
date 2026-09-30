from __future__ import annotations
import argparse, json
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

ap=argparse.ArgumentParser()
ap.add_argument("--hf3-dir",required=True); ap.add_argument("--hf2-dir",required=True)
ap.add_argument("--manifest",required=True); ap.add_argument("--out-dir",required=True)
a=ap.parse_args()
hf3=Path(a.hf3_dir); hf2=Path(a.hf2_dir); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
manifest=pl.read_csv(a.manifest).with_columns(pl.col("target_expiry").cast(pl.String))
frozen=set(manifest["target_expiry"].to_list())

c3=pl.read_csv(hf3/"variant_cycle_manifest.csv").with_columns(pl.col("target_expiry").cast(pl.String))
c2=pl.read_csv(hf2/"hf2_recovered_variant_cycles.csv").with_columns(pl.col("target_expiry").cast(pl.String))
e3=set(c3["target_expiry"].unique().to_list())
c2=c2.filter(~pl.col("target_expiry").is_in(list(e3)))
combined=pl.concat([c3,c2],how="diagonal_relaxed")
if combined.height != combined.select(["variant_id","target_expiry"]).n_unique():
    raise RuntimeError("Duplicate variant-cycle keys after source merge")
if not set(combined["target_expiry"].unique().to_list()).issubset(frozen):
    raise RuntimeError("Merged input contains expiries outside frozen 63-cycle calendar")

b3=hf3/"variant_option_bars.parquet"; b2=hf2/"hf2_recovered_variant_option_bars.parquet"
out_bars=out/"variant_option_bars.parquet"

schema3=pq.read_schema(b3); schema2=pq.read_schema(b2)
names=list(schema3.names)
if names != list(schema2.names):
    raise RuntimeError(f"Option-bar schemas differ: {names} vs {list(schema2.names)}")
# Source files are already validated independently; source precedence is disjoint by expiry.
writer=pq.ParquetWriter(out_bars,schema3,compression="zstd")
n3=n2=0
try:
    for batch in pq.ParquetFile(b3).iter_batches():
        writer.write_batch(batch); n3 += batch.num_rows
    for batch in pq.ParquetFile(b2).iter_batches():
        writer.write_batch(batch); n2 += batch.num_rows
finally:
    writer.close()

coverage=combined.group_by("target_expiry").agg(
    pl.len().alias("variant_rows"),
    (pl.col("status")=="USABLE_OHLC").sum().alias("usable_variant_rows"),
).sort("target_expiry")
coverage.write_csv(out/"combined_cycle_coverage.csv")
combined.write_csv(out/"variant_cycle_manifest.csv")
summary={
    "frozen_cycles":len(frozen),
    "hf3_expiries":len(e3),
    "hf2_added_expiries":len(set(c2["target_expiry"].unique().to_list())),
    "combined_rows":combined.height,
    "combined_usable_variant_cycles":combined.filter(pl.col("status")=="USABLE_OHLC").height,
    "hf3_bar_rows":n3,
    "hf2_bar_rows":n2,
    "combined_bar_rows":n3+n2,
    "fully_covered_expiries":coverage.filter(pl.col("usable_variant_rows")==224).height,
    "partial_or_zero_expiries":coverage.filter(pl.col("usable_variant_rows")<224).height,
}
(out/"input_validation.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
