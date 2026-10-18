# Easy Clinic Center – Web Sitesi Proje Özeti

Bu klasör, Ekim 2026'da hazırlanan kataloglardaki tüm içerik, karar ve görselleri içerir. Yeni web sitesi bu bilgilerle yapılacaktır.

## 1. Kurum bilgileri
- **Kuruluş:** 01.10.2020, İstanbul
- **Çalışma saatleri:** Haftanın 7 günü, 08:30–21:00 (Türkiye saati, GMT+3)
- **Web:** www.easycliniccenter.com · Merkez ofis: İstanbul / TÜRKİYE
- **Hedef kitle:** İngiltere'den gelen hastalar (site dilleri: Türkçe + İngilizce)
- **Model:** Kişisel sağlık danışmanlığı. Hasta yurt dışından gelip tedavi olabilir veya uzaktan 2. hekim görüşü alabilir.
- **Eksik bilgiler (henüz verilmedi):** telefon, e-posta, WhatsApp numarası, adres.

## 2. Marka
- **Renkler:** Lacivert `#24507A` · Turkuaz `#22AFC4` / `#3DD5E6` · Aqua `#1EF2D6` · Yaprak yeşili `#8DC63F` (koyu `#6FA52B`)
- **Fontlar:** Başlıklar Lora (serif), metin Inter
- **Logo:** `brand/logo.png` (açık zemin), `brand/logo_white.png` (koyu zemin)
- **Görsel dil:** Sağ kenarda turkuaz-aqua dikey gradyan şerit, yuvarlatılmış kartlar, kurumsal renklerde özel çizim illüstrasyonlar (`illustrations/`).

## 3. Çalışma mantığı (sitenin ana akışı)
İngiltere'den başvuru → Sağlık probleminin detaylandırılması → Türkiye'den hastane bazında fiyat teklifi.
Teklif **iki aşamalıdır**:
- **Seçenek A – Her şey dahil:** tedavi + uçak + konaklama + transfer
- **Seçenek B – Sadece tedavi:** gerisi opsiyonel

İzometrik şema: `illustrations/process_isometric_tr.svg` / `_en.svg`

## 4. Hizmetler
1. Kişisel sağlık danışmanlığı (tek danışman, ilk değerlendirme ücretsiz)
2. Türkiye'de tedavi
3. **2. hekim görüşü:** Kayıtlar yüklenir → ekip dosyayı düzenler → uzman hekim değerlendirir → yazılı rapor. Uzun birebir görüşme yapılmaz; canlı görüşme yalnızca hekim gerekli görürse yapılır. (Web sitesinde yapay zekâ ifadesi kaldırıldı; görüşü lisanslı uzman hekim verir. PDF kataloglar henüz eski "yapay zekâ destekli" metni içeriyor.)
4. Plastik, rekonstrüktif ve estetik cerrahi (vurgulanacak branş)
5. Opsiyonel: uçak, konaklama, transfer, koordinasyon/dil desteği, tedavi sonrası takip

## 5. Öne çıkan tedaviler (tedavi sayfaları)
Kullanıcı kararı: **Tedavi sayfalarında hastane reklamı yapılmayacak, yalnızca tedavi bilgisi verilecek.** Başlık "Öne çıkan tedavilerimiz" (diğer branşlar için danışın).
- **Plastik ve Estetik Cerrahi:** Meme implantı · Liposuction · Burun estetiği
- **Genel Cerrahi:** Obezite cerrahisi · Kanser cerrahisi · Tiroid cerrahisi
- **Diş:** İmplant tedavisi · Hollywood gülüşü
- **Dahili Branşlar:** 2. hekim görüşü · Kronik hastalık takip merkezi

Her tedavi için: ne olduğu, kimler için, işlem süresi, anestezi, hastanede kalış, Türkiye'de kalış, günlük hayata dönüş, 4 adımlık süreç. Tüm metinler `pdf/Easy_Clinic_Center_Tedaviler_TR.pdf` ve `_EN.pdf` içinde. Süreler tipik değerlerdir; hekimlere teyit ettirilmeli.

## 6. Partner hastaneler (14 kurum, 4 şehir)
- **İstanbul:** Memorial Şişli · Acıbadem Maslak · Medicana International İstanbul (Beylikdüzü)
- **Ankara:** Memorial Ankara · Medicana International Ankara · Acıbadem Ankara · Ufuk Üniversitesi Dr. Rıdvan Ege · Güven (Ayrancı + Çayyolu) · TOBB ETÜ
- **İzmir:** Acıbadem İzmir Kent · Medicana International İzmir · Medicana Çeşme **Tıp Merkezi** (hastane değil)
- **Antalya:** Memorial Antalya · Medstar Antalya

Plastik cerrahi bölümü: Medicana Çeşme hariç tümünde var.
Hekim verisi: `data/hekimler_doctors.csv` (**1.679 hekim**, hastanelerin resmi sitelerinden 12.10.2026'da derlendi; kadrolar değişebilir, sitede güncelleme tarihi ve "listede yer almak kişisel anlaşma anlamına gelmez" notu kalmalı).

## 7. Hasta formu
- Doküman no: **ECC-FR-HB-001** (EN: ECC-FR-HB-001-EN) · Rev. 00 · Yayın tarihi 12.10.2026
- 7 bölüm: kişisel bilgiler, talep, anamnez, cerrahi/plastik, belgeler, teklif ve seyahat tercihleri, beyan ve KVKK/UK GDPR açık rıza.
- **Fotoğraf kuralı: yüz görünmeyecek** (kişisel verilerin korunması). Yüze yönelik işlemlerde yüz fotoğrafları ayrı ve güvenli bir kanaldan, yalnızca onayla alınır.
- Sitede bu form online başvuru formuna dönüştürülecek (fotoğraf yükleme alanıyla birlikte).

## 8. Uyum notları
- Vize: İngiliz vatandaşları turistik ve iş seyahatlerinde 180 günde 90 güne kadar vizesiz (gov.uk). Tıbbi amaçlı giriş için Türkiye'nin Londra Büyükelçiliği'ne danışılmalı. Pasaport en az 150 gün geçerli olmalı.
- Sağlık verisi: KVKK + UK GDPR açık rıza metni hukukçuya kontrol ettirilmeli.
- Tıbbi bilgiler "hekim muayenesinin yerine geçmez" uyarısıyla verilmeli.

## 9. Önerilen site haritası (TR / EN)
Ana sayfa · Hakkımızda · Nasıl çalışır (izometrik akış + iki aşamalı teklif) · Öne çıkan tedaviler (10 tedavi sayfası) · 2. hekim görüşü · Kronik hastalık takip merkezi · Partner hastaneler ve hekim rehberi · İngiltere'den gelen hastalar için seyahat rehberi · SSS · Online başvuru formu · İletişim

## 10. Klasör içeriği
- `pdf/` – 8 PDF: kurumsal katalog, detay katalog, tedavi broşürü, hasta formu (her biri TR + EN)
- `brand/` – logolar
- `illustrations/` – 10 tedavi illüstrasyonu + izometrik süreç şeması (SVG, siteye doğrudan konabilir)
- `data/` – hekim listesi (CSV) ve PDF'leri üreten kaynak dosyalar (tüm TR/EN metinler bunların içinde)

## 11. Güncel site yapısı (18.10.2026)
- Ana odak: **ilk kez gönderene ücretsiz 2. hekim görüşü** (hero + tek adımlı başvuru formu: ad, e-posta/WhatsApp, talep, onay).
- Form şimdilik sunucusuz: özet kopyalanır/indirilir. `data/config.py` içindeki `CONTACT_EMAIL` doldurulunca "e-postayla gönder" düğmesi açılır.
- Blog (İngilizce, `blog/*.md`): `/blog/` + yazı sayfaları, RSS (`/blog/feed.xml`), sitemap, Article/Breadcrumb JSON-LD.
- Derleme: `python3 data/build_site.py` (eski `build_web.py` kaldırıldı).
