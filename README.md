# Easy Clinic Center

Website and print materials for Easy Clinic Center, a personal health consultancy in Türkiye (founded 2020).

- `site/` – static site, one page per language: `index.html` (EN, default), `fr/`, `ar/` (RTL), `ru/`; each has its own canonical + hreflang. Two-slide hero banner.
- `pdf/` – catalogues, treatments brochure and patient form (EN/TR)
- `brand/`, `illustrations/` – logos and SVG illustrations
- `data/` – doctor list (CSV) and the Python builders (`python3 data/build_web.py` regenerates all four language pages; needs Pillow)
