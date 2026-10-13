"""Builds the Easy Clinic Center website (EN default, FR / AR (RTL) / RU) as one HTML page."""
import json, base64, pathlib, html as H
import illus
from web_strings import S

LANGS = ["en", "fr", "ar", "ru"]
I18N = {l: {k: v[i] for k, v in S.items()} for i, l in enumerate(LANGS)}

def T(key, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag} data-i="{key}"{c}{a}>{S[key][0]}</{tag}>'

def b64(p):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

LOGO = b64("/home/claude/cat/web_logo.png")
LOGO_W = b64("/home/claude/cat/web_logo_white.png")
ISO = pathlib.Path("/home/claude/cat/iso_none.svg").read_text()

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

header = f'''
<a class="skip" href="#main">{S["skip"][0]}</a>
<header class="hdr" id="top">
 <div class="wrap hdr-in">
  <a class="brand" href="#top" aria-label="Easy Clinic Center"><img class="logo-l" src="{LOGO}" alt="Easy Clinic Center"/><img class="logo-d" src="{LOGO_W}" alt="Easy Clinic Center"/></a>
  <nav class="nav" aria-label="Main">
   <a href="#about">{T("nav_about")}</a><a href="#how">{T("nav_how")}</a><a href="#treatments">{T("nav_treat")}</a><a href="#second">{T("nav_second")}</a><a href="#hospitals">{T("nav_hosp")}</a><a href="#travel">{T("nav_travel")}</a><a href="#faq">{T("nav_faq")}</a>
  </nav>
  <div class="hdr-act">
   <label class="sr" for="lang">{S["lang_label"][0]}</label>
   <select id="lang" class="lang">
    <option value="en">English</option><option value="fr">Français</option><option value="ar">العربية</option><option value="ru">Русский</option>
   </select>
   <a class="btn btn-p hdr-apply" href="#apply">{T("nav_apply")}</a>
  </div>
 </div>
</header>'''

hero = f'''
<section class="hero">
 <div class="wrap hero-in">
  <div class="hero-txt">
   {T("hero_eb", "p", "eyebrow")}
   {T("hero_h1", "h1")}
   {T("hero_sub", "p", "lead")}
   <div class="ctas"><a class="btn btn-p btn-l" href="#apply">{T("cta_apply")}{ic("arrow", "ic dir")}</a><a class="btn btn-s btn-l" href="#second">{T("cta_second")}</a></div>
   <p class="hero-note">{ic("shield")}{T("hero_note")}</p>
  </div>
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
 </div>
 <div class="wrap stats">
  <div><b>2020</b>{T("st1")}</div><div><b>7/7</b>{T("st2")}</div><div><b>14</b>{T("st3")}</div><div><b>4</b>{T("st4")}</div>
 </div>
</section>
<div class="trust"><div class="wrap trust-in">
 <p>{ic("doc")}{T("tr1")}</p><p>{ic("steth")}{T("tr2")}</p><p>{ic("lock")}{T("tr3")}</p><p>{ic("user")}{T("tr4")}</p>
</div></div>'''

about = f'''
<section class="sec" id="about"><div class="wrap">
 <div class="about">
  <div>{T("ab_eb", "p", "eyebrow")}{T("ab_h2", "h2")}{T("ab_lead", "p", "lead2")}</div>
  <div class="about-p">{T("ab_p1", "p")}{T("ab_p2", "p")}</div>
 </div>
 <div class="values">
  {"".join(f'<div class="val">{ic(i)}{T(h, "h3")}{T(p, "p")}</div>' for i, h, p in [("doc", "v1_h", "v1_p"), ("steth", "v2_h", "v2_p"), ("user", "v3_h", "v3_p"), ("lock", "v4_h", "v4_p")])}
 </div>
</div></section>'''

how = f'''
<section class="sec alt" id="how"><div class="wrap">
 {T("how_eb", "p", "eyebrow")}{T("how_h2", "h2")}
 <div class="how">
  <div class="iso plate" aria-hidden="true">{ISO}</div>
  <ol class="steps">
   {"".join(f'<li><span class="sn">{n}</span><div>{T(h, "h3")}{T(p, "p")}</div></li>' for n, h, p in [(1, "s1_h", "s1_p"), (2, "s2_h", "s2_p"), (3, "s3_h", "s3_p")])}
  </ol>
 </div>
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
  {"".join(f'<li class="{c}"><span class="sn">{n}</span>{ic(i)}{T(h, "h3")}{T(p, "p")}</li>' for n, i, h, p, c in [(1, "upload", "so1_h", "so1_p", ""), (2, "ai", "so2_h", "so2_p", "ai"), (3, "steth", "so3_h", "so3_p", ""), (4, "report", "so4_h", "so4_p", "")])}
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
 <div class="faq">{"".join(f'<details><summary>{T(f"q{i}")}</summary>{T(f"a{i}", "p")}</details>' for i in range(1, 8))}</div>
</div></section>'''

# ------------------------------------------------------------------ form
def fld(id_, key, typ="text", req=False, auto="", extra="", full=False, hint=None):
    star = '<b class="req" aria-hidden="true">*</b>' if req else ""
    r = " required" if req else ""
    a = f' autocomplete="{auto}"' if auto else ""
    h = f'{T(hint, "p", "hint", f"id=\"{id_}-h\"")}' if hint else ""
    desc = f' aria-describedby="{id_}-e{(" " + id_ + "-h") if hint else ""}"'
    if typ == "textarea":
        ctl = f'<textarea id="{id_}" name="{id_}" rows="4"{r}{desc}></textarea>'
    else:
        ctl = f'<input id="{id_}" name="{id_}" type="{typ}"{r}{a}{desc}{extra}/>'
    return f'<div class="f{" full" if full else ""}"><label for="{id_}">{T(key)}{star}</label>{h}{ctl}<p class="err" id="{id_}-e" hidden></p></div>'

def sel(id_, key, opts, req=False, full=False):
    star = '<b class="req" aria-hidden="true">*</b>' if req else ""
    r = " required" if req else ""
    o = '<option value="" data-i="choose">Choose…</option>' if req else ""
    o += "".join(f'<option value="{v}"{" data-i=" + chr(34) + k + chr(34) if k else ""}>{S[k][0] if k else lbl}</option>' for v, k, lbl in opts)
    return f'<div class="f{" full" if full else ""}"><label for="{id_}">{T(key)}{star}</label><select id="{id_}" name="{id_}"{r} aria-describedby="{id_}-e">{o}</select><p class="err" id="{id_}-e" hidden></p></div>'

def tick(id_, key, req=True):
    star = '<b class="req" aria-hidden="true">*</b>' if req else ""
    r = " required" if req else ""
    return f'<div class="f full tk"><label class="chk"><input type="checkbox" id="{id_}" name="{id_}"{r} aria-describedby="{id_}-e"/><span>{T(key)}{star}</span></label><p class="err" id="{id_}-e" hidden></p></div>'

CONDS = ["c_diab", "c_bp", "c_heart", "c_blood", "c_allergy", "c_surgery", "c_smoke", "c_preg"]
step1 = f'''<fieldset class="step" data-step="1"><legend>{T("g1")}</legend><div class="fg">
 {fld("fn", "fn", req=True, auto="given-name")}{fld("ln", "ln", req=True, auto="family-name")}
 {fld("dob", "dob", "date", True, "bday")}{fld("country", "country", req=True, auto="country-name")}
 {fld("phone", "phone", "tel", True, "tel", ' inputmode="tel" dir="ltr" placeholder="+44"')}{fld("email", "email", "email", True, "email", ' dir="ltr"')}
 {sel("contact", "contact", [("whatsapp", None, "WhatsApp"), ("phone", "o_phonecall", ""), ("email", "email", "")])}
 {sel("plang", "plang", [("English", None, "English"), ("Français", None, "Français"), ("العربية", None, "العربية"), ("Русский", None, "Русский"), ("Türkçe", None, "Türkçe")])}
</div></fieldset>'''
step2 = f'''<fieldset class="step" data-step="2" hidden><legend>{T("g2")}</legend><div class="fg">
 {sel("need", "need", [("treat", "n_treat", ""), ("plastic", "n_plastic", ""), ("dental", "n_dental", ""), ("second", "n_second", ""), ("chronic", "n_chronic", ""), ("unsure", "n_unsure", "")], True, True)}
 {fld("complaint", "complaint", "textarea", True, full=True, hint="complaint_h")}
 {fld("diag", "diag", full=True)}
 {sel("pcity", "pcity", [("any", "anycity", ""), ("İstanbul", "c_ist", ""), ("Ankara", "c_ank", ""), ("İzmir", "c_izm", ""), ("Antalya", "c_ant", "")], full=True)}
 <div class="photo full" id="photoBox" hidden>
  <h3>{ic("face")}{T("photo_h")}</h3>{T("photo_p", "p")}
  <div class="dd"><div class="dd-y"><b>{ic("check")}{T("do")}</b>{T("do_p", "p")}</div><div class="dd-n"><b>{ic("x")}{T("dont")}</b>{T("dont_p", "p")}</div></div>
  {T("photo_face", "p", "pf")}
  {tick("photo_ok", "photo_ok")}
 </div>
</div></fieldset>'''
step3 = f'''<fieldset class="step" data-step="3" hidden><legend>{T("g3")}</legend><div class="fg">
 {fld("hgt", "hgt", "number", extra=' inputmode="numeric" min="50" max="250"')}{fld("wgt", "wgt", "number", extra=' inputmode="numeric" min="20" max="350"')}
 <div class="f full"><p class="lbl">{T("cond")}</p><div class="conds">{"".join(f'<label class="chk"><input type="checkbox" name="cond" value="{c}" id="{c}"/><span>{T(c)}</span></label>' for c in CONDS)}</div></div>
 <div class="full" id="detBox" hidden>{fld("details", "details", "textarea", full=True)}</div>
 {fld("meds", "meds", "textarea", full=True)}
</div></fieldset>'''
step4 = f'''<fieldset class="step" data-step="4" hidden><legend>{T("g4")}</legend><div class="fg">
 <div class="f full" role="radiogroup" aria-labelledby="quote-l"><p class="lbl" id="quote-l">{T("quote")}<b class="req" aria-hidden="true">*</b></p>
  <div class="radios">{"".join(f'<label class="rad"><input type="radio" name="quote" value="{v}" id="quote-{v}"{" required" if v == "A" else ""}/><span>{T(k)}</span></label>' for v, k in [("A", "q_a"), ("B", "q_b"), ("both", "q_both")])}</div>
  <p class="err" id="quote-e" hidden></p></div>
 {fld("dates", "dates")}{fld("comp", "comp", "number", extra=' inputmode="numeric" min="0" max="6"')}
 {tick("cons1", "cons1")}{tick("cons2", "cons2")}{tick("cons3", "cons3")}
</div></fieldset>'''

form = f'''
<section class="sec" id="apply"><div class="wrap narrow">
 {T("ap_eb", "p", "eyebrow")}{T("ap_h2", "h2")}{T("ap_p", "p", "sub")}
 <div class="formcard">
  <div class="prog" aria-hidden="true"><div class="prog-bar"><span id="progFill"></span></div>
   <ol class="prog-l">{"".join(f'<li data-n="{n}">{T(k)}</li>' for n, k in [(1, "g1"), (2, "g2"), (3, "g3"), (4, "g4")])}</ol></div>
  <p class="stepno" id="stepNo" aria-live="polite"><span data-i="step">Step</span> <span id="sN">1</span> <span data-i="of">of</span> 4</p>
  <form id="appForm" novalidate>
   {step1}{step2}{step3}{step4}
   <div class="fnav"><button type="button" class="btn btn-s" id="btnBack" hidden>{T("back")}</button><button type="button" class="btn btn-p" id="btnNext">{T("next")}</button><button type="submit" class="btn btn-p" id="btnSubmit" hidden>{T("submit")}</button></div>
  </form>
  <div class="result" id="result" hidden tabindex="-1">
   {ic("check", "ic big")}{T("res_h", "h3")}
   <p class="refl">{T("ref")}: <bdi class="ref" id="refNo"></bdi></p>
   {T("res_p", "p")}
   <pre class="sum" id="sumText" dir="ltr" tabindex="0"></pre>
   <div class="ract"><button type="button" class="btn btn-p" id="btnSave" hidden>{T("save")}</button><button type="button" class="btn btn-s" id="btnCopy">{T("copy")}</button><button type="button" class="btn btn-g" id="btnEdit">{T("edit")}</button><span class="toast" id="toast" role="status"></span></div>
   <p class="soon">{ic("clock")}{T("contacts_soon")}</p>
  </div>
  {T("fullform", "p", "full-form")}
 </div>
</div></section>'''

footer = f'''
<footer class="ftr"><div class="wrap ftr-in">
 <div class="ft-b"><img src="{LOGO_W}" alt="Easy Clinic Center" class="ft-logo"/>{T("ft_tag", "p")}</div>
 <div class="ft-c">
  <div>{T("ft_hours", "h4")}{T("ft_hours_v", "p")}</div>
  <div>{T("ft_office", "h4")}{T("ft_office_v", "p")}</div>
  <div>{T("ft_contact", "h4")}<p><span>www.easycliniccenter.com</span><br/>{T("ft_contact_v", "span", "muted")}</p></div>
 </div>
 {T("ft_legal", "p", "legal")}
 <p class="copy">© 2026 Easy Clinic Center</p>
</div></footer>
<div class="mbar"><a class="btn btn-p" href="#apply">{T("m_apply")}</a></div>'''

CSS = r'''
/* Layout: one wide column of bands; brand gradient strip runs down the inline-end edge, as in the printed catalogues. */
:root{
 --bg:#FFFFFF; --bg-alt:#F1F8FA; --surface:#FFFFFF; --ink:#16324A; --muted:#566C7E; --line:#D7E7EE;
 --navy:#24507A; --accent:#22AFC4; --accent-ink:#137C8D; --aqua:#1EE6CF; --leaf:#8DC63F; --leaf-ink:#4E7F1B;
 --plate:#EAF7FA; --btn-bg:#24507A; --btn-fg:#FFFFFF; --band:#163A5A; --band-ink:#E9F4F8; --band-muted:#B9D4E1; --band-card:#1E4B70;
 --warn-bg:#FFF2F0; --warn-line:#E7A79D; --warn-ink:#9B2F22; --ok-bg:#EFF8E6;
 --font-d:"Lora", Georgia, "Times New Roman", serif; --font-b:"Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
 --r:14px; --r-s:10px; --shadow:0 1px 2px rgba(22,50,74,.06), 0 8px 24px rgba(22,50,74,.07);
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
 --bg:#0D1A26; --bg-alt:#112231; --surface:#14293B; --ink:#E5EFF5; --muted:#9DB3C3; --line:#24394C;
 --navy:#9CCBEA; --accent:#3DD5E6; --accent-ink:#62DDEB; --aqua:#1EE6CF; --leaf:#9ED35A; --leaf-ink:#A9DA6B;
 --plate:#DCEFF3; --btn-bg:#3DD5E6; --btn-fg:#0B2233; --band:#0A2236; --band-ink:#E9F4F8; --band-muted:#A9C6D6; --band-card:#143552;
 --warn-bg:#3A1F1C; --warn-line:#8A4A40; --warn-ink:#F4B4A9; --ok-bg:#1C2E14; color-scheme:dark;
 --shadow:0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.25);}}
:root[data-theme="dark"]{
 --bg:#0D1A26; --bg-alt:#112231; --surface:#14293B; --ink:#E5EFF5; --muted:#9DB3C3; --line:#24394C;
 --navy:#9CCBEA; --accent:#3DD5E6; --accent-ink:#62DDEB; --aqua:#1EE6CF; --leaf:#9ED35A; --leaf-ink:#A9DA6B;
 --plate:#DCEFF3; --btn-bg:#3DD5E6; --btn-fg:#0B2233; --band:#0A2236; --band-ink:#E9F4F8; --band-muted:#A9C6D6; --band-card:#143552;
 --warn-bg:#3A1F1C; --warn-line:#8A4A40; --warn-ink:#F4B4A9; --ok-bg:#1C2E14; color-scheme:dark;
 --shadow:0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.25);}
:root[lang="ar"]{ --font-d:"Noto Naskh Arabic", "Lora", serif; --font-b:"Noto Sans Arabic", "Inter", system-ui, sans-serif; }
*{box-sizing:border-box}
html{scroll-behavior:smooth; scroll-padding-top:calc(84px + env(safe-area-inset-top,0px))}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto} *{transition:none!important}}
body{background:var(--bg); color:var(--ink); font-family:var(--font-b); font-size:16px; line-height:1.6; margin:0; overflow-x:hidden}
body::after{content:""; position:fixed; inset-block:0; inset-inline-end:0; width:6px; background:linear-gradient(180deg,#3DD5E6,#1EF2D6 55%,#3DD5E6); z-index:60; pointer-events:none}
.wrap{max-width:1160px; margin-inline:auto; padding-inline:max(16px, 4vw)}
.wrap.narrow{max-width:860px}
h1,h2,h3{font-family:var(--font-d); color:var(--navy); text-wrap:balance; margin:0; font-weight:500; line-height:1.15}
h1{font-size:clamp(2.1rem, 4.6vw, 3.4rem)}
h2{font-size:clamp(1.7rem, 3.2vw, 2.4rem); margin-block:.25em .5em}
h3{font-size:1.2rem; font-weight:600}
h1 em,h2 em{font-style:italic; color:var(--accent-ink)}
:root[lang="ar"] h1 em,:root[lang="ar"] h2 em{font-style:normal}
p{margin:0}
a{color:var(--accent-ink)}
.ic{width:1.15em; height:1.15em; flex:none; vertical-align:-.2em}
:root[dir="rtl"] .ic.dir{transform:scaleX(-1)}
.sr{position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap}
.skip{position:absolute; inset-inline-start:16px; top:-60px; background:var(--btn-bg); color:var(--btn-fg); padding:8px 14px; border-radius:8px; z-index:100}
.skip:focus{top:calc(8px + env(safe-area-inset-top,0px))}
:focus-visible{outline:3px solid var(--accent); outline-offset:2px; border-radius:4px}
.eyebrow{font-size:.78rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--accent-ink)}
:root[lang="ar"] .eyebrow{letter-spacing:0}
.lead{font-size:1.12rem; color:var(--muted); max-width:58ch}
.lead2{font-family:var(--font-d); font-size:1.18rem; color:var(--ink); line-height:1.55; max-width:60ch}
.sub{color:var(--muted); max-width:62ch; margin-block-end:28px}
.btn{display:inline-flex; align-items:center; justify-content:center; gap:.5em; min-height:44px; padding:10px 20px; border-radius:999px; border:1.5px solid transparent; font:600 .95rem/1.2 var(--font-b); text-decoration:none; cursor:pointer; transition:transform .15s, background .15s}
.btn:hover{transform:translateY(-1px)}
.btn-p{background:var(--btn-bg); color:var(--btn-fg)}
.btn-s{background:transparent; color:var(--navy); border-color:var(--line)}
.btn-s:hover{border-color:var(--accent)}
.btn-g{background:transparent; color:var(--muted)}
.btn-l{min-height:50px; padding:12px 24px; font-size:1rem}
.req{color:#D04A3C; margin-inline-start:2px}

/* header */
.hdr{position:sticky; top:env(safe-area-inset-top,0px); z-index:50; background:color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter:blur(10px); border-bottom:1px solid var(--line)}
.hdr-in{display:flex; align-items:center; gap:20px; min-height:72px; flex-wrap:wrap}
.brand{display:flex; align-items:center}
.brand img{height:54px; width:auto}
.logo-d{display:none}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .logo-l{display:none} :root:not([data-theme="light"]) .logo-d{display:block}}
:root[data-theme="dark"] .logo-l{display:none} :root[data-theme="dark"] .logo-d{display:block}
.nav{display:flex; gap:18px; flex:1; justify-content:center; flex-wrap:wrap}
.nav a{color:var(--ink); text-decoration:none; font-size:.92rem; font-weight:500; padding-block:6px; border-bottom:2px solid transparent}
.nav a:hover{border-color:var(--accent)}
.hdr-act{display:flex; align-items:center; gap:10px}
.lang{min-height:40px; border:1.5px solid var(--line); background:var(--surface); color:var(--ink); border-radius:999px; padding-inline:12px; font:500 .9rem var(--font-b)}

/* hero */
.hero{padding-block:56px 28px; background:radial-gradient(1100px 420px at 85% -10%, color-mix(in srgb, var(--accent) 14%, transparent), transparent 70%)}
.hero-in{display:grid; grid-template-columns:1.15fr .85fr; gap:48px; align-items:center}
.hero-txt{display:flex; flex-direction:column; gap:18px; min-width:0}
.ctas{display:flex; gap:12px; flex-wrap:wrap; margin-block-start:6px}
.hero-note{display:flex; gap:8px; align-items:flex-start; color:var(--muted); font-size:.92rem; max-width:52ch}
.hero-note .ic{color:var(--leaf-ink); margin-top:.25em}
.qcard{background:var(--surface); border:1px solid var(--line); border-radius:20px; padding:22px; box-shadow:var(--shadow); min-width:0}
.qc-ex{display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); border:1px dashed var(--line); border-radius:999px; padding:3px 10px; margin-bottom:10px}
.qcard h2{font-size:1.45rem; margin:0}
.qc-sub{color:var(--muted); font-size:.92rem; margin-block:4px 14px}
.qopts{display:grid; grid-template-columns:1fr 1fr; gap:10px}
.qopt{border-radius:var(--r-s); padding:12px; border:1.5px solid}
.qopt.a{border-color:color-mix(in srgb, var(--accent) 55%, transparent); background:color-mix(in srgb, var(--accent) 7%, var(--surface))}
.qopt.b{border-color:color-mix(in srgb, var(--leaf) 60%, transparent); background:color-mix(in srgb, var(--leaf) 8%, var(--surface))}
.qo-k{font-size:.72rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--muted)}
.qo-n{font-family:var(--font-d); font-weight:600; color:var(--navy); font-size:1.05rem; margin-bottom:6px}
.qopt ul,.wl,.after ul{list-style:none; padding:0; margin:0}
.qopt li{display:flex; gap:6px; align-items:flex-start; font-size:.88rem; padding-block:2px}
.qopt.a li .ic{color:var(--accent-ink)} .qopt.b li .ic{color:var(--leaf-ink)}
.qopt li.opt{color:var(--muted)}
.qc-note{font-size:.82rem; color:var(--muted); margin-top:12px}
.stats{display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:40px}
.stats div{display:flex; flex-direction:column; border-inline-start:3px solid var(--accent); padding-inline-start:14px; font-size:.88rem; color:var(--muted)}
.stats b{font-family:var(--font-d); font-size:1.9rem; font-weight:600; color:var(--navy); line-height:1.1; font-variant-numeric:tabular-nums}
.trust{border-block:1px solid var(--line); background:var(--bg-alt)}
.trust-in{display:grid; grid-template-columns:repeat(4,1fr); gap:16px; padding-block:16px}
.trust p{display:flex; gap:8px; align-items:flex-start; font-size:.88rem; font-weight:500; color:var(--ink)}
.trust .ic{color:var(--accent-ink); margin-top:.2em}

/* sections */
.sec{padding-block:80px}
.sec.alt{background:var(--bg-alt)}
.about{display:grid; grid-template-columns:1.1fr .9fr; gap:48px; align-items:end}
.about-p{display:flex; flex-direction:column; gap:14px; color:var(--muted)}
.values{display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:40px}
.val{border-top:2px solid var(--line); padding-top:16px; display:flex; flex-direction:column; gap:6px}
.val .ic{color:var(--accent-ink); width:26px; height:26px}
.val p{color:var(--muted); font-size:.93rem}
.plate{background:var(--plate); border-radius:var(--r)}
.plate svg{display:block; width:100%; height:auto}
.how{display:grid; grid-template-columns:1.15fr .85fr; gap:36px; align-items:center; margin-top:12px}
.iso{padding:8px; overflow:hidden}
.steps{list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:22px}
.steps li{display:flex; gap:14px}
.sn{flex:none; width:36px; height:36px; border-radius:50%; background:var(--btn-bg); color:var(--btn-fg); display:grid; place-items:center; font-weight:700}
.steps p{color:var(--muted); margin-top:4px}
.opts2{display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:36px}
.opt2{background:var(--surface); border-radius:var(--r); padding:22px; border:1px solid var(--line); display:flex; flex-direction:column; gap:6px}
.opt2.a{box-shadow:inset 0 3px 0 var(--accent)} .opt2.b{box-shadow:inset 0 3px 0 var(--leaf)}
.opt2 p{color:var(--muted)}
.best{font-size:.9rem; font-weight:600; color:var(--ink)!important; margin-top:6px}
.after{margin-top:16px; background:var(--surface); border:1px solid var(--line); border-radius:var(--r); padding:22px}
.after ul{display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:10px}
.after li{display:flex; gap:10px; color:var(--muted); font-size:.93rem}
.after .ic{color:var(--leaf-ink); margin-top:.25em}

/* treatments */
.tabs{display:flex; gap:8px; overflow-x:auto; padding-bottom:4px; margin-bottom:24px; scrollbar-width:thin}
.tabs button{flex:none; min-height:44px; padding:8px 18px; border-radius:999px; border:1.5px solid var(--line); background:var(--surface); color:var(--ink); font:600 .92rem var(--font-b); cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--btn-bg); color:var(--btn-fg); border-color:var(--btn-bg)}
.tgrid{display:grid; grid-template-columns:repeat(auto-fit, minmax(300px,1fr)); gap:20px}
.tcard{background:var(--surface); border:1px solid var(--line); border-radius:18px; overflow:hidden; display:flex; flex-direction:column}
.t-ill{border-radius:0; padding:14px 14px 0}
.t-body{padding:18px 20px 22px; display:flex; flex-direction:column; gap:10px; min-width:0}
.t-body > p{color:var(--muted); font-size:.95rem}
.who{font-size:.74rem!important; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--accent-ink)!important}
.wl li{display:flex; gap:8px; font-size:.92rem; padding-block:2px}
.wl .ic{color:var(--leaf-ink); margin-top:.2em}
.facts{display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:6px 0 0}
.facts div{background:var(--bg-alt); border-radius:var(--r-s); padding:8px 10px; min-width:0}
.facts dt{font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--muted)}
.facts dd{margin:2px 0 0; font-size:.88rem; font-weight:600; color:var(--ink); line-height:1.3}
.sched{list-style:none; padding:0; margin:4px 0 0; display:flex; flex-direction:column; gap:6px}
.sched li{font-size:.88rem; padding:6px 10px; border-radius:var(--r-s); border:1.5px dashed var(--line)}
.more{display:inline-flex; gap:6px; align-items:center; font-weight:600; text-decoration:none}
.fnote{font-size:.85rem; color:var(--muted); margin-top:18px; max-width:80ch}

/* second opinion band */
.sec.dark{background:var(--band); color:var(--band-ink)}
.sec.dark h2,.sec.dark h3{color:#FFFFFF}
.sec.dark h2 em{color:#7FE3EF}
.sec.dark .eyebrow{color:#7FE3EF}
.sec.dark .lead2{color:var(--band-ink)}
.so-top{display:grid; grid-template-columns:1.2fr .8fr; gap:40px; align-items:center}
.so-ill{max-width:340px; justify-self:end; width:100%}
.so-steps{list-style:none; padding:0; margin:36px 0 20px; display:grid; grid-template-columns:repeat(4,1fr); gap:14px}
.so-steps li{background:var(--band-card); border-radius:var(--r); padding:18px; position:relative; display:flex; flex-direction:column; gap:8px}
.so-steps li.ai{background:linear-gradient(150deg,#1A97AA,#16B9A6)}
.so-steps .sn{position:absolute; inset-inline-end:14px; top:14px; width:28px; height:28px; font-size:.85rem; background:rgba(255,255,255,.14); color:#fff}
.so-steps .ic{width:28px; height:28px; color:#7FE3EF}
.so-steps li.ai .ic{color:#fff}
.so-steps p{color:var(--band-muted); font-size:.92rem}
.so-steps li.ai p{color:#EFFFFD}
.dodont2{display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:28px}
.dodont2 p{border-radius:var(--r-s); padding:14px 16px; font-size:.93rem}
.d1{background:rgba(30,230,207,.12); border:1px solid rgba(30,230,207,.35)}
.d2{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.18)}
.sec.dark .btn-p{background:#3DD5E6; color:#0B2233}

/* hospitals */
.cities{display:grid; grid-template-columns:repeat(4,1fr); gap:18px}
.city h3{font-size:1.15rem; display:flex; align-items:baseline; gap:8px; padding-bottom:8px; border-bottom:2px solid var(--accent)}
.city h3 small{font:600 .8rem var(--font-b); color:var(--muted)}
.city ul{list-style:none; padding:0; margin:0}
.city li{display:flex; justify-content:space-between; gap:10px; align-items:flex-start; padding-block:10px; border-bottom:1px solid var(--line)}
.city li div{min-width:0; display:flex; flex-direction:column}
.city li b{font-size:.92rem; font-weight:600}
.city li span{font-size:.8rem; color:var(--muted)}
.city li a{flex:none; display:inline-flex; gap:4px; align-items:center; font-size:.82rem; font-weight:600; text-decoration:none; min-height:32px}

/* travel */
.tv{display:grid; grid-template-columns:repeat(3,1fr); gap:24px 28px; margin-top:12px}
.tvi{display:flex; gap:12px}
.tvi > .ic{width:26px; height:26px; color:var(--accent-ink)}
.tvi p{color:var(--muted); font-size:.93rem; margin-top:4px}
.nhs{display:inline-flex; gap:6px; align-items:center; margin-top:28px; font-weight:600}

/* faq */
.faq{display:flex; flex-direction:column; gap:10px; margin-top:12px}
.faq details{background:var(--surface); border:1px solid var(--line); border-radius:var(--r-s); padding:4px 18px}
.faq summary{cursor:pointer; font-weight:600; padding-block:12px; list-style:none; display:flex; justify-content:space-between; gap:12px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+"; font-size:1.3rem; line-height:1; color:var(--accent-ink)}
.faq details[open] summary::after{content:"–"}
.faq details p{color:var(--muted); padding-bottom:14px}

/* form */
.formcard{background:var(--surface); border:1px solid var(--line); border-radius:20px; padding:28px; box-shadow:var(--shadow)}
.prog-bar{height:6px; background:var(--bg-alt); border-radius:99px; overflow:hidden}
.prog-bar span{display:block; height:100%; width:25%; background:linear-gradient(90deg,var(--accent),var(--aqua)); transition:width .3s}
:root[dir="rtl"] .prog-bar span{margin-inline-start:0}
.prog-l{list-style:none; padding:0; margin:10px 0 0; display:grid; grid-template-columns:repeat(4,1fr); gap:6px; font-size:.78rem; color:var(--muted)}
.prog-l li.on{color:var(--navy); font-weight:700}
.stepno{font-size:.8rem; color:var(--muted); margin-top:14px}
fieldset{border:0; padding:0; margin:0; min-width:0}
legend{font-family:var(--font-d); font-size:1.35rem; color:var(--navy); font-weight:600; padding:0; margin-bottom:16px}
.fg{display:grid; grid-template-columns:1fr 1fr; gap:14px 16px}
.f{display:flex; flex-direction:column; gap:6px; min-width:0}
.full{grid-column:1/-1}
.f label,.lbl{font-size:.88rem; font-weight:600; color:var(--ink)}
.hint{font-size:.82rem; color:var(--muted)}
input[type=text],input[type=email],input[type=tel],input[type=date],input[type=number],select,textarea{width:100%; min-height:46px; border:1.5px solid var(--line); border-radius:var(--r-s); background:var(--bg); color:var(--ink); font:16px/1.4 var(--font-b); padding:10px 12px}
textarea{resize:vertical}
input:focus,select:focus,textarea:focus{border-color:var(--accent); outline:none; box-shadow:0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent)}
[aria-invalid="true"]{border-color:#D04A3C!important}
.err{color:#C0392B; font-size:.84rem; font-weight:500}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .err{color:#F49A8C}}
:root[data-theme="dark"] .err{color:#F49A8C}
.chk,.rad{display:flex; gap:10px; align-items:flex-start; font-size:.92rem; font-weight:400!important; cursor:pointer}
.chk input,.rad input{width:20px; height:20px; margin-top:2px; flex:none; accent-color:var(--btn-bg)}
.conds{display:grid; grid-template-columns:1fr 1fr; gap:10px 16px}
.radios{display:flex; flex-direction:column; gap:10px}
.photo{background:var(--warn-bg); border:1.5px solid var(--warn-line); border-radius:var(--r); padding:18px; display:flex; flex-direction:column; gap:10px}
.photo h3{display:flex; gap:8px; align-items:center; color:var(--warn-ink); font-family:var(--font-b); font-size:1rem; font-weight:700}
.photo h3 .ic{width:24px; height:24px}
.photo > p{font-size:.92rem}
.dd{display:grid; grid-template-columns:1fr 1fr; gap:10px}
.dd > div{background:var(--surface); border-radius:var(--r-s); padding:10px 12px; font-size:.86rem}
.dd b{display:flex; gap:6px; align-items:center}
.dd-y b{color:var(--leaf-ink)} .dd-n b{color:var(--warn-ink)}
.pf{font-size:.86rem; background:var(--surface); border-radius:var(--r-s); padding:10px 12px}
.fnav{display:flex; justify-content:space-between; gap:12px; margin-top:24px; flex-wrap:wrap}
.fnav #btnNext,.fnav #btnSubmit{margin-inline-start:auto}
.result{display:flex; flex-direction:column; gap:12px; outline:none}
.result .big{width:40px; height:40px; color:var(--btn-fg); background:var(--leaf-ink); border-radius:50%; padding:8px}
.refl{font-weight:600}
.ref{font:700 1.35rem/1.2 ui-monospace, "SFMono-Regular", Menlo, monospace; color:var(--navy); letter-spacing:.04em}
.sum{white-space:pre-wrap; word-break:break-word; background:var(--bg-alt); border:1px solid var(--line); border-radius:var(--r-s); padding:14px; font:13px/1.55 ui-monospace, "SFMono-Regular", Menlo, monospace; max-height:340px; overflow:auto; margin:0; color:var(--ink); text-align:left}
.ract{display:flex; gap:10px; flex-wrap:wrap; align-items:center}
.toast{font-weight:600; color:var(--leaf-ink)}
.soon{display:flex; gap:8px; font-size:.88rem; color:var(--muted)}
.full-form{font-size:.85rem; color:var(--muted); margin-top:18px; border-top:1px solid var(--line); padding-top:14px}

/* footer */
.ftr{background:#0B2233; color:#C9DCE6; padding-block:56px 40px}
.ftr-in{display:grid; grid-template-columns:1fr 2fr; gap:32px}
.ft-logo{height:86px; width:auto}
.ft-b p{margin-top:10px; font-size:.9rem}
.ft-c{display:grid; grid-template-columns:repeat(3,1fr); gap:20px}
.ft-c h4{margin:0 0 6px; font-size:.75rem; letter-spacing:.14em; text-transform:uppercase; color:#7FE3EF}
.ft-c p{font-size:.92rem}
.muted{color:#8FA9B9}
.legal{grid-column:1/-1; font-size:.8rem; color:#8FA9B9; border-top:1px solid #1E3A50; padding-top:18px; max-width:110ch}
.copy{grid-column:1/-1; font-size:.8rem; color:#6F8A9B}
.mbar{display:none}

/* responsive */
@media (max-width: 1020px){
 .nav{order:3; flex-basis:100%; justify-content:flex-start; overflow-x:auto; flex-wrap:nowrap; padding-bottom:8px; gap:16px}
 .nav a{flex:none}
 .hdr-in{gap:10px 16px; padding-top:8px}
 .hdr-act{margin-inline-start:auto}
 .hero-in,.about,.how,.so-top{grid-template-columns:1fr}
 .so-ill{justify-self:start; max-width:300px}
 .cities{grid-template-columns:1fr 1fr}
 .so-steps{grid-template-columns:1fr 1fr}
 .values{grid-template-columns:1fr 1fr}
 .trust-in{grid-template-columns:1fr 1fr}
}
@media (max-width: 680px){
 body{padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
 .hdr-apply{display:none}
 .brand img{height:44px}
 .sec{padding-block:56px}
 .hero{padding-block:32px 20px}
 .stats{grid-template-columns:1fr 1fr; gap:18px 12px}
 .qopts,.opts2,.after ul,.tv,.dodont2,.fg,.conds,.dd,.ft-c,.ftr-in,.so-steps,.values,.cities,.trust-in{grid-template-columns:1fr}
 .facts{grid-template-columns:1fr 1fr 1fr}
 .tgrid{grid-template-columns:1fr}
 .formcard{padding:20px 16px}
 .prog-l{font-size:.68rem}
 .mbar{display:block; position:fixed; inset-inline:0; bottom:0; z-index:55; padding:10px 16px calc(10px + env(safe-area-inset-bottom,0px)); background:color-mix(in srgb, var(--bg) 94%, transparent); backdrop-filter:blur(8px); border-top:1px solid var(--line)}
 .mbar .btn{width:100%}
}
'''

JS = r'''
(function(){
 const I18N = __I18N__;
 const root = document.documentElement;
 let lang = "en";
 const nodes = () => document.querySelectorAll("[data-i]");
 function setLang(l){
  if(!I18N[l]) l = "en";
  lang = l;
  root.lang = l; root.dir = l === "ar" ? "rtl" : "ltr";
  nodes().forEach(el => { const v = I18N[l][el.dataset.i]; if(v != null) el.innerHTML = v; });
  document.getElementById("lang").value = l;
  document.title = "Easy Clinic Center";
  try{ localStorage.setItem("ecc-lang", l); }catch(e){}
  document.querySelectorAll(".err:not([hidden])").forEach(e => { if(e.dataset.k) e.textContent = I18N[l][e.dataset.k]; });
 }
 document.getElementById("lang").addEventListener("change", e => {
  const y = window.scrollY; setLang(e.target.value); window.scrollTo(0, y);
 });
 let saved = null; try{ saved = localStorage.getItem("ecc-lang"); }catch(e){}
 if(saved && saved !== "en") setLang(saved); else { root.lang = "en"; root.dir = "ltr"; }

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
 const form = document.getElementById("appForm");
 const steps = [...form.querySelectorAll(".step")];
 const back = document.getElementById("btnBack"), next = document.getElementById("btnNext"), submit = document.getElementById("btnSubmit");
 const fill = document.getElementById("progFill"), sN = document.getElementById("sN");
 const progItems = [...document.querySelectorAll(".prog-l li")];
 let cur = 0;
 const need = document.getElementById("need"), photoBox = document.getElementById("photoBox"), photoOk = document.getElementById("photo_ok");
 function syncPhoto(){ const on = ["treat","plastic","dental"].includes(need.value); photoBox.hidden = !on; photoOk.required = on; }
 need.addEventListener("change", syncPhoto); syncPhoto();
 const detBox = document.getElementById("detBox");
 const condBoxes = [...form.querySelectorAll('input[name="cond"]')];
 function syncDet(){ detBox.hidden = !condBoxes.some(c => c.checked && ["c_blood","c_allergy","c_surgery"].includes(c.value)); }
 condBoxes.forEach(c => c.addEventListener("change", syncDet));

 function show(i){
  steps.forEach((s, k) => s.hidden = k !== i); cur = i;
  back.hidden = i === 0; next.hidden = i === steps.length - 1; submit.hidden = i !== steps.length - 1;
  fill.style.width = ((i + 1) / steps.length * 100) + "%"; sN.textContent = i + 1;
  progItems.forEach((p, k) => p.classList.toggle("on", k <= i));
 }
 function setErr(el, key){
  const id = el.type === "radio" ? "quote" : el.id;
  const e = document.getElementById(id + "-e"); if(!e) return;
  if(key){ e.dataset.k = key; e.textContent = I18N[lang][key]; e.hidden = false; el.setAttribute("aria-invalid", "true"); }
  else { e.hidden = true; e.textContent = ""; el.removeAttribute("aria-invalid"); }
 }
 function check(el){
  if(el.closest("[hidden]") && el.type !== "radio") { setErr(el, null); return true; }
  if(el.type === "radio"){ const ok = !!form.querySelector('input[name="'+el.name+'"]:checked'); setErr(el, ok ? null : "err_req"); return ok; }
  if(el.type === "checkbox"){ const ok = !el.required || el.checked; setErr(el, ok ? null : "err_tick"); return ok; }
  const v = el.value.trim();
  if(el.required && !v){ setErr(el, "err_req"); return false; }
  if(v && el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)){ setErr(el, "err_email"); return false; }
  if(v && el.type === "tel" && !(/^\+/.test(v) && v.replace(/\D/g,"").length >= 8)){ setErr(el, "err_phone"); return false; }
  setErr(el, null); return true;
 }
 form.querySelectorAll("input,select,textarea").forEach(el => {
  el.addEventListener("blur", () => { if(el.dataset.t) check(el); });
  el.addEventListener("input", () => { el.dataset.t = 1; if(el.getAttribute("aria-invalid")) check(el); });
  el.addEventListener("change", () => { el.dataset.t = 1; if(el.getAttribute("aria-invalid") || el.type === "checkbox" || el.type === "radio") check(el); });
 });
 function validStep(i){
  const els = [...steps[i].querySelectorAll("input,select,textarea")].filter(e => e.required || e.value);
  let first = null, ok = true;
  const seen = new Set();
  els.forEach(e => { if(e.type === "radio"){ if(seen.has(e.name)) return; seen.add(e.name); }
   if(!check(e)){ ok = false; if(!first) first = e; } });
  if(first) first.focus();
  return ok;
 }
 next.addEventListener("click", () => { if(validStep(cur)){ show(cur + 1); steps[cur].querySelector("legend").scrollIntoView({block:"center"}); steps[cur].querySelector("input,select,textarea").focus({preventScroll:true}); } });
 back.addEventListener("click", () => show(cur - 1));

 const EN = I18N.en;
 const strip = s => s.replace(/<[^>]+>/g, "").replace(/&amp;/g, "&");
 function val(id){ const el = document.getElementById(id); if(!el) return ""; if(el.tagName === "SELECT"){ const o = el.selectedOptions[0]; if(!o || !o.value) return ""; return o.dataset.i ? strip(EN[o.dataset.i]) : o.textContent; } return el.value.trim(); }
 function makeRef(){ const d = new Date(); const p = n => String(n).padStart(2,"0"); return "ECC-" + String(d.getFullYear()).slice(2) + p(d.getMonth()+1) + p(d.getDate()) + "-" + String(Math.floor(1000 + Math.random()*9000)); }
 const res = document.getElementById("result"), sumEl = document.getElementById("sumText"), refEl = document.getElementById("refNo");
 const toast = document.getElementById("toast");
 let summary = "", ref = "";
 form.addEventListener("submit", e => {
  e.preventDefault();
  if(!validStep(cur)) return;
  ref = makeRef();
  const L = k => strip(EN[k]);
  const conds = condBoxes.filter(c => c.checked).map(c => L(c.value)).join(", ") || "-";
  const q = form.querySelector('input[name="quote"]:checked');
  const lines = [
   "EASY CLINIC CENTER - PATIENT APPLICATION", "Reference: " + ref, "Form: ECC-FR-HB-001 (web)", "Language used: " + lang.toUpperCase(), "",
   "[1] ABOUT YOU",
   L("fn") + ": " + val("fn"), L("ln") + ": " + val("ln"), L("dob") + ": " + val("dob"), L("country") + ": " + val("country"),
   L("phone") + ": " + val("phone"), L("email") + ": " + val("email"), L("contact") + ": " + val("contact"), L("plang") + ": " + val("plang"), "",
   "[2] REQUEST",
   L("need") + ": " + val("need"), L("complaint") + ":", val("complaint"), L("diag") + ": " + (val("diag") || "-"), L("pcity") + ": " + (val("pcity") || "-"),
   photoOk.required ? "Photo rule (no face) acknowledged: yes" : "", "",
   "[3] MEDICAL HISTORY",
   L("hgt") + ": " + (val("hgt") || "-"), L("wgt") + ": " + (val("wgt") || "-"), "Conditions: " + conds,
   detBox.hidden ? "" : L("details") + ": " + (val("details") || "-"), L("meds") + ": " + (val("meds") || "-"), "",
   "[4] QUOTE & CONSENT",
   L("quote") + ": " + (q ? L({A:"q_a",B:"q_b",both:"q_both"}[q.value]) : "-"), L("dates") + ": " + (val("dates") || "-"), L("comp") + ": " + (val("comp") || "0"),
   "Information confirmed true: yes", "Consent to data processing (UK GDPR / KVKK): yes", "18+ or guardian: yes", "",
   "Prepared on: " + new Date().toISOString().slice(0,10)
  ].filter(x => x !== "");
  summary = lines.join("\n");
  refEl.textContent = ref; sumEl.textContent = summary;
  form.hidden = true; document.querySelector(".prog").hidden = true; document.getElementById("stepNo").hidden = true;
  res.hidden = false; res.focus(); res.scrollIntoView({block:"start"});
 });
 document.getElementById("btnEdit").addEventListener("click", () => {
  res.hidden = true; form.hidden = false; document.querySelector(".prog").hidden = false; document.getElementById("stepNo").hidden = false; show(0);
 });
 document.getElementById("btnCopy").addEventListener("click", async () => {
  try{ await navigator.clipboard.writeText(summary); toast.textContent = I18N[lang].copied; }
  catch(e){ const r = document.createRange(); r.selectNodeContents(sumEl); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  setTimeout(() => toast.textContent = "", 2500);
 });
 const saveBtn = document.getElementById("btnSave");
 let dl = null;
 if(window.claude && claude.use){ claude.use("downloads").then(d => { dl = d; if(d) saveBtn.hidden = false; }); }
 saveBtn.addEventListener("click", async () => {
  if(!dl) return;
  try{ const r = await dl.save({filename: ref + ".txt", data: summary}); if(r && r.status === "saved"){ toast.textContent = I18N[lang].saved; setTimeout(() => toast.textContent = "", 2500); } }
  catch(e){ if(e && ["unavailable","not_granted","capability_disabled","capability_removed"].includes(e.code)) saveBtn.hidden = true; }
 });
 show(0);
})();
'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,500;0,600;1,500&family=Noto+Naskh+Arabic:wght@500;600&family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap"/>'

page = f'''<title>Easy Clinic Center</title>
<meta name="description" content="Personal health consultancy in Türkiye: treatment at partner hospitals and AI-supported second medical opinions."/>
{FONTS}
<style>{CSS}</style>
{header}
<main id="main">{hero}{about}{how}{treat}{second}{hospitals}{travel}{faq}{form}</main>
{footer}
<script>{JS.replace("__I18N__", json.dumps(I18N, ensure_ascii=False))}</script>
'''
out = pathlib.Path("/home/claude/ecc_web/site/index.html")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page)
print(len(page) // 1024, "KB")
