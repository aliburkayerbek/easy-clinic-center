"""Easy Clinic Center – Treatments brochure (EN/TR). Usage: python3 build5.py en|tr"""
import sys, json, pathlib, weasyprint
import illus

LANG = sys.argv[1]
TR = LANG == "tr"
def t(en, tr):
    return tr if TR else en

D = json.load(open("/home/claude/cat/doctors.json"))["hospitals"]
HN = {
 "memorial_sisli": ("Memorial Şişli", "İstanbul"), "acibadem_maslak": ("Acıbadem Maslak", "İstanbul"), "medicana_istanbul": ("Medicana Int. İstanbul", "İstanbul"),
 "memorial_ankara": ("Memorial Ankara", "Ankara"), "medicana_ankara": ("Medicana Int. Ankara", "Ankara"), "acibadem_ankara": ("Acıbadem Ankara", "Ankara"),
 "ufuk": (t("Ufuk University Hospital", "Ufuk Üniversitesi Hastanesi"), "Ankara"), "guven": (t("Güven Hospital", "Güven Hastanesi"), "Ankara"), "tobb": (t("TOBB ETÜ Hospital", "TOBB ETÜ Hastanesi"), "Ankara"),
 "acibadem_kent": ("Acıbadem İzmir Kent", "İzmir"), "medicana_izmir": ("Medicana Int. İzmir", "İzmir"), "medicana_cesme": (t("Medicana Çeşme Medical Centre", "Medicana Çeşme Tıp Merkezi"), "İzmir"),
 "memorial_antalya": ("Memorial Antalya", "Antalya"), "medstar_antalya": ("Medstar Antalya", "Antalya"),
}
def where(dept):
    return [k for k, v in D.items() if any(x["d"] == dept for x in v)]
def chips(keys):
    return "".join(f'<span><b>{HN[k][0]}</b> · {HN[k][1]}</span>' for k in keys)

ICON = {
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 "bed": '<path d="M3 18V7 M3 14h18v4 M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="2"/>',
 "plane": '<path d="M2 16l20-6-20-6 4 6-4 6z M6 10h9" />',
 "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
 "check": '<path d="M5 12l4 4 10-10"/>',
 "pin": '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "doc": '<path d="M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 16h7"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18 M12 3c3 3 3 15 0 18 M12 3c-3 3-3 15 0 18"/>',
 "home": '<path d="M3 11l9-7 9 7v9H3z M9 20v-6h6v6"/>',
}
def ic(n, s=16, c="#22AFC4", w=1.9):
    return f'<svg class="ic" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</svg>'
def ul(items, c="#22AFC4"):
    return '<ul class="ck">' + "".join(f"<li>{ic('check', 12, c, 2.6)}<span>{x}</span></li>" for x in items) + "</ul>"

DEPTS = {
 "plastic": ("#6FA52B", "#8DC63F", "#EEF7E2", t("Plastic &amp; Aesthetic Surgery", "Plastik ve Estetik Cerrahi")),
 "general": ("#24507A", "#22AFC4", "#E8F6FA", t("General Surgery", "Genel Cerrahi")),
 "dental": ("#14A3B8", "#1EE6CF", "#E6FBF8", t("Dentistry", "Diş Hekimliği")),
 "internal": ("#1B3E60", "#3D7CB8", "#EAF1F8", t("Internal Medicine", "Dahili Branşlar")),
}

def facts(rows):
    icons = ["clock", "moon", "bed", "plane", "heart"]
    labels = [t("Procedure", "İşlem süresi"), t("Anaesthesia", "Anestezi"), t("Hospital stay", "Hastanede kalış"), t("Stay in Türkiye", "Türkiye'de kalış"), t("Back to daily life", "Günlük hayata dönüş")]
    return '<div class="facts">' + "".join(f'<div>{ic(i, 15)}<span>{l}</span><b>{v}</b></div>' for i, l, v in zip(icons, labels, rows) if v) + "</div>"

def treatment(dept, key, title_, tagline, what, who, how, factrows, extra=""):
    c1, c2, bg, _ = DEPTS[dept]
    return f'''<div class="tr" style="--c1:{c1};--c2:{c2};--bg:{bg}">
 <div class="tr-top">
  <div class="tr-ill">{illus.ILL[key]()}</div>
  <div class="tr-txt"><p class="tag">{tagline}</p><h3>{title_}</h3><p>{what}</p>
   <h5>{t("Who is it for?", "Kimler için?")}</h5>{ul(who, c1)}</div>
 </div>
 {facts(factrows) if factrows else ""}{f'<p class="fn">{NOTE}</p>' if factrows else ""}
 <div class="how"><h5>{t("How it works with us", "Bizimle süreç")}</h5><ol>{"".join(f"<li>{x}</li>" for x in how)}</ol></div>
 {extra}
</div>'''

def dept_banner(dept, intro, avail_label, avail):
    c1, c2, bg, name = DEPTS[dept]
    return f'''<div class="db" style="--c1:{c1};--c2:{c2};margin-bottom:5mm"><div><p class="eb">{t("Department", "Bölüm")}</p><h2>{name}</h2><p>{intro}</p></div></div>
'''

S = []
NOTE = t("Times are typical and vary from patient to patient. Your physician confirms the plan after examining you.", "Süreler tipik değerlerdir ve hastadan hastaya değişir. Planı, muayene sonrasında hekiminiz kesinleştirir.")

# ---------------- COVER
grid = "".join(f'<div>{illus.ILL[k]()}</div>' for k in ["breast", "lipo", "rhino", "obesity", "cancer", "thyroid", "implant", "hollywood", "second", "chronic"])
S.append(f'''<section class="cover">
<img src="logo.png" class="cv-logo"/>
<p class="eyebrow">{t("Treatments &amp; Centres · 2026", "Tedaviler ve Merkezler · 2026")}</p>
<h1>{t("Featured<br/><em>treatments</em>", "Öne çıkan<br/><em>tedavilerimiz</em>")}</h1>
<p class="cv-sub">{t("A selection of our treatments in plastic &amp; aesthetic surgery, general surgery, dentistry and internal medicine, coordinated for patients from the UK by one dedicated team. For other specialties, please ask us.", "Plastik ve estetik cerrahi, genel cerrahi, diş hekimliği ve dahili branşlardaki tedavilerimizden bazıları; İngiltere'den gelen hastalar için tek bir ekip tarafından koordine edilir. Diğer branşlar için bize danışabilirsiniz.")}</p>
<div class="cv-grid">{grid}</div>
<div class="cv-foot"><span>İstanbul · Ankara · İzmir · Antalya</span><a href="http://www.easycliniccenter.com/">www.easycliniccenter.com</a></div>
</section>''')

# ---------------- OVERVIEW
ov = [
 ("plastic", "breast", [t("Breast implants", "Meme implantı"), t("Liposuction", "Liposuction (yağ aldırma)"), t("Rhinoplasty", "Burun estetiği")]),
 ("general", "obesity", [t("Obesity surgery", "Obezite cerrahisi"), t("Cancer surgery", "Kanser cerrahisi"), t("Thyroid surgery", "Tiroid cerrahisi")]),
 ("dental", "implant", [t("Dental implants", "İmplant tedavisi"), t("Hollywood smile", "Hollywood gülüşü")]),
 ("internal", "second", [t("Second medical opinion", "2. hekim görüşü"), t("Chronic disease follow-up centre", "Kronik hastalık takip merkezi")]),
]
ovh = "".join(f'''<div class="ov" style="--c1:{DEPTS[d][0]};--bg:{DEPTS[d][2]}"><div class="ov-ill">{illus.ILL[k]()}</div><div><h3>{DEPTS[d][3]}</h3>{ul(items, DEPTS[d][0])}</div></div>''' for d, k, items in ov)
S.append(f'''<section class="pg"><p class="eyebrow">{t("At a glance", "Bir bakışta")}</p><h2 class="big">{t("Featured treatments<br/>in this brochure", "Bu broşürde öne çıkan<br/>tedavilerimiz")}</h2>
<p class="intro">{t("This brochure presents some of our most requested treatments; we also coordinate care in many other specialties. For each treatment we match you with an experienced specialist, obtain a hospital-based quote in two forms (all-inclusive or treatment only) and coordinate your whole journey.", "Bu broşürde en çok talep gören tedavilerimizden bazılarını bulabilirsiniz; birçok farklı branşta da hizmet veriyoruz. Her tedavi için sizi deneyimli bir uzmanla eşleştirir, iki şekilde (her şey dahil veya sadece tedavi) hastane bazlı teklif alır ve tüm yolculuğunuzu koordine ederiz.")}</p>
<div class="ovgrid">{ovh}</div>
<div class="steps4">
 <div><b>1</b><span>{t("Fill in our patient form", "Hasta formumuzu doldurun")}</span></div>
 <div><b>2</b><span>{t("Your case is reviewed by a specialist", "Vakanız uzman tarafından incelenir")}</span></div>
 <div><b>3</b><span>{t("Receive hospital-based quotes", "Hastane bazlı teklifler alın")}</span></div>
 <div><b>4</b><span>{t("Treatment &amp; follow-up", "Tedavi ve takip")}</span></div>
</div></section>''')

# ---------------- PLASTIC
ps_av = chips(where("plastic"))
S.append(f'''<section class="pg">{dept_banner("plastic", t("Aesthetic and reconstructive procedures performed by plastic surgeons in fully equipped hospitals with anaesthesia and intensive-care support.", "Estetik ve rekonstrüktif işlemler, anestezi ve yoğun bakım desteği olan tam donanımlı hastanelerde plastik cerrahlar tarafından yapılır."), t("Plastic surgery departments at:", "Plastik cerrahi bölümü bulunan hastaneler:"), ps_av)}
{treatment("plastic", "breast", t("Breast implants", "Meme implantı"), t("Breast augmentation", "Meme büyütme"),
 t("Breast augmentation uses silicone implants to increase volume and improve shape and symmetry. The surgeon helps you choose the implant size, shape and placement (above or below the muscle) that suits your body.", "Meme büyütme, hacmi artırmak ve şekli ile simetriyi iyileştirmek için silikon implantlarla yapılır. Cerrahınız vücudunuza uygun implant boyutunu, şeklini ve yerleşimini (kas üstü veya altı) birlikte belirler."),
 [t("Women who feel their breasts are small or have lost volume after pregnancy or weight loss", "Memesini küçük bulan veya gebelik ve kilo kaybı sonrası hacim kaybı yaşayan kadınlar"), t("Correcting asymmetry between the two breasts", "İki meme arasındaki asimetrinin düzeltilmesi"), t("Adults in good general health with realistic expectations", "Genel sağlık durumu iyi, gerçekçi beklentileri olan yetişkinler")],
 [t("You send photos (without your face) and your medical history", "Fotoğraflarınızı (yüzünüz görünmeden) ve tıbbi geçmişinizi gönderirsiniz"), t("The surgeon proposes an implant plan and the hospital sends a quote", "Cerrah implant planı önerir, hastane teklif gönderir"), t("Consultation and measurements in Türkiye, then surgery", "Türkiye'de muayene ve ölçümler, ardından ameliyat"), t("Check-up before flying home; remote follow-up afterwards", "Dönüş öncesi kontrol; sonrasında uzaktan takip")],
 [t("1–2 hours", "1–2 saat"), t("General", "Genel anestezi"), t("1 night", "1 gece"), t("About 6–7 days", "Yaklaşık 6–7 gün"), t("Desk work ~1 week, sport 4–6 weeks", "Masa başı iş ~1 hafta, spor 4–6 hafta")])}
</section>''')
S.append(f'''<section class="pg">
{treatment("plastic", "lipo", t("Liposuction", "Liposuction"), t("Body contouring", "Vücut şekillendirme"),
 t("Liposuction removes stubborn fat deposits that do not respond to diet and exercise, such as the abdomen, flanks, thighs, arms and chin, to reshape the body's contours. It is not a weight-loss method.", "Liposuction; karın, bel, basen, bacak, kol ve gıdı gibi bölgelerde diyet ve egzersize direnen yağların alınarak vücut hatlarının şekillendirilmesidir. Bir zayıflama yöntemi değildir."),
 [t("People close to their ideal weight with localised fat deposits", "İdeal kilosuna yakın, bölgesel yağlanması olan kişiler"), t("Good skin elasticity", "Cilt esnekliği iyi olanlar"), t("Can be combined with tummy tuck or fat transfer", "Karın germe veya yağ transferiyle birleştirilebilir")],
 [t("Photos of the areas (no face) and your weight history", "Bölgelerin fotoğrafları (yüzsüz) ve kilo geçmişiniz"), t("Surgeon defines areas and technique; quote follows", "Cerrah bölgeleri ve tekniği belirler; teklif gelir"), t("Surgery, then a compression garment for several weeks", "Ameliyat, ardından birkaç hafta korse kullanımı"), t("Check-up before your flight home", "Dönüş uçuşundan önce kontrol")],
 [t("1–3 hours", "1–3 saat"), t("General or sedation", "Genel anestezi veya sedasyon"), t("0–1 night", "0–1 gece"), t("About 5–7 days", "Yaklaşık 5–7 gün"), t("Work in 3–7 days", "İşe dönüş 3–7 gün")])}
{treatment("plastic", "rhino", t("Rhinoplasty", "Burun estetiği"), t("Nose reshaping", "Rinoplasti"),
 t("Rhinoplasty reshapes the nose to bring it into harmony with the face and can also improve breathing (septorhinoplasty). Open or closed techniques are planned according to your anatomy.", "Rinoplasti, burnu yüzle uyumlu hâle getirmek için yeniden şekillendirir; gerektiğinde nefes almayı da iyileştirir (septorinoplasti). Açık veya kapalı teknik anatominize göre planlanır."),
 [t("Hump, wide or drooping tip, asymmetry", "Kemer, geniş veya düşük burun ucu, asimetri"), t("Breathing problems due to a deviated septum", "Septum eğriliğine bağlı nefes sorunları"), t("Adults whose facial growth is complete", "Yüz gelişimi tamamlanmış yetişkinler")],
 [t("Your consultant arranges a secure way to share face photos, only with your consent", "Danışmanınız yüz fotoğrafları için, yalnızca onayınızla, güvenli bir paylaşım yolu ayarlar"), t("Surgeon assessment and quote", "Cerrah değerlendirmesi ve teklif"), t("Surgery; a splint stays on for about a week", "Ameliyat; atel yaklaşık bir hafta kalır"), t("Splint removal in Türkiye before you fly home", "Dönüşten önce Türkiye'de atelin alınması")],
 [t("2–3 hours", "2–3 saat"), t("General", "Genel anestezi"), t("1 night", "1 gece"), t("About 7–8 days", "Yaklaşık 7–8 gün"), t("Social life ~2 weeks; final shape up to 12 months", "Sosyal hayat ~2 hafta; son şekil 12 aya kadar")])}
</section>''')

# ---------------- GENERAL SURGERY
S.append(f'''<section class="pg">{dept_banner("general", t("Laparoscopic and robotic surgery, obesity and metabolic surgery, oncological and endocrine surgery.", "Laparoskopik ve robotik cerrahi, obezite ve metabolik cerrahi, onkolojik ve endokrin cerrahi."), t("General surgery is available at all 14 partner hospitals and centres. Dedicated obesity surgery centres include:", "Genel cerrahi 14 partner kurumun tamamında mevcuttur. Obezite cerrahisi merkezleri:"), chips(["acibadem_maslak", "medstar_antalya"]))}
{treatment("general", "obesity", t("Obesity surgery", "Obezite cerrahisi"), t("Bariatric &amp; metabolic surgery", "Bariatrik ve metabolik cerrahi"),
 t("Obesity surgery helps people with severe obesity lose weight permanently and often improves type 2 diabetes, high blood pressure and sleep apnoea. The most common operations are sleeve gastrectomy and gastric bypass, performed laparoscopically.", "Obezite cerrahisi, ciddi obezitesi olan kişilerin kalıcı olarak kilo vermesine yardımcı olur; çoğu zaman tip 2 diyabet, yüksek tansiyon ve uyku apnesini de iyileştirir. En sık yapılan ameliyatlar laparoskopik tüp mide ve gastrik bypass'tır."),
 [t("BMI of 40 or above, or 35 or above with related conditions such as diabetes", "Vücut kitle indeksi 40 ve üzeri ya da diyabet gibi eşlik eden hastalıkla 35 ve üzeri"), t("Previous diet attempts without lasting success", "Kalıcı sonuç vermemiş diyet denemeleri"), t("Final suitability is decided by the surgeon and anaesthetist", "Uygunluğa son kararı cerrah ve anestezi uzmanı verir")],
 [t("Your height, weight, illnesses and medicines via our patient form", "Hasta formumuzla boy, kilo, hastalık ve ilaç bilgileriniz"), t("Pre-operative tests: blood work, endoscopy, cardiology and anaesthesia review", "Ameliyat öncesi tetkikler: kan tahlilleri, endoskopi, kardiyoloji ve anestezi değerlendirmesi"), t("Laparoscopic surgery and a few days in hospital", "Laparoskopik ameliyat ve birkaç gün hastanede kalış"), t("Dietitian plan and long-term remote follow-up", "Diyetisyen planı ve uzun dönem uzaktan takip")],
 [t("1–2 hours", "1–2 saat"), t("General", "Genel anestezi"), t("2–3 nights", "2–3 gece"), t("About 7–10 days", "Yaklaşık 7–10 gün"), t("Work ~2 weeks; staged diet for several weeks", "İşe dönüş ~2 hafta; birkaç hafta kademeli diyet")])}
</section>''')
S.append(f'''<section class="pg">
{treatment("general", "cancer", t("Cancer surgery", "Kanser cerrahisi"), t("Surgical oncology", "Cerrahi onkoloji"),
 t("Surgical removal of tumours of the breast, stomach, bowel, liver, pancreas and other organs, planned by a multidisciplinary tumour board together with oncology, radiology and pathology. Laparoscopic or robotic techniques are used where suitable.", "Meme, mide, bağırsak, karaciğer, pankreas ve diğer organların tümörlerinin cerrahi olarak çıkarılması; onkoloji, radyoloji ve patoloji ile birlikte multidisipliner tümör konseyinde planlanır. Uygun durumlarda laparoskopik veya robotik teknik kullanılır."),
 [t("Patients with a confirmed or suspected cancer diagnosis", "Kesinleşmiş veya şüpheli kanser tanısı olan hastalar"), t("Patients wanting a second opinion before surgery", "Ameliyat öncesi ikinci görüş isteyen hastalar"), t("Patients needing treatment without long waiting times", "Uzun bekleme olmadan tedavi olmak isteyen hastalar")],
 [t("Send your pathology, imaging (DICOM) and reports", "Patoloji, görüntüleme (DICOM) ve raporlarınızı gönderin"), t("Tumour board review and treatment plan", "Tümör konseyi değerlendirmesi ve tedavi planı"), t("Surgery, plus chemotherapy or radiotherapy if needed", "Ameliyat; gerekirse kemoterapi veya radyoterapi"), t("Reports for your UK oncologist and ongoing follow-up", "İngiltere'deki onkoloğunuz için raporlar ve takip")],
 [t("Depends on the operation", "Ameliyata göre değişir"), t("General", "Genel anestezi"), t("Planned individually", "Kişiye özel planlanır"), t("Planned individually", "Kişiye özel planlanır"), ""])}
{treatment("general", "thyroid", t("Thyroid surgery", "Tiroid cerrahisi"), t("Endocrine surgery", "Endokrin cerrahi"),
 t("Partial or total removal of the thyroid gland for nodules, goitre, overactive thyroid or thyroid cancer. Nerve monitoring is used during surgery to protect the voice.", "Nodül, guatr, aşırı çalışan tiroid veya tiroid kanseri nedeniyle tiroid bezinin bir kısmının ya da tamamının alınması. Sesi korumak için ameliyat sırasında sinir monitörizasyonu kullanılır."),
 [t("Large or growing nodules and goitre", "Büyük veya büyüyen nodül ve guatr"), t("Suspicious biopsy results or thyroid cancer", "Şüpheli biyopsi sonucu veya tiroid kanseri"), t("Overactive thyroid not controlled with medicines", "İlaçla kontrol edilemeyen aşırı çalışan tiroid")],
 [t("Send your ultrasound, biopsy and thyroid blood tests", "Ultrason, biyopsi ve tiroid tahlillerinizi gönderin"), t("Endocrinology and surgical review; quote", "Endokrinoloji ve cerrahi değerlendirme; teklif"), t("Surgery with voice and calcium checks", "Ses ve kalsiyum kontrolleriyle ameliyat"), t("Pathology result and hormone plan for your GP", "Patoloji sonucu ve aile hekiminiz için hormon planı")],
 [t("1.5–3 hours", "1,5–3 saat"), t("General", "Genel anestezi"), t("1–2 nights", "1–2 gece"), t("About 5–7 days", "Yaklaşık 5–7 gün"), t("Work in 1–2 weeks", "İşe dönüş 1–2 hafta")])}
</section>''')

# ---------------- DENTAL
S.append(f'''<section class="pg">{dept_banner("dental", t("Restoring missing teeth and designing natural, confident smiles with digital planning and modern materials.", "Dijital planlama ve modern materyallerle eksik dişlerin tamamlanması ve doğal, özgüvenli gülüşlerin tasarlanması."), t("Dental departments at:", "Diş bölümü bulunan hastaneler:"), chips(where("dental")))}
{treatment("dental", "implant", t("Dental implants", "İmplant tedavisi"), t("Fixed replacement teeth", "Sabit diş tedavisi"),
 t("A titanium implant placed in the jawbone replaces the root of a missing tooth and carries a crown that looks and feels natural. Single teeth, bridges or full arches (for example all-on-4 / all-on-6) can be restored.", "Çene kemiğine yerleştirilen titanyum implant, eksik dişin kökünün yerini alır ve doğal görünen bir kronu taşır. Tek diş, köprü veya tam çene (örneğin all-on-4 / all-on-6) restorasyonu yapılabilir."),
 [t("One or more missing teeth", "Bir veya daha fazla eksik diş"), t("Loose dentures you want to replace with fixed teeth", "Hareketli protez yerine sabit diş isteyenler"), t("Sufficient bone, or bone grafting when needed", "Yeterli kemik ya da gerektiğinde kemik grefti")],
 [t("Send a recent panoramic X-ray or 3D scan (CBCT) and photos of your teeth", "Güncel panoramik röntgen veya 3D tomografi (CBCT) ve diş fotoğraflarınızı gönderin"), t("Treatment plan and quote", "Tedavi planı ve teklif"), t("Visit 1: implants placed, temporary teeth", "1. ziyaret: implantlar yerleştirilir, geçici dişler"), t("Visit 2 (after healing): permanent crowns", "2. ziyaret (iyileşme sonrası): kalıcı kronlar")],
 [t("About 1 hour per implant", "İmplant başına yaklaşık 1 saat"), t("Local (sedation optional)", "Lokal (isteğe bağlı sedasyon)"), t("Not required", "Gerekmez"), t(" Visit 1: 4–7 days · Visit 2: 5–7 days", "1. ziyaret: 4–7 gün · 2. ziyaret: 5–7 gün"), t("Healing 3–6 months between visits", "Ziyaretler arası iyileşme 3–6 ay")])}
</section>''')
S.append(f'''<section class="pg">
{treatment("dental", "hollywood", t("Hollywood smile", "Hollywood gülüşü"), t("Smile design", "Gülüş tasarımı"),
 t("A Hollywood smile is a personalised smile design using porcelain veneers, E-max laminates or zirconia crowns to change the colour, shape and alignment of the visible teeth. Digital smile design lets you preview the result before treatment.", "Hollywood gülüşü; porselen veneer, E-max lamina veya zirkonyum kronlarla görünen dişlerin rengini, şeklini ve dizilimini değiştiren kişiye özel bir gülüş tasarımıdır. Dijital gülüş tasarımıyla sonucu tedaviden önce görebilirsiniz."),
 [t("Discoloured, worn, chipped or uneven teeth", "Renk değişikliği, aşınma, kırık veya düzensiz dişler"), t("Gaps between teeth", "Diş araları açıklığı"), t("Healthy gums; gum treatment is completed first if needed", "Sağlıklı diş eti; gerekirse önce diş eti tedavisi yapılır")],
 [t("Send smile photos and, if available, a panoramic X-ray", "Gülüş fotoğraflarınızı ve varsa panoramik röntgeninizi gönderin"), t("Digital smile design, number of teeth and material are agreed", "Dijital gülüş tasarımı; diş sayısı ve materyal belirlenir"), t("Preparation, impressions and temporary teeth", "Hazırlık, ölçü ve geçici dişler"), t("Try-in and final fitting before you fly home", "Prova ve dönüş öncesi kalıcı yapıştırma")],
 [t("2–3 sessions", "2–3 seans"), t("Local if needed", "Gerekirse lokal"), t("Not required", "Gerekmez"), t("About 5–7 days", "Yaklaşık 5–7 gün"), t("Immediately", "Hemen")],
 f'<div class="mat"><div><b>{t("Porcelain / E-max", "Porselen / E-max")}</b><span>{t("Thin, translucent, very natural look", "İnce, ışık geçiren, çok doğal görünüm")}</span></div><div><b>{t("Zirconia", "Zirkonyum")}</b><span>{t("Very strong; suits heavier restorations", "Çok dayanıklı; geniş restorasyonlara uygun")}</span></div><div><b>{t("Laminate veneers", "Lamina veneer")}</b><span>{t("Minimal preparation of your own teeth", "Kendi dişlerinizden minimum aşındırma")}</span></div></div>')}
</section>''')

# ---------------- INTERNAL
S.append(f'''<section class="pg">{dept_banner("internal", t("Specialist opinions and long-term management of chronic conditions, without the need to travel for every step.", "Uzman görüşü ve kronik hastalıkların uzun dönem takibi; her adım için seyahat etmenize gerek kalmadan."), t("Internal medicine and endocrinology at:", "Dahiliye ve endokrinoloji bölümleri:"), chips(sorted(set(where("internal")) | set(where("endo")), key=list(HN).index)))}
{treatment("internal", "second", t("Second medical opinion", "2. hekim görüşü"), t("AI-supported", "Yapay zekâ destekli"),
 t("An independent specialist opinion on your diagnosis or treatment plan. Our AI-supported system organises your records into a structured summary; a specialist physician reviews it with your original files, and we send you a written report. Lengthy one-to-one appointments are not needed.", "Tanınız veya tedavi planınız hakkında bağımsız uzman görüşü. Yapay zekâ destekli sistemimiz kayıtlarınızı yapılandırılmış bir özete dönüştürür; uzman hekim bunu orijinal dosyalarınızla inceler ve size yazılı rapor iletiriz. Uzun birebir görüşmelere gerek kalmaz."),
 [t("A new or serious diagnosis (e.g. cancer, heart disease)", "Yeni veya ciddi bir tanı (ör. kanser, kalp hastalığı)"), t("A recommended operation you are unsure about", "Emin olmadığınız bir ameliyat önerisi"), t("Treatment that is not working as expected", "Beklendiği gibi sonuç vermeyen tedavi")],
 [t("Upload reports, imaging and lab results", "Rapor, görüntü ve tahlil sonuçlarınızı yükleyin"), t("AI-assisted summary and key questions", "Yapay zekâ destekli özet ve kritik sorular"), t("Specialist review and opinion", "Uzman incelemesi ve görüşü"), t("Written report; video call only if the physician considers it necessary", "Yazılı rapor; görüntülü görüşme yalnızca hekim gerekli görürse")],
 None,
 f'<p class="aiNote">{t("AI organises and prepares your file; every medical opinion is given by a specialist physician.", "Yapay zekâ dosyanızı düzenler ve hazırlar; her tıbbi görüşü uzman hekim verir.")}</p>')}
</section>''')
S.append(f'''<section class="pg">
{treatment("internal", "chronic", t("Chronic disease follow-up centre", "Kronik hastalık takip merkezi"), t("Long-term care, remotely", "Uzaktan, uzun dönem takip"),
 t("A structured follow-up programme for long-term conditions. Internal medicine and endocrinology specialists review your results at regular intervals, adjust your plan and send you clear reports, while you stay at home. It works alongside your GP in the UK, not instead of them.", "Uzun süreli hastalıklar için yapılandırılmış bir takip programı. Dahiliye ve endokrinoloji uzmanları sonuçlarınızı düzenli aralıklarla inceler, planınızı günceller ve size anlaşılır raporlar gönderir; siz evinizden ayrılmazsınız. İngiltere'deki aile hekiminizin yerine değil, onunla birlikte çalışır."),
 [t("Diabetes and insulin resistance", "Diyabet ve insülin direnci"), t("High blood pressure, heart disease, cholesterol", "Yüksek tansiyon, kalp hastalığı, kolesterol"), t("Thyroid, kidney and lung conditions (asthma / COPD)", "Tiroid, böbrek ve akciğer hastalıkları (astım / KOAH)")],
 [t("Enrolment with your history, medicines and recent tests", "Geçmişiniz, ilaçlarınız ve güncel tetkiklerinizle kayıt"), t("A personal follow-up calendar for tests and reviews", "Tahlil ve kontroller için kişisel takip takvimi"), t("Specialist review of each set of results, AI-supported tracking of trends", "Her sonuç setinin uzman tarafından incelenmesi; eğilimlerin yapay zekâ destekli izlenmesi"), t("Written reports; optional annual check-up in Türkiye", "Yazılı raporlar; isteğe bağlı yıllık check-up Türkiye'de")],
 None,
 f'''<div class="cal"><div><b>{t("Every 3 months", "3 ayda bir")}</b><span>{t("Results review (e.g. HbA1c, blood pressure log)", "Sonuç değerlendirmesi (ör. HbA1c, tansiyon takibi)")}</span></div><div><b>{t("Every 6 months", "6 ayda bir")}</b><span>{t("Medication and plan review", "İlaç ve plan değerlendirmesi")}</span></div><div><b>{t("Every year", "Yılda bir")}</b><span>{t("Comprehensive report; optional check-up in Türkiye", "Kapsamlı rapor; isteğe bağlı Türkiye'de check-up")}</span></div></div>
<p class="aiNote">{t("Example schedule; your specialist sets the intervals for your condition. In an emergency, always contact your local emergency services.", "Örnek takvimdir; aralıkları hastalığınıza göre uzmanınız belirler. Acil durumlarda her zaman bulunduğunuz yerdeki acil servise başvurun.")}</p>''')}
</section>''')

# ---------------- BACK
S.append(f'''<section class="back">
<img src="logo_white.png" class="bk-logo"/>
<h2>{t("Start with our patient form", "Hasta formumuzla başlayın")}</h2>
<p class="bk-sub">{t("Fill in the Patient Information &amp; Medical History Form (ECC-FR-HB-001) and send it to us with your documents. A personal consultant will get back to you with the next steps.", "Hasta Bilgi ve Anamnez Formu'nu (ECC-FR-HB-001) doldurup belgelerinizle birlikte bize gönderin. Kişisel danışmanınız sonraki adımlarla size dönüş yapacaktır.")}</p>
<div class="bk-info">
  <div>{ic("clock", 22, "#FFFFFF")}<b>{t("7 days a week", "Haftanın 7 günü")}</b><span>08:30 – 21:00 (GMT+3)</span></div>
  <div>{ic("globe", 22, "#FFFFFF")}<b>{t("Website", "Web sitesi")}</b><a href="http://www.easycliniccenter.com/">www.easycliniccenter.com</a></div>
  <div>{ic("home", 22, "#FFFFFF")}<b>{t("Head office", "Merkez ofis")}</b><span>İstanbul / TÜRKİYE</span></div>
</div>
<p class="bk-legal">{t("This brochure is for general information and does not replace a medical consultation. Durations are typical and vary; suitability, treatment plan and price are confirmed individually after medical review. Illustrations are schematic.", "Bu broşür genel bilgilendirme amaçlıdır ve hekim muayenesinin yerine geçmez. Süreler tipik değerlerdir ve değişebilir; uygunluk, tedavi planı ve fiyat tıbbi değerlendirme sonrasında kişiye özel netleştirilir. Görseller şematiktir.")}</p>
</section>''')

CSS = r'''
@page { size: A4; margin: 16mm 24mm 16mm 16mm; background: url(pagebg.png) no-repeat; background-size: 210mm 297mm;
  @bottom-left { content: "EASY CLINIC CENTER"; font-family: Inter; font-size: 6.5pt; letter-spacing: 2.5px; color: #9AAAB8; }
  @bottom-right { content: counter(page, decimal-leading-zero); font-family: Inter; font-size: 7pt; font-weight: 700; color: #22AFC4; } }
@page full { margin: 0; background: none; @bottom-left { content: none } @bottom-right { content: none } }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter; color: #33475A; font-size: 8.9pt; line-height: 1.5; }
.pg { page-break-before: always; }
.cover, .back { page: full; width: 210mm; height: 297mm; position: relative; overflow: hidden; }
.eyebrow { font-size: 7.6pt; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #22AFC4; margin: 0 0 2mm; }
h1, h2 { font-family: Lora; font-weight: 500; color: #24507A; margin: 0; line-height: 1.1; }
h1 em, h2 em { font-style: italic; color: #22AFC4; }
.big { font-size: 26pt; margin-bottom: 4mm; }
.intro { font-size: 10pt; color: #4F6475; margin: 0 0 5mm; }
.ck { list-style: none; padding: 0; margin: 0; }
.ck li { display: flex; gap: 1.8mm; margin-bottom: 1.1mm; font-size: 8.5pt; }
.ck li .ic { flex: none; margin-top: .9mm; }
.ic { display: inline-block; }
.note { font-size: 7.2pt; color: #8495A4; margin: 2mm 0 0; }
.fn { font-size: 6.6pt; color: #8495A4; margin: -1.5mm 0 2.5mm; }
/* cover */
.cover { background: linear-gradient(180deg, #FFFFFF 0%, #F2FBFC 100%); padding: 18mm 18mm; }
.cover::before { content: ""; position: absolute; right: 0; top: 0; width: 9mm; height: 297mm; background: linear-gradient(180deg, #3DD5E6, #1EF2D6 60%, #3DD5E6); }
.cv-logo { width: 42mm; margin-bottom: 10mm; }
.cover h1 { font-size: 34pt; margin-bottom: 4mm; }
.cv-sub { font-size: 10.5pt; color: #4F6475; width: 140mm; margin: 0 0 8mm; }
.cv-grid { display: flex; flex-wrap: wrap; gap: 3mm; width: 174mm; margin-top: 4mm; }
.cv-grid div { width: 32.4mm; }
.cv-foot { position: absolute; left: 18mm; right: 27mm; bottom: 12mm; display: flex; justify-content: space-between; font-size: 8.5pt; color: #24507A; font-weight: 600; border-top: 1.5px solid #8DC63F; padding-top: 3.5mm; }
.cv-foot a { color: #22AFC4; text-decoration: none; }
/* overview */
.ovgrid { display: flex; flex-wrap: wrap; gap: 4mm; margin-bottom: 6mm; }
.ov { width: calc(50% - 2mm); display: flex; gap: 3.5mm; background: var(--bg); border-radius: 4mm; padding: 3.5mm; border-top: 3px solid var(--c1); }
.ov-ill { width: 30mm; flex: none; }
.ov h3 { font-family: Lora; font-size: 12pt; color: var(--c1); margin: 0 0 2mm; font-weight: 600; }
.steps4 { display: flex; gap: 3mm; }
.steps4 div { flex: 1; display: flex; gap: 2.5mm; align-items: center; border: 1px solid #DCEFF3; border-radius: 3mm; padding: 3mm; }
.steps4 b { flex: none; width: 8mm; height: 8mm; border-radius: 50%; background: #22AFC4; color: #fff; display: flex; align-items: center; justify-content: center; }
.steps4 span { font-size: 8.3pt; color: #24507A; font-weight: 600; }
/* department banner */
.db { background: linear-gradient(90deg, var(--c1), var(--c2)); color: #fff; border-radius: 4mm; padding: 5mm 6mm; margin-bottom: 3mm; }
.db .eb { margin: 0; font-size: 7pt; letter-spacing: 3px; text-transform: uppercase; font-weight: 700; opacity: .85; }
.db h2 { color: #fff; font-size: 22pt; margin: 1mm 0 1.5mm; }
.db p { margin: 0; font-size: 9pt; }
.avail { margin-bottom: 5mm; }
.avail p { margin: 0 0 1.5mm; font-size: 8pt; color: #24507A; }
.avail p .ic { vertical-align: -2px; }
.avail span { display: inline-block; font-size: 7.4pt; background: #F2F6F8; border-radius: 3mm; padding: .6mm 2.4mm; margin: 0 1.2mm 1.2mm 0; }
.avail span b { color: var(--c1); }
/* treatment */
.tr { border: 1px solid #DCEFF3; border-radius: 4mm; padding: 4.5mm; margin-bottom: 5mm; break-inside: avoid; border-left: 4px solid var(--c1); }
.tr-top { display: flex; gap: 5mm; }
.tr-ill { width: 62mm; flex: none; }
.tag { margin: 0; font-size: 7pt; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; color: var(--c1); }
.tr h3 { font-family: Lora; font-size: 16pt; color: #24507A; margin: .5mm 0 1.5mm; font-weight: 600; }
.tr-txt > p { margin: 0 0 2mm; font-size: 8.7pt; }
.tr h5 { margin: 0 0 1.2mm; font-size: 8pt; color: var(--c1); text-transform: uppercase; letter-spacing: .8px; }
.facts { display: flex; gap: 2mm; margin: 3.5mm 0 3mm; }
.facts div { flex: 1; background: var(--bg); border-radius: 2.5mm; padding: 2.2mm 2.6mm; }
.facts span { display: block; font-size: 6.6pt; color: #5E7385; text-transform: uppercase; letter-spacing: .5px; margin-top: .5mm; }
.facts b { display: block; font-size: 8pt; color: #24507A; line-height: 1.3; }
.facts .ic { stroke: var(--c1); }
.how ol { margin: 0; padding: 0; list-style: none; display: flex; gap: 2mm; counter-reset: s; }
.how li { flex: 1; counter-increment: s; font-size: 7.9pt; background: #FAFCFD; border: 1px solid #E3EEF2; border-radius: 2.5mm; padding: 2mm 2.5mm 2mm 2.5mm; }
.how li::before { content: counter(s); display: block; font-family: Lora; font-weight: 600; color: var(--c1); font-size: 11pt; line-height: 1; margin-bottom: .8mm; }
.mat, .cal { display: flex; gap: 2mm; margin-top: 3mm; }
.mat div, .cal div { flex: 1; border: 1.2px dashed var(--c1); border-radius: 2.5mm; padding: 2.2mm 2.6mm; }
.mat b, .cal b { display: block; font-size: 8.2pt; color: #24507A; }
.mat span, .cal span { font-size: 7.6pt; color: #5E7385; }
.aiNote { margin: 3mm 0 0; font-size: 7.8pt; background: var(--bg); border-radius: 2mm; padding: 2mm 3mm; color: #24507A; }
/* back */
.back { background: linear-gradient(160deg, #24507A 0%, #1E6C93 55%, #22AFC4 100%); color: #fff; padding: 40mm 24mm; page-break-before: always; }
.bk-logo { width: 58mm; margin-bottom: 24mm; }
.back h2 { color: #fff; font-size: 28pt; }
.bk-sub { font-size: 11pt; color: #D7F5F9; margin: 4mm 0 14mm; width: 150mm; }
.bk-info { display: flex; gap: 5mm; }
.bk-info div { flex: 1; background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.25); border-radius: 4mm; padding: 6mm 5mm; }
.bk-info b { display: block; margin: 3mm 0 1mm; font-size: 10.5pt; }
.bk-info span, .bk-info a { font-size: 9pt; color: #D7F5F9; text-decoration: none; }
.bk-legal { position: absolute; left: 24mm; right: 24mm; bottom: 16mm; font-size: 7.5pt; color: #BDE6EE; border-top: 1px solid rgba(255,255,255,.3); padding-top: 4mm; }
'''
title = t("Easy Clinic Center – Featured Treatments", "Easy Clinic Center – Öne Çıkan Tedavilerimiz")
html = f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{"".join(S)}</body></html>'
out = t("Easy_Clinic_Center_Treatments_EN.pdf", "Easy_Clinic_Center_Tedaviler_TR.pdf")
weasyprint.HTML(string=html, base_url="/home/claude/cat/").write_pdf(f"/home/claude/cat/{out}")
print(out)
