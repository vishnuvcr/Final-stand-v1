from __future__ import annotations
import argparse, csv, hashlib, json, re, zipfile
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://nsearchives.nseindia.com/archives/nsccl/span/nsccl.{year}.s.zip"
DATE_RE = re.compile(r"(20\d{6})")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def download(url: str, dst: Path) -> None:
    if dst.exists() and dst.stat().st_size > 0:
        return
    req=Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urlopen(req, timeout=120) as r, dst.open("wb") as f:
        while True:
            b=r.read(1024*1024)
            if not b: break
            f.write(b)

def wanted_dates(manifest: Path) -> set[str]:
    dates=set()
    with manifest.open(newline="") as f:
        for row in csv.DictReader(f):
            if row["status"] != "USABLE_OHLC": continue
            for k in ("entry_day","lock_day","target_expiry"):
                if row.get(k): dates.add(row[k].replace("-",""))
    return dates

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest", default="research/phase16w_capital_validation/frozen_cycle_manifest.csv")
    ap.add_argument("--cache", default="research/phase16w_capital_validation/cache/span")
    ap.add_argument("--output", default="research/phase16w_capital_validation/output/span_manifest.json")
    args=ap.parse_args()
    cache=Path(args.cache); extracted=cache/"extracted"; cache.mkdir(parents=True,exist_ok=True); extracted.mkdir(parents=True,exist_ok=True)
    dates=wanted_dates(Path(args.manifest))
    years=sorted({d[:4] for d in dates})
    report={"requested_dates":sorted(dates),"years":years,"archives":[],"members":[]}
    for year in years:
        archive=cache/f"nsccl.{year}.s.zip"
        url=BASE.format(year=year)
        download(url,archive)
        entry={"year":year,"url":url,"path":str(archive),"sha256":sha256(archive),"size_bytes":archive.stat().st_size}
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
            entry["member_count"]=len(names)
            matched=[]
            for name in names:
                token_match=DATE_RE.search(name)
                if not token_match or token_match.group(1) not in dates: continue
                if not name.lower().endswith((".spn",".zip",".xml")): continue
                target=extracted/Path(name).name
                if not target.exists():
                    with z.open(name) as src, target.open("wb") as dst:
                        dst.write(src.read())
                matched.append({"member":name,"extracted":str(target),"sha256":sha256(target),"size_bytes":target.stat().st_size})
            entry["matched_count"]=len(matched)
            report["members"].extend(matched)
        report["archives"].append(entry)
    Path(args.output).write_text(json.dumps(report,indent=2))
    print(json.dumps({"years":years,"requested_dates":len(dates),"matched_members":len(report["members"])},indent=2))

if __name__=="__main__": main()
