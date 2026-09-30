import os, subprocess
from pathlib import Path
repo=Path("/tmp/hf_stocks")
if not repo.exists():
    subprocess.run(["git","clone","--filter=blob:none","--no-checkout","https://huggingface.co/datasets/johnwick3690/stocks.git",str(repo)],check=True)
path="nifty historical data/nifty 50 1min options weekly expiries/20240613_WEEK.parquet"
subprocess.run(["git","-C",str(repo),"lfs","fetch","origin","main","--include",path],check=True)
subprocess.run(["git","-C",str(repo),"lfs","checkout",path],check=True)
p=repo/path
print({"path":str(p),"exists":p.exists(),"size":p.stat().st_size if p.exists() else None})
