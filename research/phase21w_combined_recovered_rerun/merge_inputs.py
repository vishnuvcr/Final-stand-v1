from __future__ import annotations
import argparse, json
from pathlib import Path
import polars as pl

ap=argparse.ArgumentParser()
ap.add_argument("--hf3-dir",required=True)
ap.add_argument("--hf2-dir",required=True)
ap.add_argument("--manifest",required=True)
ap.add_argument("--out-dir",required=True)
a=ap.parse_args()
hf3=Path(a.hf3_dir); hf2=Path(a.hf2_dir); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)

manifest=pl.read_csv(a.manifest).with_columns(pl.col("target_expiry").cast(pl.String))
frozen=manifest["target_expiry"].to_list()

c3=pl.read_csv(hf3/"variant_cycle_manifest.csv").with_columns(pl.col("target_expiry").cast(pl.String))
c2=pl.read_csv(hf2/"hf2_recovered_variant_cycles.csv").with_columns(pl.col("target_expiry").cast(pl.String))
# Deterministic precedence: HF-03 for cycles it covers; HF-02 only for cycles absent from HF-03.
e3=set(c3["target_expiry"].unique().to_list())
c2=c2.filter(~pl.col("target_expiry").is_in(list(e3)))
combined=pl.concat([c3,c2],how="diagonal_relaxed")

if combined.select(["variant_id","target_expiry"]).n_unique()!=combined.height:
    raise RuntimeError("Duplicate variant-cycle keys after source merge")
if not set(combined["target_expiry"].unique().to_list()).issubset(set(frozen)):
    raise RuntimeError("Merged input contains expiry dates outside frozen 63-cycle calendar")

b3=pl.read_parquet(hf3/"variant_option_bars.parquet").with_columns(
    pl.col("timestamp").cast(pl.String).str.replace(r" ","T").str.slice(0,19),
    pl.col("strike").cast(pl.Float64)
)
b2=pl.read_parquet(hf2/"hf2_recovered_variant_option_bars.parquet").with_columns(
    pl.col("timestamp").cast(pl.String).str.replace(r" ","T").str.slice(0,19),
    pl.col("strike").cast(pl.Float64)
)
b2=b2.filter(pl.col("target_expiry").is_in(list(c2["target_expiry"].unique())))
bars=pl.concat([b3,b2],how="diagonal_relaxed")
dups=bars.group_by(["variant_id","target_expiry","timestamp","strike"]).len().filter(pl.col("len")>1)
if dups.height:
    raise RuntimeError(f"Duplicate executable bars detected: {dups.height}")
# Source provenance summary.
coverage=(combined.group_by("target_expiry").agg(pl.len().alias("variant_rows"),(pl.col("status")=="USABLE_OHLC").sum().alias("usable_variant_rows")).sort("target_expiry"))
coverage.write_csv(out/"combined_cycle_coverage.csv")
combined.write_csv(out/"variant_cycle_manifest.csv")
bars.write_parquet(out/"variant_option_bars.parquet",compression="zstd")
summary={
 "frozen_cycles":len(frozen),
 "hf3_expiries":len(e3),
 "hf2_added_expiries":len(set(c2["target_expiry"].unique().to_list())),
 "combined_rows":combined.height,
 "combined_usable_variant_cycles":combined.filter(pl.col("status")=="USABLE_OHLC").height,
 "combined_bar_rows":bars.height,
 "hf3_bar_rows":b3.height,
 "hf2_bar_rows":b2.height,
 "fully_covered_expiries":coverage.filter(pl.col("usable_variant_rows")==224).height,
 "partial_or_zero_expiries":coverage.filter(pl.col("usable_variant_rows")<224).height,
}
(out/"input_validation.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
