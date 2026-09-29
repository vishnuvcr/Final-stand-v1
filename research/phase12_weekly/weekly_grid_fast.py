from __future__ import annotations

import argparse
import bisect
import json
from dataclasses import asdict
from pathlib import Path

import polars as pl
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'phase11_weekly'))
from weekly_backtest import CostConfig, TradeResult, cost_rupees, exit_locked_cf, exit_prelock_cf, entry_cf, lock_cf, intrinsic, lot_size_for_expiry


def key(ts: str) -> str:
    return str(ts).replace(' ', 'T')[:19]


class Index:
    def __init__(self, options: pl.DataFrame, spot: pl.DataFrame):
        self.options = options
        self.by_ts_strike: dict[tuple[str, float], float] = {}
        self.timestamps: list[str] = []
        self.spot_expiry: dict[str, float] = {}
        for r in options.select(['timestamp','strike','open']).iter_rows(named=True):
            self.by_ts_strike[(key(str(r['timestamp'])), float(r['strike']))] = float(r['open'])
        self.timestamps = sorted({k[0] for k in self.by_ts_strike})
        for expiry, g in spot.group_by(pl.col('timestamp').cast(pl.String).str.slice(0,10), maintain_order=True):
            d=str(expiry[0] if isinstance(expiry, tuple) else expiry)
            if g.height:
                self.spot_expiry[d]=float(g.sort('timestamp')['close'][-1])
        self.complete_cache: dict[tuple[tuple[float,...],str,str], list[str]] = {}

    def marks(self, ts: str, strikes: list[float]) -> dict[float,float]:
        kk=key(ts)
        return {s:self.by_ts_strike[(kk,s)] for s in strikes if (kk,s) in self.by_ts_strike}

    def complete_times(self, strikes: list[float], lo: str, hi: str|None) -> list[str]:
        ss=tuple(sorted(float(s) for s in strikes))
        ck=(ss,lo,hi or '')
        if ck in self.complete_cache: return self.complete_cache[ck]
        out=[]
        for ts in self.timestamps:
            if ts <= lo: continue
            if hi is not None and ts >= hi: break
            if all((ts,s) in self.by_ts_strike for s in ss): out.append(ts)
        self.complete_cache[ck]=out
        return out


def fast_cycle(cycle: dict, idx: Index, stop_loss: float|None, cfg: CostConfig):
    if cycle['status'] != 'USABLE_OHLC': return None
    expiry=cycle['target_expiry']
    k1,k2,k3=(float(cycle['k1']),float(cycle['k2']),float(cycle['k3']))
    lot=lot_size_for_expiry(expiry,cfg); slip=cfg.slippage_points_per_leg
    entry_ts,lock_ts=cycle['entry_timestamp'],cycle['lock_timestamp']
    entry=idx.marks(entry_ts,[k1,k2,k3])
    if len(entry)!=3:return None
    net_cf=entry_cf(entry[k1],entry[k2],entry[k3],slip)
    entry_buy=(entry[k1]+slip)*lot
    entry_sell=((entry[k2]-slip)+(entry[k3]-slip))*lot
    orders=3
    if stop_loss is not None:
        for ts in idx.complete_times([k1,k2,k3],key(entry_ts),key(lock_ts)):
            m=idx.marks(ts,[k1,k2,k3])
            mtm=net_cf+m[k1]-m[k2]-m[k3]
            if mtm <= -abs(stop_loss):
                later=idx.complete_times([k1,k2,k3],ts,None)
                if later:
                    nt=later[0]; nm=idx.marks(nt,[k1,k2,k3])
                    net_cf += exit_prelock_cf(nm[k1],nm[k2],nm[k3],slip); orders += 3
                    buy_turn=entry_buy+(nm[k2]+slip)*lot+(nm[k3]+slip)*lot
                    sell_turn=entry_sell+(nm[k1]-slip)*lot
                    costs=cost_rupees(buy_turn,sell_turn,orders,cfg,nt[:10]); gross=net_cf
                    return TradeResult(expiry,entry_ts,lock_ts,nt,k1,k2,k3,float(cycle['entry_spot']),float(cycle['p1'])-float(cycle['p2']),float(cycle['target_premium']),float(cycle['target_error']) if cycle['target_error'] is not None else None,lot,stop_loss,'stop_prelock',gross,costs/lot,gross-costs/lot,gross*lot,costs,gross*lot-costs,orders,False,'OHLC_RECONSTRUCTION')
    lock=idx.marks(lock_ts,[k1,k2,k3])
    if len(lock)!=3:return None
    net_cf += lock_cf(lock[k2],slip); orders += 1
    if stop_loss is not None:
        for ts in idx.complete_times([k1,k3],key(lock_ts),None):
            m=idx.marks(ts,[k1,k3]); mtm=net_cf+m[k1]-m[k3]
            if mtm <= -abs(stop_loss):
                later=idx.complete_times([k1,k3],ts,None)
                if later:
                    nt=later[0]; nm=idx.marks(nt,[k1,k3])
                    net_cf += exit_locked_cf(nm[k1],nm[k3],slip); orders += 2
                    buy_turn=entry_buy+(lock[k2]+slip)*lot+(nm[k3]+slip)*lot
                    sell_turn=entry_sell+(nm[k1]-slip)*lot
                    costs=cost_rupees(buy_turn,sell_turn,orders,cfg,nt[:10]); gross=net_cf
                    return TradeResult(expiry,entry_ts,lock_ts,nt,k1,k2,k3,float(cycle['entry_spot']),float(cycle['p1'])-float(cycle['p2']),float(cycle['target_premium']),float(cycle['target_error']) if cycle['target_error'] is not None else None,lot,stop_loss,'stop_postlock',gross,costs/lot,gross-costs/lot,gross*lot,costs,gross*lot-costs,orders,True,'OHLC_RECONSTRUCTION')
    if expiry not in idx.spot_expiry:return None
    s=idx.spot_expiry[expiry]; gross=net_cf+intrinsic(s,k1)-intrinsic(s,k3)
    buy_turn=entry_buy+(lock[k2]+slip)*lot; sell_turn=entry_sell
    costs=cost_rupees(buy_turn,sell_turn,orders,cfg,expiry)
    return TradeResult(expiry,entry_ts,lock_ts,f'{expiry}T15:30:00+05:30',k1,k2,k3,float(cycle['entry_spot']),float(cycle['p1'])-float(cycle['p2']),float(cycle['target_premium']),float(cycle['target_error']) if cycle['target_error'] is not None else None,lot,stop_loss,'expiry',gross,costs/lot,gross-costs/lot,gross*lot,costs,gross*lot-costs,orders,True,'OHLC_RECONSTRUCTION')


def run_grid(manifest: str, options_path: str, spot_path: str, output_dir: str):
    cycles=pl.read_csv(manifest); options=pl.read_parquet(options_path); spot=pl.read_parquet(spot_path); idx=Index(options,spot)
    outdir=Path(output_dir); outdir.mkdir(parents=True,exist_ok=True)
    for slip in [0.00,0.25,0.50,1.00,2.00]:
        for stop in [None,50,100,150,200,300]:
            cfg=CostConfig(slippage_points_per_leg=slip); results=[]
            for row in cycles.iter_rows(named=True):
                try:
                    r=fast_cycle(row,idx,stop,cfg)
                    if r: results.append(asdict(r))
                except Exception as exc:
                    print(f'cycle {row.get("target_expiry")} failed slip={slip} stop={stop}: {exc}',flush=True)
            stem=f'trades_slip_{slip:.2f}_stop_{"none" if stop is None else int(stop)}'
            cols=[f.name for f in TradeResult.__dataclass_fields__.values()]
            df=pl.DataFrame(results,schema=cols) if results else pl.DataFrame({c:[] for c in cols})
            df.write_csv(outdir/(stem+'.csv'))
            summary={'trades':len(results),'stop_loss_points':stop,'slippage_points':slip,'net_rupees':sum(x['net_rupees'] for x in results),'mean_net_rupees':(sum(x['net_rupees'] for x in results)/len(results)) if results else None,'win_rate':(sum(x['net_rupees']>0 for x in results)/len(results)) if results else None,'total_costs_rupees':sum(x['costs_rupees'] for x in results),'execution_quality':'OHLC_RECONSTRUCTION'}
            (outdir/(stem+'.summary.json')).write_text(json.dumps(summary,indent=2),encoding='utf-8')
            print(json.dumps(summary),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest',required=True); ap.add_argument('--options',required=True); ap.add_argument('--spot',required=True); ap.add_argument('--output-dir',required=True)
    a=ap.parse_args(); run_grid(a.manifest,a.options,a.spot,a.output_dir)