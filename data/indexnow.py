"""Tell IndexNow (Bing and partners) which pages changed in the last deployment.

Usage: python3 data/indexnow.py <commit-before>   (or: python3 data/indexnow.py --all)
Reads the changed site/**/index.html files from git and maps them to public URLs.
Never fails the deployment: any problem is printed and the script exits 0.
"""
import json, subprocess, sys, time, urllib.request, pathlib, re

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from config import SITE, INDEXNOW_KEY

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = re.compile(r"^google[0-9a-f]+\.html$")

def to_url(path):
    p = pathlib.PurePosixPath(path).relative_to("site")
    if p.name != "index.html":
        return None
    d = "/".join(p.parts[:-1])
    return f"{SITE}/{d}/" if d else f"{SITE}/"

def all_urls():
    return [u for u in (to_url(str(f.relative_to(ROOT).as_posix())) for f in sorted((ROOT / "site").rglob("index.html"))) if u]

def changed_urls(before):
    out = subprocess.run(["git", "diff", "--name-only", before, "HEAD", "--", "site"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return sorted({u for u in (to_url(l) for l in out.split() if l.endswith("index.html")) if u})

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        urls = all_urls() if arg == "--all" else changed_urls(arg)
    except Exception as e:
        print("IndexNow: could not work out changed pages:", e); return
    if not urls:
        print("IndexNow: no changed pages, nothing to send"); return
    host = SITE.split("//", 1)[1]
    body = json.dumps({"host": host, "key": INDEXNOW_KEY, "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
    time.sleep(0 if arg == "--all" else 30)   # let the new deployment reach the CDN first
    try:
        req = urllib.request.Request("https://api.indexnow.org/IndexNow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: sent {len(urls)} URL(s), HTTP {r.status}")
    except Exception as e:
        print("IndexNow: request failed:", e)

main()
