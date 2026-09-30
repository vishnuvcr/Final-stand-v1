import os
from huggingface_hub import hf_hub_download
p="nifty historical data/nifty 50 1min options weekly expiries/20240613_WEEK.parquet"
x=hf_hub_download("johnwick3690/stocks",filename=p,revision="f90f7acad633ba5a803f25cf431fb5f13ce3d162",repo_type="dataset",token=os.getenv("HF_TOKEN"),cache_dir=os.getenv("HF_CACHE","~/.cache/huggingface"))
print(x)
