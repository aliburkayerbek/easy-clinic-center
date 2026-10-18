# Easy Clinic Center

Website and print materials for Easy Clinic Center, a personal health consultancy in Türkiye (founded 2020).

- `site/` – static site, one page per language: `index.html` (EN, default), `fr/`, `ar/` (RTL), `ru/`; each has its own canonical + hreflang. Two-slide hero banner.
- `pdf/` – catalogues, treatments brochure and patient form (EN/TR)
- `brand/`, `illustrations/` – logos and SVG illustrations
- `data/` – doctor list (CSV) and the Python builders (`python3 data/build_site.py` regenerates all four language pages; needs Pillow)

## Editing the site
- Texts (EN/FR/AR/RU): `data/web_strings.py` and `data/site_strings.py` (the latter wins on duplicate keys).
- Settings: `data/config.py` - set `CONTACT_EMAIL` and the form result gets a "Send by e-mail" button; `SITE` is the final domain.
- Blog: add `blog/<slug>.md` with front matter (`title`, `description`, `date`, `tags`), then push; posts, index, RSS and sitemap are generated.
- Push to `main`: GitHub Actions rebuilds and publishes the site (`.github/workflows/pages.yml`).
