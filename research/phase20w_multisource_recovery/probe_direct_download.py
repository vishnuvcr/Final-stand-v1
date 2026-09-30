import os
from huggingface_hub import hf_hub_download
p=hf_hub_download("artist-23/nifty-options-data",filename="NIFTY/WEEK/ATM+0_CE.parquet",revision="45e0a043f34f3f40f9694e52a944297803c2af8b",repo_type="dataset",token=os.getenv("HF_TOKEN"),cache_dir=os.getenv("HF_CACHE","~/.cache/huggingface"))
print({"path":p,"size":__import__("os").path.getsize(p)})
