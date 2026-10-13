"""Easy Clinic Center – detailed catalogue (patient & partner guide + physician directory). Usage: python3 build3.py en|tr"""
import sys, json, pathlib, html, weasyprint

LANG = sys.argv[1]
TR = LANG == "tr"
def t(en, tr):
    return tr if TR else en

DATA = json.load(open("/home/claude/cat/doctors.json"))
DOCS = DATA["hospitals"]
DEPTS = DATA["depts"]          # key -> [tr, en]
ORDER = DATA["order"]
EN_TITLE = DATA["en_title"]
ISO = pathlib.Path(f"/home/claude/cat/iso_{LANG}.svg").read_text()

def dname(k):
    tr, en = DEPTS[k]
    return tr if TR else en
def title(tt):
    return tt if TR else EN_TITLE.get(tt, tt)
e = html.escape

# ---------------------------------------------------------------- hospitals
H = [
 # key, en, tr, city, district, type_en, type_tr, url, domain
 ("memorial_sisli", "Memorial Şişli Hospital", "Memorial Şişli Hastanesi", "İstanbul", "Şişli", "Private hospital", "Özel hastane",
  "https://www.memorial.com.tr/doktorlar/memorial-sisli-hastanesi-doktorlari"),
 ("acibadem_maslak", "Acıbadem Maslak Hospital", "Acıbadem Maslak Hastanesi", "İstanbul", "Sarıyer", "Private hospital", "Özel hastane",
  "https://www.acibadem.com.tr/doktorlar/?hospital=Maslak%20Hastanesi"),
 ("medicana_istanbul", "Medicana International İstanbul", "Medicana International İstanbul", "İstanbul", "Beylikdüzü", "Private hospital", "Özel hastane",
  "https://www.medicanainternational.com/en/international-istanbul/doctors"),
 ("memorial_ankara", "Memorial Ankara Hospital", "Memorial Ankara Hastanesi", "Ankara", "Balgat, Çankaya", "Private hospital", "Özel hastane",
  "https://www.memorial.com.tr/doktorlar/memorial-ankara-hastanesi-doktorlari"),
 ("medicana_ankara", "Medicana International Ankara", "Medicana International Ankara", "Ankara", "Söğütözü, Çankaya", "Private hospital", "Özel hastane",
  "https://www.medicanainternational.com/en/international-ankara/doctors"),
 ("acibadem_ankara", "Acıbadem Ankara Hospital", "Acıbadem Ankara Hastanesi", "Ankara", "Çankaya", "Private hospital", "Özel hastane",
  "https://www.acibadem.com.tr/doktorlar/?hospital=Ankara%20Hastanesi"),
 ("ufuk", "Ufuk University Dr. Rıdvan Ege Hospital", "Ufuk Üniversitesi Dr. Rıdvan Ege Hastanesi", "Ankara", "Balgat, Çankaya", "University hospital", "Üniversite hastanesi",
  "https://hastane.ufuk.edu.tr/doktorlarimiz"),
 ("guven", "Güven Hospital", "Güven Hastanesi", "Ankara", "Ayrancı & Çayyolu", "Private hospital (2 campuses)", "Özel hastane (2 yerleşke)",
  "https://www.guven.com.tr/doktorlar"),
 ("tobb", "TOBB ETÜ Hospital", "TOBB ETÜ Hastanesi", "Ankara", "Söğütözü, Çankaya", "University hospital", "Üniversite hastanesi",
  "https://hastane.etu.edu.tr/doktorlar/"),
 ("acibadem_kent", "Acıbadem İzmir Kent Hospital", "Acıbadem İzmir Kent Hastanesi", "İzmir", "Çiğli", "Private hospital", "Özel hastane",
  "https://www.acibadem.com.tr/doktorlar/?hospital=Kent%20Hastanesi%20(%C4%B0zmir)"),
 ("medicana_izmir", "Medicana International İzmir", "Medicana International İzmir", "İzmir", "Konak", "Private hospital", "Özel hastane",
  "https://www.medicanainternational.com/en/international-izmir/doctors"),
 ("medicana_cesme", "Medicana Çeşme Medical Centre", "Medicana Çeşme Tıp Merkezi", "İzmir", "Çeşme", "Medical centre", "Tıp merkezi",
  "https://www.medicanainternational.com/en/cesme/doctors"),
 ("memorial_antalya", "Memorial Antalya Hospital", "Memorial Antalya Hastanesi", "Antalya", "Kepez", "Private hospital", "Özel hastane",
  "https://www.memorial.com.tr/doktorlar/memorial-antalya-hastanesi-doktorlari"),
 ("medstar_antalya", "Medstar Antalya Hospital", "Medstar Antalya Hastanesi", "Antalya", "Muratpaşa", "Private hospital", "Özel hastane",
  "https://www.memorial.com.tr/doktorlar/medstar-antalya-hastanesi-doktorlari"),
]
HM = {h[0]: h for h in H}
def hname(k):
    h = HM[k]
    return h[2] if TR else h[1]
def domain(u):
    return u.split("//")[1].split("/")[0].replace("www.", "")

TOTAL = sum(len(v) for v in DOCS.values())
NUM = f"{TOTAL:,}".replace(",", "." if TR else ",")
PLASTIC = [(k, d) for k in HM for d in DOCS[k] if d["d"] == "plastic"]
DATE = t("12 October 2026", "12 Ekim 2026")

ICON = {
 "steth": '<path d="M5 3v6a5 5 0 0 0 10 0V3 M10 14v2a5 5 0 0 0 10 0v-3"/><circle cx="20" cy="11" r="2"/>',
 "ai": '<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9z M9 2v3 M15 2v3 M9 19v3 M15 19v3 M2 9h3 M2 15h3 M19 9h3 M19 15h3"/>',
 "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
 "plane": '<path d="M2 16l20-6-20-6 4 6-4 6z M6 10h9" />',
 "hotel": '<path d="M3 20V8h18v12 M3 14h18"/><circle cx="7" cy="11" r="1.5"/>',
 "car": '<path d="M3 15l2-6h14l2 6v4H3z M3 15h18"/><circle cx="7.5" cy="19" r="1.6"/><circle cx="16.5" cy="19" r="1.6"/>',
 "lang": '<path d="M3 5h10 M8 3v2 M5 5c1 5 5 8 8 9 M11 5c-1 4-4 7-7 9 M13 21l4-10 4 10 M14.5 18h5"/>',
 "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 15-5 16 0"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z M9 12l2 2 4-4"/>',
 "check": '<path d="M5 12l4 4 10-10"/>',
 "doc": '<path d="M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 16h7"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18 M12 3c3 3 3 15 0 18 M12 3c-3 3-3 15 0 18"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "arrow": '<path d="M5 12h14 M13 6l6 6-6 6"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 "home": '<path d="M3 11l9-7 9 7v9H3z M9 20v-6h6v6"/>',
}
def ic(name, size=20, color="#24507A", sw=1.8):
    return f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>'
def ul(items, color="#22AFC4"):
    return '<ul class="ck">' + "".join(f"<li>{ic('check', 13, color, 2.4)}<span>{x}</span></li>" for x in items) + "</ul>"

S = []  # sections

def section(sid, eyebrow, h, body, cls=""):
    S.append(f'<section class="sec {cls}" id="{sid}"><p class="eyebrow">{eyebrow}</p><h2>{h}</h2>{body}</section>')

# ---------------------------------------------------------------- COVER
cover = f'''<section class="cover">
<div class="cv-top"><img src="logo.png" class="cv-logo"/></div>
<div class="cv-mid">
  <p class="eyebrow">{t("Detailed Catalogue · Patient &amp; Partner Guide · 2026", "Detay Katalog · Hasta ve Partner Rehberi · 2026")}</p>
  <h1>{t("Everything we do,<br/><em>explained in full</em>", "Yaptığımız her şey,<br/><em>tüm ayrıntılarıyla</em>")}</h1>
  <p class="cv-sub">{t(f"Our services, the patient journey from the UK to Türkiye, the two-stage quote, AI-supported second opinions, plastic surgery and a directory of {NUM} physicians at our 14 partner hospitals and centres.",
                        f"Hizmetlerimiz, İngiltere'den Türkiye'ye hasta yolculuğu, iki aşamalı teklif, yapay zekâ destekli ikinci görüş, plastik cerrahi ve 14 partner hastane ve merkezimizdeki {NUM} hekimin listesi.")}</p>
</div>
<div class="cv-stats">
  <div><b>14</b><span>{t("partner hospitals &amp; centres", "partner hastane ve merkez")}</span></div>
  <div><b>{NUM}</b><span>{t("physicians listed", "hekim listelendi")}</span></div>
  <div><b>4</b><span>{t("cities", "şehir")}</span></div>
  <div><b>7/7</b><span>08:30–21:00</span></div>
</div>
<div class="cv-foot"><span>İstanbul · Ankara · İzmir · Antalya</span><a href="http://www.easycliniccenter.com/">www.easycliniccenter.com</a></div>
</section>'''

# ---------------------------------------------------------------- CONTENTS (filled later)
TOC = []
def toc(sid, label):
    TOC.append((sid, label))

# ---------------------------------------------------------------- 1 ABOUT
toc("about", t("About Easy Clinic Center", "Easy Clinic Center hakkında"))
section("about", t("01 · About us", "01 · Hakkımızda"), t("A personal health consultancy,<br/>built around you", "Size göre kurgulanmış<br/>kişisel sağlık danışmanlığı"), f'''
<div class="lead">{t("Easy Clinic Center was founded on <b>1 October 2020</b> with the mission of making a difference through pioneering practices in our sector and becoming a world health brand, guided by ethical principles, a distinguished team and a satisfaction-focused service that meets international quality standards.",
"Easy Clinic Center; seçkin kadrosu ve memnuniyet odaklı, uluslararası kalite standartlarındaki hizmet anlayışıyla, etik ilkeler ışığında sektörde öncü uygulamalarla fark yaratmak ve sağlıkta dünya markası olmak misyonuyla <b>01.10.2020</b> tarihinde kurulmuştur.")}</div>
<div class="cols2">
<p>{t("We are not a hospital. We are your independent coordinator between you and Türkiye's leading hospitals. Our role is to understand your medical situation, find the right specialist and hospital, obtain transparent hospital-based prices, and then organise every part of the journey so that you can focus on your treatment and recovery.",
"Biz bir hastane değiliz; sizinle Türkiye'nin önde gelen hastaneleri arasındaki bağımsız koordinatörünüzüz. Görevimiz sağlık durumunuzu anlamak, doğru uzmanı ve hastaneyi bulmak, şeffaf ve hastane bazlı fiyatları almak ve ardından yolculuğun her aşamasını organize etmektir; böylece siz yalnızca tedavinize ve iyileşmenize odaklanırsınız.")}</p>
<p>{t("At our partner hospitals, treatments are delivered to international standards and supported by radiological imaging and advanced laboratory services. We treat your health as we would treat our own: with specialist physicians, experienced nurses and a modern management approach, our aim is quality healthcare with one team looking after every detail.",
"Anlaşmalı hastanelerimizde uygulama ve tedaviler uluslararası standartlarda gerçekleştirilir; radyolojik görüntüleme ve gelişmiş laboratuvar hizmetleriyle desteklenir. Sağlığınızı kendi sağlığımızla eş değer görürüz: alanında uzman hekimlerimiz, tecrübeli hemşirelerimiz ve çağdaş yönetim anlayışımızla amacımız, her ayrıntıyla tek bir ekibin ilgilendiği kaliteli sağlık hizmetidir.")}</p>
</div>
<div class="facts">
 <div>{ic("clock", 24, "#22AFC4")}<b>{t("7 days a week", "Haftanın 7 günü")}</b><span>08:30 – 21:00 {t("(Türkiye time, GMT+3)", "(Türkiye saati, GMT+3)")}</span></div>
 <div>{ic("globe", 24, "#22AFC4")}<b>{t("4 cities", "4 şehir")}</b><span>İstanbul · Ankara · İzmir · Antalya</span></div>
 <div>{ic("user", 24, "#22AFC4")}<b>{t("One consultant", "Tek danışman")}</b><span>{t("from first contact to follow-up", "ilk temastan kontrollere kadar")}</span></div>
 <div>{ic("shield", 24, "#22AFC4")}<b>{t("Ethics first", "Önce etik")}</b><span>{t("transparent, hospital-based pricing", "şeffaf, hastane bazlı fiyat")}</span></div>
</div>
<h3>{t("Our values", "Değerlerimiz")}</h3>
<div class="vals">
 <div><h4>{t("Transparency", "Şeffaflık")}</h4><p>{t("Every price we present comes from the hospital itself. You see what is included and what is optional before you decide.", "Sunduğumuz her fiyat doğrudan hastaneden gelir. Karar vermeden önce neyin dahil, neyin opsiyonel olduğunu görürsünüz.")}</p></div>
 <div><h4>{t("Medical integrity", "Tıbbi dürüstlük")}</h4><p>{t("Treatment decisions belong to you and your physician. We never push a procedure; if a specialist advises against treatment, we tell you.", "Tedavi kararı size ve hekiminize aittir. Hiçbir işlemi dayatmayız; uzman tedaviyi önermiyorsa bunu size açıkça söyleriz.")}</p></div>
 <div><h4>{t("Personal care", "Kişisel ilgi")}</h4><p>{t("You have one named consultant who knows your file and is reachable seven days a week throughout your journey.", "Dosyanızı bilen ve yolculuğunuz boyunca haftanın 7 günü ulaşabileceğiniz tek bir danışmanınız olur.")}</p></div>
 <div><h4>{t("Privacy", "Gizlilik")}</h4><p>{t("Your medical information is shared only with the hospitals and physicians involved in your case, and only with your consent.", "Tıbbi bilgileriniz yalnızca vakanızla ilgili hastane ve hekimlerle ve yalnızca onayınızla paylaşılır.")}</p></div>
</div>
''')

# ---------------------------------------------------------------- 2 WHY TÜRKIYE
toc("why", t("Why Türkiye, why us", "Neden Türkiye, neden biz"))
section("why", t("02 · Why Türkiye", "02 · Neden Türkiye"), t("Why patients from the UK<br/>choose Türkiye", "İngiltere'deki hastalar<br/>neden Türkiye'yi seçiyor"), f'''
<p class="intro">{t("Türkiye has become one of the world's most visited destinations for healthcare. For patients in the UK, a few hours' flight connects them with large private and university hospitals, experienced specialists and short waiting times.", "Türkiye, dünyada sağlık için en çok tercih edilen ülkelerden biri hâline geldi. İngiltere'deki hastalar, birkaç saatlik uçuşla büyük özel ve üniversite hastanelerine, deneyimli uzmanlara ve kısa bekleme sürelerine ulaşabiliyor.")}</p>
<div class="grid3">
 <div class="card">{ic("clock", 26, "#22AFC4")}<h4>{t("Shorter waiting times", "Daha kısa bekleme")}</h4><p>{t("Consultations, imaging and surgery can usually be scheduled within days or weeks rather than months.", "Muayene, görüntüleme ve ameliyatlar çoğunlukla aylar yerine günler ya da haftalar içinde planlanabilir.")}</p></div>
 <div class="card">{ic("steth", 26, "#22AFC4")}<h4>{t("Experienced specialists", "Deneyimli uzmanlar")}</h4><p>{t("Many of the physicians in this catalogue are professors and associate professors with academic careers.", "Bu katalogdaki hekimlerin önemli bir kısmı akademik kariyere sahip profesör ve doçentlerdir.")}</p></div>
 <div class="card">{ic("doc", 26, "#22AFC4")}<h4>{t("Clear, comparable prices", "Net, karşılaştırılabilir fiyat")}</h4><p>{t("Hospital-based quotes let you compare options side by side before you commit to anything.", "Hastane bazlı teklifler, hiçbir taahhütte bulunmadan seçenekleri yan yana karşılaştırmanızı sağlar.")}</p></div>
 <div class="card">{ic("plane", 26, "#22AFC4")}<h4>{t("Direct flights", "Direkt uçuşlar")}</h4><p>{t("İstanbul, Ankara, İzmir and Antalya are all served by flights from the UK, many of them direct.", "İstanbul, Ankara, İzmir ve Antalya'ya İngiltere'den, çoğu direkt olmak üzere uçuşlar bulunur.")}</p></div>
 <div class="card">{ic("hotel", 26, "#22AFC4")}<h4>{t("Recovery in comfort", "Konforlu iyileşme")}</h4><p>{t("Hotels close to the hospital and coastal cities such as Antalya and İzmir make recovery more pleasant.", "Hastaneye yakın oteller ve Antalya, İzmir gibi sahil şehirleri iyileşme sürecini daha keyifli kılar.")}</p></div>
 <div class="card">{ic("user", 26, "#22AFC4")}<h4>{t("Someone on your side", "Yanınızda biri")}</h4><p>{t("With Easy Clinic Center, a consultant who speaks your language coordinates every step.", "Easy Clinic Center ile dilinizi konuşan bir danışman her adımı koordine eder.")}</p></div>
</div>
<div class="callout">{ic("shield", 22, "#24507A")}<p>{t("<b>Our promise:</b> we only work with established private and university hospitals. Every procedure in this catalogue is performed in a hospital setting by a specialist physician, never in unlicensed clinics.", "<b>Taahhüdümüz:</b> yalnızca köklü özel ve üniversite hastaneleriyle çalışırız. Bu katalogdaki her işlem, uzman hekim tarafından hastane ortamında yapılır; asla ruhsatsız kliniklerde değil.")}</p></div>
''')

# ---------------------------------------------------------------- 3 SERVICES
toc("services", t("Our services in detail", "Hizmetlerimiz ayrıntılı"))
svc = [
 ("user", t("Personal health consultancy", "Kişisel sağlık danışmanlığı"),
  t("Your starting point. A consultant listens to your situation, reviews your existing reports and explains your options in plain language: which specialty you need, which hospitals have experience in your condition, and what the next steps would be.",
    "Başlangıç noktanız. Danışmanınız durumunuzu dinler, mevcut raporlarınızı inceler ve seçeneklerinizi sade bir dille anlatır: hangi branşa ihtiyacınız olduğunu, hangi hastanelerin bu konuda deneyimli olduğunu ve sonraki adımların neler olacağını."),
  [t("Free initial assessment of your request", "Talebinizin ücretsiz ön değerlendirmesi"), t("Guidance on specialty and hospital choice", "Branş ve hastane seçiminde yönlendirme"), t("One named consultant for your whole journey", "Tüm süreç boyunca tek bir danışman")]),
 ("steth", t("Treatment in Türkiye", "Türkiye'de tedavi"),
  t("Once you decide to be treated in Türkiye, we book your consultation, tests and procedure, share your file with the hospital in advance and stay with you through admission, treatment and discharge.",
    "Türkiye'de tedavi olmaya karar verdiğinizde muayene, tetkik ve işlem randevularınızı ayarlar, dosyanızı önceden hastaneyle paylaşır; yatış, tedavi ve taburculuk boyunca yanınızda oluruz."),
  [t("Appointment planning before you travel", "Seyahat öncesi randevu planlaması"), t("Hospital admission and discharge support", "Hastaneye yatış ve taburculuk desteği"), t("Medical reports collected for your UK GP", "İngiltere'deki aile hekiminiz için raporların toplanması")]),
 ("ai", t("AI-supported second medical opinion", "Yapay zekâ destekli ikinci hekim görüşü"),
  t("Get a specialist's view without travelling. Our AI-supported system prepares a structured summary of your records, a specialist at a partner hospital gives an opinion, and we send you a written report. Lengthy one-to-one appointments are not needed.",
    "Seyahat etmeden uzman görüşü alın. Yapay zekâ destekli sistemimiz kayıtlarınızın yapılandırılmış özetini hazırlar, partner hastanedeki uzman görüşünü verir ve size yazılı rapor iletiriz. Uzun birebir görüşmelere gerek kalmaz."),
  [t("Structured analysis of reports and imaging", "Rapor ve görüntülerin yapılandırılmış analizi"), t("Opinion given by a specialist physician", "Görüşü uzman hekim verir"), t("Clear written report with options", "Seçenekleri içeren anlaşılır yazılı rapor")]),
 ("spark", t("Plastic, reconstructive & aesthetic surgery", "Plastik, rekonstrüktif ve estetik cerrahi"),
  t("From rhinoplasty to body contouring and post-cancer reconstruction, we work with plastic surgeons at our partner hospitals. Pre-assessment from your photos happens before you book a flight.",
    "Burun estetiğinden vücut şekillendirmeye ve kanser sonrası rekonstrüksiyona kadar partner hastanelerimizdeki plastik cerrahlarla çalışırız. Fotoğraflarınızla ön değerlendirme, uçak bileti almadan önce yapılır."),
  [t("Surgeon matching and pre-assessment", "Cerrah eşleştirme ve ön değerlendirme"), t("All procedures in fully equipped hospitals", "Tüm işlemler tam donanımlı hastanelerde"), t("Post-operative checks and remote follow-up", "Ameliyat sonrası kontroller ve uzaktan takip")]),
 ("plane", t("Flights", "Uçak bileti"), t("Optional. We plan flights around your treatment dates and your surgeon's advice on when it is safe to fly home.", "Opsiyoneldir. Uçuşları tedavi tarihlerinize ve cerrahınızın ne zaman güvenle uçabileceğinize dair önerisine göre planlarız."), []),
 ("hotel", t("Accommodation", "Konaklama"), t("Optional. Hotels close to your hospital, chosen for comfort and easy access, for you and a companion.", "Opsiyoneldir. Size ve refakatçinize, hastaneye yakın, konforlu ve ulaşımı kolay oteller."), []),
 ("car", t("Transfers", "Transferler"), t("Optional. Private airport, hotel and hospital transfers with a driver waiting for you on arrival.", "Opsiyoneldir. Varışta sizi bekleyen şoförle özel havalimanı, otel ve hastane transferleri."), []),
 ("lang", t("Coordination & language support", "Koordinasyon ve dil desteği"), t("Your consultant helps you communicate with hospital staff and is reachable seven days a week, 08:30–21:00.", "Danışmanınız hastane personeliyle iletişiminize yardımcı olur ve haftanın 7 günü 08:30–21:00 arasında ulaşılabilirdir."), []),
 ("heart", t("Aftercare & follow-up", "Tedavi sonrası takip"), t("After you return home we stay in touch, arrange remote check-ins with your physician when needed and help share reports with your UK doctor.", "Eve döndükten sonra iletişimde kalır, gerektiğinde hekiminizle uzaktan kontrol ayarlar ve raporlarınızın İngiltere'deki doktorunuzla paylaşılmasına yardımcı oluruz."), []),
]
big = "".join(f'<div class="svc"><div class="svc-h">{ic(i, 22, "#FFFFFF")}<h4>{h}</h4></div><p>{p}</p>{ul(b) if b else ""}</div>' for i, h, p, b in svc[:4])
small = "".join(f'<div class="svc s"><div class="svc-h s">{ic(i, 20, "#24507A")}<h4>{h}</h4></div><p>{p}</p></div>' for i, h, p, b in svc[4:])
section("services", t("03 · Services", "03 · Hizmetler"), t("Our services in detail", "Hizmetlerimiz ayrıntılı"), f'''
<p class="intro">{t("Our core services cover medical guidance and treatment. Travel services are always optional and can be added to any quote.", "Temel hizmetlerimiz tıbbi yönlendirme ve tedaviyi kapsar. Seyahat hizmetleri her zaman opsiyoneldir ve her teklife eklenebilir.")}</p>
<div class="svcgrid">{big}</div><h3>{t("Optional travel &amp; support services", "Opsiyonel seyahat ve destek hizmetleri")}</h3><div class="svcgrid sm">{small}</div>''')

# ---------------------------------------------------------------- 4 JOURNEY
toc("journey", t("How it works: the patient journey", "Çalışma mantığımız: hasta yolculuğu"))
steps = [
 (t("Apply from the UK", "İngiltere'den başvuru"), t("Contact us online, by phone or WhatsApp. Tell us briefly about your health problem and what you are looking for.", "Bize online, telefonla veya WhatsApp üzerinden ulaşın. Sağlık sorununuzu ve beklentinizi kısaca anlatın.")),
 (t("Detailing your medical case", "Sağlık probleminin detaylandırılması"), t("We collect your reports, imaging and history and, where needed, use our AI-supported system to build a structured medical summary for the hospitals.", "Raporlarınızı, görüntülerinizi ve geçmişinizi toplar; gerektiğinde yapay zekâ destekli sistemimizle hastaneler için yapılandırılmış bir tıbbi özet hazırlarız.")),
 (t("Specialist review", "Uzman değerlendirmesi"), t("Specialists at suitable partner hospitals review your file and propose a treatment plan.", "Uygun partner hastanelerdeki uzmanlar dosyanızı inceler ve tedavi planı önerir.")),
 (t("Hospital-based quotes from Türkiye", "Türkiye'den hastane bazlı teklif"), t("You receive a quote from each hospital, in two forms: all-inclusive (treatment, flights, accommodation, transfers) or treatment only, with the rest optional.", "Her hastaneden iki şekilde teklif alırsınız: her şey dahil (tedavi, uçak, konaklama, transfer) ya da sadece tedavi, gerisi opsiyonel.")),
 (t("Your decision", "Kararınız"), t("Compare hospitals, ask questions and take your time. Nothing is booked until you confirm.", "Hastaneleri karşılaştırın, sorularınızı sorun ve acele etmeyin. Siz onaylamadan hiçbir rezervasyon yapılmaz.")),
 (t("Planning & travel", "Planlama ve seyahat"), t("We confirm appointments and, if you chose them, arrange flights, hotel and transfers.", "Randevuları kesinleştirir; seçtiyseniz uçak, otel ve transferleri ayarlarız.")),
 (t("Treatment in Türkiye", "Türkiye'de tedavi"), t("Your consultant accompanies you from arrival to discharge and keeps your family informed if you wish.", "Danışmanınız varıştan taburculuğa kadar yanınızdadır; isterseniz ailenizi de bilgilendirir.")),
 (t("Home & follow-up", "Dönüş ve takip"), t("We send your medical reports, arrange remote check-ins and stay in touch during your recovery.", "Tıbbi raporlarınızı iletir, uzaktan kontroller ayarlar ve iyileşme sürecinizde iletişimde kalırız.")),
]
stephtml = "".join(f'<div class="step"><div class="sn">{i+1}</div><div><h4>{a}</h4><p>{b}</p></div></div>' for i, (a, b) in enumerate(steps))
section("journey", t("04 · How it works", "04 · Çalışma mantığımız"), t("From the UK to treatment,<br/>step by step", "İngiltere'den tedaviye,<br/>adım adım"), f'''
<p class="intro">{t("The diagram shows the core of our model: you apply from the UK, we detail your health problem, and you receive hospital-based quotes from Türkiye in two forms.", "Şema modelimizin özünü gösterir: İngiltere'den başvurursunuz, sağlık probleminizi detaylandırırız ve Türkiye'den hastane bazında iki farklı şekilde teklif alırsınız.")}</p>
<div class="iso">{ISO}</div>
<h3 class="pb">{t("The eight steps in full", "Sekiz adımın tamamı")}</h3><div class="steps">{stephtml}</div>''')

# ---------------------------------------------------------------- 5 QUOTE
toc("quote", t("The two-stage quote", "İki aşamalı teklif"))
rows = [
 (t("Hospital treatment (as quoted by the hospital)", "Hastane tedavisi (hastanenin teklif ettiği)"), "✓", "✓"),
 (t("Specialist and surgeon fees included in the hospital quote", "Hastane teklifine dahil uzman ve cerrah ücretleri"), "✓", "✓"),
 (t("Easy Clinic Center coordination and consultant", "Easy Clinic Center koordinasyonu ve danışman"), "✓", "✓"),
 (t("Return flights", "Gidiş-dönüş uçuş"), "✓", t("optional", "opsiyonel")),
 (t("Hotel accommodation near the hospital", "Hastaneye yakın otel konaklaması"), "✓", t("optional", "opsiyonel")),
 (t("Airport, hotel and hospital transfers", "Havalimanı, otel ve hastane transferleri"), "✓", t("optional", "opsiyonel")),
]
trs = "".join(f"<tr><td>{a}</td><td class='c a'>{b}</td><td class='c b'>{c}</td></tr>" for a, b, c in rows)
section("quote", t("05 · Your quote", "05 · Teklifiniz"), t("The two-stage quote,<br/>explained", "İki aşamalı teklif,<br/>açıklamalı"), f'''
<p class="intro">{t("For every case we prepare a separate quote for each suitable partner hospital. Each quote is offered in two forms, so you decide how much we organise.", "Her vaka için uygun her partner hastaneye ayrı teklif hazırlarız. Her teklif iki şekilde sunulur; ne kadarını bizim organize edeceğimize siz karar verirsiniz.")}</p>
<table class="qt"><thead><tr><th></th><th class="c a">{t("Option A<br/>All-inclusive", "Seçenek A<br/>Her şey dahil")}</th><th class="c b">{t("Option B<br/>Treatment only", "Seçenek B<br/>Sadece tedavi")}</th></tr></thead><tbody>{trs}</tbody></table>
<div class="cols2">
<div><h3>{t("What affects the price", "Fiyatı neler etkiler")}</h3>{ul([t("The hospital and the specialist you choose", "Seçtiğiniz hastane ve uzman"), t("The exact procedure and technique", "İşlemin ve tekniğin kendisi"), t("Length of hospital stay and room type", "Hastanede kalış süresi ve oda tipi"), t("Additional tests the physician requires", "Hekimin istediği ek tetkikler"), t("Travel dates, hotel category and companions (Option A)", "Seyahat tarihleri, otel kategorisi ve refakatçi (Seçenek A)")])}</div>
<div><h3>{t("Good to know", "Bilmenizde fayda var")}</h3>{ul([t("Quotes are based on the information in your file; the final plan is confirmed after the physician examines you.", "Teklifler dosyanızdaki bilgilere dayanır; nihai plan hekim sizi muayene ettikten sonra kesinleşir."), t("Validity, payment terms and what happens if the plan changes are written in each offer.", "Geçerlilik süresi, ödeme koşulları ve plan değişirse ne olacağı her teklifte yazılıdır."), t("You can switch from Option B to Option A at any time before travel.", "Seyahatten önce istediğiniz zaman Seçenek B'den A'ya geçebilirsiniz.")])}</div>
</div>''')

# ---------------------------------------------------------------- 6 AI SECOND OPINION
toc("second", t("AI-supported second medical opinion", "Yapay zekâ destekli ikinci hekim görüşü"))
section("second", t("06 · Second opinion", "06 · İkinci görüş"), t("A specialist's opinion,<br/><em>powered by AI</em>", "Uzman hekim görüşü,<br/><em>yapay zekâ</em> desteğiyle"), f'''
<p class="intro">{t("A second opinion helps you feel confident about a diagnosis or a treatment plan. With our new AI-supported system you get a specialist physician's opinion without travelling and without lengthy one-to-one appointments: we put your case to the physician and report the answer back to you.", "İkinci görüş, bir tanı ya da tedavi planından emin olmanıza yardımcı olur. Yeni yapay zekâ destekli sistemimizle seyahat etmeden ve uzun birebir görüşmelere gerek kalmadan uzman hekim görüşü alırsınız: vakanızı hekime biz sunar, cevabını raporlayarak size iletiriz.")}</p>
<div class="flow4">
 <div><span>1</span><h4>{t("Upload", "Yükleme")}</h4><p>{t("You send your reports, imaging (CD/DICOM), lab results and current treatment plan.", "Raporlarınızı, görüntülerinizi (CD/DICOM), tahlil sonuçlarınızı ve mevcut tedavi planınızı gönderirsiniz.")}</p></div>
 <div class="ai"><span>2</span><h4>{t("AI analysis", "Yapay zekâ analizi")}</h4><p>{t("Our system organises the files, builds a structured summary, flags missing information and lists the key clinical questions.", "Sistemimiz dosyaları düzenler, yapılandırılmış özet çıkarır, eksik bilgileri işaretler ve kritik klinik soruları listeler.")}</p></div>
 <div><span>3</span><h4>{t("Specialist review", "Uzman değerlendirmesi")}</h4><p>{t("A specialist at a partner hospital reviews the summary together with your original files and gives an opinion.", "Partner hastanedeki uzman, özeti orijinal dosyalarınızla birlikte inceler ve görüşünü verir.")}</p></div>
 <div><span>4</span><h4>{t("Written report", "Yazılı rapor")}</h4><p>{t("You receive the physician's evaluation and treatment options in a clear, written report.", "Hekimin değerlendirmesini ve tedavi seçeneklerini anlaşılır, yazılı bir raporla alırsınız.")}</p></div>
</div>
<div class="cols2">
<div><h3>{t("What to send us", "Bize neler göndermelisiniz")}</h3>{ul([t("Specialist letters and discharge summaries", "Uzman yazıları ve epikrizler"), t("Imaging on CD/USB in DICOM format, plus radiology reports", "DICOM formatında CD/USB görüntüler ve radyoloji raporları"), t("Pathology/biopsy reports, if any", "Varsa patoloji/biyopsi raporları"), t("Recent blood tests", "Güncel kan tahlilleri"), t("List of current medicines and allergies", "Kullandığınız ilaçlar ve alerjileriniz"), t("Your own questions for the physician", "Hekime sormak istedikleriniz")])}</div>
<div><h3>{t("What the AI does and does not do", "Yapay zekâ ne yapar, ne yapmaz")}</h3>
<div class="dodont"><p class="do"><b>{t("Does:", "Yapar:")}</b> {t("translate and organise documents, summarise your history, highlight what the specialist needs to see.", "belgeleri düzenler ve çevirir, geçmişinizi özetler, uzmanın görmesi gerekenleri öne çıkarır.")}</p>
<p class="dont"><b>{t("Does not:", "Yapmaz:")}</b> {t("diagnose or recommend treatment. Every medical opinion in your report is given by a qualified specialist physician.", "tanı koymaz, tedavi önermez. Raporunuzdaki her tıbbi görüş uzman hekim tarafından verilir.")}</p></div>
<h3>{t("One-to-one consultation", "Birebir görüşme")}</h3><p>{t("A live video consultation is arranged only if the physician considers it necessary, for example when examination or discussion would change the opinion.", "Canlı görüntülü görüşme yalnızca hekim gerekli görürse planlanır; örneğin muayene ya da görüşme sonucun değişmesine yol açacaksa.")}</p></div>
</div>
<div class="callout">{ic("lock", 22, "#24507A")}<p>{t("<b>Privacy:</b> your documents are used only to prepare your second opinion and are shared only with the physician reviewing your case.", "<b>Gizlilik:</b> belgeleriniz yalnızca ikinci görüşünüzü hazırlamak için kullanılır ve yalnızca vakanızı değerlendiren hekimle paylaşılır.")}</p></div>''')

# ---------------------------------------------------------------- 7 PLASTIC
toc("plastic", t("Plastic, reconstructive & aesthetic surgery", "Plastik, rekonstrüktif ve estetik cerrahi"))
procs = [
 (t("Face", "Yüz"), [(t("Rhinoplasty", "Rinoplasti"), t("Reshaping the nose for appearance and/or breathing.", "Görünüm ve/veya nefes için burnun yeniden şekillendirilmesi.")),
                     (t("Face & neck lift", "Yüz ve boyun germe"), t("Tightening sagging skin and tissues of the face and neck.", "Yüz ve boyundaki sarkmış deri ve dokuların toparlanması.")),
                     (t("Eyelid surgery", "Göz kapağı estetiği"), t("Removing excess skin or fat from upper or lower eyelids.", "Üst veya alt göz kapağındaki fazla deri ya da yağın alınması.")),
                     (t("Otoplasty", "Otoplasti"), t("Correcting prominent ears.", "Kepçe kulak düzeltmesi."))]),
 (t("Breast", "Meme"), [(t("Augmentation", "Büyütme"), t("Increasing breast volume with implants or fat transfer.", "Protez veya yağ transferiyle meme hacminin artırılması.")),
                       (t("Reduction & lift", "Küçültme ve dikleştirme"), t("Reducing size and/or restoring a lifted shape.", "Boyutun küçültülmesi ve/veya dik formun yeniden kazandırılması.")),
                       (t("Gynaecomastia", "Jinekomasti"), t("Treatment of enlarged breast tissue in men.", "Erkeklerde meme dokusu büyümesinin tedavisi.")),
                       (t("Reconstruction", "Rekonstrüksiyon"), t("Rebuilding the breast after cancer surgery.", "Kanser ameliyatı sonrası memenin yeniden oluşturulması."))]),
 (t("Body", "Vücut"), [(t("Liposuction", "Liposuction"), t("Removing stubborn fat deposits to reshape the body.", "Vücudu şekillendirmek için inatçı yağların alınması.")),
                      (t("Tummy tuck", "Karın germe"), t("Removing excess abdominal skin and tightening the muscles.", "Karındaki fazla derinin alınması ve kasların sıkılaştırılması.")),
                      (t("Brazilian butt lift (fat transfer)", "Brezilya popo kaldırma (yağ transferi)"), t("Using your own fat to add fullness and shape to the buttocks.", "Kendi yağınızla kalçaya dolgunluk ve form kazandırılması.")),
                      (t("Mummy makeover", "Anne estetiği"), t("Combined breast and abdominal procedures after pregnancy.", "Gebelik sonrası meme ve karın işlemlerinin birlikte yapılması."))]),
 (t("Reconstructive", "Rekonstrüktif"), [(t("Post-cancer reconstruction", "Kanser sonrası rekonstrüksiyon"), t("Restoring form and function after tumour surgery.", "Tümör ameliyatı sonrası form ve fonksiyonun geri kazandırılması.")),
                      (t("Scar revision", "Skar düzeltme"), t("Improving the appearance of scars.", "Yara izlerinin görünümünün iyileştirilmesi.")),
                      (t("Hand surgery", "El cerrahisi"), t("Treatment of injuries and conditions of the hand.", "Elin yaralanma ve hastalıklarının tedavisi.")),
                      (t("Body contouring after weight loss", "Kilo kaybı sonrası şekillendirme"), t("Removing excess skin after major weight loss.", "Ciddi kilo kaybı sonrası fazla derinin alınması."))]),
]
proc_html = "".join(f'<div class="pcat"><div class="pcat-h">{c}</div><dl>' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in items) + "</dl></div>" for c, items in procs)
ps_rows = "".join(f"<tr><td>{title(d['t'])} {e(d['n'])}</td><td>{hname(k)}</td><td>{HM[k][3]}</td></tr>" for k, d in PLASTIC)
section("plastic", t("07 · Specialty spotlight", "07 · Öne çıkan branş"), t("Plastic, reconstructive<br/>&amp; <em>aesthetic</em> surgery", "Plastik, rekonstrüktif<br/>ve <em>estetik</em> cerrahi"), f'''
<p class="intro">{t("Plastic surgery is one of the most requested treatments in Türkiye. Through our partner hospitals we work with plastic surgeons for both aesthetic and reconstructive procedures, always in a hospital setting with anaesthesia and intensive care support.", "Plastik cerrahi, Türkiye'de en çok tercih edilen tedavilerden biridir. Partner hastanelerimiz aracılığıyla estetik ve rekonstrüktif işlemler için plastik cerrahlarla çalışırız; işlemler her zaman anestezi ve yoğun bakım desteği olan hastane ortamında yapılır.")}</p>
<div class="pgrid">{proc_html}</div>
<h3>{t("How a plastic surgery journey works", "Plastik cerrahi süreci nasıl işler")}</h3>
<div class="cols2"><div>{ul([t("You send photos and your medical history", "Fotoğraflarınızı ve tıbbi geçmişinizi gönderirsiniz"), t("The surgeon reviews them and confirms whether you are a suitable candidate", "Cerrah bunları inceler ve uygun aday olup olmadığınızı teyit eder"), t("You receive a hospital-based quote (Option A or B)", "Hastane bazlı teklif alırsınız (Seçenek A veya B)")], "#6FA52B")}</div>
<div>{ul([t("Face-to-face consultation with the surgeon before surgery", "Ameliyattan önce cerrahla yüz yüze muayene"), t("Surgery and hospital stay as advised by the surgeon", "Cerrahın önerdiği şekilde ameliyat ve hastanede kalış"), t("Check-ups before flying home and remote follow-up after", "Dönüş öncesi kontroller ve sonrasında uzaktan takip")], "#6FA52B")}</div></div>
<div class="callout g">{ic("heart", 22, "#6FA52B")}<p>{t("Your surgeon will advise how long you should stay in Türkiye after your operation and when it is safe to fly. Please plan your travel with this in mind.", "Ameliyattan sonra Türkiye'de ne kadar kalmanız gerektiğini ve ne zaman güvenle uçabileceğinizi cerrahınız belirler. Seyahatinizi buna göre planlayın.")}</p></div>
<h3>{t(f"Plastic surgeons in our network ({len(PLASTIC)})", f"Ağımızdaki plastik cerrahlar ({len(PLASTIC)})")}</h3>
<table class="sum"><thead><tr><th>{t("Surgeon", "Cerrah")}</th><th>{t("Hospital", "Hastane")}</th><th>{t("City", "Şehir")}</th></tr></thead><tbody>{ps_rows}</tbody></table>
<p class="small">{t(f"Source: hospitals' official websites, {DATE}.", f"Kaynak: hastanelerin resmi web siteleri, {DATE}.")}</p>''')

# ---------------------------------------------------------------- 8 SPECIALTIES
toc("specialties", t("Medical specialties", "Tıbbi branşlar"))
def count(k):
    return sum(1 for v in DOCS.values() for d in v if d["d"] in k)
sp = [
 (["med_onc", "rad_onc", "haem", "paed_onc"], t("Oncology & haematology", "Onkoloji ve hematoloji"), t("Medical and radiation oncology, haematology and bone marrow transplantation, with multidisciplinary tumour boards at the larger hospitals.", "Tıbbi ve radyasyon onkolojisi, hematoloji ve kemik iliği nakli; büyük hastanelerde multidisipliner tümör konseyleri.")),
 (["cardio", "cv_surg", "paed_cardio"], t("Heart & vascular", "Kalp ve damar"), t("Cardiology, angiography, bypass and valve surgery, vascular and varicose vein treatment.", "Kardiyoloji, anjiyografi, bypass ve kapak cerrahisi, damar ve varis tedavisi.")),
 (["ortho", "spine"], t("Orthopaedics & spine", "Ortopedi ve omurga"), t("Joint replacement including robotic surgery, sports injuries, hand surgery and spine surgery.", "Robotik cerrahi dahil eklem protezi, spor yaralanmaları, el cerrahisi ve omurga cerrahisi.")),
 (["neurosurg", "neuro"], t("Brain & nervous system", "Beyin ve sinir sistemi"), t("Neurosurgery for tumours and spine, and neurology for epilepsy, migraine, stroke and movement disorders.", "Tümör ve omurga için beyin cerrahisi; epilepsi, migren, inme ve hareket bozuklukları için nöroloji.")),
 (["transplant", "nephro"], t("Organ transplantation & kidney", "Organ nakli ve böbrek"), t("Kidney and liver transplant centres, nephrology and dialysis support.", "Böbrek ve karaciğer nakli merkezleri, nefroloji ve diyaliz desteği.")),
 (["ivf", "gyn"], t("Women's health & IVF", "Kadın sağlığı ve tüp bebek"), t("Gynaecology, high-risk pregnancy, gynaecological oncology and IVF centres.", "Jinekoloji, riskli gebelik, jinekolojik onkoloji ve tüp bebek merkezleri.")),
 (["gen_surg", "gastro", "thor_surg"], t("General & digestive surgery", "Genel ve sindirim sistemi cerrahisi"), t("Laparoscopic and robotic surgery, obesity surgery, liver-pancreas surgery, endoscopy.", "Laparoskopik ve robotik cerrahi, obezite cerrahisi, karaciğer-pankreas cerrahisi, endoskopi.")),
 (["eye", "ent"], t("Eye & ENT", "Göz ve KBB"), t("Cataract, retina and refractive surgery; ear, nose and throat surgery.", "Katarakt, retina ve refraktif cerrahi; kulak burun boğaz cerrahisi.")),
 (["checkup", "internal", "endo"], t("Check-up & internal medicine", "Check-up ve iç hastalıkları"), t("Comprehensive check-up programmes, diabetes and thyroid care, internal medicine.", "Kapsamlı check-up programları, diyabet ve tiroid takibi, iç hastalıkları.")),
]
sp_html = "".join(f'<div class="spc"><div class="spn">{count(k)}</div><div><h4>{h}</h4><p>{p}</p></div></div>' for k, h, p in sp)
section("specialties", t("08 · Specialties", "08 · Branşlar"), t("Medical specialties<br/>across our network", "Ağımızdaki<br/>tıbbi branşlar"), f'''
<p class="intro">{t("Our partner hospitals cover almost every specialty. The number next to each area shows how many physicians in this catalogue work in it.", "Partner hastanelerimiz neredeyse tüm branşları kapsar. Her alanın yanındaki sayı, bu katalogda o alanda çalışan hekim sayısını gösterir.")}</p>
<div class="spgrid">{sp_html}</div>''')

# ---------------------------------------------------------------- 9 NETWORK TABLE
toc("network", t("Partner hospitals at a glance", "Partner hastanelere genel bakış"))
net = ""
for k, en, tr, city, dist, ten, ttr, url in H:
    n = len(DOCS[k]); ps = any(d["d"] == "plastic" for d in DOCS[k])
    net += f'<tr><td><a href="#h_{k}">{tr if TR else en}</a><span class="sub">{dist} · {ttr if TR else ten}</span></td><td>{city}</td><td class="c">{n}</td><td class="c">{ic("check", 13, "#6FA52B", 2.6) if ps else "–"}</td><td><a class="lnk" href="{url}">{domain(url)}</a></td></tr>'
section("network", t("09 · Our solution partners", "09 · Çözüm ortaklarımız"), t("Partner hospitals<br/>at a glance", "Partner hastanelere<br/>genel bakış"), f'''
<p class="intro">{t("We work with leading private and university hospitals in İstanbul, Ankara, İzmir and Antalya. Hospital names link to their section in the physician directory; the web addresses open each hospital's official physician list.", "İstanbul, Ankara, İzmir ve Antalya'da önde gelen özel ve üniversite hastaneleriyle çalışıyoruz. Hastane adları hekim rehberindeki bölümüne, web adresleri ise hastanenin resmi hekim listesine gider.")}</p>
<table class="net"><thead><tr><th>{t("Hospital", "Hastane")}</th><th>{t("City", "Şehir")}</th><th class="c">{t("Physicians", "Hekim")}</th><th class="c">{t("Plastic surgery", "Plastik cerrahi")}</th><th>{t("Official list", "Resmi liste")}</th></tr></thead><tbody>{net}</tbody>
<tfoot><tr><td colspan="2">{t("Total", "Toplam")}</td><td class="c">{TOTAL}</td><td></td><td></td></tr></tfoot></table>''')

# ---------------------------------------------------------------- 10 TITLES GUIDE
toc("titles", t("Reading the directory: Turkish medical titles", "Rehberi okumak: hekim unvanları"))
tit = [
 ("Prof. Dr.", t("Professor", "Profesör"), t("Full professor; the highest academic rank, typically with many years of specialist and teaching experience.", "Akademik kariyerin en üst basamağı; genellikle uzun yıllar uzmanlık ve eğitim deneyimi.")),
 (t("Assoc. Prof. Dr.", "Doç. Dr."), t("Associate professor (Doçent)", "Doçent"), t("Specialist who has completed the national associate professorship process.", "Ulusal doçentlik sürecini tamamlamış uzman hekim.")),
 (t("Asst. Prof. Dr.", "Dr. Öğr. Üyesi"), t("Assistant professor", "Doktor öğretim üyesi"), t("Specialist holding an academic faculty position at a university.", "Üniversitede akademik kadroda bulunan uzman hekim.")),
 (t("Spec. Dr.", "Uzm. Dr."), t("Specialist physician", "Uzman doktor"), t("Physician who has completed specialty training in a non-surgical field.", "Cerrahi dışı bir alanda uzmanlık eğitimini tamamlamış hekim.")),
 ("Op. Dr.", t("Operator doctor", "Operatör doktor"), t("Specialist who has completed training in a surgical field.", "Cerrahi bir alanda uzmanlık eğitimini tamamlamış hekim.")),
 ("Dr.", t("Doctor", "Doktor"), t("Physician (often emergency or general practice).", "Hekim (çoğunlukla acil veya genel pratisyen).")),
 (t("Dent. / Dr. Dent.", "Dt. / Dr. Dt."), t("Dentist", "Diş hekimi"), t("Dentist or dental specialist.", "Diş hekimi veya diş hekimliği uzmanı.")),
]
tit_html = "".join(f"<tr><td class='tt'>{a}</td><td><b>{b}</b><br/><span>{c}</span></td></tr>" for a, b, c in tit)
section("titles", t("10 · Physician directory guide", "10 · Hekim rehberi kılavuzu"), t("How to read<br/>the physician directory", "Hekim rehberi<br/>nasıl okunur"), f'''
<p class="intro">{t(f"The following pages list {TOTAL} physicians at our partner hospitals and centres, grouped by hospital and department. Names are shown as published by each hospital; titles are explained below.", f"Sonraki sayfalarda partner hastane ve merkezlerimizdeki {TOTAL} hekim, hastane ve bölüme göre listelenmiştir. İsimler her hastanenin yayımladığı şekilde verilmiş, unvanlar aşağıda açıklanmıştır.")}</p>
<table class="tit">{tit_html}</table>
<div class="callout">{ic("doc", 22, "#24507A")}<p>{t(f"<b>About this directory:</b> compiled from each hospital's official website on {DATE}. Hospital teams change over time, so please use the hospital's link to check the latest list. Our consultants confirm availability before any appointment is booked. Inclusion in the list does not mean that a physician has a personal agreement with Easy Clinic Center. Support staff such as dietitians, psychologists and physiotherapists are not listed.", f"<b>Bu rehber hakkında:</b> {DATE} tarihinde her hastanenin resmi web sitesinden derlenmiştir. Hastane kadroları zamanla değişebilir; güncel liste için hastanenin linkini kullanın. Danışmanlarımız randevu oluşturmadan önce hekimin uygunluğunu teyit eder. Listede yer almak, hekimin Easy Clinic Center ile kişisel bir anlaşması olduğu anlamına gelmez. Diyetisyen, psikolog ve fizyoterapist gibi destek personeli listelenmemiştir.")}</p></div>''')

# ---------------------------------------------------------------- 11 DIRECTORY
toc("directory", t("Physician directory", "Hekim rehberi"))
dir_html = []
city_order = ["İstanbul", "Ankara", "İzmir", "Antalya"]
for city in city_order:
    for k, en, tr, c, dist, ten, ttr, url in H:
        if c != city:
            continue
        docs = DOCS[k]
        groups = {}
        for d in docs:
            groups.setdefault(d["d"], []).append(d)
        rank = {"Prof. Dr.": 0, "Doç. Dr.": 1, "Dr. Öğr. Üyesi": 2, "Op. Dr.": 3, "Uzm. Dr.": 3, "Dr. Dt.": 4, "Uzm. Dt.": 4, "Dr.": 5, "Dt.": 6}
        body = ""
        for dk in ORDER:
            if dk not in groups:
                continue
            g = sorted(groups[dk], key=lambda d: (rank.get(d["t"], 9), d["n"]))
            cls = " ps" if dk == "plastic" else ""
            items = "".join(f'<li><span class="tl">{title(d["t"])}</span> {e(d["n"])}{" <i>(" + d["campus"] + ")</i>" if d.get("campus") and k == "guven" else ""}</li>' for d in g)
            body += f'<div class="dg{cls}"><h5>{dname(dk)} <span>{len(g)}</span></h5><ul>{items}</ul></div>'
        ps = any(d["d"] == "plastic" for d in docs)
        top = sorted(((dk, len(v)) for dk, v in groups.items() if dk not in ("emerg", "anaes", "radiology", "patho")), key=lambda x: -x[1])[:4]
        tops = " · ".join(f"{dname(dk)} ({n})" for dk, n in top)
        dir_html.append(f'''<div class="hosp" id="h_{k}">
<div class="hh"><div><p class="hcity">{city} · {dist}</p><h3>{tr if TR else en}</h3><p class="htype">{ttr if TR else ten}{(" · <b class='psb'>" + t("Plastic surgery", "Plastik cerrahi") + "</b>") if ps else ""}</p></div>
<div class="hnum"><b>{len(docs)}</b><span>{t("physicians", "hekim")}</span></div></div>
<p class="htop">{t("Largest departments:", "En kalabalık bölümler:")} {tops}</p>
<p class="hlink">{t("Official physician list:", "Resmi hekim listesi:")} <a href="{url}">{url.replace("https://", "")}</a></p>
<div class="dcols">{body}</div></div>''')
section("directory", t("11 · Physician directory", "11 · Hekim rehberi"), t("Physicians at our<br/>partner hospitals", "Partner hastanelerimizdeki<br/>hekimler"), "".join(dir_html), "dir")

# ---------------------------------------------------------------- 12 TRAVEL
toc("travel", t("Travel & stay guide", "Seyahat ve konaklama rehberi"))
section("travel", t("12 · Travel guide", "12 · Seyahat rehberi"), t("Travelling to Türkiye<br/>for treatment", "Tedavi için<br/>Türkiye'ye seyahat"), f'''
<div class="cols2">
<div><h3>{ic("doc", 20, "#22AFC4")} {t("Passport & entry", "Pasaport ve giriş")}</h3>
<p>{t("According to the UK government's travel advice, British citizens do not need a visa for tourist or business visits to Türkiye and can stay up to 90 days in any 180-day period. Your passport must be valid for at least 150 days from your arrival date and have at least one blank page.", "İngiltere hükümetinin seyahat önerilerine göre İngiliz vatandaşları turistik veya iş amaçlı Türkiye ziyaretlerinde vize gerektirmez ve 180 günlük süre içinde 90 güne kadar kalabilir. Pasaportunuzun varış tarihinden itibaren en az 150 gün geçerli olması ve en az bir boş sayfası bulunması gerekir.")}</p>
<p class="note">{t("Entry for medical purposes may have separate requirements. Please check the latest rules on gov.uk and with the Turkish Embassy in London before you travel; we can help you prepare the documents.", "Tıbbi amaçlı girişlerde farklı koşullar olabilir. Seyahatten önce gov.uk'taki ve Türkiye'nin Londra Büyükelçiliği'ndeki güncel kuralları kontrol edin; belgelerin hazırlanmasında size yardımcı oluruz.")}</p>
<h3>{ic("plane", 20, "#22AFC4")} {t("Flights", "Uçuşlar")}</h3>
<p>{t("All four cities have international airports with flights from the UK. Your surgeon decides when you can fly after treatment; we plan the return date accordingly.", "Dört şehrin de İngiltere'den uçuş bulunan uluslararası havalimanları vardır. Tedavi sonrası ne zaman uçabileceğinize cerrahınız karar verir; dönüş tarihini buna göre planlarız.")}</p>
<h3>{ic("hotel", 20, "#22AFC4")} {t("Accommodation", "Konaklama")}</h3>
<p>{t("We recommend hotels close to your hospital. Many patients bring a companion; we arrange rooms for both of you.", "Hastanenize yakın oteller öneririz. Pek çok hasta refakatçiyle gelir; ikiniz için de oda ayarlarız.")}</p></div>
<div><h3>{ic("check", 20, "#22AFC4")} {t("What to bring", "Yanınıza alacaklarınız")}</h3>
{ul([t("Passport and travel insurance documents", "Pasaport ve seyahat sigortası belgeleri"), t("All medical reports, imaging CDs and your medicine list", "Tüm tıbbi raporlar, görüntü CD'leri ve ilaç listeniz"), t("Your regular medicines for the whole stay", "Tüm kalış süresince düzenli kullandığınız ilaçlar"), t("Comfortable, loose clothing for after treatment", "Tedavi sonrası için rahat ve bol kıyafetler"), t("A UK plug adapter (Türkiye uses Type C/F sockets, 230 V)", "Priz adaptörü (Türkiye'de C/F tipi, 230 V priz kullanılır)"), t("Some Turkish lira for small expenses; cards are widely accepted", "Küçük harcamalar için biraz Türk lirası; kartlar yaygın olarak geçerlidir")])}
<h3>{ic("shield", 20, "#22AFC4")} {t("Insurance", "Sigorta")}</h3>
<p>{t("Standard travel insurance often excludes planned medical treatment. Ask your insurer about cover for treatment abroad and possible complications.", "Standart seyahat sigortaları çoğu zaman planlı tedaviyi kapsamaz. Sigortacınıza yurt dışında tedavi ve olası komplikasyonlara ilişkin teminatı sorun.")}</p>
<h3>{ic("clock", 20, "#22AFC4")} {t("Time & language", "Saat ve dil")}</h3>
<p>{t("Türkiye is on GMT+3 all year (2 hours ahead of the UK in summer, 3 in winter). Your consultant helps with communication at the hospital.", "Türkiye yıl boyunca GMT+3 saat dilimindedir (İngiltere'den yazın 2, kışın 3 saat ileri). Hastanede iletişimde danışmanınız yardımcı olur.")}</p></div>
</div>''')

# ---------------------------------------------------------------- 13 PRIVACY & RIGHTS
toc("rights", t("Your rights, privacy & ethics", "Haklarınız, gizlilik ve etik"))
section("rights", t("13 · Your rights", "13 · Haklarınız"), t("Your rights, privacy<br/>and our ethics", "Haklarınız, gizlilik<br/>ve etik ilkelerimiz"), f'''
<div class="grid2">
 <div class="card">{ic("lock", 24, "#22AFC4")}<h4>{t("Your data", "Verileriniz")}</h4><p>{t("We process your personal and health data only to provide the services you ask for, in line with UK GDPR and Türkiye's personal data protection law (KVKK). You can ask what we hold about you and request its deletion.", "Kişisel ve sağlık verilerinizi yalnızca talep ettiğiniz hizmetleri sunmak amacıyla, İngiltere GDPR ve Türkiye'nin Kişisel Verilerin Korunması Kanunu (KVKK) çerçevesinde işleriz. Hakkınızda hangi bilgileri tuttuğumuzu sorabilir ve silinmesini talep edebilirsiniz.")}</p></div>
 <div class="card">{ic("check", 24, "#22AFC4")}<h4>{t("Informed consent", "Bilgilendirilmiş onam")}</h4><p>{t("Before any procedure, the hospital explains the benefits, risks and alternatives and asks for your written consent. You can ask questions and take time to decide.", "Her işlemden önce hastane fayda, risk ve alternatifleri açıklar ve yazılı onamınızı alır. Soru sorabilir, karar vermek için zaman ayırabilirsiniz.")}</p></div>
 <div class="card">{ic("doc", 24, "#22AFC4")}<h4>{t("Medical records", "Tıbbi kayıtlar")}</h4><p>{t("You receive copies of your reports, imaging and discharge summary to take home and share with your doctor in the UK.", "Raporlarınızın, görüntülerinizin ve epikrizinizin kopyalarını alır, İngiltere'deki doktorunuzla paylaşabilirsiniz.")}</p></div>
 <div class="card">{ic("shield", 24, "#22AFC4")}<h4>{t("No pressure", "Baskı yok")}</h4><p>{t("We never pressure you into treatment. Free second thoughts are part of good medicine, and you may withdraw before booking at any time.", "Sizi asla tedaviye zorlamayız. Tekrar düşünmek iyi hekimliğin parçasıdır; rezervasyondan önce istediğiniz zaman vazgeçebilirsiniz.")}</p></div>
</div>
<div class="callout">{ic("chat", 22, "#24507A")}<p>{t("<b>Complaints & feedback:</b> if anything does not meet your expectations, tell your consultant first. We will work with the hospital to resolve it and keep you informed in writing.", "<b>Şikâyet ve geri bildirim:</b> beklentilerinizi karşılamayan bir durum olursa önce danışmanınıza iletin. Hastaneyle birlikte çözmek için çalışır ve sizi yazılı olarak bilgilendiririz.")}</p></div>''')

# ---------------------------------------------------------------- 14 FAQ
toc("faq", t("Frequently asked questions", "Sık sorulan sorular"))
faq = [
 (t("Is the first assessment free?", "İlk değerlendirme ücretsiz mi?"), t("Yes. Reviewing your request and explaining your options does not cost anything.", "Evet. Talebinizin incelenmesi ve seçeneklerin anlatılması ücretsizdir.")),
 (t("Can I choose my own doctor?", "Kendi doktorumu seçebilir miyim?"), t("Yes. You can choose any physician in this directory; we check availability and ask for a quote from that hospital.", "Evet. Bu rehberdeki herhangi bir hekimi seçebilirsiniz; uygunluğunu kontrol eder ve o hastaneden teklif isteriz.")),
 (t("How long does it take to receive quotes?", "Teklifler ne kadar sürede gelir?"), t("It depends on the case and how complete your file is. Your consultant gives you an estimate once your documents are in.", "Vakaya ve dosyanızın ne kadar eksiksiz olduğuna bağlıdır. Belgeleriniz tamamlandığında danışmanınız size tahmini bir süre verir.")),
 (t("What is the difference between Option A and B?", "Seçenek A ile B arasındaki fark nedir?"), t("Option A includes treatment, flights, accommodation and transfers. Option B is the treatment price only; travel services can be added if you want them.", "Seçenek A tedavi, uçak, konaklama ve transferi kapsar. Seçenek B yalnızca tedavi fiyatıdır; istersek seyahat hizmetleri eklenebilir.")),
 (t("Will I speak to the physician for a second opinion?", "İkinci görüş için hekimle görüşecek miyim?"), t("Usually not needed: the physician reviews your file and we report the opinion to you in writing. A video consultation is arranged if the physician considers it necessary.", "Çoğunlukla gerekmez: hekim dosyanızı inceler, görüşünü size yazılı olarak iletiriz. Hekim gerekli görürse görüntülü görüşme ayarlanır.")),
 (t("Does AI make medical decisions?", "Kararı yapay zekâ mı veriyor?"), t("No. AI organises and summarises your documents. Every medical opinion is given by a specialist physician.", "Hayır. Yapay zekâ belgelerinizi düzenler ve özetler. Her tıbbi görüşü uzman hekim verir.")),
 (t("Can a family member come with me?", "Bir yakınım benimle gelebilir mi?"), t("Yes, and we recommend it for surgery. We can include your companion's flights and accommodation in Option A.", "Evet, ameliyatlar için öneririz. Refakatçinizin uçuş ve konaklamasını Seçenek A'ya ekleyebiliriz.")),
 (t("What happens after I return home?", "Eve döndükten sonra ne olur?"), t("You take your reports with you, and we arrange remote check-ins with your physician and stay in touch during your recovery.", "Raporlarınızı yanınızda götürürsünüz; hekiminizle uzaktan kontroller ayarlar ve iyileşme sürecinizde iletişimde kalırız.")),
 (t("What are your working hours?", "Çalışma saatleriniz nedir?"), t("Seven days a week, 08:30–21:00 Türkiye time (GMT+3).", "Haftanın 7 günü, Türkiye saatiyle 08:30–21:00 (GMT+3).")),
 (t("Which cities do you work in?", "Hangi şehirlerde çalışıyorsunuz?"), t("İstanbul, Ankara, İzmir and Antalya, with 14 partner hospitals and centres.", "İstanbul, Ankara, İzmir ve Antalya'da, 14 partner hastane ve merkezle.")),
]
faq_html = "".join(f'<div class="fq"><h4>{q}</h4><p>{a}</p></div>' for q, a in faq)
section("faq", t("14 · FAQ", "14 · SSS"), t("Frequently asked<br/>questions", "Sık sorulan<br/>sorular"), f'<div class="faq">{faq_html}</div>')

# ---------------------------------------------------------------- BACK
back = f'''<section class="back">
<img src="logo_white.png" class="bk-logo"/>
<h2>{t("Let's plan your care together", "Tedavinizi birlikte planlayalım")}</h2>
<p class="bk-sub">{t("Send us your request and a personal consultant will get back to you.", "Talebinizi iletin, kişisel danışmanınız size dönüş yapsın.")}</p>
<div class="bk-info">
  <div>{ic("clock", 24, "#FFFFFF")}<b>{t("7 days a week", "Haftanın 7 günü")}</b><span>08:30 – 21:00 (GMT+3)</span></div>
  <div>{ic("globe", 24, "#FFFFFF")}<b>{t("Website", "Web sitesi")}</b><a href="http://www.easycliniccenter.com/">www.easycliniccenter.com</a></div>
  <div>{ic("home", 24, "#FFFFFF")}<b>{t("Head office", "Merkez ofis")}</b><span>İstanbul / TÜRKİYE</span></div>
</div>
<p class="bk-legal">{t("This catalogue is for general information and does not replace a medical consultation. Treatment plans and prices are confirmed individually after medical review. Physician lists were compiled from hospitals' official websites on " + DATE + " and may change.", "Bu katalog genel bilgilendirme amaçlıdır ve hekim muayenesinin yerine geçmez. Tedavi planları ve fiyatlar tıbbi değerlendirme sonrasında kişiye özel netleştirilir. Hekim listeleri " + DATE + " tarihinde hastanelerin resmi web sitelerinden derlenmiştir ve değişebilir.")}</p>
</section>'''

# ---------------------------------------------------------------- TOC page
toc_rows = "".join(f'<li><a href="#{sid}"><span class="tn">{i+1:02d}</span><span class="tl2">{lab}</span><span class="tp"></span></a></li>' for i, (sid, lab) in enumerate(TOC))
toc_page = f'''<section class="sec tocp"><p class="eyebrow">{t("Contents", "İçindekiler")}</p><h2>{t("In this catalogue", "Bu katalogda")}</h2><ol class="toc">{toc_rows}</ol>
<div class="tocnote">{ic("doc", 20, "#22AFC4")}<p>{t("This is our detailed catalogue. For a short overview, see the Easy Clinic Center corporate catalogue.", "Bu, detay kataloğumuzdur. Kısa bir tanıtım için Easy Clinic Center kurumsal kataloğuna bakabilirsiniz.")}</p></div></section>'''

CSS = r'''
@page { size: A4; margin: 20mm 26mm 20mm 20mm;
  background: url(pagebg.png) no-repeat; background-size: 210mm 297mm;
  @bottom-left { content: "EASY CLINIC CENTER"; font-family: Inter; font-size: 6.5pt; letter-spacing: 2.5px; color: #9AAAB8; }
  @bottom-right { content: counter(page, decimal-leading-zero); font-family: Inter; font-size: 7pt; font-weight: 700; color: #22AFC4; }
}
@page full { margin: 0; background: none; @bottom-left { content: none } @bottom-right { content: none } }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter; color: #33475A; font-size: 9.4pt; line-height: 1.55; }
a { color: inherit; }
.cover, .back { page: full; width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; }
.sec { page-break-before: always; }
.tocp { page-break-before: always; }
.eyebrow { font-size: 7.6pt; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #22AFC4; margin: 0 0 2.5mm; }
h1, h2 { font-family: Lora; font-weight: 500; color: #24507A; margin: 0; line-height: 1.12; }
h2 { font-size: 25pt; margin-bottom: 6mm; }
h2 em, h1 em { font-style: italic; color: #22AFC4; }
h3 { font-family: Lora; font-size: 13.5pt; color: #24507A; font-weight: 600; margin: 6mm 0 2.5mm; }
h3 .ic { vertical-align: -3px; }
h4 { margin: 0 0 1mm; color: #24507A; font-size: 10pt; }
.pb { page-break-before: always; margin-top: 0; }
.intro { font-size: 10.2pt; color: #4F6475; margin: 0 0 5mm; }
.small { font-size: 7.5pt; color: #8495A4; }
.ck { list-style: none; padding: 0; margin: 0; }
.ck li { display: flex; gap: 2mm; margin-bottom: 1.6mm; }
.ck li .ic { flex: none; margin-top: 1mm; }
.cols2 { display: flex; gap: 8mm; }
.cols2 > * { flex: 1; }
.callout { display: flex; gap: 3mm; background: #F2FBFC; border-left: 3px solid #22AFC4; border-radius: 3mm; padding: 4.5mm; margin-top: 5mm; }
.callout.g { background: #F5FAEE; border-left-color: #8DC63F; }
.callout p { margin: 0; }
.callout .ic { flex: none; }
.note { font-size: 8.5pt; background: #FFF8E8; border-radius: 2mm; padding: 2.5mm 3mm; color: #6B5A2A; }

/* cover */
.cover::before { content: ""; position: absolute; right: 0; top: 0; width: 72mm; height: 297mm; background: linear-gradient(180deg, #3DD5E6, #1EF2D6 60%, #3DD5E6); }
.cv-top { position: absolute; top: 26mm; left: 22mm; }
.cv-logo { width: 60mm; }
.cv-mid { position: absolute; top: 108mm; left: 22mm; width: 118mm; }
.cover h1 { font-size: 30pt; margin-bottom: 6mm; }
.cv-sub { font-size: 10.5pt; color: #4F6475; }
.cv-stats { position: absolute; left: 22mm; top: 205mm; display: flex; gap: 3mm; }
.cv-stats div { width: 34mm; background: #24507A; color: #fff; border-radius: 3.5mm; padding: 4mm; }
.cv-stats div:nth-child(2) { background: #22AFC4; } .cv-stats div:nth-child(3) { background: #8DC63F; } .cv-stats div:nth-child(4) { background: #1B3E60; }
.cv-stats b { display: block; font-family: Lora; font-size: 17pt; line-height: 1.1; }
.cv-stats span { font-size: 7.5pt; line-height: 1.25; display: block; margin-top: 1mm; }
.cv-foot { position: absolute; left: 22mm; right: 82mm; bottom: 16mm; display: flex; justify-content: space-between; font-size: 8.5pt; color: #24507A; font-weight: 600; border-top: 1.5px solid #8DC63F; padding-top: 4mm; }
.cv-foot a { color: #22AFC4; text-decoration: none; }

/* toc */
.toc { list-style: none; padding: 0; margin: 0 0 8mm; }
.toc li a { display: block; position: relative; text-decoration: none; padding: 2.6mm 12mm 2.6mm 0; border-bottom: 1px solid #E3EEF2; font-size: 11pt; color: #24507A; }
.tn { font-family: Lora; color: #22AFC4; font-weight: 600; display: inline-block; width: 12mm; }
.tl2 { }
.toc li a::after { position: absolute; right: 0; top: 2.9mm; content: target-counter(attr(href url), page, decimal-leading-zero); font-weight: 700; color: #22AFC4; font-size: 9.5pt; }
.toc li a { }
.tocnote { display: flex; gap: 3mm; font-size: 8.8pt; color: #5E7385; }
.tocnote p { margin: 0; }

/* about */
.lead { font-family: Lora; font-size: 12.5pt; line-height: 1.55; color: #24507A; border-left: 3px solid #8DC63F; padding-left: 6mm; margin-bottom: 6mm; }
.facts { display: flex; gap: 3mm; margin: 6mm 0 2mm; }
.facts div { flex: 1; background: #F2FBFC; border-radius: 3mm; padding: 4mm; }
.facts b { display: block; color: #24507A; font-size: 10pt; margin-top: 2mm; }
.facts span { font-size: 8pt; color: #5E7385; }
.vals { display: flex; flex-wrap: wrap; gap: 4mm; }
.vals div { width: calc(50% - 2mm); border: 1px solid #DCEFF3; border-radius: 3mm; padding: 4mm; }
.vals p { margin: 0; font-size: 8.8pt; }
.grid3 { display: flex; flex-wrap: wrap; gap: 4mm; }
.grid3 .card { width: calc(33.33% - 2.7mm); }
.grid2 { display: flex; flex-wrap: wrap; gap: 4mm; }
.grid2 .card { width: calc(50% - 2mm); }
.card { border: 1px solid #DCEFF3; border-radius: 3.5mm; padding: 4.5mm; }
.card h4 { margin-top: 2mm; }
.card p { margin: 0; font-size: 8.8pt; color: #5E7385; }

/* services */
.svcgrid { display: flex; flex-wrap: wrap; gap: 4mm; }
.svc { width: calc(50% - 2mm); border: 1px solid #BFEAF0; border-radius: 3.5mm; overflow: hidden; background: #FBFEFF; }
.svc-h { background: linear-gradient(90deg, #24507A, #22AFC4); display: flex; align-items: center; gap: 2.5mm; padding: 3mm 4mm; }
.svc-h h4 { color: #fff; margin: 0; font-size: 10pt; }
.svc p { margin: 3mm 4mm 2mm; font-size: 8.8pt; }
.svc .ck { margin: 0 4mm 3mm; font-size: 8.6pt; }
.svcgrid.sm .svc { width: calc(33.33% - 2.7mm); background: #fff; border-color: #DCEFF3; }
.svc-h.s { background: #E6F8FA; }
.svc-h.s h4 { color: #24507A; font-size: 9.4pt; }

/* journey */
.iso { margin: -2mm -4mm 0 -6mm; }
.steps { display: flex; flex-wrap: wrap; gap: 4mm; }
.step { width: calc(50% - 2mm); display: flex; gap: 3.5mm; border: 1px solid #DCEFF3; border-radius: 3.5mm; padding: 4.5mm; }
.sn { flex: none; width: 10mm; height: 10mm; border-radius: 50%; background: #22AFC4; color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 11pt; }
.step:nth-child(4) .sn { background: #8DC63F; }
.step p { margin: 0; font-size: 8.8pt; }

/* quote */
table.qt { width: 100%; border-collapse: collapse; margin-bottom: 6mm; }
.qt th { font-size: 9pt; color: #fff; padding: 3mm; }
.qt th.a { background: #14B8A4; } .qt th.b { background: #6FA52B; }
.qt th:first-child { background: none; }
.qt td { border-bottom: 1px solid #E3EEF2; padding: 2.6mm 3mm; font-size: 9pt; }
.qt td.c { text-align: center; width: 34mm; font-weight: 700; }
.qt td.a { color: #14B8A4; background: #F0FBF9; } .qt td.b { color: #6FA52B; background: #F5FAEE; }
.c { text-align: center; }

/* second */
.flow4 { display: flex; gap: 3mm; margin-bottom: 4mm; }
.flow4 div { flex: 1; border: 1px solid #DCEFF3; border-radius: 3.5mm; padding: 4mm; position: relative; }
.flow4 span { font-family: Lora; font-size: 18pt; color: #CDEFF4; font-weight: 600; position: absolute; top: 2mm; right: 3mm; }
.flow4 div.ai { background: linear-gradient(160deg, #22AFC4, #1EE6CF); border: 0; }
.flow4 div.ai h4, .flow4 div.ai p { color: #fff; } .flow4 div.ai span { color: rgba(255,255,255,.5); }
.flow4 p { margin: 0; font-size: 8.4pt; }
.dodont p { margin: 0 0 2mm; padding: 2.5mm 3mm; border-radius: 2mm; font-size: 8.8pt; }
.do { background: #F0FBF9; } .dont { background: #FFF1F1; }

/* plastic */
.pgrid { display: flex; flex-wrap: wrap; gap: 4mm; }
.pcat { width: calc(50% - 2mm); border: 1px solid #D5EBB8; border-radius: 3.5mm; overflow: hidden; }
.pcat-h { background: linear-gradient(90deg, #6FA52B, #8DC63F); color: #fff; padding: 2.5mm 4mm; font-weight: 700; }
.pcat dl { margin: 2.5mm 4mm 3mm; }
.pcat dt { font-weight: 700; color: #24507A; font-size: 9pt; }
.pcat dd { margin: 0 0 1.8mm; font-size: 8.4pt; color: #5E7385; }
table.sum, table.net { width: 100%; border-collapse: collapse; font-size: 8.6pt; }
.sum th, .net th { text-align: left; font-size: 6.8pt; letter-spacing: 1.5px; text-transform: uppercase; color: #22AFC4; border-bottom: 1.5px solid #BFEAF0; padding: 2mm; }
.sum td, .net td { border-bottom: 1px solid #E8F3F6; padding: 1.35mm 2mm; vertical-align: top; }
.net td a { text-decoration: none; font-weight: 600; color: #24507A; }
.net td a.lnk { color: #22AFC4; font-weight: 500; font-size: 7.8pt; }
.net .sub { display: block; font-size: 7.4pt; color: #8495A4; }
.net tfoot td { font-weight: 700; color: #24507A; border-top: 1.5px solid #BFEAF0; }

/* specialties */
.spgrid { display: flex; flex-wrap: wrap; gap: 4mm; }
.spc { width: calc(50% - 2mm); display: flex; gap: 4mm; border: 1px solid #DCEFF3; border-radius: 3.5mm; padding: 4mm; }
.spn { flex: none; width: 15mm; height: 15mm; border-radius: 3mm; background: #24507A; color: #fff; font-family: Lora; font-size: 14pt; font-weight: 600; display: flex; align-items: center; justify-content: center; }
.spc p { margin: 0; font-size: 8.6pt; }

/* titles */
table.tit { width: 100%; border-collapse: collapse; }
.tit td { border-bottom: 1px solid #E3EEF2; padding: 2.6mm 3mm; vertical-align: top; font-size: 9pt; }
.tit td.tt { width: 40mm; font-weight: 700; color: #22AFC4; font-size: 10pt; }
.tit span { color: #5E7385; font-size: 8.6pt; }

/* directory */
.dir h2 { margin-bottom: 4mm; }
.hosp { page-break-before: always; }
.dir h2 + .hosp { page-break-before: auto; }
.hh { display: flex; justify-content: space-between; align-items: flex-end; background: linear-gradient(90deg, #24507A, #1E6C93); color: #fff; border-radius: 3.5mm; padding: 4.5mm 5mm; }
.hh h3 { color: #fff; margin: 0.5mm 0; font-size: 15pt; }
.hcity { margin: 0; font-size: 7.4pt; letter-spacing: 2px; text-transform: uppercase; color: #9FE6EF; font-weight: 700; }
.htype { margin: 0; font-size: 8pt; color: #D7F0F6; }
.psb { color: #C6F08C; }
.hnum { text-align: right; }
.hnum b { display: block; font-family: Lora; font-size: 22pt; line-height: 1; }
.hnum span { font-size: 7.4pt; color: #D7F0F6; }
.htop { margin: 2.5mm 0 0.5mm; font-size: 7.8pt; color: #5E7385; }
.hlink { margin: 0 0 3mm; font-size: 7.6pt; }
.hlink a { color: #22AFC4; text-decoration: none; }
.dcols { column-count: 3; column-gap: 5mm; column-fill: auto; }
.dg { break-inside: auto; margin-bottom: 2.5mm; }
.dg h5 { break-after: avoid; margin: 0 0 1mm; font-size: 7.4pt; color: #24507A; text-transform: uppercase; letter-spacing: .6px; border-bottom: 1.2px solid #3DD5E6; padding-bottom: .6mm; }
.dg h5 { display: flex; justify-content: space-between; gap: 2mm; } .dg h5 span { color: #22AFC4; font-weight: 700; flex: none; }
.dg.ps h5 { color: #fff; background: #6FA52B; border: 0; padding: .8mm 1.6mm; border-radius: 1.2mm; }
.dg.ps h5 span { color: #fff; }
.dg ul { list-style: none; padding: 0; margin: 0; }
.dg li { font-size: 7.3pt; line-height: 1.32; padding: .25mm 0; break-inside: avoid; }
.dg li .tl { color: #8495A4; font-size: 6.6pt; }
.dg li i { color: #8495A4; font-size: 6.4pt; }

/* faq */
.faq { display: flex; flex-wrap: wrap; gap: 4mm; }
.fq { width: calc(50% - 2mm); border: 1px solid #DCEFF3; border-radius: 3.5mm; padding: 4mm; }
.fq p { margin: 0; font-size: 8.8pt; }

/* back */
.back { background: linear-gradient(160deg, #24507A 0%, #1E6C93 55%, #22AFC4 100%); color: #fff; padding: 40mm 24mm; page-break-after: auto; page-break-before: always; }
.bk-logo { width: 60mm; margin-bottom: 28mm; }
.back h2 { color: #fff; font-size: 30pt; }
.bk-sub { font-size: 12pt; color: #D7F5F9; margin: 0 0 16mm; }
.bk-info { display: flex; gap: 5mm; }
.bk-info div { flex: 1; background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.25); border-radius: 4mm; padding: 6mm 5mm; }
.bk-info b { display: block; margin: 3mm 0 1mm; font-size: 10.5pt; }
.bk-info span, .bk-info a { font-size: 9pt; color: #D7F5F9; text-decoration: none; }
.bk-legal { position: absolute; left: 24mm; right: 24mm; bottom: 16mm; font-size: 7.5pt; color: #BDE6EE; border-top: 1px solid rgba(255,255,255,.3); padding-top: 4mm; }
.ic { display: inline-block; }
'''

doc_title = t("Easy Clinic Center – Detailed Catalogue", "Easy Clinic Center – Detay Katalog")
html_doc = f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{doc_title}</title><style>{CSS}</style></head><body>{cover}{toc_page}{"".join(S)}{back}</body></html>'
pathlib.Path(f"/home/claude/cat/detail_{LANG}.html").write_text(html_doc)
out = t("Easy_Clinic_Center_Detailed_Catalogue_EN.pdf", "Easy_Clinic_Center_Detay_Katalog_TR.pdf")
weasyprint.HTML(string=html_doc, base_url="/home/claude/cat/").write_pdf(f"/home/claude/cat/{out}")
print(out)
