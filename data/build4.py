"""Easy Clinic Center – fillable patient information & medical history form (EN/TR). Usage: python3 build4.py en|tr"""
import sys, weasyprint, itertools

LANG = sys.argv[1]
TR = LANG == "tr"
def t(en, tr):
    return tr if TR else en

DOC_NO = "ECC-FR-HB-001" + ("" if TR else "-EN")
REV = "00"
DATE = "12.10.2026"
_id = itertools.count(1)

def fid(prefix):
    return f"{prefix}_{next(_id):03d}"

def field(label, w="100%", req=False, hint="", name=None):
    n = name or fid("f")
    star = '<b class="req">*</b>' if req else ""
    h = f'<span class="hint">{hint}</span>' if hint else ""
    return f'<div class="fld" style="width:{w}"><label>{label}{star}{h}</label><input type="text" name="{n}"/></div>'

def area(label, h="16mm", req=False, hint=""):
    star = '<b class="req">*</b>' if req else ""
    hh = f'<span class="hint">{hint}</span>' if hint else ""
    return f'<div class="fld" style="width:100%"><label>{label}{star}{hh}</label><textarea name="{fid("t")}" style="height:{h}"></textarea></div>'

def checks(label, options, cols=3, other=False, req=False):
    star = '<b class="req">*</b>' if req else ""
    items = "".join(f'<span class="cb"><input type="checkbox" name="{fid("c")}"/>{o}</span>' for o in options)
    oth = f'<span class="cb oth"><input type="checkbox" name="{fid("c")}"/>{t("Other:", "Diğer:")} <input type="text" class="inl" name="{fid("f")}"/></span>' if other else ""
    lab = f"<label>{label}{star}</label>" if label else ""
    return f'<div class="grp">{lab}<div class="cbs c{cols}">{items}{oth}</div></div>'

def yesno(q, detail=True, dlabel=None):
    d = f'<input type="text" class="inl wide" name="{fid("f")}" />' if detail else ""
    dl = f'<span class="dl">{dlabel or t("If yes, details:", "Evet ise açıklayınız:")}</span>' if detail else ""
    return f'''<div class="yn"><span class="q">{q}</span><span class="opts"><span class="cb"><input type="checkbox" name="{fid("c")}"/>{t("No", "Hayır")}</span><span class="cb"><input type="checkbox" name="{fid("c")}"/>{t("Yes", "Evet")}</span></span>{dl}{d}</div>'''

def row(*items):
    return '<div class="row">' + "".join(items) + "</div>"

def sec(num, title_, sub, body, cls=""):
    return f'<section class="sec {cls}"><div class="sh"><span class="sn">{num}</span><div><h2>{title_}</h2>{f"<p>{sub}</p>" if sub else ""}</div></div><div class="sb">{body}</div></section>'

P = []

# ------------------------------------------------------------------ intro
P.append(f'''
<div class="hero">
 <div>
  <h1>{t("Patient Information &amp; Medical History Form", "Hasta Bilgi ve Anamnez Formu")}</h1>
  <p class="lead">{t("Thank you for contacting Easy Clinic Center. The information you give here allows us and our partner hospitals to understand your situation and prepare an accurate, hospital-based quote for you.", "Easy Clinic Center'a ulaştığınız için teşekkür ederiz. Bu formdaki bilgiler, durumunuzu bizim ve partner hastanelerimizin doğru anlamasını ve size eksiksiz, hastane bazlı bir fiyat teklifi hazırlanmasını sağlar.")}</p>
 </div>
 <div class="how">
  <p><b>{t("About 10–15 minutes", "Yaklaşık 10–15 dakika")}</b></p>
  <ul>
   <li>{t("Fields marked <b class='req'>*</b> are required.", "<b class='req'>*</b> işaretli alanlar zorunludur.")}</li>
   <li>{t("If you are not sure, leave it blank. We will ask.", "Emin değilseniz boş bırakın, biz sorarız.")}</li>
   <li>{t("Section 4 is only for surgical / plastic surgery requests.", "4. bölüm yalnızca cerrahi / plastik cerrahi talepleri içindir.")}</li>
   <li>{t("Fill in on screen and save, or print and scan.", "Ekranda doldurup kaydedebilir ya da yazdırıp tarayabilirsiniz.")}</li>
  </ul>
 </div>
</div>''')

# ------------------------------------------------------------------ 1 personal
P.append(sec("1", t("Personal &amp; contact details", "Kişisel ve iletişim bilgileri"), "",
  row(field(t("First name", "Adı"), "33%", True), field(t("Surname", "Soyadı"), "33%", True), field(t("Date of birth (DD/MM/YYYY)", "Doğum tarihi (GG/AA/YYYY)"), "34%", True)) +
  row(checks(t("Sex", "Cinsiyet"), [t("Female", "Kadın"), t("Male", "Erkek"), t("Prefer not to say", "Belirtmek istemiyorum")], 3, req=True)) +
  row(field(t("Nationality", "Uyruk"), "33%"), field(t("Country of residence", "Yaşadığınız ülke"), "33%", True), field(t("City", "Şehir"), "34%")) +
  row(field(t("Mobile phone (with country code)", "Cep telefonu (ülke koduyla)"), "50%", True), field(t("E-mail", "E-posta"), "50%", True)) +
  row(checks(t("Preferred contact", "Tercih ettiğiniz iletişim"), ["WhatsApp", t("Phone call", "Telefon"), "E-mail"], 3),
      checks(t("Best time to call (UK time)", "Aranmak için uygun saat (İngiltere saati)"), [t("Morning", "Sabah"), t("Afternoon", "Öğleden sonra"), t("Evening", "Akşam")], 3)) +
  row(field(t("Language(s) you speak", "Konuştuğunuz dil(ler)"), "50%"), field(t("How did you hear about us?", "Bizi nereden duydunuz?"), "50%")) +
  row(field(t("Is someone filling this form for you? Name &amp; relationship", "Formu sizin adınıza biri mi dolduruyor? Ad ve yakınlık"), "100%"))
))

# ------------------------------------------------------------------ 2 request
P.append(sec("2", t("Your request", "Talebiniz"), t("Tell us in your own words what is wrong and what you would like.", "Sorununuzu ve beklentinizi kendi cümlelerinizle anlatın."),
  checks(t("What do you need?", "Neye ihtiyacınız var?"), [t("Treatment in Türkiye", "Türkiye'de tedavi"), t("AI-supported second opinion", "Yapay zekâ destekli ikinci görüş"), t("Plastic / aesthetic surgery", "Plastik / estetik cerrahi"), t("Check-up", "Check-up"), t("Not sure yet, I need advice", "Henüz emin değilim, yönlendirme istiyorum")], 3, True, True) +
  checks(t("Which area is it about?", "Hangi alanla ilgili?"), [t("Cancer / oncology", "Kanser / onkoloji"), t("Heart &amp; vessels", "Kalp ve damar"), t("Bones, joints, spine", "Kemik, eklem, omurga"), t("Brain &amp; nerves", "Beyin ve sinir"), t("Women's health / IVF", "Kadın sağlığı / tüp bebek"), t("Digestive system / weight loss", "Sindirim sistemi / obezite"), t("Eyes / ENT", "Göz / KBB"), t("Kidney, urology", "Böbrek, üroloji"), t("Plastic &amp; aesthetic", "Plastik ve estetik"), t("Dental", "Diş"), t("Organ transplant", "Organ nakli")], 3, True) +
  area(t("Describe your main complaint or problem", "Ana şikâyetinizi / sorununuzu anlatın"), "26mm", True, t(" What do you feel, where, how does it affect your daily life?", " Ne hissediyorsunuz, nerede, günlük hayatınızı nasıl etkiliyor?")) +
  row(field(t("Since when?", "Ne zamandan beri?"), "33%", True), checks(t("Is it getting", "Durumunuz"), [t("worse", "kötüleşiyor"), t("stable", "aynı"), t("better", "iyileşiyor")], 3)) +
  row(field(t("Diagnosis you have been given (if any)", "Size konulan tanı (varsa)"), "100%")) +
  area(t("Treatments you have had so far for this problem", "Bu sorun için şimdiye kadar aldığınız tedaviler"), "16mm") +
  area(t("What has your doctor recommended?", "Doktorunuz ne önerdi?"), "14mm") +
  area(t("What would you like from us? Your questions and expectations", "Bizden beklentiniz nedir? Sorularınız"), "16mm") +
  row(checks(t("How soon would you like treatment?", "Tedaviyi ne zaman düşünüyorsunuz?"), [t("As soon as possible", "En kısa sürede"), t("Within 1–3 months", "1–3 ay içinde"), t("3–6 months", "3–6 ay"), t("Just researching", "Sadece araştırıyorum")], 4)) +
  row(checks(t("Preferred city", "Tercih ettiğiniz şehir"), ["İstanbul", "Ankara", "İzmir", "Antalya", t("No preference", "Fark etmez")], 5)) +
  row(field(t("Preferred hospital or doctor (optional, see our catalogue)", "Tercih ettiğiniz hastane veya hekim (opsiyonel, kataloğumuza bakabilirsiniz)"), "100%"))
))

# ------------------------------------------------------------------ 3 medical history
P.append(sec("3", t("Medical history (anamnesis)", "Tıbbi geçmiş (anamnez)"), t("This helps the physician assess whether treatment is safe for you.", "Bu bilgiler, hekimin tedavinin sizin için güvenli olup olmadığını değerlendirmesine yardımcı olur."),
  row(field(t("Height (cm)", "Boy (cm)"), "25%", True), field(t("Weight (kg)", "Kilo (kg)"), "25%", True), field(t("Blood group (if known)", "Kan grubu (biliyorsanız)"), "25%"), field(t("Your GP / clinic in the UK", "İngiltere'deki aile hekiminiz"), "25%")) +
  checks(t("Do you have, or have you had, any of the following?", "Aşağıdakilerden herhangi biri sizde var mı / oldu mu?"), [t("Diabetes", "Diyabet"), t("High blood pressure", "Yüksek tansiyon"), t("Heart disease / arrhythmia", "Kalp hastalığı / ritim bozukluğu"), t("Stroke", "İnme (felç)"), t("Asthma / COPD", "Astım / KOAH"), t("Sleep apnoea", "Uyku apnesi"), t("Thyroid disease", "Tiroid hastalığı"), t("Kidney disease", "Böbrek hastalığı"), t("Liver disease / hepatitis", "Karaciğer hastalığı / hepatit"), t("Blood clot (DVT / embolism)", "Pıhtı (DVT / emboli)"), t("Bleeding disorder", "Kanama bozukluğu"), t("Epilepsy", "Epilepsi"), t("Cancer (now or past)", "Kanser (şu an / geçmişte)"), t("HIV", "HIV"), t("Depression / anxiety", "Depresyon / anksiyete"), t("Autoimmune disease", "Otoimmün hastalık"), t("None of these", "Hiçbiri")], 3, True) +
  area(t("Previous operations (what, when, any complications?)", "Geçirdiğiniz ameliyatlar (ne, ne zaman, komplikasyon oldu mu?)"), "16mm") +
  area(t("Medicines you take regularly (name and dose), including supplements", "Düzenli kullandığınız ilaçlar (ad ve doz), takviyeler dahil"), "16mm") +
  yesno(t("Do you take blood thinners (e.g. aspirin, warfarin, apixaban)?", "Kan sulandırıcı kullanıyor musunuz (aspirin, warfarin, apiksaban vb.)?"), True, t("Which one:", "Hangisi:")) +
  yesno(t("Do you have any allergies (medicines, latex, food)?", "Alerjiniz var mı (ilaç, lateks, gıda)?"), True, t("To what:", "Neye:")) +
  yesno(t("Have you ever had a problem with anaesthesia?", "Daha önce anesteziyle ilgili sorun yaşadınız mı?")) +
  checks(t("Smoking", "Sigara"), [t("Never", "Hiç içmedim"), t("I quit", "Bıraktım"), t("Yes, fewer than 10 a day", "Evet, günde 10'dan az"), t("Yes, 10 or more a day", "Evet, günde 10 ve üzeri"), t("E-cigarette / vape", "Elektronik sigara")], 3) +
  checks(t("Alcohol", "Alkol"), [t("Never", "Hiç"), t("Occasionally", "Ara sıra"), t("Regularly", "Düzenli")], 3) +
  yesno(t("For women: are you pregnant, breastfeeding or planning pregnancy?", "Kadınlar için: hamile misiniz, emziriyor musunuz veya hamilelik planınız var mı?"), False) +
  area(t("Illnesses in your family (parents, siblings) that we should know about", "Ailenizde (anne, baba, kardeş) bilmemiz gereken hastalıklar"), "12mm")
))

# ------------------------------------------------------------------ 4 surgical / plastic
P.append(sec("4", t("Surgical &amp; plastic surgery requests", "Cerrahi ve plastik cerrahi talepleri"), t("Only fill in this section if you are asking about an operation.", "Bu bölümü yalnızca bir ameliyat için başvuruyorsanız doldurun."),
  checks(t("Which procedure are you interested in?", "Hangi işlemle ilgileniyorsunuz?"), [t("Rhinoplasty", "Burun estetiği"), t("Face / neck lift", "Yüz / boyun germe"), t("Eyelid surgery", "Göz kapağı estetiği"), t("Breast augmentation", "Meme büyütme"), t("Breast reduction / lift", "Meme küçültme / dikleştirme"), t("Gynaecomastia", "Jinekomasti"), t("Liposuction", "Liposuction"), t("Tummy tuck", "Karın germe"), t("Brazilian butt lift", "Brezilya popo kaldırma"), t("Mummy makeover", "Anne estetiği"), t("Reconstruction", "Rekonstrüksiyon"), t("Non-aesthetic surgery", "Estetik dışı ameliyat")], 3, other=True) +
  yesno(t("Have you had any previous surgery or aesthetic procedure in the same area?", "Aynı bölgeye daha önce ameliyat veya estetik işlem yapıldı mı?"), True, t("What and when:", "Ne ve ne zaman:")) +
  row(checks(t("Has your weight been stable for the last 6 months?", "Son 6 ayda kilonuz sabit mi?"), [t("Yes", "Evet"), t("No, I lost weight", "Hayır, kilo verdim"), t("No, I gained weight", "Hayır, kilo aldım")], 3)) +
  area(t("What result would you like? What bothers you about this area?", "Nasıl bir sonuç istiyorsunuz? Bu bölgede sizi rahatsız eden ne?"), "16mm") +
  f'''<div class="photo">
   <div class="ph-h"><b>{t("Photos", "Fotoğraflar")}</b><span>{t("For plastic surgery and other operations, the surgeon needs photos of the area to prepare your quote.", "Plastik cerrahi ve diğer ameliyatlarda, teklif hazırlanabilmesi için cerrahın ilgili bölgenin fotoğraflarını görmesi gerekir.")}</span></div>
   <div class="nf">
     <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#C0392B" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="9" r="4.5"/><path d="M4 21c1.2-4.5 14.8-4.5 16 0"/><path d="M3 3l18 18"/></svg>
     <div><b>{t("PLEASE DO NOT SHOW YOUR FACE IN THE PHOTOS", "LÜTFEN FOTOĞRAFLARDA YÜZÜNÜZ GÖRÜNMESİN")}</b>
     <p>{t("To protect your personal data, crop or frame the photos so that your face, and any other identifying features such as tattoos or jewellery, cannot be seen. Only the area to be treated should be visible.", "Kişisel verilerinizin korunması için fotoğrafları yüzünüz ve dövme, takı gibi sizi tanıtabilecek başka detaylar görünmeyecek şekilde çekin veya kırpın. Yalnızca tedavi edilecek bölge görünmelidir.")}</p>
     <p class="face">{t("<b>Facial procedures</b> (e.g. rhinoplasty, eyelid, face lift): do not send face photos with this form. Your consultant will arrange a separate, secure way to share them, only if you agree.", "<b>Yüze yönelik işlemler</b> (burun, göz kapağı, yüz germe vb.): yüz fotoğraflarını bu formla göndermeyin. Danışmanınız, yalnızca onay vermeniz hâlinde, bunlar için ayrı ve güvenli bir paylaşım yolu ayarlayacaktır.")}</p></div>
   </div>
   <div class="ph-tips">
     <div><b>{t("Angles", "Açılar")}</b><p>{t("Front, right side, left side, both 45° angles, and back if relevant.", "Önden, sağ yandan, sol yandan, iki tarafta 45° ve gerekiyorsa arkadan.")}</p></div>
     <div><b>{t("Light &amp; background", "Işık ve arka plan")}</b><p>{t("Daylight or bright room, plain wall behind you, no filters.", "Gün ışığı veya aydınlık oda, düz duvar önünde, filtresiz.")}</p></div>
     <div><b>{t("Clothing", "Kıyafet")}</b><p>{t("Plain underwear so the area is clearly visible.", "Bölge net görünecek şekilde sade iç çamaşırı.")}</p></div>
     <div><b>{t("How to send", "Nasıl gönderilir")}</b><p>{t("By e-mail or WhatsApp to your consultant, with your name in the message.", "E-posta veya WhatsApp ile danışmanınıza, mesajda adınızı belirterek.")}</p></div>
   </div>
  </div>''' +
  row(checks(t("Photos", "Fotoğraflar"), [t("I will send photos without my face", "Yüzüm görünmeden fotoğraf göndereceğim"), t("I would prefer to discuss this first", "Önce görüşmek istiyorum")], 2))
, "s4"))

# ------------------------------------------------------------------ 5 documents
P.append(sec("5", t("Your medical documents", "Tıbbi belgeleriniz"), t("Please send copies to your consultant. You do not need to send originals.", "Kopyalarını danışmanınıza gönderin; asıllarına gerek yoktur."),
  checks(t("Which documents do you have?", "Hangi belgeleriniz var?"), [t("Doctor's / specialist letters", "Doktor / uzman yazıları"), t("Discharge summary", "Epikriz"), t("MRI / CT / X-ray images (CD or DICOM)", "MR / BT / röntgen görüntüleri (CD veya DICOM)"), t("Radiology reports", "Radyoloji raporları"), t("Pathology / biopsy reports", "Patoloji / biyopsi raporları"), t("Recent blood tests", "Güncel kan tahlilleri"), t("ECG / echocardiography", "EKG / ekokardiyografi"), t("None yet", "Henüz yok")], 3)
))

# ------------------------------------------------------------------ 6 quote & travel
P.append(sec("6", t("Your quote &amp; travel preferences", "Teklif ve seyahat tercihleriniz"), t("We prepare a quote for each suitable hospital, in two forms.", "Uygun her hastane için iki şekilde teklif hazırlarız."),
  checks(t("Which quote would you like?", "Nasıl bir teklif istersiniz?"), [t("<b>Option A</b> – All-inclusive: treatment + flights + accommodation + transfers", "<b>Seçenek A</b> – Her şey dahil: tedavi + uçak + konaklama + transfer"), t("<b>Option B</b> – Treatment only; I will arrange my own travel", "<b>Seçenek B</b> – Sadece tedavi; seyahatimi kendim ayarlayacağım"), t("Please send both", "İkisini de gönderin")], 1, req=True) +
  row(field(t("Departure airport", "Kalkış havalimanı"), "33%"), field(t("Preferred travel dates", "Tercih ettiğiniz tarihler"), "33%"), field(t("Number of companions", "Refakatçi sayısı"), "34%")) +
  row(checks(t("Accommodation", "Konaklama"), [t("Standard", "Standart"), t("Comfort", "Konforlu"), t("Premium", "Premium")], 3), checks(t("Budget is", "Bütçe"), [t("Very important", "Çok önemli"), t("Important", "Önemli"), t("Not decisive", "Belirleyici değil")], 3)) +
  row(field(t("Special needs (wheelchair, diet, other)", "Özel ihtiyaçlar (tekerlekli sandalye, diyet, diğer)"), "60%"), field(t("Health / travel insurance (if any)", "Sağlık / seyahat sigortası (varsa)"), "40%"))
))

# ------------------------------------------------------------------ 7 consent
P.append(sec("7", t("Declaration &amp; consent", "Beyan ve onay"), "",
  f'''<div class="cons">
  <p class="cb2"><input type="checkbox" name="{fid("c")}"/><span>{t("I confirm that the information I have given is true and complete to the best of my knowledge. I understand that this form does not replace a medical examination and that any quote is confirmed only after the physician has assessed me.", "Verdiğim bilgilerin bildiğim kadarıyla doğru ve eksiksiz olduğunu beyan ederim. Bu formun hekim muayenesinin yerine geçmediğini ve fiyat teklifinin ancak hekim değerlendirmesinden sonra kesinleşeceğini anlıyorum.")} <b class="req">*</b></span></p>
  <p class="cb2"><input type="checkbox" name="{fid("c")}"/><span>{t("I give my explicit consent for Easy Clinic Center to process my personal and health data, including any photos I send, and to share them with partner hospitals and physicians only for the purpose of assessing my case and preparing a quote, in line with UK GDPR and Turkish data protection law (KVKK). I can withdraw this consent at any time.", "Kişisel ve sağlık verilerimin, göndereceğim fotoğraflar dahil, yalnızca vakamın değerlendirilmesi ve fiyat teklifi hazırlanması amacıyla Easy Clinic Center tarafından işlenmesine ve partner hastane ve hekimlerle paylaşılmasına, İngiltere GDPR ve Kişisel Verilerin Korunması Kanunu (KVKK) kapsamında açık rıza veriyorum. Bu rızamı istediğim zaman geri alabilirim.")} <b class="req">*</b></span></p>
  <p class="cb2"><input type="checkbox" name="{fid("c")}"/><span>{t("I agree to be contacted by Easy Clinic Center by phone, WhatsApp or e-mail about my request.", "Talebimle ilgili olarak Easy Clinic Center tarafından telefon, WhatsApp veya e-posta ile iletişime geçilmesini kabul ediyorum.")}</span></p>
  </div>''' +
  row(field(t("Full name", "Ad soyad"), "40%", True), field(t("Date", "Tarih"), "25%", True), field(t("Signature (type your name if filling in on screen)", "İmza (ekranda dolduruyorsanız adınızı yazın)"), "35%"))
))

# ------------------------------------------------------------------ office use
P.append(f'''<div class="office"><p class="ot">{t("FOR OFFICE USE ONLY", "YALNIZCA KURUM İÇİ KULLANIM İÇİNDİR")}</p>
<div class="row">{field(t("Case no.", "Vaka no"), "20%")}{field(t("Received", "Alınış tarihi"), "20%")}{field(t("Consultant", "Danışman"), "20%")}{field(t("Specialty / hospitals", "Branş / hastaneler"), "40%")}</div>
<div class="row">{checks("", [t("Documents complete", "Belgeler tamam"), t("Photos received (no face)", "Fotoğraflar alındı (yüzsüz)"), t("Sent to hospitals", "Hastanelere gönderildi"), t("Quote sent", "Teklif gönderildi")], 4)}</div></div>''')

LOGO = '<img src="logo.png" style="height:15mm"/>'
CSS = r'''
@page { size: A4; margin: 30mm 16mm 18mm 16mm;
  @top-left { content: element(hdr); }
  @top-right { content: element(dc); }
  @bottom-left { content: "''' + t("This form does not replace a medical examination. Please keep a copy for your records.", "Bu form hekim muayenesinin yerine geçmez. Lütfen bir kopyasını saklayınız.") + r'''"; font-family: Inter; font-size: 6.5pt; color: #8495A4; }
  @bottom-right { content: "''' + DOC_NO + r''' · Rev. ''' + REV + r''' · ''' + t("Page ", "Sayfa ") + r'''" counter(page) " / " counter(pages); font-family: Inter; font-size: 6.5pt; color: #22AFC4; font-weight: 700; }
}
* { box-sizing: border-box; }
body { font-family: Inter; color: #33475A; font-size: 8.6pt; line-height: 1.4; margin: 0; }
.hdr { position: running(hdr); display: flex; align-items: center; gap: 4mm; }
.hdr .tt { border-left: 1.5px solid #8DC63F; padding-left: 4mm; }
.hdr .tt b { display: block; font-family: Lora; font-size: 11.5pt; color: #24507A; font-weight: 600; }
.hdr .tt span { font-size: 7pt; color: #22AFC4; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; }
.dc { position: running(dc); }
.dc table { border-collapse: collapse; font-size: 6.6pt; }
.dc td { border: 1px solid #BFEAF0; padding: .7mm 2mm; }
.dc td:first-child { color: #8495A4; background: #F2FBFC; }
.dc td:last-child { color: #24507A; font-weight: 700; }
h1 { font-family: Lora; font-weight: 500; color: #24507A; font-size: 20pt; margin: 0 0 2mm; line-height: 1.15; }
.hero { display: flex; gap: 6mm; margin-bottom: 5mm; }
.hero > div:first-child { flex: 1.35; }
.lead { margin: 0; font-size: 9.2pt; color: #4F6475; }
.how { flex: 1; background: #F2FBFC; border-radius: 3mm; padding: 3.5mm 4mm; border-left: 3px solid #22AFC4; }
.how p { margin: 0 0 1.5mm; color: #24507A; }
.how ul { margin: 0; padding-left: 4mm; font-size: 8pt; }
.req { color: #D35454; font-weight: 700; margin-left: .6mm; }
.sec { margin-bottom: 5mm; break-inside: auto; }
.sh { display: flex; gap: 3mm; align-items: center; background: linear-gradient(90deg, #24507A, #22AFC4); color: #fff; border-radius: 2.5mm; padding: 2.2mm 4mm; margin-bottom: 3mm; break-after: avoid; }
.sn { width: 7.5mm; height: 7.5mm; border-radius: 50%; background: #fff; color: #24507A; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 10pt; flex: none; }
.sh h2 { margin: 0; font-size: 11pt; font-weight: 700; }
.sh p { margin: 0; font-size: 7.6pt; color: #D7F5F9; }
.sec.s4 .sh { background: linear-gradient(90deg, #6FA52B, #8DC63F); }
.sec.s4 .sn { color: #6FA52B; }
.row { display: flex; gap: 3mm; break-inside: avoid; }
.fld { margin-bottom: 2.6mm; break-inside: avoid; }
.fld label, .grp > label { display: block; font-size: 7.4pt; font-weight: 600; color: #24507A; margin-bottom: .8mm; }
.hint { font-weight: 400; color: #8495A4; }
input[type=text], textarea { width: 100%; height: 6.4mm; border: 1px solid #BFD9E2; border-radius: 1.4mm; background: #FBFEFF; font-family: Inter; font-size: 8.5pt; }
textarea { display: block; }
.grp { margin-bottom: 2.6mm; break-inside: avoid; flex: 1; }
.cbs { display: flex; flex-wrap: wrap; row-gap: 1.2mm; }
.cbs .cb { font-size: 8pt; display: inline-flex; align-items: center; gap: 1.5mm; }
.cbs.c1 .cb { width: 100%; } .cbs.c2 .cb { width: 50%; } .cbs.c3 .cb { width: 33.3%; } .cbs.c4 .cb { width: 25%; } .cbs.c5 .cb { width: 20%; }
.cbs .cb.oth { width: 100%; }
input[type=checkbox] { width: 3.4mm; height: 3.4mm; border: 1px solid #22AFC4; border-radius: .6mm; margin: 0; flex: none; }
input.inl { display: inline-block; height: 5mm; width: 60mm; }
input.inl.wide { flex: 1; width: auto; }
.yn { display: flex; align-items: center; gap: 3mm; margin-bottom: 2.4mm; flex-wrap: wrap; break-inside: avoid; }
.yn .q { flex: 0 0 76mm; font-size: 8pt; color: #24507A; font-weight: 600; }
.yn .opts { display: inline-flex; gap: 3mm; }
.yn .cb { display: inline-flex; align-items: center; gap: 1.2mm; font-size: 8pt; }
.yn .dl { font-size: 7.4pt; color: #8495A4; }
.yn input.inl.wide { min-width: 40mm; }
.photo { border: 1.5px solid #D5EBB8; border-radius: 3mm; padding: 3.5mm; margin: 1mm 0 3mm; background: #FBFDF7; break-inside: avoid; }
.ph-h b { display: block; color: #6FA52B; font-size: 9.5pt; }
.ph-h span { font-size: 8pt; }
.nf { display: flex; gap: 3mm; background: #FFF1F1; border: 1.5px solid #E8A0A0; border-radius: 2.5mm; padding: 3mm; margin: 2.5mm 0; }
.nf b { color: #B03A2E; font-size: 9pt; letter-spacing: .3px; }
.nf p { margin: 1mm 0 0; font-size: 7.8pt; }
.nf .face { background: #fff; border-radius: 1.5mm; padding: 1.5mm 2mm; }
.ph-tips { display: flex; gap: 2.5mm; }
.ph-tips div { flex: 1; background: #fff; border-radius: 2mm; padding: 2mm 2.5mm; border: 1px solid #E3EEDB; }
.ph-tips b { font-size: 7.6pt; color: #24507A; }
.ph-tips p { margin: .5mm 0 0; font-size: 7.2pt; }
.cons .cb2 { display: flex; gap: 2.5mm; margin: 0 0 2.5mm; font-size: 8pt; break-inside: avoid; }
.cons .cb2 input { margin-top: .6mm; }
.office { border: 1.5px dashed #9AAAB8; border-radius: 3mm; padding: 3mm 4mm 1mm; background: #F7F9FA; break-inside: avoid; }
.ot { margin: 0 0 2mm; font-size: 7pt; letter-spacing: 2px; font-weight: 700; color: #8495A4; }
'''
hdr = f'''<div class="hdr">{LOGO}<div class="tt"><span>{t("Patient form", "Hasta formu")}</span><b>{t("Patient Information &amp; Medical History", "Hasta Bilgi ve Anamnez Formu")}</b></div></div>
<div class="dc"><table>
<tr><td>{t("Document no.", "Doküman no")}</td><td>{DOC_NO}</td></tr>
<tr><td>{t("Issue date", "Yayın tarihi")}</td><td>{DATE}</td></tr>
<tr><td>{t("Revision no. / date", "Revizyon no / tarihi")}</td><td>{REV} / –</td></tr>
</table></div>'''
html = f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{t("Easy Clinic Center – Patient Information & Medical History Form", "Easy Clinic Center – Hasta Bilgi ve Anamnez Formu")}</title><style>{CSS}</style></head><body>{hdr}<form>{"".join(P)}</form></body></html>'
out = t("ECC_Patient_Information_Form_EN.pdf", "ECC_Hasta_Bilgi_ve_Anamnez_Formu_TR.pdf")
weasyprint.HTML(string=html, base_url="/home/claude/cat/").write_pdf(f"/home/claude/cat/{out}", pdf_forms=True)
print(out)
