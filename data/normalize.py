"""Normalise raw doctor lists into one JSON: hospitals -> departments -> doctors."""
import json, re, pathlib

RAW = pathlib.Path("/home/claude/raw")

# file, hospital key, has_title_column, extra campus column
FILES = {
    "memorial_sisli": ("mem_sisli.tsv", "joined"),
    "acibadem_maslak": ("aci_maslak.tsv", "split"),
    "medicana_istanbul": ("mc_beylikduzu.tsv", "split"),
    "memorial_ankara": ("mem_ankara.tsv", "joined"),
    "medicana_ankara": ("mc_ankara.tsv", "split"),
    "acibadem_ankara": ("aci_ankara.tsv", "split"),
    "ufuk": ("ufuk.tsv", "split"),
    "guven": ("guven.tsv", "split"),
    "tobb": ("tobb.tsv", "split"),
    "acibadem_kent": ("aci_kent.tsv", "split"),
    "medicana_izmir": ("mc_izmir.tsv", "split"),
    "medicana_cesme": ("mc_cesme.tsv", "split"),
    "memorial_antalya": ("mem_antalya.tsv", "joined"),
    "medstar_antalya": ("medstar_antalya.tsv", "joined"),
}

TITLE_PAT = re.compile(r"^(Prof\.\s*Dr\.|Doç\.\s*Dr\.|Dr\.\s*Öğr\.\s*Üyesi|Dr\.\s*Öğrt\.\s*Üyesi|Dr\.Öğr\.Ü\.|Uzm\.\s*Dr\.|Op\.\s*Dr\.|Dr\.\s*Uzm\.\s*Dt\.|Dr\.\s*Dt\.|Uzm\.\s*Dt\.|Dt\.|Dr\.)\s*")

def norm_title(t):
    t = re.sub(r"\s+", "", t)
    m = {
        "Prof.Dr.": "Prof. Dr.", "Doç.Dr.": "Doç. Dr.", "Dr.Öğr.Üyesi": "Dr. Öğr. Üyesi", "Dr.Öğrt.Üyesi": "Dr. Öğr. Üyesi",
        "Dr.Öğr.Ü.": "Dr. Öğr. Üyesi", "Uzm.Dr.": "Uzm. Dr.", "Op.Dr.": "Op. Dr.", "Dr.Uzm.Dt.": "Dr. Dt.",
        "Dr.Dt.": "Dr. Dt.", "Uzm.Dt.": "Uzm. Dt.", "Dt.": "Dt.", "Dr.": "Dr.",
    }
    return m.get(t, t)

EN_TITLE = {"Prof. Dr.": "Prof. Dr.", "Doç. Dr.": "Assoc. Prof. Dr.", "Dr. Öğr. Üyesi": "Asst. Prof. Dr.",
            "Uzm. Dr.": "Spec. Dr.", "Op. Dr.": "Op. Dr.", "Dr.": "Dr.", "Dr. Dt.": "Dr. Dent.", "Uzm. Dt.": "Spec. Dent.", "Dt.": "Dent."}

SKIP_TITLES = re.compile(r"^(Dyt|Uzm\.?\s*Dyt|Dr\.?\s*Dyt|Diyetisyen|Psk|Uzm\.?\s*Psk|Psikolog|KlinikPsk|Fzt|Odyolog|Embriyolog|D\.K\.T)", re.I)

LOW = {"I": "ı", "İ": "i"}
def tr_lower(s):
    return "".join(LOW.get(c, c.lower()) for c in s)
def tr_cap(w):
    if not w:
        return w
    if "." in w and len(w) <= 3:  # initials like "A." or "M."
        return w[0].upper() + w[1:]
    f = w[0]
    f = "İ" if f == "i" else ("I" if f == "ı" else f.upper())
    return f + tr_lower(w[1:])
def norm_name(n):
    n = re.sub(r"\(M\)", "", n).strip()
    n = re.sub(r"\s+", " ", n)
    n = re.sub(r"\.(?=\S)", ". ", n)
    parts = []
    for w in n.split(" "):
        if "-" in w:
            parts.append("-".join(tr_cap(tr_lower(x)) for x in w.split("-")))
        else:
            parts.append(tr_cap(tr_lower(w)))
    return " ".join(parts)

# canonical department: (key, tr, en) rules checked in order on lowercase first dept
DEPTS = [
    ("plastic", "Plastik, Rekonstrüktif ve Estetik Cerrahi", "Plastic, Reconstructive & Aesthetic Surgery", ["plastik"]),
    ("ivf", "Tüp Bebek (IVF) ve Üreme Sağlığı", "IVF & Reproductive Health", ["tüp bebek", "üreme"]),
    ("transplant", "Organ Nakli", "Organ Transplantation", ["organ nakli", "böbrek nakli", "karaciğer nakli"]),
    ("paed_onc", "Çocuk Hematolojisi ve Onkolojisi", "Paediatric Haematology & Oncology", ["çocuk (pediatrik) hem", "çocuk (pediatrik) onk", "çocuk hematoloji", "çocuk onkoloji"]),
    ("paed_cardio", "Çocuk Kardiyolojisi", "Paediatric Cardiology", ["çocuk kardiyo"]),
    ("paed_surg", "Çocuk Cerrahisi", "Paediatric Surgery", ["çocuk cerrah", "çocuk kalp", "çocuk ürolo", "çocuk ortopedi"]),
    ("paed_sub", "Çocuk Yan Dalları", "Paediatric Subspecialties", ["çocuk nefro", "çocuk nöro", "çocuk endokr", "çocuk gastro", "çocuk alerj", "çocuk immün", "çocuk romat", "çocuk enfeks", "çocuk genetik"]),
    ("child_psy", "Çocuk ve Ergen Psikiyatrisi", "Child & Adolescent Psychiatry", ["çocuk ve ergen", "çocuk psikiyatri"]),
    ("neonat", "Yenidoğan Yoğun Bakım", "Neonatal Intensive Care", ["yenidoğan"]),
    ("paed", "Çocuk Sağlığı ve Hastalıkları", "Paediatrics", ["çocuk sağlığı", "pediatri"]),
    ("dental", "Ağız ve Diş Sağlığı", "Dentistry & Oral Surgery", ["diş", "pedodonti", "periodont", "ortodonti", "protetik", "endodonti"]),
    ("rad_onc", "Radyasyon Onkolojisi", "Radiation Oncology", ["radyasyon onk"]),
    ("med_onc", "Tıbbi Onkoloji", "Medical Oncology", ["medikal onk", "tıbbi onk", "onkoloji"]),
    ("haem", "Hematoloji ve Kemik İliği Nakli", "Haematology & Bone Marrow Transplant", ["hematoloji", "kemik iliği"]),
    ("cv_surg", "Kalp ve Damar Cerrahisi", "Cardiovascular Surgery", ["kalp ve damar", "kalp damar", "kvc", "damar cerrahisi"]),
    ("cardio", "Kardiyoloji", "Cardiology", ["kardiyoloji", "kalp sağlığı"]),
    ("neurosurg", "Beyin ve Sinir Cerrahisi", "Neurosurgery", ["beyin ve sinir", "beyın ve sinir", "nöroşirürji"]),
    ("spine", "Omurga Cerrahisi", "Spine Surgery", ["omurga merkezi"]),
    ("ortho", "Ortopedi ve Travmatoloji", "Orthopaedics & Traumatology", ["ortopedi", "el cerrahisi"]),
    ("gen_surg", "Genel Cerrahi", "General Surgery", ["genel cerrahi", "gastroenterolojik cerrahi", "cerrahi onkoloji", "meme merkezi", "endokrin cerrahi"]),
    ("thor_surg", "Göğüs Cerrahisi", "Thoracic Surgery", ["göğüs cerrahi"]),
    ("gyn", "Kadın Hastalıkları ve Doğum", "Obstetrics & Gynaecology", ["kadın hastalık", "jinekolo", "perinatoloji", "endometriozis"]),
    ("uro", "Üroloji ve Androloji", "Urology & Andrology", ["üroloji", "androloji", "prostat"]),
    ("gastro", "Gastroenteroloji", "Gastroenterology", ["gastroenteroloji"]),
    ("endo", "Endokrinoloji ve Metabolizma", "Endocrinology & Metabolism", ["endokrinoloji"]),
    ("nephro", "Nefroloji", "Nephrology", ["nefroloji"]),
    ("internal", "İç Hastalıkları", "Internal Medicine", ["iç hastalık", "dahiliye", "geriatri"]),
    ("pulm", "Göğüs Hastalıkları", "Pulmonology", ["göğüs hastalık"]),
    ("allergy", "İmmünoloji ve Alerji", "Immunology & Allergy", ["alerji", "immünoloji", "doku tipleme"]),
    ("infect", "Enfeksiyon Hastalıkları", "Infectious Diseases", ["enfeksiyon"]),
    ("rheum", "Romatoloji", "Rheumatology", ["romatoloji"]),
    ("neuro", "Nöroloji", "Neurology", ["nöroloji"]),
    ("psych", "Psikiyatri", "Psychiatry", ["psikiyatri", "ruh sağlığı"]),
    ("ent", "Kulak Burun Boğaz", "Ear, Nose & Throat (ENT)", ["kulak burun"]),
    ("eye", "Göz Hastalıkları", "Ophthalmology", ["göz hastalık"]),
    ("derm", "Dermatoloji", "Dermatology", ["dermatoloji", "deri ve zührevi", "deri hastalık"]),
    ("ftr", "Fizik Tedavi ve Rehabilitasyon", "Physical Medicine & Rehabilitation", ["fizik tedavi", "fiziksel tıp", "inme ve beyin", "lenfödem"]),
    ("algology", "Algoloji (Ağrı)", "Pain Medicine (Algology)", ["algoloji"]),
    ("nuclear", "Nükleer Tıp", "Nuclear Medicine", ["nükleer"]),
    ("int_rad", "Girişimsel Radyoloji", "Interventional Radiology", ["girişimsel"]),
    ("radiology", "Radyoloji", "Radiology", ["radyoloji"]),
    ("patho", "Patoloji ve Laboratuvar", "Pathology & Laboratory", ["patoloji", "biyokimya", "laboratuvar", "mikrobiyoloji", "genetik"]),
    ("anaes", "Anestezi ve Yoğun Bakım", "Anaesthesia & Intensive Care", ["anestez", "yoğun bakım"]),
    ("checkup", "Check-Up ve Aile Hekimliği", "Check-Up & Family Medicine", ["check", "aile hekim"]),
    ("emerg", "Acil Tıp", "Emergency Medicine", ["acil"]),
    ("tcm", "Geleneksel ve Tamamlayıcı Tıp", "Traditional & Complementary Medicine", ["geleneksel"]),
]
ORDER = [d[0] for d in DEPTS]
DEPT_INFO = {k: (tr, en) for k, tr, en, _ in DEPTS}

def classify(dept):
    first = tr_lower(dept)
    # prefer plastic anywhere
    if "plastik" in first:
        return "plastic"
    for k, tr, en, keys in DEPTS:
        if any(x in first.split(",")[0] for x in keys):
            return k
    for k, tr, en, keys in DEPTS:
        if any(x in first for x in keys):
            return k
    return None

out = {}
unknown = set()
for key, (fn, mode) in FILES.items():
    rows = []
    for line in (RAW / fn).read_text().splitlines():
        if not line.strip():
            continue
        p = line.split("\t")
        if mode == "joined":
            m = TITLE_PAT.match(p[0].strip())
            if not m:
                if SKIP_TITLES.match(p[0].strip()):
                    continue
                title, name = "", p[0].strip()
            else:
                title, name = m.group(1), p[0].strip()[m.end():]
            dept = p[1] if len(p) > 1 else ""
            campus = ""
        else:
            title, name, dept = p[0].strip(), p[1].strip(), (p[2] if len(p) > 2 else "")
            campus = p[3].strip() if len(p) > 3 else ""
            if SKIP_TITLES.match(title):
                continue
        if SKIP_TITLES.match(title or ""):
            continue
        dept = dept.strip()
        if re.search(r"Kat (ve Triaj )?Hekim|PCR|Online Doktor|Hastane Direktör|İşyeri Hekimi|Klinik Psikoloji|Psikoloji \(Klinik\)|Beslenme|Odyoloji|Dil ve Konuşma", dept):
            continue
        c = classify(dept)
        if c is None:
            unknown.add(dept)
            continue
        t = norm_title(title) if title else "Dr."
        rows.append({"t": t, "n": norm_name(name), "d": c, "raw": dept, "campus": campus})
    # dedupe by name
    seen = {}
    for r in rows:
        seen.setdefault(r["n"], r)
    out[key] = list(seen.values())

print("UNKNOWN:", unknown)
total = 0
for k, v in out.items():
    print(f"{k:20s} {len(v):4d}  plastic={sum(1 for r in v if r['d']=='plastic')}")
    total += len(v)
print("TOTAL", total)
json.dump({"hospitals": out, "order": ORDER, "depts": DEPT_INFO, "en_title": EN_TITLE},
          open("/home/claude/cat/doctors.json", "w"), ensure_ascii=False, indent=0)
