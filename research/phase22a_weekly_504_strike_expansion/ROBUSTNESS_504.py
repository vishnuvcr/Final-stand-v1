from pathlib import Path
import pandas as pd
import numpy as np
import argparse


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trades',required=True)
    ap.add_argument('--out-dir',required=True)
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.trades)
    df['target_expiry']=pd.to_datetime(df['target_expiry'])
    m=df['variant_id'].str.extract(r'^(OTM\\d+|ATM_NEAREST|ATM_UP|ITM\\d+)_(NEXT\\d+|MIRROR_GAP)_K3M(.+)$')
    df['k1_rule']=m[0]; df['k2_rule']=m[1]; df['k3_multiplier']=m[2].astype(float)
    rows=[]
    for v,g in df.groupby('variant_id',sort=True):
        g=g.sort_values('target_expiry'); valid=g[g.net_rupees.notna()].copy(); x=valid.net_rupees.to_numpy(float)
        eq=np.cumsum(x); peak=np.maximum.accumulate(np.r_[0.,eq]); dd=peak[1:]-eq
        pos=x[x>0].sum(); neg=-x[x<0].sum()
        rows.append({'variant_id':v,'k1_rule':g.k1_rule.iloc[0],'k2_rule':g.k2_rule.iloc[0],'k3_multiplier':g.k3_multiplier.iloc[0],
          'cycles':len(g),'valid_net_cycles':len(valid),'missing_net_cycles':len(g)-len(valid),'total_net_rupees':x.sum(),
          'mean_net_rupees':x.mean(),'median_net_rupees':np.median(x),'win_rate':(x>0).mean(),
          'profit_factor':pos/neg if neg>0 else np.inf,'max_drawdown_rupees':dd.max(),'worst_trade_rupees':x.min(),
          'best_trade_rupees':x.max(),'total_orders':valid.orders.sum(),
          'additional_cost_buffer_points_per_order':x.sum()/(valid.orders*valid.lot_size).sum()})
    r=pd.DataFrame(rows); r.to_csv(out/'ROBUSTNESS_504_METRICS.csv',index=False)
    stresses=[]
    for s in [0,.25,.5,1,1.5,2,3]:
        for v,g in df.groupby('variant_id',sort=True):
            g=g.sort_values('target_expiry'); g=g[g.net_rupees.notna()]
            y=g.net_rupees.to_numpy(float)-s*g.orders.to_numpy(float)*g.lot_size.to_numpy(float)
            eq=np.cumsum(y); peak=np.maximum.accumulate(np.r_[0.,eq]); dd=peak[1:]-eq
            stresses.append({'variant_id':v,'extra_cost_points_per_order':s,'total_net_rupees':y.sum(),'win_rate':(y>0).mean(),'max_drawdown_rupees':dd.max()})
    pd.DataFrame(stresses).to_csv(out/'ROBUSTNESS_504_STRESS_DETAIL.csv',index=False)
    summary=pd.DataFrame(stresses).groupby('extra_cost_points_per_order').agg(configurations=('variant_id','size'),positive_configurations=('total_net_rupees',lambda s:(s>0).sum()),positive_share=('total_net_rupees',lambda s:(s>0).mean()),median_net_rupees=('total_net_rupees','median'),mean_net_rupees=('total_net_rupees','mean'),median_max_drawdown_rupees=('max_drawdown_rupees','median')).reset_index()
    summary.to_csv(out/'SLIPPAGE_STRESS_SUMMARY.csv',index=False)

if __name__=='__main__': main()
