import json
from pathlib import Path
import polars as pl
base=json.loads(Path("research/phase19w_recovered_rerun/output/baseline_calendar.json").read_text())
trade=pl.read_csv("research/phase19w_recovered_rerun/output/trades_ITM3_NEXT1_K3M4.csv")
got=set(trade["target_expiry"].cast(pl.String).to_list())
missing=[x for x in base if x not in got]
vc=pl.read_csv("research/phase19w_recovered_rerun/output/variant_cycle_manifest.csv")
vc=vc.with_columns(pl.col("target_expiry").cast(pl.String))
overlap=vc.filter(pl.col("target_expiry").is_in(missing))
Path("research/phase20w_executable_bar_recovery/output/manifest_diagnostic.json").write_text(json.dumps({"vc_rows":vc.height,"vc_unique_variants":vc["variant_id"].n_unique(),"vc_unique_expiries":vc["target_expiry"].n_unique(),"missing_cycles":missing,"overlap_rows":overlap.height,"overlap_unique_expiries":overlap["target_expiry"].n_unique()},indent=2))
overlap.select(["variant_id","target_expiry","entry_timestamp","lock_timestamp","k1","k2","k3"]).write_csv("research/phase20w_executable_bar_recovery/output/required_missing_variant_bars.csv")
print(json.dumps({"vc_rows":vc.height,"missing":len(missing),"overlap_rows":overlap.height,"overlap_expiries":overlap["target_expiry"].n_unique()}))
