"""Static SEO audit of the built site (run after build_site.py): python3 data/seo_audit.py"""
import pathlib, re, html, collections, urllib.parse

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
pages = sorted(SITE.rglob("index.html"))
rows, titles, descs, problems = [], collections.defaultdict(list), collections.defaultdict(list), []

def attr(tag, name):
    m = re.search(name + r'="([^"]*)"', tag)
    return html.unescape(m.group(1)) if m else None

def resolve(base, href):
    href = href.split("#")[0].split("?")[0]
    if not href or href.startswith(("http", "mailto:", "tel:", "javascript:")):
        return None
    p = (base.parent / href).resolve()
    if p.is_dir():
        p = p / "index.html"
    return p

for f in pages:
    rel = f.relative_to(SITE).as_posix()
    h = f.read_text(encoding="utf-8")
    t = html.unescape((re.search(r"<title>(.*?)</title>", h, re.S) or [None, ""])[1]).strip()
    d = next((attr(m, "content") for m in re.findall(r"<meta[^>]+name=\"description\"[^>]*>", h)), "") or ""
    canon = next((attr(m, "href") for m in re.findall(r"<link[^>]+rel=\"canonical\"[^>]*>", h)), None)
    h1 = re.findall(r"<h1[\s>]", h)
    imgs = re.findall(r"<img\b[^>]*>", h)
    noalt = [i for i in imgs if attr(i, "alt") is None]
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S)
    words = len(html.unescape(body).split())
    broken = []
    for href in re.findall(r'<a\b[^>]*href="([^"]+)"', h):
        p = resolve(f, html.unescape(href))
        if p is not None and not p.exists():
            broken.append(href)
    jsonld = len(re.findall(r"application/ld\+json", h))
    titles[t].append(rel); descs[d].append(rel)
    rows.append((rel, len(t), len(d), len(h1), bool(canon), len(noalt), words, len(broken), jsonld))
    if not t or len(t) > 65: problems.append(f"{rel}: title length {len(t)} (aim <=60)")
    if len(d) < 70 or len(d) > 165: problems.append(f"{rel}: meta description length {len(d)} (aim 70-160)")
    if len(h1) != 1: problems.append(f"{rel}: {len(h1)} <h1> (want exactly 1)")
    if not canon: problems.append(f"{rel}: no canonical")
    if noalt: problems.append(f"{rel}: {len(noalt)} <img> without alt")
    if broken: problems.append(f"{rel}: broken internal links {sorted(set(broken))[:5]}")
    if rel.startswith("blog/") and rel != "blog/index.html" and words < 600: problems.append(f"{rel}: thin content ({words} words)")

for name, store in (("title", titles), ("meta description", descs)):
    for k, v in store.items():
        if len(v) > 1 and k and not all(x in ("index.html","fr/index.html","ar/index.html","ru/index.html") for x in v):
            problems.append(f"duplicate {name} on {v}")

sm = (SITE / "sitemap.xml").read_text()
listed = set(re.findall(r"<loc>([^<]+)</loc>", sm))
for f in pages:
    rel = f.relative_to(SITE).as_posix()
    url = "https://www.easycliniccenter.com/" + ("" if rel == "index.html" else rel[:-len("index.html")])
    if url not in listed: problems.append(f"{rel}: missing from sitemap.xml")

print(f"{'page':58} {'title':>5} {'desc':>4} h1 canon noalt words broken ld")
for r in rows:
    print(f"{r[0]:58} {r[1]:>5} {r[2]:>4} {r[3]:>2} {str(r[4])[0]:>5} {r[5]:>5} {r[6]:>5} {r[7]:>6} {r[8]:>2}")
print("\nPROBLEMS:" if problems else "\nNo problems found.")
for p in problems: print(" -", p)
