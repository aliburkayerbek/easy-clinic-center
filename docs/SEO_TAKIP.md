# Easy Clinic Center – SEO takip rehberi

## Nereden takip edeceksin

| Ne | Nerede | Ne zaman bak | Neye bak |
|---|---|---|---|
| Google'da görünürlük | Google Search Console → `https://www.easycliniccenter.com/` (search.google.com/search-console) | Haftada 1 | **Performans**: tıklama, gösterim, ortalama sıra, hangi sorgular. **Sayfalar / Dizin oluşturma**: kaç sayfa dizinde, hata var mı. **Site haritaları**: `sitemap.xml` "Başarılı" mı |
| Bing'de görünürlük | Bing Webmaster Tools (bing.com/webmasters) → `www.easycliniccenter.com` | 2 haftada 1 | Search Performance, Sitemaps, URL Inspection, Site Scan |
| Ziyaretçi davranışı | Google Analytics 4 (analytics.google.com) → mülk "Easy Clinic Center" (`G-23CYTMPX81`) | Haftada 1 | Raporlar → Edinme (trafik nereden geliyor), Etkileşim → Sayfalar, Gerçek zamanlı (test için) |
| Başvurular | `info@easycliniccenter.com` (https://mailmatik.com webmail) | Günlük | Konu: `Request ECC-… - …` |
| Yayın sağlığı | github.com/aliburkayerbek/easy-clinic-center → Actions | Yayın sonrası | Yeşil tik = site güncel |

Not: Analytics yalnızca çerez çubuğunda **Kabul** edenleri sayar; gerçek trafik rakamın üstünde olur. Search Console ve Bing çerezden bağımsız, gerçek arama verisini gösterir.

## İlk 3 ayda ne beklemeli
- **1–2. hafta:** Search Console'da sayfalar "Keşfedildi/Dizine eklendi" olmaya başlar; ilk gösterimler marka adıyla (Easy Clinic Center).
- **1–3. ay:** Blog yazıları uzun kuyruk sorgularda (ör. "second opinion before surgery") 30–100. sıralarda görünür; tıklama çok az.
- **3–12. ay:** İçerik ve geri bağlantı arttıkça sıra yükselir. Rekabetli sorgularda ("plastic surgery Turkey") ilk sayfa gerçekçi değil.
- Hızlandıranlar: düzenli yazı (haftada 1), geri bağlantı (rehber siteleri, forumlar, hastane/dernek sayfaları), Google İşletme Profili (uygunsa), gerçek hasta yorumları (izinle).

## Haftalık rutin (20 dakika)
1. Search Console → Performans → son 28 gün: en çok gösterim alan 10 sorguyu yaz.
2. Gösterimi yüksek ama tıklaması düşük sayfalar: başlık ve açıklamayı iyileştir.
3. Sorgu ile eşleşen yazı yoksa yeni yazı fikri olarak ekle.
4. Yeni yazı yayınladıysan: Search Console → URL denetimi → "Dizine eklenmesini iste".

## Yeni yazı nasıl eklenir
`blog/<kisa-baslik>.md` dosyası oluştur (başlık, açıklama, tarih, etiket + metin), `git push`. Siteyi, sitemap'i, RSS'i ve Bing/IndexNow bildirimini otomatik üretir.
Başlık ≤ 60 karakter, açıklama 120–160 karakter olsun. Denetim: `python3 data/seo_audit.py`.

## Yazı takvimi
İlk 10 konu yayınlandı (toplam 19 blog yazısı, 31 Ekim 2026). Hepsi UK hastası odaklı, İngilizce, temkinli yazıldı; fiyat yalnızca "30 $'dan başlar" olarak geçiyor.

Sıradaki fikirler (Search Console'daki gerçek sorgulara göre sırala):
1. `plastic-surgery-complications-what-to-know` – komplikasyon planı ve kime başvurulur
2. `liposuction-abroad-questions` – liposuction öncesi sorular
3. `cancer-diagnosis-second-opinion` – kanser tanısında ikinci görüş
4. `hair-and-skin-treatments-abroad-checklist` – saç/cilt işlemleri için dikkat edilecekler
5. `medical-records-translation-for-treatment-abroad` – belgelerin çevirisi
6. `after-a-second-opinion-what-next` – ikinci görüşten sonra ne yapılır
7. Kısa SSS yazıları: "Do I need a visa for treatment in Türkiye?", "How do I pay for treatment abroad?"

Her yazıdan sonra: `python3 data/seo_audit.py`, `git push`, haftalık rutinle sorgu takibi.

## Teknik SEO durumu (kontrol listesi)
- [x] Her dil için ayrı sayfa, `hreflang`, `canonical`
- [x] `sitemap.xml` (16 sayfa), `robots.txt`, RSS (`/blog/feed.xml`)
- [x] Yapılandırılmış veri: Organization, WebSite, Service/Offer, FAQPage, BlogPosting, BreadcrumbList
- [x] Search Console + Bing Webmaster doğrulandı, site haritası gönderildi
- [x] IndexNow (yeni/değişen sayfalar otomatik bildirilir)
- [x] Mobil uyumlu, HTTPS, hızlı (statik sayfa)
- [ ] Yazı tiplerini kendi sunucuna almak (hız + gizlilik)
- [ ] FR/AR/RU blog çevirileri (şu an blog yalnızca İngilizce)
- [ ] Geri bağlantı çalışması
