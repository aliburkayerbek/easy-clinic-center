import sys, pathlib, weasyprint

LANG = sys.argv[1]
TR = LANG == "tr"
def t(en, tr):
    return tr if TR else en

ISO = pathlib.Path(f"/home/claude/cat/iso_{LANG}.svg").read_text()

# department dictionary EN -> TR
D = {
 "Plastic Surgery": "Plastik Cerrahi",
 "Organ Transplantation": "Organ Nakli", "Oncology": "Onkoloji", "Cardiovascular Surgery": "Kalp ve Damar Cerrahisi",
 "Robotic Surgery": "Robotik Cerrahi", "IVF": "Tüp Bebek (IVF)", "Neurosurgery": "Beyin ve Sinir Cerrahisi",
 "Cardiology & Cardiac Surgery": "Kardiyoloji ve Kalp Cerrahisi", "Orthopaedics": "Ortopedi", "Check-Up": "Check-Up",
 "Medical Oncology": "Tıbbi Onkoloji", "Bone Marrow Transplant": "Kemik İliği Nakli", "Oncology Centre": "Onkoloji Merkezi",
 "Spine Centre": "Omurga Merkezi", "Cardiology": "Kardiyoloji", "Urology": "Üroloji", "Gynaecology & IVF": "Kadın Doğum ve IVF",
 "General Surgery": "Genel Cerrahi", "Dermatology": "Dermatoloji", "Surgical Oncology": "Cerrahi Onkoloji",
 "Gynaecology & Obstetrics": "Kadın Hastalıkları ve Doğum", "Gynaecologic Oncology": "Jinekolojik Onkoloji",
 "Aortic & Cardiac Surgery": "Aort ve Kalp Cerrahisi", "Kent Oncology Centre": "Kent Onkoloji Merkezi",
 "Nuclear Medicine": "Nükleer Tıp", "Oncology & CyberKnife": "Onkoloji ve CyberKnife", "Gynaecology": "Kadın Hastalıkları",
 "Internal Medicine": "İç Hastalıkları", "Paediatrics": "Çocuk Sağlığı", "Cardiology & Angiography": "Kardiyoloji ve Anjiyo",
 "Interventional Radiology": "Girişimsel Radyoloji", "Oncology & Chemotherapy": "Onkoloji ve Kemoterapi",
 "Oncology & Radiotherapy": "Onkoloji ve Radyoterapi", "Obesity Surgery": "Obezite Cerrahisi",
 "Thoracic Surgery": "Göğüs Cerrahisi", "Robotic Orthopaedics": "Robotik Ortopedi",
}
def dep(x):
    return D.get(x, x) if TR else x

# name, location(en,tr), plastic?, departments, url, domain
HOSP = {
 "istanbul": [
  ("Memorial Şişli Hospital", "Memorial Şişli Hastanesi", "Şişli, İstanbul", True,
   ["Organ Transplantation", "Oncology", "Cardiovascular Surgery", "Robotic Surgery", "IVF"],
   "https://www.memorial.com.tr/doktorlar/memorial-sisli-hastanesi-doktorlari", "memorial.com.tr"),
  ("Acıbadem Maslak Hospital", "Acıbadem Maslak Hastanesi", "Sarıyer, İstanbul", True,
   ["Oncology", "Organ Transplantation", "Neurosurgery", "Cardiology & Cardiac Surgery", "Orthopaedics"],
   "https://www.acibadem.com.tr/doktorlar/?hospital=Maslak%20Hastanesi", "acibadem.com.tr"),
  ("Medicana International İstanbul", "Medicana International İstanbul", "Beylikdüzü, İstanbul", True,
   ["Cardiovascular Surgery", "Medical Oncology", "Bone Marrow Transplant", "Orthopaedics", "IVF"],
   "https://www.medicanainternational.com/en/international-istanbul/doctors", "medicanainternational.com"),
 ],
 "ankara": [
  ("Memorial Ankara Hospital", "Memorial Ankara Hastanesi", "Balgat, Çankaya", True,
   ["Organ Transplantation", "Bone Marrow Transplant", "Oncology Centre", "Spine Centre", "Robotic Surgery"],
   "https://www.memorial.com.tr/doktorlar/memorial-ankara-hastanesi-doktorlari", "memorial.com.tr"),
  ("Medicana International Ankara", "Medicana International Ankara", "Söğütözü, Çankaya", True,
   ["Cardiology", "Cardiovascular Surgery", "Medical Oncology", "Neurosurgery", "Urology"],
   "https://www.medicanainternational.com/en/international-ankara/doctors", "medicanainternational.com"),
  ("Acıbadem Ankara Hospital", "Acıbadem Ankara Hastanesi", "Ankara", True,
   ["Robotic Orthopaedics", "Neurosurgery", "Cardiovascular Surgery", "Gynaecology & Obstetrics", "Urology"],
   "https://www.acibadem.com.tr/doktorlar/?hospital=Ankara%20Hastanesi", "acibadem.com.tr"),
  ("Ufuk University Dr. Rıdvan Ege Hospital", "Ufuk Üniversitesi Dr. Rıdvan Ege Hastanesi", "Balgat, Çankaya", True,
   ["Medical Oncology", "Surgical Oncology", "Cardiology", "Cardiovascular Surgery", "Orthopaedics", "Neurosurgery"],
   "https://hastane.ufuk.edu.tr/doktorlarimiz", "hastane.ufuk.edu.tr"),
  ("Güven Hospital", "Güven Hastanesi", "Ayrancı & Çayyolu, Ankara", True,
   ["Cardiology", "Cardiovascular Surgery", "General Surgery", "Orthopaedics", "Gynaecology & Obstetrics", "Neurosurgery"],
   "https://www.guven.com.tr/doktorlar", "guven.com.tr"),
  ("TOBB ETÜ Hospital", "TOBB ETÜ Hastanesi", "Söğütözü, Çankaya", True,
   ["Medical Oncology", "Gynaecologic Oncology", "Cardiology", "Cardiovascular Surgery", "Neurosurgery", "Orthopaedics"],
   "https://hastane.etu.edu.tr/doktorlar/", "hastane.etu.edu.tr"),
 ],
 "izmir": [
  ("Acıbadem İzmir Kent Hospital", "Acıbadem İzmir Kent Hastanesi", "Çiğli, İzmir", True,
   ["Aortic & Cardiac Surgery", "Neurosurgery", "Organ Transplantation", "Kent Oncology Centre", "IVF"],
   "https://www.acibadem.com.tr/doktorlar/?hospital=Kent%20Hastanesi%20(%C4%B0zmir)", "acibadem.com.tr"),
  ("Medicana International İzmir", "Medicana International İzmir", "Konak, İzmir", True,
   ["Oncology & CyberKnife", "Neurosurgery", "Orthopaedics", "Gynaecology", "Cardiology"],
   "https://www.medicanainternational.com/en/international-izmir/doctors", "medicanainternational.com"),
  ("Medicana Çeşme Medical Centre", "Medicana Çeşme Tıp Merkezi", "Çeşme, İzmir", False,
   ["Internal Medicine", "General Surgery", "Orthopaedics", "Gynaecology", "Paediatrics", "Check-Up"],
   "https://www.medicanainternational.com/en/cesme/doctors", "medicanainternational.com"),
 ],
 "antalya": [
  ("Memorial Antalya Hospital", "Memorial Antalya Hastanesi", "Kepez, Antalya", False,
   ["Cardiology & Angiography", "Interventional Radiology", "Oncology & Chemotherapy", "Orthopaedics", "Neurosurgery", "Check-Up"],
   "https://www.memorial.com.tr/doktorlar/memorial-antalya-hastanesi-doktorlari", "memorial.com.tr"),
  ("Medstar Antalya Hospital", "Medstar Antalya Hastanesi", "Antalya", True,
   ["Bone Marrow Transplant", "Oncology & Radiotherapy", "Obesity Surgery", "Spine Centre", "Cardiovascular Surgery"],
   "https://www.memorial.com.tr/doktorlar/medstar-antalya-hastanesi-doktorlari", "memorial.com.tr"),
 ],
}
CITY = {"istanbul": "İstanbul", "ankara": "Ankara", "izmir": "İzmir", "antalya": "Antalya"}

ICON = {
 "plane": '<path d="M2 16l20-6-20-6 4 6-4 6z M6 10h9" />',
 "steth": '<path d="M5 3v6a5 5 0 0 0 10 0V3 M10 14v2a5 5 0 0 0 10 0v-3"/><circle cx="20" cy="11" r="2"/>',
 "doc": '<path d="M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 16h7"/>',
 "hotel": '<path d="M3 20V8h18v12 M3 14h18"/><circle cx="7" cy="11" r="1.5"/>',
 "car": '<path d="M3 15l2-6h14l2 6v4H3z M3 15h18"/><circle cx="7.5" cy="19" r="1.6"/><circle cx="16.5" cy="19" r="1.6"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 15-5 16 0"/>',
 "lang": '<path d="M3 5h10 M8 3v2 M5 5c1 5 5 8 8 9 M11 5c-1 4-4 7-7 9 M13 21l4-10 4 10 M14.5 18h5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z M9 12l2 2 4-4"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18 M12 3c3 3 3 15 0 18 M12 3c-3 3-3 15 0 18"/>',
 "check": '<path d="M5 12l4 4 10-10"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "upload": '<path d="M12 16V4 M7 9l5-5 5 5 M4 20h16"/>',
 "report": '<path d="M6 3h12v18H6z M9 8h6 M9 12h6 M9 16h3"/>',
 "arrow": '<path d="M5 12h14 M13 6l6 6-6 6"/>',
 "ai": '<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9z M9 2v3 M15 2v3 M9 19v3 M15 19v3 M2 9h3 M2 15h3 M19 9h3 M19 15h3"/>',
 "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z M19 16l.7 1.8 1.8.7-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z"/>',
 "face": '<circle cx="12" cy="12" r="9"/><path d="M9 10h.01 M15 10h.01 M8.5 15c2 2 5 2 7 0"/>',
 "body": '<circle cx="12" cy="4.5" r="2"/><path d="M8 9c2-1 6-1 8 0 M9 9l-1 6 2 1v5 M15 9l1 6-2 1v5"/>',
 "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
 "fast": '<path d="M13 3L4 14h7l-1 7 9-11h-7z"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
}
def ic(name, size=22, color="#24507A", sw=1.8):
    return f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>'

def page(inner, cls="", num=None):
    foot = f'<div class="foot"><span>EASY CLINIC CENTER</span><span class="pn">{num:02d}</span></div>' if num else ""
    return f'<section class="page {cls}"><div class="bar"></div>{inner}{foot}</section>'

PS_CHIP = f'<span class="ps">{ic("spark", 10, "#FFFFFF", 2.2)} {t("Plastic Surgery", "Plastik Cerrahi")}</span>'

def hosp_cards(city):
    out = ""
    for en, tr, loc, ps, deps, url, dom in HOSP[city]:
        chips = (PS_CHIP if ps else "") + "".join(f"<span>{dep(d)}</span>" for d in deps)
        out += f'''<div class="hcard{' psc' if ps else ''}">
  <div class="hhead"><div><h4>{t(en, tr)}</h4><p class="loc">{loc} · <a class="url" href="{url}">{dom}</a></p></div>
  <a class="btn" href="{url}">{t("View doctors", "Hekimleri gör")} {ic("arrow", 13, "#FFFFFF", 2.2)}</a></div>
  <div class="chips">{chips}</div>
</div>'''
    return out

def city_block(city):
    n = len(HOSP[city])
    cnt = t(f"{n} partners", f"{n} partner kurum")
    return f'''<div class="city"><div class="cityhead"><span class="pin">{ic("globe", 16, "#FFFFFF", 2)}</span><h3>{CITY[city]}</h3><span class="cnt">{cnt}</span></div>
{hosp_cards(city)}</div>'''

LEGEND = f'<div class="legend">{PS_CHIP}<span>{t("= Plastic, Reconstructive & Aesthetic Surgery department available", "= Plastik, Rekonstrüktif ve Estetik Cerrahi bölümü mevcut")}</span></div>'

pages = []

# 1 COVER
pages.append(f'''<section class="page cover">
<div class="cv-top"><img src="logo.png" class="cv-logo"/></div>
<div class="cv-mid">
  <p class="eyebrow">{t("Corporate Catalogue · 2026", "Kurumsal Katalog · 2026")}</p>
  <h1>{t("Your personal health<br/>consultancy in <em>Türkiye</em>", "Türkiye'deki kişisel<br/><em>sağlık danışmanınız</em>")}</h1>
  <p class="cv-sub">{t("Treatment planning, partner hospitals and AI-supported second medical opinions, coordinated by one dedicated team from first message to recovery.", "Tedavi planlaması, partner hastaneler ve yapay zekâ destekli ikinci hekim görüşü; ilk mesajdan iyileşmenize kadar tek bir ekip tarafından koordine edilir.")}</p>
</div>
<div class="cv-tiles">
  <div>{ic("steth", 26, "#FFFFFF")}<b>{t("Treatment in Türkiye", "Türkiye'de tedavi")}</b></div>
  <div>{ic("ai", 26, "#FFFFFF")}<b>{t("AI-supported second opinion", "Yapay zekâ destekli ikinci görüş")}</b></div>
  <div>{ic("spark", 26, "#FFFFFF")}<b>{t("Plastic &amp; aesthetic surgery", "Plastik ve estetik cerrahi")}</b></div>
</div>
<div class="cv-foot"><span>İstanbul · Ankara · İzmir · Antalya</span><a href="http://www.easycliniccenter.com/">www.easycliniccenter.com</a></div>
</section>''')

# 2 ABOUT
pages.append(page(f'''
<p class="eyebrow">{t("About us", "Hakkımızda")}</p>
<h2>{t("Health in Türkiye,<br/>made <em>easy</em>", "Türkiye'de sağlık,<br/>artık <em>kolay</em>")}</h2>
<div class="lead">{t("Easy Clinic Center was founded on <b>1 October 2020</b> with a clear mission: to make a difference through pioneering practices in our sector and to become a world health brand, guided by ethical principles, a distinguished team and a satisfaction-focused service built on international quality standards.",
 "Easy Clinic Center; seçkin kadrosu ve memnuniyet odaklı, uluslararası kalite standartlarındaki hizmet anlayışıyla, etik ilkeler ışığında sektörde öncü uygulamalarla fark yaratmak ve sağlıkta dünya markası olmak misyonuyla <b>01.10.2020</b> tarihinde kurulmuştur.")}</div>
<div class="two">
  <p>{t("At our partner hospitals, treatments are delivered to international standards, supported by radiological imaging and advanced laboratory services. We treat your health as we would treat our own.",
   "Anlaşmalı olduğumuz hastanelerde uygulama ve tedaviler uluslararası standartlarda gerçekleştirilir; radyolojik görüntüleme ve gelişmiş laboratuvar hizmetleriyle desteklenir. Sizin sağlığınızı kendi sağlığımızla eş değer görüyoruz.")}</p>
  <p>{t("With specialist physicians, experienced nurses and a modern management approach, our aim is simple: quality healthcare, with a single team looking after every detail of your journey.",
   "Alanında uzman hekimlerimiz, tecrübeli hemşirelerimiz ve çağdaş yönetim anlayışımızla amacımız net: kaliteli sağlık hizmeti ve yolculuğunuzun her detayıyla ilgilenen tek bir ekip.")}</p>
</div>
<div class="stats">
  <div><b>2020</b><span>{t("Founded in<br/>İstanbul", "İstanbul'da<br/>kuruldu")}</span></div>
  <div><b>7</b><span>{t("Days a week<br/>at your service", "Haftanın 7 günü<br/>hizmetinizde")}</span></div>
  <div><b>08:30–21:00</b><span>{t("Daily service hours<br/>(Türkiye time, GMT+3)", "Günlük hizmet saatleri<br/>(Türkiye saati, GMT+3)")}</span></div>
  <div><b>14</b><span>{t("Partner hospitals &amp;<br/>centres in 4 cities", "4 şehirde partner<br/>hastane ve merkez")}</span></div>
</div>
<div class="values">
  <div>{ic("shield", 26, "#22AFC4")}<h5>{t("Ethical", "Etik")}</h5><p>{t("Transparent, hospital-based pricing and honest medical guidance.", "Şeffaf, hastane bazlı fiyatlandırma ve dürüst tıbbi yönlendirme.")}</p></div>
  <div>{ic("globe", 26, "#22AFC4")}<h5>{t("International standards", "Uluslararası standartlar")}</h5><p>{t("Leading private hospitals with modern imaging and laboratories.", "Modern görüntüleme ve laboratuvar altyapısına sahip önde gelen özel hastaneler.")}</p></div>
  <div>{ic("user", 26, "#22AFC4")}<h5>{t("Personal", "Kişisel")}</h5><p>{t("One consultant follows your case from first contact to follow-up.", "İlk temastan kontrollere kadar vakanızı tek bir danışman takip eder.")}</p></div>
</div>
''', "about", 2))

# 3 SERVICES
ck = lambda c: ic("check", 14, c, 2.4)
pages.append(page(f'''
<p class="eyebrow">{t("What we do", "Neler yapıyoruz")}</p>
<h2>{t("Personal health<br/>consultancy services", "Kişisel sağlık<br/>danışmanlığı hizmetleri")}</h2>
<p class="intro">{t("Whether you travel to Türkiye for treatment or stay at home and ask for a specialist's view, we coordinate everything around you.", "İster tedavi için Türkiye'ye gelin, ister evinizden ayrılmadan uzman görüşü alın; tüm süreci size göre koordine ediyoruz.")}</p>
<div class="svc-grid">
  <div class="svc big"><div class="svc-ic">{ic("steth", 30, "#FFFFFF")}</div><h4>{t("Treatment in Türkiye", "Türkiye'de tedavi")}</h4>
    <p>{t("We match your case with the right specialist and partner hospital, collect quotes and organise every appointment, so you arrive with a clear plan.", "Vakanızı doğru uzman ve partner hastaneyle eşleştirir, teklifleri toplar ve tüm randevuları organize ederiz; Türkiye'ye net bir planla gelirsiniz.")}</p>
    <ul><li>{ck("#22AFC4")} {t("Specialist and hospital matching", "Uzman ve hastane eşleştirme")}</li><li>{ck("#22AFC4")} {t("Hospital-based price quotes", "Hastane bazlı fiyat teklifleri")}</li><li>{ck("#22AFC4")} {t("Plastic, aesthetic &amp; all major specialties", "Plastik, estetik ve tüm ana branşlar")}</li></ul></div>
  <div class="svc big alt"><div class="svc-ic g">{ic("ai", 30, "#FFFFFF")}</div><h4>{t("AI-supported second opinion", "Yapay zekâ destekli ikinci görüş")}</h4>
    <p>{t("Share your reports and imaging. Our AI-supported system prepares your case, a specialist physician gives their opinion and we send you a written report, with no long one-to-one appointments.", "Raporlarınızı ve görüntülerinizi paylaşın. Yapay zekâ destekli sistemimiz vakanızı hazırlar, uzman hekim görüşünü verir ve size yazılı rapor iletiriz; uzun birebir görüşmelere gerek kalmaz.")}</p>
    <ul><li>{ck("#6FA52B")} {t("AI-assisted analysis of your records", "Kayıtlarınızın yapay zekâ destekli analizi")}</li><li>{ck("#6FA52B")} {t("Specialist physician review", "Uzman hekim değerlendirmesi")}</li><li>{ck("#6FA52B")} {t("Written second-opinion report", "Yazılı ikinci görüş raporu")}</li></ul></div>
  <div class="svc"><div class="svc-ic s">{ic("plane", 22, "#24507A")}</div><h4>{t("Flights", "Uçak bileti")}</h4><p>{t("Optional booking around your treatment dates.", "Tedavi tarihlerinize göre opsiyonel rezervasyon.")}</p></div>
  <div class="svc"><div class="svc-ic s">{ic("hotel", 22, "#24507A")}</div><h4>{t("Accommodation", "Konaklama")}</h4><p>{t("Hotels close to your hospital for you and a companion.", "Size ve refakatçinize hastaneye yakın oteller.")}</p></div>
  <div class="svc"><div class="svc-ic s">{ic("car", 22, "#24507A")}</div><h4>{t("Transfers", "Transfer")}</h4><p>{t("Airport, hotel and hospital transfers, with private vehicles.", "Özel araçlarla havalimanı, otel ve hastane transferleri.")}</p></div>
  <div class="svc"><div class="svc-ic s">{ic("lang", 22, "#24507A")}</div><h4>{t("Patient coordination", "Hasta koordinasyonu")}</h4><p>{t("A consultant on hand 7 days a week throughout your stay.", "Kaldığınız süre boyunca haftanın 7 günü yanınızda bir danışman.")}</p></div>
</div>
''', "services", 3))

# 4 PLASTIC SURGERY SPOTLIGHT
PS_HOSP = [(t(en, tr), CITY[c]) for c in HOSP for en, tr, loc, ps, *_ in HOSP[c] if ps]
ps_list = "".join(f'<span><b>{n}</b> · {c}</span>' for n, c in PS_HOSP)
cats = [
 ("face", t("Face", "Yüz"), [t("Rhinoplasty", "Rinoplasti (burun estetiği)"), t("Facelift &amp; neck lift", "Yüz ve boyun germe"), t("Eyelid surgery", "Göz kapağı estetiği"), t("Ear surgery (otoplasty)", "Kepçe kulak (otoplasti)")]),
 ("heart", t("Breast", "Meme"), [t("Breast augmentation", "Meme büyütme"), t("Breast reduction &amp; lift", "Meme küçültme ve dikleştirme"), t("Gynaecomastia", "Jinekomasti"), t("Breast reconstruction", "Meme rekonstrüksiyonu")]),
 ("body", t("Body", "Vücut"), [t("Liposuction", "Liposuction"), t("Tummy tuck", "Karın germe"), t("Brazilian butt lift (fat transfer)", "Brezilya popo kaldırma (yağ transferi)"), t("Mummy makeover", "Anne estetiği (mommy makeover)")]),
 ("shield", t("Reconstructive", "Rekonstrüktif"), [t("Post-cancer reconstruction", "Kanser sonrası rekonstrüksiyon"), t("Scar revision", "Skar (iz) düzeltme"), t("Hand surgery", "El cerrahisi"), t("Post-weight-loss body contouring", "Kilo kaybı sonrası vücut şekillendirme")]),
]
cat_html = "".join(f'<div class="pcat"><div class="pcat-h">{ic(i, 20, "#FFFFFF", 2)}<b>{h}</b></div><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>" for i, h, items in cats)
pages.append(page(f'''
<p class="eyebrow">{t("Specialty spotlight", "Öne çıkan branş")}</p>
<h2>{t("Plastic, reconstructive<br/>&amp; <em>aesthetic</em> surgery", "Plastik, rekonstrüktif<br/>ve <em>estetik</em> cerrahi")}</h2>
<p class="intro">{t("Plastic surgery is one of the most requested treatments in Türkiye. We work with experienced plastic surgeons at our partner hospitals for both aesthetic and reconstructive procedures, always in a hospital setting.", "Plastik cerrahi, Türkiye'de en çok tercih edilen tedavilerden biridir. Estetik ve rekonstrüktif işlemler için partner hastanelerimizdeki deneyimli plastik cerrahlarla çalışıyoruz; tüm işlemler hastane ortamında yapılır.")}</p>
<div class="pgrid">{cat_html}</div>
<div class="pwhy">
  <div>{ic("ai", 24, "#22AFC4")}<h5>{t("Pre-assessment before you travel", "Seyahat öncesi ön değerlendirme")}</h5><p>{t("Your photos and medical history are reviewed so the surgeon can plan before you arrive.", "Fotoğraflarınız ve tıbbi geçmişiniz incelenir; cerrah planlamayı siz gelmeden yapar.")}</p></div>
  <div>{ic("shield", 24, "#22AFC4")}<h5>{t("Hospital safety", "Hastane güvencesi")}</h5><p>{t("Operations take place in fully equipped private hospitals with intensive care units.", "Ameliyatlar, yoğun bakım ünitesine sahip tam donanımlı özel hastanelerde yapılır.")}</p></div>
  <div>{ic("heart", 24, "#22AFC4")}<h5>{t("Recovery &amp; follow-up", "İyileşme ve takip")}</h5><p>{t("Post-op checks before you fly home and remote follow-up after your return.", "Dönüş öncesi kontroller ve döndükten sonra uzaktan takip.")}</p></div>
</div>
<div class="pavail"><p class="pav-t">{PS_CHIP} {t("Available at", "Bölümün bulunduğu hastaneler")}</p><div class="pav-l">{ps_list}</div></div>
''', "plastic", 4))

# 5 HOW IT WORKS
pages.append(page(f'''
<p class="eyebrow">{t("How it works", "Çalışma mantığımız")}</p>
<h2>{t("From the UK to treatment,<br/>in three clear steps", "İngiltere'den tedaviye,<br/>üç net adımda")}</h2>
<p class="intro">{t("You apply from the UK, we detail your medical case, and you receive hospital-based offers from Türkiye in two forms, so you choose exactly how much we arrange for you.", "İngiltere'den başvurursunuz, sağlık probleminizi detaylandırırız ve Türkiye'den hastane bazında iki farklı şekilde teklif alırsınız; ne kadarını bizim organize etmemizi istediğinize siz karar verirsiniz.")}</p>
<div class="iso">{ISO}</div>
''', "how", 5))

# 6 QUOTE
def li(icn, col, b, s, cls=""):
    return f'<li class="{cls}">{ic(icn, 20, col)}<div><b>{b}</b><span>{s}</span></div></li>'
tr_line = t("Hospital fees, specialist and procedure as quoted by the hospital", "Hastanenin teklif ettiği hastane, hekim ve işlem ücretleri")
opt = t("optional", "opsiyonel")
pages.append(page(f'''
<p class="eyebrow">{t("Your quote, your choice", "Teklifiniz, tercihiniz")}</p>
<h2>{t("A two-stage offer,<br/>tailored to you", "Size özel<br/>iki aşamalı teklif")}</h2>
<p class="intro">{t("For every case we prepare a quote per partner hospital. Each quote is offered in two ways: everything arranged, or the treatment alone with the rest left optional.", "Her vaka için partner hastane bazında teklif hazırlarız. Her teklif iki şekilde sunulur: her şey dahil ya da sadece tedavi, gerisi opsiyonel.")}</p>
<div class="opts">
  <div class="opt a"><span class="tag">{t("OPTION A", "SEÇENEK A")}</span><h3>{t("All-Inclusive Package", "Her Şey Dahil Paket")}</h3><p class="optsub">{t("One price, everything arranged", "Tek fiyat, her şey organize")}</p>
    <ul>
      {li("steth", "#14B8A4", t("Treatment", "Tedavi"), tr_line)}
      {li("plane", "#14B8A4", t("Flights", "Uçak bileti"), t("Return flights planned around your treatment dates", "Tedavi tarihlerinize göre gidiş-dönüş uçuş"))}
      {li("hotel", "#14B8A4", t("Accommodation", "Konaklama"), t("Hotel near the hospital for your recovery period", "İyileşme süreciniz için hastaneye yakın otel"))}
      {li("car", "#14B8A4", t("Transfers", "Transfer"), t("Airport, hotel and hospital transfers included", "Havalimanı, otel ve hastane transferleri dahil"))}
    </ul>
    <p class="best">{t("Best for: patients who want a fully managed, stress-free trip.", "Kimin için: her şeyin organize edildiği, stressiz bir süreç isteyenler.")}</p></div>
  <div class="opt b"><span class="tag">{t("OPTION B", "SEÇENEK B")}</span><h3>{t("Treatment Only", "Sadece Tedavi")}</h3><p class="optsub">{t("Treatment price, everything else optional", "Tedavi fiyatı, gerisi opsiyonel")}</p>
    <ul>
      {li("steth", "#6FA52B", t("Treatment", "Tedavi"), tr_line)}
      {li("plus", "#9AAAB8", t("Flights", "Uçak bileti") + " · " + opt, t("Add if you need it, or book your own", "İsterseniz ekleyin ya da kendiniz ayarlayın"), "optl")}
      {li("plus", "#9AAAB8", t("Accommodation", "Konaklama") + " · " + opt, t("Add if you need it, or book your own", "İsterseniz ekleyin ya da kendiniz ayarlayın"), "optl")}
      {li("plus", "#9AAAB8", t("Transfers", "Transfer") + " · " + opt, t("Add if you need it, or arrange your own", "İsterseniz ekleyin ya da kendiniz ayarlayın"), "optl")}
    </ul>
    <p class="best">{t("Best for: patients who prefer to organise their own travel.", "Kimin için: seyahatini kendi planlamak isteyenler.")}</p></div>
</div>
<div class="note">{ic("doc", 20, "#24507A")}<p>{t("Quotes are prepared individually for each hospital after your medical case has been reviewed, so you can compare hospitals side by side before deciding.", "Teklifler, sağlık durumunuz incelendikten sonra her hastane için ayrı hazırlanır; karar vermeden önce hastaneleri yan yana karşılaştırabilirsiniz.")}</p></div>
''', "quote", 6))

# 7-9 HOSPITALS
intro_h = t("We work with leading private and university hospitals in four cities. Tap <b>View doctors</b> on any hospital to open its official physician directory.",
            "Dört şehirde önde gelen özel ve üniversite hastaneleriyle çalışıyoruz. Hastanenin resmi hekim listesini açmak için <b>Hekimleri gör</b> butonuna dokunun.")
pages.append(page(f'''
<p class="eyebrow">{t("Our solution partners", "Çözüm ortaklarımız")}</p>
<h2>{t("Partner hospitals", "Partner hastaneler")}</h2>
<p class="intro">{intro_h}</p>{LEGEND}
<div class="cities">{city_block("ankara")}</div>
''', "hosp", 7))
pages.append(page(f'''
<p class="eyebrow">{t("Our solution partners", "Çözüm ortaklarımız")}</p>
<h2>{t("Partner hospitals", "Partner hastaneler")}</h2>{LEGEND}
<div class="cities">{city_block("istanbul")}{city_block("izmir")}</div>
''', "hosp", 8))

# summary table
rows = ""
for c in ["ankara", "istanbul", "izmir", "antalya"]:
    for en, tr, loc, ps, deps, url, dom in HOSP[c]:
        rows += f'<tr><td>{CITY[c]}</td><td><a href="{url}">{t(en, tr)}</a></td><td class="c">{ic("check", 14, "#6FA52B", 2.6) if ps else "–"}</td></tr>'
pages.append(page(f'''
<p class="eyebrow">{t("Our solution partners", "Çözüm ortaklarımız")}</p>
<h2>{t("Partner hospitals", "Partner hastaneler")}</h2>{LEGEND}
<div class="cities">{city_block("antalya")}</div>
<h3 class="sumh">{t("Network at a glance", "Ağımıza genel bakış")}</h3>
<table class="sum"><thead><tr><th>{t("City", "Şehir")}</th><th>{t("Hospital", "Hastane")}</th><th class="c">{t("Plastic Surgery", "Plastik Cerrahi")}</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">{t("Departments shown are highlights; each hospital offers a wider range. Physician lists are maintained by the hospitals on their official websites.", "Gösterilen bölümler öne çıkanlardır; her hastanede çok daha fazla bölüm bulunur. Hekim listeleri hastanelerin resmi web sitelerinde güncel tutulur.")}</p>
''', "hosp", 9))

# 10 AI SECOND OPINION
pages.append(page(f'''
<p class="eyebrow">{t("AI-supported second medical opinion", "Yapay zekâ destekli ikinci hekim görüşü")}</p>
<h2>{t("A specialist's opinion,<br/><em>powered by AI</em>", "Uzman hekim görüşü,<br/><em>yapay zekâ</em> desteğiyle")}</h2>
<p class="intro">{t("Our new AI-supported system lets you get a specialist physician's opinion without travelling and without lengthy one-to-one appointments. We put your case to the physician and report the answer back to you.", "Yeni yapay zekâ destekli sistemimizle, seyahat etmeden ve uzun birebir görüşmelere gerek kalmadan uzman hekim görüşü alırsınız. Vakanızı hekime biz sunar, görüşünü raporlayarak size iletiriz.")}</p>
<div class="so">
  <div class="sostep"><div class="sonum">1</div>{ic("upload", 28, "#22AFC4")}<h5>{t("Upload your records", "Kayıtlarınızı yükleyin")}</h5><p>{t("Reports, imaging (CD/DICOM), lab results and your current treatment plan.", "Raporlar, görüntüler (CD/DICOM), tahlil sonuçları ve mevcut tedavi planınız.")}</p></div>
  <div class="sostep ai"><div class="sonum">2</div>{ic("ai", 28, "#FFFFFF")}<h5>{t("AI-assisted case analysis", "Yapay zekâ ile vaka analizi")}</h5><p>{t("Our system organises your files into a structured medical summary and highlights the key questions.", "Sistemimiz dosyalarınızı yapılandırılmış bir tıbbi özete dönüştürür ve kritik soruları belirler.")}</p></div>
  <div class="sostep"><div class="sonum">3</div>{ic("user", 28, "#22AFC4")}<h5>{t("Specialist review", "Uzman hekim değerlendirmesi")}</h5><p>{t("A specialist at a partner hospital reviews the summary and your original files and gives their opinion.", "Partner hastanedeki uzman hekim özeti ve orijinal dosyalarınızı inceleyerek görüşünü verir.")}</p></div>
  <div class="sostep"><div class="sonum">4</div>{ic("report", 28, "#22AFC4")}<h5>{t("Written report", "Yazılı rapor")}</h5><p>{t("You receive a clear report with the physician's evaluation and treatment options.", "Hekimin değerlendirmesini ve tedavi seçeneklerini içeren anlaşılır bir rapor alırsınız.")}</p></div>
</div>
<div class="whyai">
  <div>{ic("fast", 24, "#22AFC4")}<h5>{t("Faster", "Daha hızlı")}</h5><p>{t("No waiting for appointment slots or scheduling video calls across time zones.", "Randevu beklemeden, saat farkıyla görüntülü görüşme ayarlamadan.")}</p></div>
  <div>{ic("target", 24, "#22AFC4")}<h5>{t("More focused", "Daha odaklı")}</h5><p>{t("The physician's time goes into your case, not into collecting your history.", "Hekimin zamanı geçmişinizi toplamaya değil, doğrudan vakanıza ayrılır.")}</p></div>
  <div>{ic("user", 24, "#22AFC4")}<h5>{t("One-to-one only if needed", "Birebir görüşme yalnızca gerekirse")}</h5><p>{t("A live consultation is arranged only when the physician considers it necessary.", "Canlı görüşme yalnızca hekim gerekli gördüğünde planlanır.")}</p></div>
</div>
<div class="sobox">
  <div><h4>{t("Good to know", "Bilmenizde fayda var")}</h4><p>{t("Artificial intelligence organises and prepares your file; every medical opinion in your report is given by a qualified specialist physician.", "Yapay zekâ dosyanızı düzenler ve hazırlar; raporunuzdaki tüm tıbbi görüşler uzman hekim tarafından verilir.")}</p></div>
  <div><h4>{t("What happens next", "Sonraki adım")}</h4><p>{t("If you decide to be treated in Türkiye, your second-opinion file becomes the starting point of your hospital-based quote, so nothing has to be repeated.", "Türkiye'de tedavi olmaya karar verirseniz, ikinci görüş dosyanız hastane bazlı teklifinizin başlangıç noktası olur; hiçbir şeyi tekrarlamanız gerekmez.")}</p></div>
</div>
''', "second", 10))

# 11 BACK
pages.append(f'''<section class="page back">
<img src="logo_white.png" class="bk-logo"/>
<h2>{t("Let's plan your care together", "Tedavinizi birlikte planlayalım")}</h2>
<p class="bk-sub">{t("Send us your request and a personal consultant will get back to you.", "Talebinizi iletin, kişisel danışmanınız size dönüş yapsın.")}</p>
<div class="bk-info">
  <div>{ic("clock", 24, "#FFFFFF")}<b>{t("7 days a week", "Haftanın 7 günü")}</b><span>08:30 – 21:00 (GMT+3)</span></div>
  <div>{ic("globe", 24, "#FFFFFF")}<b>{t("Website", "Web sitesi")}</b><a href="http://www.easycliniccenter.com/">www.easycliniccenter.com</a></div>
  <div>{ic("hotel", 24, "#FFFFFF")}<b>{t("Head office", "Merkez ofis")}</b><span>İstanbul / TÜRKİYE</span></div>
</div>
<p class="bk-legal">{t("The information in this catalogue is for general guidance and does not replace a medical consultation. Treatment plans and prices are confirmed individually after medical review.", "Bu katalogdaki bilgiler genel bilgilendirme amaçlıdır ve hekim muayenesinin yerine geçmez. Tedavi planları ve fiyatlar, tıbbi değerlendirme sonrasında kişiye özel olarak netleştirilir.")}</p>
</section>''')

CSS = pathlib.Path("/home/claude/cat/style.css").read_text()
title = t("Easy Clinic Center – Corporate Catalogue", "Easy Clinic Center – Kurumsal Katalog")
html = f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
out = t("Easy_Clinic_Center_Catalogue_EN.pdf", "Easy_Clinic_Center_Katalog_TR.pdf")
weasyprint.HTML(string=html, base_url="/home/claude/cat/").write_pdf(f"/home/claude/cat/{out}")
print(out)
