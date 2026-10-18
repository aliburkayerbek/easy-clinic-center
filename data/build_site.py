"""Builds the Easy Clinic Center website (EN default, FR / AR (RTL) / RU) as one HTML page."""
import json, base64, pathlib, re, shutil, datetime, html as H
import illus
from web_strings import S
from site_strings import S2, META2
from config import SITE, CONTACT_EMAIL
S.update(S2)
FAQ_N = 8

import os, sys, subprocess
LANGS = ["en", "fr", "ar", "ru"]
if "ECC_LI" not in os.environ:   # driver: build every language page in its own process
    for i in range(len(LANGS)):
        subprocess.run([sys.executable, __file__], check=True, env={**os.environ, "ECC_LI": str(i)})
    sys.exit(0)
LI = int(os.environ["ECC_LI"]); LC = LANGS[LI]
I18N = {l: {k: v[i] for k, v in S.items()} for i, l in enumerate(LANGS)}

def T(key, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag} data-i="{key}"{c}{a}>{S[key][LI]}</{tag}>'

def b64(p):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = pathlib.Path(__file__).resolve().parent / "_build"
BUILD.mkdir(exist_ok=True)

def web_logo(name):
    """Downscale the brand logo to 300 px wide for embedding."""
    from PIL import Image
    im = Image.open(ROOT / "brand" / name)
    im = im.resize((240, round(im.height * 240 / im.width)), Image.LANCZOS)
    out = BUILD / f"web_{name}"
    im.save(out, optimize=True)
    return out

LOGO = "assets/logo.png"
LOGO_W = "assets/logo_white.png"
import subprocess, sys
subprocess.run([sys.executable, str(BUILD.parent / "iso.py"), "none"], check=True)
ISO = (BUILD / "iso_none.svg").read_text()

ICON = {
 "check": '<path d="M5 12l4 4 10-10"/>',
 "dash": '<path d="M7 12h10"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "plane": '<path d="M2 16l20-6-20-6 4 6-4 6z M6 10h9"/>',
 "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z M9 12l2 2 4-4"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 15-5 16 0"/>',
 "doc": '<path d="M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 16h7"/>',
 "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "steth": '<path d="M5 3v6a5 5 0 0 0 10 0V3 M10 14v2a5 5 0 0 0 10 0v-3"/><circle cx="20" cy="11" r="2"/>',
 "hotel": '<path d="M3 20V8h18v12 M3 14h18"/><circle cx="7" cy="11" r="1.5"/>',
 "car": '<path d="M3 15l2-6h14l2 6v4H3z M3 15h18"/><circle cx="7.5" cy="19" r="1.6"/><circle cx="16.5" cy="19" r="1.6"/>',
 "bag": '<rect x="4" y="7" width="16" height="13" rx="2"/><path d="M9 7V5h6v2"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18 M12 3c3 3 3 15 0 18 M12 3c-3 3-3 15 0 18"/>',
 "upload": '<path d="M12 16V4 M7 9l5-5 5 5 M4 20h16"/>',
 "ai": '<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9z M9 2v3 M15 2v3 M9 19v3 M15 19v3 M2 9h3 M2 15h3 M19 9h3 M19 15h3"/>',
 "report": '<path d="M6 3h12v18H6z M9 8h6 M9 12h6 M9 16h3"/>',
 "home": '<path d="M3 11l9-7 9 7v9H3z M9 20v-6h6v6"/>',
 "arrow": '<path d="M5 12h14 M13 6l6 6-6 6"/>',
 "ext": '<path d="M14 4h6v6 M20 4l-9 9 M18 14v6H4V6h6"/>',
 "x": '<path d="M6 6l12 12 M18 6L6 18"/>',
 "face": '<circle cx="12" cy="10" r="5"/><path d="M4 21c1.5-4.5 14.5-4.5 16 0 M3 3l18 18"/>',
}
def ic(n, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'

# ------------------------------------------------------------------ data
TREAT = {
 "plastic": [("breast", "t_breast"), ("lipo", "t_lipo"), ("rhino", "t_rhino")],
 "general": [("obesity", "t_obesity"), ("cancer", "t_cancer"), ("thyroid", "t_thyroid")],
 "dental": [("implant", "t_implant"), ("hollywood", "t_holly")],
 "internal": [("second", "t_second"), ("chronic", "t_chronic")],
}
HOSP = [
 ("c_ist", [("Memorial Şişli Hospital", "Şişli", "t_priv", "https://www.memorial.com.tr/doktorlar/memorial-sisli-hastanesi-doktorlari"),
            ("Acıbadem Maslak Hospital", "Sarıyer", "t_priv", "https://www.acibadem.com.tr/doktorlar/?hospital=Maslak%20Hastanesi"),
            ("Medicana International İstanbul", "Beylikdüzü", "t_priv", "https://www.medicanainternational.com/en/international-istanbul/doctors")]),
 ("c_ank", [("Memorial Ankara Hospital", "Çankaya", "t_priv", "https://www.memorial.com.tr/doktorlar/memorial-ankara-hastanesi-doktorlari"),
            ("Medicana International Ankara", "Çankaya", "t_priv", "https://www.medicanainternational.com/en/international-ankara/doctors"),
            ("Acıbadem Ankara Hospital", "Çankaya", "t_priv", "https://www.acibadem.com.tr/doktorlar/?hospital=Ankara%20Hastanesi"),
            ("Ufuk University Dr. Rıdvan Ege Hospital", "Çankaya", "t_uni", "https://hastane.ufuk.edu.tr/doktorlarimiz"),
            ("Güven Hospital", "Ayrancı &amp; Çayyolu", "t_priv", "https://www.guven.com.tr/doktorlar"),
            ("TOBB ETÜ Hospital", "Çankaya", "t_uni", "https://hastane.etu.edu.tr/doktorlar/")]),
 ("c_izm", [("Acıbadem İzmir Kent Hospital", "Çiğli", "t_priv", "https://www.acibadem.com.tr/doktorlar/?hospital=Kent%20Hastanesi%20(%C4%B0zmir)"),
            ("Medicana International İzmir", "Konak", "t_priv", "https://www.medicanainternational.com/en/international-izmir/doctors"),
            ("Medicana Çeşme Medical Centre", "Çeşme", "t_med", "https://www.medicanainternational.com/en/cesme/doctors")]),
 ("c_ant", [("Memorial Antalya Hospital", "Kepez", "t_priv", "https://www.memorial.com.tr/doktorlar/memorial-antalya-hastanesi-doktorlari"),
            ("Medstar Antalya Hospital", "Muratpaşa", "t_priv", "https://www.memorial.com.tr/doktorlar/medstar-antalya-hastanesi-doktorlari")]),
]

# ------------------------------------------------------------------ sections
def check_li(key):
    return f'<li>{ic("check")}{T(key)}</li>'

LANG_NAMES = {"en": "English", "fr": "Français", "ar": "العربية", "ru": "Русский"}
LANG_PATH = {"en": "/", "fr": "/fr/", "ar": "/ar/", "ru": "/ru/"}
REL = "" if LC == "en" else "../"   # pages live at /, /fr/, /ar/, /ru/ - keep links relative so any base path works
def rel_href(l):
    return (REL + LANG_PATH[l].strip("/") + ("/" if l != "en" else "")) or "./"
LANG_OPTS = "".join(f'<option value="{rel_href(l)}"{" selected" if l == LC else ""}>{LANG_NAMES[l]}</option>' for l in LANGS)


CSS = (pathlib.Path(__file__).resolve().parent / "web.css").read_text(encoding="utf-8")

QCARD = f'''
  <aside class="qcard" aria-label="Example quote format">
   {T("qc_ex", "p", "qc-ex")}
   {T("qc_title", "h2")}
   {T("qc_sub", "p", "qc-sub")}
   <div class="qopts">
    <div class="qopt a"><p class="qo-k">{T("optA")}</p><p class="qo-n">{T("optA_n")}</p>
     <ul>{"".join(f'<li>{ic("check")}{T(k)}</li>' for k in ["i_treat", "i_flights", "i_hotel", "i_transfer"])}</ul></div>
    <div class="qopt b"><p class="qo-k">{T("optB")}</p><p class="qo-n">{T("optB_n")}</p>
     <ul><li>{ic("check")}{T("i_treat")}</li>{"".join(f'<li class="opt">{ic("dash")}<span>{T(k)} · {T("i_optional")}</span></li>' for k in ["i_flights", "i_hotel", "i_transfer"])}</ul></div>
   </div>
   {T("qc_note", "p", "qc-note")}
  </aside>
'''
QCARD = QCARD.replace('<aside class="qcard"', '<aside class="qcard qcard-how"')
how = f'''
<section class="sec alt" id="how"><div class="wrap">
 {T("how_eb", "p", "eyebrow")}{T("how_h2", "h2")}
 <div class="how">
  <div class="iso plate" aria-hidden="true">{ISO}</div>
  <ol class="steps">
   {"".join(f'<li><span class="sn">{n}</span><div>{T(h, "h3")}{T(p, "p")}</div></li>' for n, h, p in [(1, "s1_h", "s1_p"), (2, "s2_h", "s2_p"), (3, "s3_h", "s3_p")])}
  </ol>
 </div>
 {QCARD}
 <div class="opts2">
  <div class="opt2 a"><p class="qo-k">{T("optA")}</p>{T("optA_n", "h3")}{T("optA_d", "p")}{T("best_A", "p", "best")}</div>
  <div class="opt2 b"><p class="qo-k">{T("optB")}</p>{T("optB_n", "h3")}{T("optB_d", "p")}{T("best_B", "p", "best")}</div>
 </div>
 <div class="after">
  {T("af_h", "h3")}
  <ul>{"".join(f'<li>{ic(i)}{T(k)}</li>' for i, k in [("heart", "af1"), ("report", "af2"), ("shield", "af3")])}</ul>
 </div>
</div></section>'''

def tcard(ill, key, dept):
    facts = ""
    extra = ""
    if dept not in ("internal",):
        facts = '<dl class="facts">' + "".join(f'<div><dt>{T(l)}</dt><dd>{T(f"{key}_f{i}")}</dd></div>' for i, l in [(1, "f_proc"), (2, "f_stay"), (3, "f_back")]) + "</dl>"
    if ill == "chronic":
        extra = '<ul class="sched">' + "".join(f"<li>{T(k)}</li>" for k in ["ch1", "ch2", "ch3"]) + "</ul>"
    if ill == "second":
        extra = f'<a class="more" href="#second">{T("more_second")}{ic("arrow", "ic dir")}</a>'
    return f'''<article class="tcard">
 <div class="plate t-ill" aria-hidden="true">{illus.ILL[ill]()}</div>
 <div class="t-body">{T(key, "h3")}{T(key + "_d", "p")}
  <p class="who">{T("who")}</p><ul class="wl">{check_li(key + "_w1")}{check_li(key + "_w2")}</ul>
  {facts}{extra}
 </div></article>'''

tabs = "".join(f'<button type="button" role="tab" id="tab-{d}" aria-controls="panel-{d}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{T("d_" + d)}</button>' for i, d in enumerate(TREAT))
panels = "".join(f'<div class="tpanel" role="tabpanel" id="panel-{d}" aria-labelledby="tab-{d}"{"" if i == 0 else " hidden"}><div class="tgrid">{"".join(tcard(il, k, d) for il, k in items)}</div></div>' for i, (d, items) in enumerate(TREAT.items()))
treat = f'''
<section class="sec" id="treatments"><div class="wrap">
 {T("tr_eb", "p", "eyebrow")}{T("tr_h2", "h2")}{T("tr_sub", "p", "sub")}
 <div class="tabs" role="tablist" aria-label="Departments">{tabs}</div>
 {panels}
 {T("fact_note", "p", "fnote")}
</div></section>'''

second = f'''
<section class="sec dark" id="second"><div class="wrap">
 <div class="so-top">
  <div>{T("so_eb", "p", "eyebrow")}{T("so_h2", "h2")}{T("so_p", "p", "lead2")}</div>
  <div class="plate so-ill" aria-hidden="true">{illus.ILL["second"]()}</div>
 </div>
 <ol class="so-steps">
  {"".join(f'<li class="{c}"><span class="sn">{n}</span>{ic(i)}{T(h, "h3")}{T(p, "p")}</li>' for n, i, h, p, c in [(1, "upload", "so1_h", "so1_p", ""), (2, "doc", "so2_h", "so2_p", ""), (3, "steth", "so3_h", "so3_p", "ai"), (4, "report", "so4_h", "so4_p", "")])}
 </ol>
 <div class="dodont2"><p class="d1">{T("so_do")}</p><p class="d2">{T("so_dont")}</p></div>
 <a class="btn btn-p btn-l" href="#apply">{T("cta_second")}{ic("arrow", "ic dir")}</a>
</div></section>'''

hosp_html = ""
for ck, items in HOSP:
    rows = "".join(f'<li><div><b>{n}</b><span>{d} · {T(tk)}</span></div><a href="{u}" target="_blank" rel="noopener">{T("h_link")}{ic("ext")}</a></li>' for n, d, tk, u in items)
    hosp_html += f'<div class="city"><h3>{T(ck)} <small>{len(items)}</small></h3><ul>{rows}</ul></div>'
hospitals = f'''
<section class="sec alt" id="hospitals"><div class="wrap">
 {T("h_eb", "p", "eyebrow")}{T("h_h2", "h2")}{T("h_p", "p", "sub")}
 <div class="cities">{hosp_html}</div>
</div></section>'''

travel = f'''
<section class="sec" id="travel"><div class="wrap">
 {T("tv_eb", "p", "eyebrow")}{T("tv_h2", "h2")}
 <div class="tv">
  {"".join(f'<div class="tvi">{ic(i)}<div>{T(h, "h3")}{T(p, "p")}</div></div>' for i, h, p in [("globe", "tv1_h", "tv1_p"), ("plane", "tv2_h", "tv2_p"), ("hotel", "tv3_h", "tv3_p"), ("bag", "tv4_h", "tv4_p"), ("shield", "tv5_h", "tv5_p"), ("clock", "tv6_h", "tv6_p")])}
 </div>
 <a class="nhs" href="https://www.nhs.uk/using-the-nhs/healthcare-abroad/going-abroad-for-treatment/" target="_blank" rel="noopener">{T("nhs")}{ic("ext")}</a>
</div></section>'''

faq = f'''
<section class="sec alt" id="faq"><div class="wrap narrow">
 {T("faq_eb", "p", "eyebrow")}{T("faq_h2", "h2")}
 <div class="faq">{"".join(f'<details><summary>{T(f"q{i}")}</summary>{T(f"a{i}", "p")}</details>' for i in range(1, FAQ_N + 1))}</div>
</div></section>'''

# ------------------------------------------------------------------ form
def fld(id_, key, typ="text", req=False, auto="", extra="", full=False, hint=None):
    star = '<b class="req" aria-hidden="true">*</b>' if req else ""
    r = " required" if req else ""
    a = f' autocomplete="{auto}"' if auto else ""
    hattr = f'id="{id_}-h"'
    h = T(hint, "p", "hint", hattr) if hint else ""
    desc = f' aria-describedby="{id_}-e{(" " + id_ + "-h") if hint else ""}"'
    if typ == "textarea":
        ctl = f'<textarea id="{id_}" name="{id_}" rows="4"{r}{desc}></textarea>'
    else:
        ctl = f'<input id="{id_}" name="{id_}" type="{typ}"{r}{a}{desc}{extra}/>'
    return f'<div class="f{" full" if full else ""}"><label for="{id_}">{T(key)}{star}</label>{h}{ctl}<p class="err" role="alert" id="{id_}-e" hidden></p></div>'

def sel(id_, key, opts, req=False, full=False):
    star = '<b class="req" aria-hidden="true">*</b>' if req else ""
    r = " required" if req else ""
    o = '<option value="" data-i="choose">Choose…</option>' if req else ""
    o += "".join(f'<option value="{v}"{" data-i=" + chr(34) + k + chr(34) if k else ""}>{S[k][LI] if k else lbl}</option>' for v, k, lbl in opts)
    return f'<div class="f{" full" if full else ""}"><label for="{id_}">{T(key)}{star}</label><select id="{id_}" name="{id_}"{r} aria-describedby="{id_}-e">{o}</select><p class="err" role="alert" id="{id_}-e" hidden></p></div>'

def tick(id_, key, req=True):
    star = '<b class="req" aria-hidden="true">*</b>' if req else ""
    r = " required" if req else ""
    return f'<div class="f full tk"><label class="chk"><input type="checkbox" id="{id_}" name="{id_}"{r} aria-describedby="{id_}-e"/><span>{T(key)}{star}</span></label><p class="err" role="alert" id="{id_}-e" hidden></p></div>'

CONDS = ["c_diab", "c_bp", "c_heart", "c_blood", "c_allergy", "c_surgery", "c_smoke", "c_preg"]

# ------------------------------------------------------------------ blog source
def load_posts():
    posts = []
    for f in sorted((ROOT / "blog").glob("*.md")):
        m = re.match(r"---\n(.*?)\n---\n(.*)", f.read_text(encoding="utf-8"), re.S)
        meta = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)}
        body = m.group(2).strip()
        posts.append(dict(slug=f.stem, title=meta["title"], desc=meta["description"], date=meta["date"],
                          tags=[t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                          body=body, mins=max(1, round(len(body.split()) / 200))))
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts

POSTS = load_posts()

# ------------------------------------------------------------------ header / footer (shared with blog pages)
# A = prefix to site root for assets and /blog/, N = prefix for in-page anchors (empty on a home page).
def make_header(A, N, opts):
    return f'''
<a class="skip" href="#main">{S["skip"][LI]}</a>
<header class="hdr" id="top">
 <div class="wrap hdr-in">
  <a class="brand" href="{N}#top" aria-label="Easy Clinic Center"><img class="logo-l" src="{A}{LOGO}" width="64" height="65" alt="Easy Clinic Center"/><img class="logo-d" src="{A}{LOGO_W}" width="64" height="65" alt="Easy Clinic Center"/></a>
  <nav class="nav" aria-label="Main">
   <a href="{N}#second">{T("nav_second")}</a><a href="{N}#treatments">{T("nav_treat")}</a><a href="{N}#hospitals">{T("nav_hosp")}</a><a href="{A}blog/">{T("nav_blog")}</a><a href="{N}#faq">{T("nav_faq")}</a>
  </nav>
  <div class="hdr-act">
   <label class="sr" for="lang">{S["lang_label"][LI]}</label>
   <select id="lang" class="lang">{opts}</select>
   <a class="btn btn-p hdr-apply" href="{N}#apply">{T("nav_apply")}</a>
  </div>
 </div>
</header>'''

def make_footer(A, N):
    return f'''
<footer class="ftr"><div class="wrap ftr-in">
 <div class="ft-b"><img src="{A}{LOGO_W}" width="86" height="87" alt="Easy Clinic Center" class="ft-logo" loading="lazy"/>{T("ft_tag", "p")}</div>
 <div class="ft-c">
  <div>{T("ft_hours", "h4")}{T("ft_hours_v", "p")}</div>
  <div>{T("ft_office", "h4")}{T("ft_office_v", "p")}</div>
  <div>{T("ft_contact", "h4")}<p><span>www.easycliniccenter.com</span><br/>{T("ft_contact_v", "span", "muted")}</p><p><a href="{A}blog/">{T("nav_blog")}</a></p></div>
 </div>
 {T("ft_legal", "p", "legal")}
 <p class="copy">© 2026 Easy Clinic Center</p>
</div></footer>
<div class="mbar"><a class="btn btn-p" href="{N}#apply">{T("m_apply")}</a></div>'''

header = make_header(REL, "", LANG_OPTS)
footer = make_footer(REL, "")

# ------------------------------------------------------------------ hero with the one-step request form
hero = f'''
<section class="hero" aria-label="Easy Clinic Center">
 <div class="wrap hero2">
  <div class="h-txt">
   <p class="freebadge">{ic("heart")}{T("h_eb")}</p>
   {T("h_h1", "h1")}
   {T("h_p", "p", "lead")}
   <ul class="bn-chips">{"".join(f'<li>{ic("check")}{T(k)}</li>' for k in ("h_c1", "h_c2", "h_c3"))}</ul>
   <p class="hero-note">{ic("shield")}{T("hero_note")}</p>
  </div>
  <div class="formcard" id="apply">
   {T("f_title", "h2")}
   <form id="appForm" novalidate>
    <div class="fg">
     {sel("need", "f_need", [("second", "n_second", ""), ("treat", "n_treat", ""), ("unsure", "n_unsure", "")], full=True)}
     {fld("fullname", "f_name", req=True, auto="name", full=True)}
     {fld("contact", "f_contact", req=True, auto="email", extra=' inputmode="email" dir="ltr"', full=True)}
     {fld("msg", "f_msg", typ="textarea", req=True, hint="f_msg_h", full=True)}
    </div>
    <details class="more-d"><summary>{T("f_more")}</summary>
     <div class="fg">
      {fld("country", "country", auto="country-name", full=True)}
      {fld("meds", "meds", typ="textarea", full=True)}
     </div>
     <p class="hint">{ic("face")}{T("f_photo")}</p>
    </details>
    {tick("consent", "f_consent")}
    <button type="submit" class="btn btn-p btn-l full" id="btnSubmit">{T("f_submit")}{ic("arrow", "ic dir")}</button>
    <p class="form-reassure">{ic("lock")}{T("form_reassure")}</p>
   </form>
   <div class="result" id="result" hidden tabindex="-1">
    {ic("check", "ic big")}{T("res_h", "h3")}
    <p class="refl">{T("ref")}: <bdi class="ref" id="refNo"></bdi></p>
    {T("res_p", "p")}
    <pre class="sum" id="sumText" dir="ltr" tabindex="0"></pre>
    <div class="ract"><a class="btn btn-p" id="btnMail" href="#" hidden>{T("f_mail")}</a><button type="button" class="btn btn-p" id="btnSave">{T("save")}</button><button type="button" class="btn btn-s" id="btnCopy">{T("copy")}</button><button type="button" class="btn btn-g" id="btnEdit">{T("edit")}</button><span class="toast" id="toast" role="status"></span></div>
    <p class="soon" id="soonNote">{ic("clock")}{T("contacts_soon")}</p>
   </div>
  </div>
 </div>
</section>
<div class="trust"><div class="wrap trust-in">
 <p>{ic("heart")}{T("tr1")}</p><p>{ic("steth")}{T("tr2")}</p><p>{ic("lock")}{T("tr3")}</p><p>{ic("user")}{T("tr4")}</p>
</div></div>'''

# ------------------------------------------------------------------ home sections that are new
def post_cards(posts, A):
    return "".join(
        f'<a class="pcard" href="{A}blog/{p["slug"]}/"><span class="ptag">{H.escape(p["tags"][0]) if p["tags"] else ""}</span>'
        f'<h3>{H.escape(p["title"])}</h3><p>{H.escape(p["desc"])}</p><span class="pmore">{T("blog_read")}{ic("arrow", "ic dir")}</span></a>'
        for p in posts)

blogsec = f'''
<section class="sec" id="blog"><div class="wrap">
 {T("blog_eb", "p", "eyebrow")}{T("blog_h2", "h2")}
 <div class="pgrid">{post_cards(POSTS[:3], REL)}</div>
 <p class="pall"><a class="btn btn-s" href="{REL}blog/">{T("blog_all")}{ic("arrow", "ic dir")}</a></p>
</div></section>'''

cta2 = f'''
<section class="sec cta2"><div class="wrap">
 {T("cta2_h", "h2")}
 <a class="btn btn-p btn-l" href="#apply">{T("m_apply")}{ic("arrow", "ic dir")}</a>
</div></section>'''


JS = r'''
(function(){
 const I18N = __I18N__;
 const root = document.documentElement;
 const lang = root.lang;
 const CONTACT = "__CONTACT__";
 const L = I18N[lang] || I18N.en;
 document.getElementById("lang").addEventListener("change", e => { location.href = e.target.value + location.hash; });

 /* tabs */
 const tabs = [...document.querySelectorAll('[role="tab"]')];
 function selectTab(t){
  tabs.forEach(b => { const on = b === t; b.setAttribute("aria-selected", on); b.tabIndex = on ? 0 : -1;
   document.getElementById(b.getAttribute("aria-controls")).hidden = !on; });
  t.scrollIntoView({block:"nearest", inline:"nearest"});
 }
 tabs.forEach((t, i) => {
  t.addEventListener("click", () => selectTab(t));
  t.addEventListener("keydown", e => {
   const rtl = root.dir === "rtl"; let d = 0;
   if(e.key === "ArrowRight") d = rtl ? -1 : 1; if(e.key === "ArrowLeft") d = rtl ? 1 : -1;
   if(d){ e.preventDefault(); const n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); selectTab(n); }
  });
 });

 /* form */

 /* request form */
 const form = document.getElementById("appForm");
 function setErr(el, key){
  const e = document.getElementById(el.id + "-e"); if(!e) return;
  if(key){ e.dataset.k = key; e.textContent = L[key]; e.hidden = false; el.setAttribute("aria-invalid", "true"); }
  else { e.hidden = true; e.textContent = ""; el.removeAttribute("aria-invalid"); }
 }
 function check(el){
  if(el.type === "checkbox"){ const ok = !el.required || el.checked; setErr(el, ok ? null : "err_tick"); return ok; }
  const v = el.value.trim();
  if(el.required && !v){ setErr(el, "err_req"); return false; }
  if(v && el.id === "contact"){
   const mail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
   const phone = /^\+?[\d\s().-]{8,}$/.test(v) && v.replace(/\D/g, "").length >= 8;
   if(!mail && !phone){ setErr(el, "err_contact"); return false; }
  }
  setErr(el, null); return true;
 }
 form.querySelectorAll("input,select,textarea").forEach(el => {
  el.addEventListener("blur", () => { if(el.dataset.t) check(el); });
  el.addEventListener("input", () => { el.dataset.t = 1; if(el.getAttribute("aria-invalid")) check(el); });
  el.addEventListener("change", () => { el.dataset.t = 1; if(el.getAttribute("aria-invalid") || el.type === "checkbox") check(el); });
 });

 const EN = I18N.en;
 const strip = s => s.replace(/<[^>]+>/g, "").replace(/&amp;/g, "&");
 function makeRef(){ const d = new Date(); const p = n => String(n).padStart(2, "0"); return "ECC-" + String(d.getFullYear()).slice(2) + p(d.getMonth() + 1) + p(d.getDate()) + "-" + String(Math.floor(1000 + Math.random() * 9000)); }
 const res = document.getElementById("result"), sumEl = document.getElementById("sumText"), refEl = document.getElementById("refNo");
 const toast = document.getElementById("toast"), mail = document.getElementById("btnMail"), soon = document.getElementById("soonNote");
 let summary = "", ref = "";
 form.addEventListener("submit", e => {
  e.preventDefault();
  let first = null;
  [...form.querySelectorAll("input,select,textarea")].filter(x => x.required || x.value).forEach(x => { if(!check(x) && !first) first = x; });
  if(first){ first.focus(); return; }
  ref = makeRef();
  const need = form.elements.need.selectedOptions[0];
  const lines = ["EASY CLINIC CENTER - REQUEST", "Reference: " + ref, "Language used: " + lang.toUpperCase(),
   "Request: " + strip(EN[need.dataset.i]) + (form.elements.need.value === "second" ? " (first request - free)" : ""),
   "Name: " + form.elements.fullname.value.trim(), "Contact: " + form.elements.contact.value.trim(),
   "Message: " + form.elements.msg.value.trim()];
  if(form.elements.country.value.trim()) lines.push("Country: " + form.elements.country.value.trim());
  if(form.elements.meds.value.trim()) lines.push("Medicines / allergies / previous operations: " + form.elements.meds.value.trim());
  summary = lines.join("\n");
  refEl.textContent = ref; sumEl.textContent = summary;
  if(CONTACT){
   mail.href = "mailto:" + CONTACT + "?subject=" + encodeURIComponent("Request " + ref) + "&body=" + encodeURIComponent(summary.slice(0, 1500));
   mail.hidden = false; soon.hidden = true;
  }
  form.hidden = true; res.hidden = false; res.focus(); res.scrollIntoView({block: "start"});
 });
 document.getElementById("btnEdit").addEventListener("click", () => { res.hidden = true; form.hidden = false; form.elements.fullname.focus(); });
 document.getElementById("btnCopy").addEventListener("click", async () => {
  try{ await navigator.clipboard.writeText(summary); toast.textContent = L.copied; }
  catch(err){ const r = document.createRange(); r.selectNodeContents(sumEl); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  setTimeout(() => toast.textContent = "", 2500);
 });
 document.getElementById("btnSave").addEventListener("click", () => {
  const url = URL.createObjectURL(new Blob([summary], {type: "text/plain;charset=utf-8"}));
  const a = document.createElement("a"); a.href = url; a.download = ref + ".txt";
  document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  toast.textContent = L.saved; setTimeout(() => toast.textContent = "", 2500);
 });

 /* hide the sticky mobile button while the form is on screen */
 const mbar = document.querySelector(".mbar"), ap = document.getElementById("apply");
 if(mbar && ap && "IntersectionObserver" in window){
  new IntersectionObserver(es => mbar.classList.toggle("off", es.some(e => e.isIntersecting))).observe(ap);
 }
})();
'''


# ------------------------------------------------------------------ SEO, assets, blog, page assembly
META = {
 "en": ("JavaScript is needed for the request form.", "en_GB"),
 "fr": ("JavaScript est nécessaire pour le formulaire de demande.", "fr_FR"),
 "ar": ("يلزم تفعيل جافاسكربت لاستخدام نموذج الطلب.", "ar_AR"),
 "ru": ("Для формы заявки нужен JavaScript.", "ru_RU"),
}
TITLE, META_DESC = META2[LC]
NOSCRIPT, OG_LOCALE = META[LC]
URL = SITE + LANG_PATH[LC]
DIR = "rtl" if LC == "ar" else "ltr"
ESC = lambda t: H.escape(t, quote=True)

def plain(t):
    return H.unescape(re.sub(r"<[^>]+>", "", t)).strip()

def hreflang(l):
    return "en-GB" if l == "en" else l

def og_image(path):
    return SITE + "/" + path

# ---- markdown (small subset used by the blog)
def inline_md(t, A):
    t = H.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith("/"):
            url = A + url.lstrip("/")
        ext = ' rel="noopener" target="_blank"' if url.startswith("http") else ""
        return f'<a href="{url}"{ext}>{text}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)

def md_to_html(body, A):
    out, para, items = [], [], []
    def flush():
        nonlocal para, items
        if para: out.append("<p>" + inline_md(" ".join(para), A) + "</p>"); para = []
        if items: out.append("<ul>" + "".join(f"<li>{inline_md(i, A)}</li>" for i in items) + "</ul>"); items = []
    for line in body.splitlines():
        s = line.strip()
        if not s: flush(); continue
        if s.startswith("### "): flush(); out.append(f"<h3>{inline_md(s[4:], A)}</h3>")
        elif s.startswith("## "): flush(); out.append(f"<h2>{inline_md(s[3:], A)}</h2>")
        elif s.startswith(("- ", "* ")):
            if para: flush()
            items.append(s[2:].strip())
        else:
            if items: flush()
            para.append(s)
    flush()
    return "\n".join(out)

BLOG_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,500;0,600;1,500&display=swap"/>'

def blog_opts(A):
    en = A or "./"
    o = f'<option value="{en}" selected>English</option>'
    o += "".join(f'<option value="{A}{l}/">{LANG_NAMES[l]}</option>' for l in LANGS if l != "en")
    return o

def blog_page(A, title, desc, canonical, main_html, jsonld="", ogtype="website"):
    head = f'''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{ESC(title)}</title>
<meta name="description" content="{ESC(desc)}"/>
<meta name="theme-color" content="#24507A"/>
<link rel="canonical" href="{canonical}"/>
<link rel="icon" href="{A}favicon.ico" sizes="any"/>
<link rel="apple-touch-icon" href="{A}apple-touch-icon.png"/>
<meta property="og:type" content="{ogtype}"/><meta property="og:site_name" content="Easy Clinic Center"/>
<meta property="og:title" content="{ESC(title)}"/><meta property="og:description" content="{ESC(desc)}"/>
<meta property="og:url" content="{canonical}"/><meta property="og:image" content="{og_image('og.png')}"/><meta property="og:locale" content="en_GB"/>
<meta name="twitter:card" content="summary_large_image"/>
{jsonld}
{BLOG_FONTS}
<link rel="stylesheet" href="{A}assets/site.css"/>
</head>
<body>
{make_header(A, A, blog_opts(A))}
<main id="main">{main_html}</main>
{make_footer(A, A)}
<script>document.getElementById("lang").addEventListener("change", e => {{ location.href = e.target.value; }});</script>
</body>
</html>
'''
    return head

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

def build_blog():
    site = ROOT / "site"
    (site / "blog").mkdir(exist_ok=True)
    # index
    A = "../"
    idx = f'''
<section class="sec"><div class="wrap">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="{A}">Home</a> <span aria-hidden="true">/</span> <span>Blog</span></nav>
 <p class="eyebrow">Guides</p><h1 class="blog-h1">Health guides for patients considering a second opinion or treatment in Türkiye</h1>
 <p class="lead2 blog-lead">Plain-language checklists written to help you decide with confidence. They are general information and do not replace advice from your own doctor.</p>
 <div class="pgrid">{post_cards(POSTS, A)}</div>
</div></section>
<section class="sec cta2"><div class="wrap"><h2>Your first second opinion is free</h2><a class="btn btn-p btn-l" href="{A}#apply">{T("m_apply")}{ic("arrow", "ic dir")}</a></div></section>'''
    ld_idx = ld({"@context": "https://schema.org", "@type": "Blog", "name": "Easy Clinic Center guides", "url": SITE + "/blog/", "inLanguage": "en-GB",
                 "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]})
    (site / "blog" / "index.html").write_text(blog_page(A, "Health guides: second opinion and treatment in Türkiye | Easy Clinic Center",
        "Plain-language guides for UK patients: second medical opinions, preparing records, questions to ask before treatment abroad and planning a trip to Türkiye.",
        SITE + "/blog/", idx, ld_idx), encoding="utf-8")
    # posts
    for n, p in enumerate(POSTS):
        A = "../../"
        related = [q for q in POSTS if q["slug"] != p["slug"]][:2]
        url = f"{SITE}/blog/{p['slug']}/"
        art = f'''
<article class="sec post"><div class="wrap narrow">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="{A}">Home</a> <span aria-hidden="true">/</span> <a href="{A}blog/">Blog</a></nav>
 <h1 class="blog-h1">{ESC(p["title"])}</h1>
 <p class="pmeta"><time datetime="{p["date"]}">{p["date"]}</time> · {p["mins"]} min read</p>
 <div class="prose">{md_to_html(p["body"], A)}</div>
 <aside class="postcta"><h2>{ic("heart")} Your first second opinion is free</h2><p>Send us your question and records. A specialist physician reviews them and writes you a report.</p><a class="btn btn-p btn-l" href="{A}#apply">{T("m_apply")}{ic("arrow", "ic dir")}</a></aside>
 <h2 class="rel-h">More guides</h2><div class="pgrid two">{post_cards(related, A)}</div>
</div></article>'''
        j = ld({"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
             "inLanguage": "en-GB", "mainEntityOfPage": url, "image": og_image("og.png"),
             "author": {"@type": "Organization", "name": "Easy Clinic Center"},
             "publisher": {"@type": "Organization", "name": "Easy Clinic Center", "logo": {"@type": "ImageObject", "url": SITE + "/apple-touch-icon.png"}}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]})
        d = site / "blog" / p["slug"]; d.mkdir(exist_ok=True)
        (d / "index.html").write_text(blog_page(A, p["title"] + " | Easy Clinic Center", p["desc"], url, art, j, "article"), encoding="utf-8")
    # RSS
    items = "".join(f'<item><title>{ESC(p["title"])}</title><link>{SITE}/blog/{p["slug"]}/</link><guid>{SITE}/blog/{p["slug"]}/</guid><pubDate>{datetime.date.fromisoformat(p["date"]).strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate><description>{ESC(p["desc"])}</description></item>' for p in POSTS)
    (site / "blog" / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Easy Clinic Center guides</title><link>{SITE}/blog/</link><description>Health guides for patients considering a second opinion or treatment in Türkiye.</description><language>en-gb</language>{items}</channel></rss>', encoding="utf-8")

def make_assets():
    from PIL import Image
    site = ROOT / "site"
    (site / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(web_logo("logo.png"), site / "assets" / "logo.png")
    shutil.copy(web_logo("logo_white.png"), site / "assets" / "logo_white.png")
    (site / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    logo = Image.open(ROOT / "brand" / "logo.png").convert("RGBA")
    sq = Image.new("RGBA", (max(logo.size),) * 2, (255, 255, 255, 255))
    sq.paste(logo, ((sq.width - logo.width) // 2, (sq.height - logo.height) // 2), logo)
    sq.resize((180, 180), Image.LANCZOS).convert("RGB").save(site / "apple-touch-icon.png")
    sq.resize((32, 32), Image.LANCZOS).save(site / "favicon.ico", sizes=[(32, 32)])
    og = Image.new("RGB", (1200, 630), (36, 80, 122))
    wl = Image.open(ROOT / "brand" / "logo_white.png").convert("RGBA")
    wl = wl.resize((round(wl.width * 420 / wl.height), 420), Image.LANCZOS)
    og.paste(wl, ((1200 - wl.width) // 2, (630 - wl.height) // 2), wl)
    og.save(site / "og.png", optimize=True)
    (site / ".nojekyll").write_text("")
    (site / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    hl = "".join(f'<xhtml:link rel="alternate" hreflang="{hreflang(l)}" href="{SITE}{LANG_PATH[l]}"/>' for l in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
    urls = "".join(f"<url><loc>{SITE}{LANG_PATH[l]}</loc>{hl}</url>" for l in LANGS)
    urls += f"<url><loc>{SITE}/blog/</loc></url>" + "".join(f"<url><loc>{SITE}/blog/{p['slug']}/</loc><lastmod>{p['date']}</lastmod></url>" for p in POSTS)
    (site / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n')

if LI == 0:
    make_assets()
    build_blog()

JSONLD = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": SITE + "/#org", "name": "Easy Clinic Center", "url": SITE + "/",
     "logo": SITE + "/apple-touch-icon.png", "foundingDate": "2020-10-01",
     "areaServed": {"@type": "Country", "name": "United Kingdom"}, "description": META_DESC},
    {"@type": "WebSite", "@id": SITE + "/#web", "url": SITE + "/", "name": "Easy Clinic Center",
     "inLanguage": [hreflang(l) for l in LANGS], "publisher": {"@id": SITE + "/#org"}},
    {"@type": "FAQPage", "url": URL, "inLanguage": hreflang(LC), "mainEntity": [
        {"@type": "Question", "name": plain(S[f"q{i}"][LI]),
         "acceptedAnswer": {"@type": "Answer", "text": plain(S[f"a{i}"][LI])}} for i in range(1, FAQ_N + 1)]},
]}, ensure_ascii=False).replace("</", "<\\/")

ALT = "".join(f'<link rel="alternate" hreflang="{hreflang(l)}" href="{SITE}{LANG_PATH[l]}"/>\n' for l in LANGS)
ALT += f'<link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
OG_ALT = "".join(f'<meta property="og:locale:alternate" content="{META[l][1]}"/>' for l in LANGS if l != LC)
HEAD_SEO = f'''<meta name="description" content="{ESC(META_DESC)}"/>
<meta name="theme-color" content="#24507A"/>
<link rel="canonical" href="{URL}"/>
{ALT}
<link rel="icon" href="{REL}favicon.ico" sizes="any"/>
<link rel="apple-touch-icon" href="{REL}apple-touch-icon.png"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Easy Clinic Center"/>
<meta property="og:title" content="{ESC(TITLE)}"/>
<meta property="og:description" content="{ESC(META_DESC)}"/>
<meta property="og:url" content="{URL}"/>
<meta property="og:image" content="{SITE}/og.png"/>
<meta property="og:locale" content="{OG_LOCALE}"/>{OG_ALT}
<meta name="twitter:card" content="summary_large_image"/>
<link rel="alternate" type="application/rss+xml" title="Easy Clinic Center guides" href="{REL}blog/feed.xml"/>
<script type="application/ld+json">{JSONLD}</script>'''

AR_FONTS = "&family=Noto+Naskh+Arabic:wght@500;600&family=Noto+Sans+Arabic:wght@400;500;600;700" if LC == "ar" else ""
FONTS = f'<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,500;0,600;1,500{AR_FONTS}&display=swap"/>'

JS_I18N = {LC: I18N[LC], "en": I18N["en"]}
page = f'''<!doctype html>
<html lang="{LC}" dir="{DIR}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{ESC(TITLE)}</title>
{HEAD_SEO}
{FONTS}
<link rel="stylesheet" href="{REL}assets/site.css"/>
</head>
<body>
<noscript><p style="padding:16px;text-align:center">{NOSCRIPT}</p></noscript>
{header}
<main id="main">{hero}{second}{treat}{how}{hospitals}{travel}{blogsec}{faq}{cta2}</main>
{footer}
<script>{JS.replace("__I18N__", json.dumps(JS_I18N, ensure_ascii=False)).replace("__CONTACT__", CONTACT_EMAIL)}</script>
</body>
</html>
'''
out = ROOT / "site" / LANG_PATH[LC].strip("/") / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page, encoding="utf-8")
print(LC, len(page) // 1024, "KB")
