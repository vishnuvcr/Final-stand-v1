from pathlib import Path
import polars as pl, json
hf03=Path('phase21w_combined_frozen_rerun/hf03_build')
if not (hf03/'variant_cycle_manifest.csv').exists():
    candidates=list(Path('.').glob('**/hf03_build/variant_cycle_manifest.csv'))
    if not candidates: raise FileNotFoundError('Prepared HF03 interface not found after artifact extraction')
    hf03=candidates[0].parent
hf2=Path('research/phase20w_executable_bar_recovery/output')
out=Path('research/phase21w_combined_frozen_rerun/combined_input'); out.mkdir(parents=True,exist_ok=True)
c3=pl.read_csv(hf03/'variant_cycle_manifest.csv'); b3=pl.read_parquet(hf03/'variant_option_bars.parquet')
c2=pl.read_csv(hf2/'hf2_recovered_variant_cycles.csv').filter(pl.col('status')=='USABLE_OHLC')
b2=pl.read_parquet(hf2/'hf2_recovered_variant_option_bars.parquet')
if 'expiry' not in b2.columns: b2=b2.with_columns(pl.col('target_expiry').alias('expiry'))
key=['variant_id','target_expiry']
overlap=c2.join(c3.select(key),on=key,how='inner').height
if overlap: raise RuntimeError(f'Unexpected HF03/HF02 overlap: {overlap}')
for col in c3.columns:
    if col not in c2.columns:
        c2=c2.with_columns(pl.lit(None).alias(col))
c2=c2.select(c3.columns)
c=pl.concat([c3,c2],how='diagonal_relaxed').unique(subset=key,keep='first')
meta=c2.select(['variant_id','target_expiry','entry_timestamp','lock_timestamp','k3_multiplier']).unique()
b2=b2.join(meta,on=key,how='left')
if 'oi' in b2.columns: b2=b2.rename({'oi':'open_interest'})
if 'trading_day' not in b2.columns: b2=b2.with_columns(pl.col('timestamp').str.slice(0,10).alias('trading_day'))
if 'symbol' not in b2.columns: b2=b2.with_columns(pl.lit('NIFTY').alias('symbol'))
if 'option_type' not in b2.columns: b2=b2.with_columns(pl.lit('CE').alias('option_type'))
if 'option_type' not in b2.columns: b2=b2.with_columns(pl.lit('CALL').alias('option_type'))
missing=[x for x in b3.columns if x not in b2.columns]
if missing: raise RuntimeError(f'Unmapped HF2 schema columns: {missing}')
b2=b2.select(b3.columns,strict=False)
b=pl.concat([b3,b2],how='diagonal_relaxed')
dups=b.group_by(['variant_id','target_expiry','timestamp','strike']).len().filter(pl.col('len')>1)
if dups.height: raise RuntimeError(f'Duplicate option observations: {dups.height}')
c.write_csv(out/'variant_cycle_manifest.csv'); b.write_parquet(out/'variant_option_bars.parquet',compression='zstd')
coverage={'hf03_cycle_cells':c3.height,'hf2_usable_cycle_cells':c2.height,'combined_cycle_cells':c.height,'combined_unique_expiries':c['target_expiry'].n_unique(),'combined_coverage_fraction':c.height/(224*63),'overlap_cells':overlap}
(out/'coverage.json').write_text(json.dumps(coverage,indent=2)); print(json.dumps(coverage,indent=2))
# Phase 21 execution trigger: frozen adapter logic unchanged.
