from pathlib import Path
import polars as pl, json

hf03=Path('phase21w_combined_frozen_rerun/hf03_build')
if not (hf03/'variant_cycle_manifest.csv').exists():
    candidates=list(Path('.').glob('**/hf03_build/variant_cycle_manifest.csv'))
    if not candidates:
        raise FileNotFoundError('Prepared HF03 interface not found after artifact extraction')
    hf03=candidates[0].parent

hf2=Path('research/phase20w_executable_bar_recovery/output')
out=Path('research/phase21w_combined_frozen_rerun/combined_input')
out.mkdir(parents=True,exist_ok=True)

c3=pl.read_csv(hf03/'variant_cycle_manifest.csv')
c2=pl.read_csv(hf2/'hf2_recovered_variant_cycles.csv').filter(pl.col('status')=='USABLE_OHLC')
baseline=pl.read_csv('research/phase9_weekly/output/weekly_cycle_manifest.csv').filter(pl.col('status')=='USABLE_OHLC').head(63)
baseline_expiries=sorted(baseline['target_expiry'].cast(pl.String).to_list())
key=['variant_id','target_expiry']
overlap=c2.join(c3.select(key),on=key,how='inner').height
if overlap:
    raise RuntimeError(f'Unexpected HF03/HF02 overlap: {overlap}')
for col in c3.columns:
    if col not in c2.columns:
        c2=c2.with_columns(pl.lit(None).alias(col))
c2=c2.select(c3.columns)
c=pl.concat([c3,c2],how='diagonal_relaxed').unique(subset=key,keep='first')
covered_expiries=sorted(c['target_expiry'].cast(pl.String).unique().to_list())
unexpected_expiries=sorted(set(covered_expiries)-set(baseline_expiries))
missing_expiries=sorted(set(baseline_expiries)-set(covered_expiries))
if unexpected_expiries:
    raise RuntimeError(f'Combined input contains non-baseline expiries: {unexpected_expiries}')

# Keep the large option tables lazy/streaming. Eagerly loading both source
# parquets caused runner shutdowns during schema adaptation.
b3_path=hf03/'variant_option_bars.parquet'
b2_path=hf2/'hf2_recovered_variant_option_bars.parquet'
b3_lf=pl.scan_parquet(b3_path)
b2_lf=pl.scan_parquet(b2_path)
b3_cols=b3_lf.collect_schema().names()
b2_cols=set(b2_lf.collect_schema().names())

if 'expiry' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.col('target_expiry').alias('expiry'))
    b2_cols.add('expiry')
if 'oi' in b2_cols and 'open_interest' not in b2_cols:
    b2_lf=b2_lf.rename({'oi':'open_interest'})
    b2_cols.discard('oi'); b2_cols.add('open_interest')
if 'trading_day' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.col('timestamp').cast(pl.String).str.slice(0,10).alias('trading_day'))
    b2_cols.add('trading_day')
if 'symbol' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.lit('NIFTY').alias('symbol'))
    b2_cols.add('symbol')
if 'option_type' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.lit('CE').alias('option_type'))
    b2_cols.add('option_type')

# Reconstruct the three repeated HF03 metadata fields without joining the
# multi-million-row bar table to cycle metadata.
meta=c2.select(['variant_id','target_expiry','entry_timestamp','lock_timestamp']).unique(subset=key)
entry_map=dict(zip(meta['target_expiry'].to_list(),meta['entry_timestamp'].to_list()))
lock_map=dict(zip(meta['target_expiry'].to_list(),meta['lock_timestamp'].to_list()))
if 'entry_timestamp' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.col('target_expiry').cast(pl.String).replace_strict(entry_map,return_dtype=pl.String).alias('entry_timestamp'))
    b2_cols.add('entry_timestamp')
if 'lock_timestamp' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.col('target_expiry').cast(pl.String).replace_strict(lock_map,return_dtype=pl.String).alias('lock_timestamp'))
    b2_cols.add('lock_timestamp')
if 'k3_multiplier' not in b2_cols:
    b2_lf=b2_lf.with_columns(pl.col('variant_id').str.extract(r'K3M([0-9]+(?:\.[0-9]+)?)$',1).cast(pl.Float64).alias('k3_multiplier'))
    b2_cols.add('k3_multiplier')

missing=[x for x in b3_cols if x not in b2_cols]
if missing:
    raise RuntimeError(f'Unmapped HF2 schema columns: {missing}')

required_metadata=['entry_timestamp','lock_timestamp','k3_multiplier']
null_meta=b2_lf.select([
    pl.col('entry_timestamp').is_null().sum().alias('null_entry_timestamp'),
    pl.col('lock_timestamp').is_null().sum().alias('null_lock_timestamp'),
    pl.col('k3_multiplier').is_null().sum().alias('null_k3_multiplier'),
]).collect(streaming=True).row(0)
if any(int(x)>0 for x in null_meta):
    raise RuntimeError(f'HF2 metadata reconstruction produced nulls: entry={null_meta[0]}, lock={null_meta[1]}, k3={null_meta[2]}')

# Source-local duplicate checks remain, but operate as lazy streaming queries.
dups3=int(b3_lf.group_by(['variant_id','target_expiry','timestamp','strike']).len().filter(pl.col('len')>1).select(pl.len()).collect(streaming=True).item())
dups2=int(b2_lf.group_by(['variant_id','target_expiry','timestamp','strike']).len().filter(pl.col('len')>1).select(pl.len()).collect(streaming=True).item())
if dups3 or dups2:
    raise RuntimeError(f'Duplicate option observations: HF03={dups3}, HF02={dups2}')

norm_path=out/'hf2_normalized_variant_option_bars.parquet'
combined_path=out/'variant_option_bars.parquet'
norm_path.unlink(missing_ok=True)
combined_path.unlink(missing_ok=True)
b2_lf.select(b3_cols).sink_parquet(norm_path,compression='zstd',maintain_order=False)
pl.concat([b3_lf,pl.scan_parquet(norm_path)],how='vertical_relaxed').sink_parquet(combined_path,compression='zstd',maintain_order=False)
norm_path.unlink(missing_ok=True)

c.write_csv(out/'variant_cycle_manifest.csv')
coverage={'baseline_unique_expiries':len(baseline_expiries),'hf03_cycle_cells':c3.height,'hf2_usable_cycle_cells':c2.height,'combined_cycle_cells':c.height,'combined_unique_expiries':len(covered_expiries),'missing_expiry_count':len(missing_expiries),'missing_expiries':missing_expiries,'unexpected_expiry_count':len(unexpected_expiries),'combined_coverage_fraction':c.height/(224*63),'overlap_cells':overlap,'hf03_duplicate_groups':dups3,'hf2_duplicate_groups':dups2}
(out/'coverage.json').write_text(json.dumps(coverage,indent=2))
print(json.dumps(coverage,indent=2))
# Phase 21 execution trigger: frozen adapter logic unchanged.
