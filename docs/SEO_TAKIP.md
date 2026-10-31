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

## Yazı takvimi (sıradaki 10 konu)
Hepsi UK hastası odaklı, İngilizce, temkinli ve kaynaklı yazılmalı (sağlık içeriği). Fiyat yalnızca "30 $'dan başlar" olarak geçsin.

1. `second-opinion-vs-nhs-referral` – NHS yönlendirmesi ile online ikinci görüş farkı
2. `what-to-expect-second-opinion-report` – Yazılı raporda neler bulunur
3. `rhinoplasty-recovery-flying-home` – Burun estetiği sonrası eve uçuş ve iyileşme zamanı
4. `breast-surgery-abroad-questions` – Meme ameliyatı için sorulacak sorular
5. `bariatric-surgery-abroad-checklist` – Obezite cerrahisi öncesi kontrol listesi
6. `thyroid-surgery-second-opinion` – Tiroid ameliyatı öncesi ikinci görüş
7. `dental-implant-aftercare-abroad` – İmplant sonrası bakım ve takip
8. `medical-travel-insurance-uk` – Tedavi için seyahat sigortası
9. `how-to-read-a-hospital-quote` – Hastane teklifini okumak (A/B seçenek)
10. `istanbul-hospitals-international-patients` – İstanbul'da uluslararası hasta hizmeti nasıl işler

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
