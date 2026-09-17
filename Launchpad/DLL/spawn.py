#!/usr/bin/env python3
"""Brand Launchpad generator — HARD LAW 17/09/2026 (Rob).

Concept faces (Duron / Ironbark / Tusk / C3N6) skin colour, type and voice ONLY.
Product titles MUST start with Superware (melamine) or Polysafe (polycarbonate).
Seller: Hospitality Products (Yatala) via this specialist storefront.
NEVER emit fake PL titles like "Duron Dinner Plate".
"""
from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from html import escape
from pathlib import Path

DLL = Path(__file__).resolve().parent
ROOT = DLL.parents[1]
SITES = ROOT / "Sites"
STORES = SITES / "stores"
CATALOGUE = DLL / "catalogue.unbreakable.json"

CATCHLINE = "Coast life, unbroken."
SELLER = "Hospitality Products"
ORIGIN = "Yatala QLD"
RANGE_PROOF = "80+ melamine & polycarbonate lines"
CONCEPT = (
    f"Concept storefront · not taking payment yet · "
    f"Sold by {SELLER} ({ORIGIN}) via this specialist store"
)

BRANDS = ["duron", "ironbark", "tusk", "c3n6"]
CATEGORIES = [
    ("plates", "Plates"),
    ("bowls", "Bowls"),
    ("mugs-cups", "Mugs & cups"),
    ("platters-trays", "Platters & trays"),
    ("drinkware", "Drinkware"),
]
CAT_LABEL = dict(CATEGORIES)
SECTORS = [
    ("aged-care", "Aged care", "Quietly tough ware for dining rooms that run every shift."),
    ("childcare-oshc", "Childcare & OSHC", "Tables that take a hit — without looking institutional."),
    ("marine-galley", "Marine galley", "Wet decks and galleys that do not forgive china."),
    ("camp-outdoor", "Camp & outdoor", "Coast packs that fold into real life."),
    ("cafes-venues", "Cafés & venues", "Service ware that survives the rush and the wash."),
    ("schools", "Schools", "Canteen and boarding tables built for volume."),
]
FAKE_PL_RE = re.compile(
    r"\b(Duron|Ironbark|Tusk|C3N6|C3n6)\s+"
    r"(Dinner\s+Plate|Side\s+Plate|Bowl|Mug|Cup|Tumbler|Platter|Tray|Drinkware|Plate)\b",
    re.I,
)
MANUFACTURERS = ("Superware", "Polysafe")


def load_tokens(slug: str) -> dict:
    return json.loads((DLL / f"tokens.{slug}.json").read_text(encoding="utf-8"))


def load_catalogue() -> list[dict]:
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    out = []
    for p in data["products"]:
        if not p.get("image"):
            continue
        if (p.get("vendor") or "").strip() not in MANUFACTURERS:
            continue
        out.append(p)
    if len(out) < 80:
        raise SystemExit(f"Need ≥80 SKUs with images; got {len(out)}")
    return out


def title_case_piece(text: str) -> str:
    small = {"of", "and", "or", "the", "a", "an", "for", "with", "in", "to", "pack"}
    parts = []
    for i, w in enumerate(re.split(r"(\s+|-)", text.strip())):
        if not w or w.isspace() or w == "-":
            parts.append(w)
            continue
        low = w.lower()
        if re.fullmatch(r"\d+(mm|ml|cm|l)?", low):
            parts.append(low)
            continue
        if low in small and i > 0:
            parts.append(low)
            continue
        if w.isupper() and len(w) > 1:
            parts.append(w.capitalize())
        else:
            parts.append(w[:1].upper() + w[1:])
    return "".join(parts)


def display_title(p: dict) -> str:
    vendor = (p.get("vendor") or "").strip()
    ops = (p.get("ops_title") or p.get("piece") or "").strip()
    cleaned = ops
    for m in MANUFACTURERS:
        if cleaned.upper().startswith(m.upper() + " "):
            cleaned = cleaned[len(m) :].strip()
            vendor = vendor or m
            break
    if vendor not in MANUFACTURERS:
        kit = (p.get("ops_kit") or "").lower()
        vendor = "Polysafe" if ("polysafe" in kit or "polycarb" in kit) else "Superware"
    piece = title_case_piece(cleaned or p.get("piece") or p["handle"])
    title = f"{vendor} {piece}".strip()
    if FAKE_PL_RE.search(title):
        raise ValueError(f"Fake PL title: {title}")
    if not any(title.startswith(m) for m in MANUFACTURERS):
        title = f"{vendor} {piece}"
    return title


def aud(n: float) -> str:
    return f"${n:,.2f} AUD"


def rel(depth: int, to: str) -> str:
    return ("../" * depth) + to


def depth_for(path: str) -> int:
    return max(0, len(Path(path).parts) - 1)


def by_category(products: list[dict]) -> dict[str, list[dict]]:
    g: dict[str, list[dict]] = defaultdict(list)
    for p in products:
        g[p["category"]].append(p)
    return g


def brand_css(t: dict) -> str:
    slug = t["slug"]
    c = t["colors"]
    if slug == "ironbark":
        root = (
            f"--bg:{c['sand']};--ink:{c['ink']};--accent:{c['bark']};--accent2:{c['sap']};"
            f"--card:{c['paper']};--line:rgba(44,24,16,.14);--mute:{c.get('muted', c.get('mute'))};"
            f"--cta:{c['leaf']};--cta-ink:#F5F0E6;--banner-bg:{c['bark']};--banner-ink:{c['sand']};"
            f"--radius:3px;--display:Fraunces,Georgia,serif;--body:\"Source Sans 3\",system-ui,sans-serif;"
            f"--nav-size:.72rem;--btn-radius:3px;--card-radius:3px;"
        )
        extras = ""
        logo = ".logo{font-family:var(--display);font-weight:700;font-size:1.65rem;color:var(--accent);letter-spacing:-.02em}"
    elif slug == "c3n6":
        root = (
            f"--bg:{c['paper']};--ink:{c['ink']};--accent:{c['accent']};--accent2:{c['ink']};"
            f"--card:#fff;--line:{c['line']};--mute:{c.get('mute', c.get('muted'))};"
            f"--cta:{c['accent']};--cta-ink:#fff;--banner-bg:{c['ink']};--banner-ink:#fff;"
            f"--radius:0;--display:\"IBM Plex Sans\",system-ui,sans-serif;--body:\"IBM Plex Sans\",system-ui,sans-serif;"
            f"--nav-size:10px;--btn-radius:0;--card-radius:0;"
        )
        extras = (
            ".nav a,.btn,.kicker,.proof,.pcard .name,.soldby,.foot-brand,.subnav a,.logo"
            '{font-family:"IBM Plex Mono",monospace;text-transform:uppercase;letter-spacing:.08em}'
        )
        logo = '.logo{font:600 14px "IBM Plex Mono",monospace;letter-spacing:.12em}.logo span{color:var(--accent)}'
    elif slug == "tusk":
        root = (
            f"--bg:{c['void']};--ink:{c['bone']};--accent:{c['bone']};--accent2:{c['strike']};"
            f"--card:#111;--line:{c['bone']};--mute:{c.get('mute', c.get('muted'))};"
            f"--cta:{c['bone']};--cta-ink:{c['void']};--banner-bg:{c['strike']};--banner-ink:#fff;"
            f"--radius:0;--display:\"Archivo Black\",sans-serif;--body:Archivo,system-ui,sans-serif;"
            f"--nav-size:.68rem;--btn-radius:0;--card-radius:0;"
        )
        extras = (
            "h1,h2,.display,.logo,.foot-brand{text-transform:uppercase}"
            ".pcard,.gallery,.hero-vis,.trust{border:4px solid var(--line)}"
            ".site-header,.site-footer{border-width:4px}"
        )
        logo = ".logo{font-family:var(--display);font-size:1.3rem;letter-spacing:.04em}"
    else:
        root = (
            f"--bg:{c['stone']};--ink:{c['ink']};--accent:{c['teal']};--accent2:{c['soft']};"
            f"--card:#fff;--line:{c['line']};--mute:{c['soft']};"
            f"--cta:{c['teal']};--cta-ink:#fff;--banner-bg:{c['teal']};--banner-ink:#E7F7F3;"
            f"--radius:16px;--display:\"DM Serif Display\",Georgia,serif;--body:\"DM Sans\",system-ui,sans-serif;"
            f"--nav-size:.78rem;--btn-radius:999px;--card-radius:18px;"
        )
        extras = (
            ".hero{text-align:center}.hero .lede{margin-left:auto;margin-right:auto}"
            f".kicker{{display:inline-block;background:{c['mint']};color:var(--accent);"
            "padding:.38rem .7rem;border-radius:99px}"
        )
        logo = ".logo{font-family:var(--display);font-size:1.5rem;color:var(--accent)}"

    return f"""
:root{{{root}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--body);background:var(--bg);color:var(--ink);line-height:1.55}}
a{{color:inherit;text-decoration:none}} img{{max-width:100%;display:block}}
.banner{{background:var(--banner-bg);color:var(--banner-ink);font:700 11px/1.3 var(--body);letter-spacing:.1em;text-transform:uppercase;padding:.55rem 1rem;text-align:center}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 1.25rem}}
.site-header{{display:flex;justify-content:space-between;align-items:end;padding:1.35rem 0 1rem;border-bottom:2px solid var(--accent);gap:1rem;flex-wrap:wrap}}
{logo}
.logo small{{display:block;font-family:var(--body);font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-top:.2rem}}
.nav{{display:flex;flex-wrap:wrap;gap:.1rem .65rem}}
.nav a{{color:var(--mute);font-weight:700;font-size:var(--nav-size)}}
.nav a:hover{{color:var(--accent)}}
.btn{{display:inline-block;background:var(--cta);color:var(--cta-ink);font-weight:700;padding:.85rem 1.2rem;border-radius:var(--btn-radius);border:none;cursor:pointer;font:inherit}}
.btn-ghost{{background:transparent;color:var(--accent);border:2px solid var(--accent)}}
.btn.is-disabled,.btn[disabled]{{opacity:.45;cursor:not-allowed}}
.hero{{display:grid;grid-template-columns:1.05fr .95fr;gap:2rem;padding:2.2rem 0;align-items:center}}
.kicker{{font:700 12px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);margin-bottom:.75rem}}
h1,.display{{font-family:var(--display);font-weight:700;line-height:1.08;color:var(--accent)}}
h1{{font-size:clamp(1.9rem,4.2vw,3rem);margin-bottom:.9rem}}
h2{{font-family:var(--display);font-size:clamp(1.35rem,2.6vw,1.85rem);color:var(--accent);margin-bottom:.7rem}}
.lede{{font-size:1.05rem;max-width:48ch;color:var(--mute);margin-bottom:1.15rem}}
.hero-vis,.gallery{{background:var(--card);border:1px solid var(--line);border-radius:var(--card-radius);overflow:hidden}}
.hero-vis img,.gallery img{{width:100%;aspect-ratio:1;object-fit:cover}}
.proof{{display:inline-block;background:var(--card);border:1.5px solid var(--accent);padding:.4rem .85rem;font-weight:700;font-size:.82rem;border-radius:99px;margin-bottom:.85rem}}
.catgrid,.secgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.75rem;margin:1.15rem 0}}
.cat{{background:var(--card);border:1px solid var(--line);border-radius:var(--card-radius);padding:1rem;font-weight:700;color:var(--accent);display:block}}
.cat span{{display:block;font-weight:600;font-size:.78rem;color:var(--mute);margin-top:.35rem}}
.trust{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2rem 0}}
.trust > div{{background:var(--card);border:1px solid var(--line);border-radius:var(--card-radius);padding:1.25rem}}
.trust h3{{font-family:var(--display);font-size:1.05rem;color:var(--accent);margin-bottom:.3rem}}
.trust p{{font-size:.88rem;color:var(--mute)}}
.section{{padding:1.7rem 0}}
.pgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:1rem}}
.pcard{{background:var(--card);border:1px solid var(--line);border-radius:var(--card-radius);overflow:hidden;color:inherit;display:block}}
.pcard img{{width:100%;aspect-ratio:1;object-fit:cover;background:#fff}}
.pcard .body{{padding:.85rem}}
.pcard .name{{font-weight:700;font-size:.88rem;color:var(--accent)}}
.pcard .price{{font-weight:700;margin-top:.3rem}}
.pcard .note{{font-size:.7rem;color:var(--mute);margin-top:.22rem}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:1.8rem;padding:2rem 0;align-items:start}}
.price-lg{{font-size:1.4rem;font-weight:700;color:var(--accent);margin:.5rem 0 1rem}}
.soldby{{font-size:.88rem;font-weight:700;color:var(--accent2);margin-bottom:1rem}}
.bullets{{margin:1rem 0 1.15rem;padding-left:1.1rem}} .bullets li{{margin:.3rem 0}}
.note-soft{{font-size:.84rem;color:var(--mute);margin-top:.7rem}}
.prose{{max-width:62ch}} .prose p{{margin:0 0 1rem}}
.faq details{{border-bottom:1px solid var(--line);padding:1rem 0}}
.faq summary{{font-weight:700;cursor:pointer;color:var(--accent)}}
.form{{display:grid;gap:.8rem;max-width:420px}}
.form label{{font-weight:700;font-size:.84rem;display:grid;gap:.3rem}}
.form input,.form textarea,.form select{{padding:.7rem .8rem;border:1.5px solid var(--line);border-radius:12px;font:inherit;background:var(--card);color:var(--ink)}}
.table{{width:100%;border-collapse:collapse;margin:1rem 0}}
.table th,.table td{{text-align:left;padding:.6rem .5rem;border-bottom:1px solid var(--line);font-size:.94rem}}
.site-footer{{border-top:2px solid var(--accent);padding:1.4rem 0 2.4rem;margin-top:2rem;font-size:.84rem;color:var(--mute)}}
.foot-grid{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:1.2rem}}
.site-footer a{{color:var(--mute)}} .site-footer a:hover{{color:var(--accent)}}
.foot-brand{{font-family:var(--display);font-size:1.15rem;color:var(--accent);font-weight:700}}
.subnav{{display:flex;flex-wrap:wrap;gap:.45rem;margin:1rem 0 1.35rem}}
.subnav a{{border:1.5px solid var(--accent);padding:.32rem .7rem;border-radius:99px;font-weight:700;font-size:.74rem}}
{extras}
@media(max-width:860px){{.hero,.pdp,.trust,.foot-grid{{grid-template-columns:1fr}}.pgrid{{grid-template-columns:1fr 1fr}}}}
"""


def logo_html(t: dict, depth: int) -> str:
    href = rel(depth, "index.html")
    tag = escape(t.get("tagline_short") or "")
    if t["slug"] == "c3n6":
        return f'<a class="logo" href="{href}">C3<span>N</span>6<small>{tag}</small></a>'
    return f'<a class="logo" href="{href}">{escape(t["name"])}<small>{tag}</small></a>'


def nav_html(t: dict, depth: int) -> str:
    short = {
        "aged-care": "Aged care",
        "childcare-oshc": "Childcare",
        "marine-galley": "Marine",
        "camp-outdoor": "Camp",
        "cafes-venues": "Cafés",
        "schools": "Schools",
    }
    links = [("Shop", "shop/index.html")]
    for slug, _label, _ in SECTORS:
        links.append((short[slug], f"sectors/{slug}/index.html"))
    links += [("About", "about/index.html"), ("FAQ", "faq/index.html"), ("Contact", "contact/index.html")]
    parts = [f'<a href="{rel(depth, href)}">{escape(label)}</a>' for label, href in links]
    return '<nav class="nav">' + "".join(parts) + "</nav>"


def footer_html(t: dict, depth: int) -> str:
    n = escape(t["name"])
    sec = "".join(
        f'<a href="{rel(depth, f"sectors/{s}/index.html")}">{escape(lab)}</a><br/>'
        for s, lab, _ in SECTORS
    )
    cats = "".join(
        f'<a href="{rel(depth, f"shop/{c}/index.html")}">{escape(lab)}</a><br/>'
        for c, lab in CATEGORIES
    )
    return f"""
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <div class="foot-brand">{n}</div>
      <p style="margin-top:.5rem">{CATCHLINE}</p>
      <p style="margin-top:.5rem">Concept face for colour, type and voice. Sold by {SELLER} ({ORIGIN}) via this specialist storefront.</p>
    </div>
    <div><strong>Shop</strong><br/><a href="{rel(depth,'shop/index.html')}">All products</a><br/>{cats}</div>
    <div><strong>Sectors</strong><br/>{sec}</div>
    <div>
      <strong>Help</strong><br/>
      <a href="{rel(depth,'shipping/index.html')}">Shipping</a><br/>
      <a href="{rel(depth,'returns/index.html')}">Returns</a><br/>
      <a href="{rel(depth,'faq/index.html')}">FAQ</a><br/>
      <a href="{rel(depth,'contact/index.html')}">Contact</a><br/>
      <a href="{rel(depth,'privacy/index.html')}">Privacy</a><br/>
      <a href="{rel(depth,'terms/index.html')}">Terms</a><br/>
      <a href="{rel(depth,'about/index.html')}">About {n}</a>
    </div>
  </div>
</footer>"""


def schema_product(p: dict, title: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": title,
        "sku": p.get("sku") or "",
        "image": p.get("image"),
        "description": p.get("blurb") or title,
        "brand": {"@type": "Brand", "name": p.get("vendor") or "Superware"},
        "offers": {
            "@type": "Offer",
            "priceCurrency": "AUD",
            "price": f"{float(p['price']):.2f}",
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": SELLER},
        },
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def page_shell(t: dict, path: str, title: str, body: str, extra_head: str = "") -> str:
    depth = depth_for(path)
    css = brand_css(t)
    fonts = t["fonts"]["google"]
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{escape(title)}</title>
<meta name="description" content="{escape(t['name'])} concept store — {CATCHLINE} Superware melamine &amp; Polysafe polycarbonate from {ORIGIN}."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="{fonts}" rel="stylesheet"/>
<style>{css}</style>
{extra_head}
</head>
<body>
<div class="banner">{CONCEPT}</div>
<div class="wrap">
  <header class="site-header">
    {logo_html(t, depth)}
    {nav_html(t, depth)}
  </header>
</div>
{body}
{footer_html(t, depth)}
</body>
</html>
"""


def product_cards(products: list[dict], depth: int, limit: int | None = None) -> str:
    items = products[:limit] if limit else products
    cards = []
    for p in items:
        title = display_title(p)
        href = rel(depth, f"product/{p['handle']}/index.html")
        cards.append(
            f"""<a class="pcard" href="{href}" data-ops-kit="{escape(p.get('ops_kit') or '')}" data-vendor="{escape(p.get('vendor') or '')}">
  <img src="{escape(p['image'])}" alt="{escape(title)}"/>
  <div class="body">
    <div class="name">{escape(title)}</div>
    <div class="price">{aud(float(p['price']))}</div>
    <div class="note">Sold by {SELLER} · {ORIGIN}</div>
  </div>
</a>"""
        )
    return '<div class="pgrid">' + "\n".join(cards) + "</div>"


def category_tiles(depth: int, counts: dict[str, int]) -> str:
    tiles = []
    for slug, label in CATEGORIES:
        n = counts.get(slug, 0)
        tiles.append(
            f'<a class="cat" href="{rel(depth, f"shop/{slug}/index.html")}">{escape(label)}'
            f"<span>{n} lines</span></a>"
        )
    return '<div class="catgrid">' + "".join(tiles) + "</div>"


def sector_strip(depth: int) -> str:
    tiles = []
    for slug, label, blurb in SECTORS:
        tiles.append(
            f'<a class="cat" href="{rel(depth, f"sectors/{slug}/index.html")}">{escape(label)}'
            f"<span>{escape(blurb)}</span></a>"
        )
    return '<div class="secgrid">' + "".join(tiles) + "</div>"


def trust_strip(t: dict) -> str:
    bits = list(t["voice"]["trust"])
    cells = []
    for i, b in enumerate(bits):
        if i == len(bits) - 1:
            cells.append(f"<div><h3>{escape(b)}</h3><p>Sold by {SELLER} · {ORIGIN}</p></div>")
        else:
            cells.append(f"<div><h3>{escape(b)}</h3><p>{CATCHLINE}</p></div>")
    return f'<div class="trust">{"".join(cells)}</div>'


def shop_subnav(depth: int) -> str:
    links = [f'<a href="{rel(depth, "shop/index.html")}">All</a>']
    for slug, label in CATEGORIES:
        links.append(f'<a href="{rel(depth, f"shop/{slug}/index.html")}">{escape(label)}</a>')
    return '<div class="subnav">' + "".join(links) + "</div>"


def home_page(t: dict, products: list[dict], grouped: dict[str, list[dict]]) -> str:
    depth = 0
    n = t["name"]
    counts = {k: len(v) for k, v in grouped.items()}
    featured = products[:8]
    hero_img = products[0]["image"]
    hero_alt = display_title(products[0])
    voice = t["voice"]
    hero = f"""
<section class="wrap">
  <div class="hero">
    <div>
      <div class="kicker">Archetype · {escape(t.get('archetype') or '')}</div>
      <div class="proof">{RANGE_PROOF}</div>
      <h1>{escape(t.get('hero') or n)}</h1>
      <p class="lede">{escape(voice['home_lede'])}</p>
      <a class="btn" href="{rel(depth,'shop/index.html')}">{escape(voice['cta_shop'])}</a>
      &nbsp; <a class="btn btn-ghost" href="{rel(depth,'about/index.html')}">{escape(voice['cta_about'])}</a>
    </div>
    <div class="hero-vis"><img src="{escape(hero_img)}" alt="{escape(hero_alt)}"/></div>
  </div>
</section>"""
    body = f"""
{hero}
<div class="wrap">
  <section class="section">
    <h2 class="display">Shop by category</h2>
    <p class="lede">Real Superware melamine and Polysafe polycarbonate — not private-label fiction.</p>
    {category_tiles(depth, counts)}
  </section>
  <section class="section">
    <h2 class="display">Built for the rooms that break china</h2>
    {sector_strip(depth)}
  </section>
  {trust_strip(t)}
  <section class="section">
    <h2 class="display">Featured lines</h2>
    <p class="lede" style="margin-bottom:1.2rem">{CATCHLINE} {len(products)} SKUs with images. Sold by {SELLER}.</p>
    {product_cards(featured, depth)}
    <p style="margin-top:1.2rem"><a class="btn" href="{rel(depth,'shop/index.html')}">Browse all {len(products)} lines</a></p>
  </section>
</div>
"""
    return page_shell(t, "index.html", f"{n} — {CATCHLINE} · {RANGE_PROOF}", body)


def shop_page(t: dict, products: list[dict], category: str | None = None) -> str:
    if category:
        items = [p for p in products if p["category"] == category]
        label = CAT_LABEL[category]
        path = f"shop/{category}/index.html"
        depth = 2
        h1 = label
        title = f"{label} — {t['name']}"
    else:
        items = products
        path = "shop/index.html"
        depth = 1
        h1 = f"Shop · {len(items)} lines"
        title = f"Shop — {t['name']}"
    body = f"""
<div class="wrap section">
  <div class="kicker">Shop · Superware &amp; Polysafe</div>
  <h1>{escape(h1)}</h1>
  <p class="lede">{RANGE_PROOF}. Checkout not live. Sold by {SELLER} · fulfilled from {ORIGIN}.</p>
  {shop_subnav(depth)}
  {product_cards(items, depth)}
</div>
"""
    return page_shell(t, path, title, body)


def pdp_page(t: dict, p: dict) -> str:
    depth = 2
    title = display_title(p)
    material = "melamine" if p.get("vendor") == "Superware" else "polycarbonate"
    cat = p["category"]
    cat_label = CAT_LABEL.get(cat, cat)
    schema = schema_product(p, title)
    body = f"""
<!-- ops kit: {escape(p.get('ops_kit') or '')} -->
<div class="wrap">
  <div class="pdp" data-vendor="{escape(p.get('vendor') or '')}" data-sku="{escape(p.get('sku') or '')}">
    <div>
      <div class="gallery"><img src="{escape(p['image'])}" alt="{escape(title)}"/></div>
    </div>
    <div class="pdp-body">
      <div class="kicker">{escape(cat_label)} · {escape(p.get('vendor') or '')}</div>
      <h1 style="font-size:clamp(1.5rem,3vw,2.1rem)">{escape(title)}</h1>
      <div class="price-lg">{aud(float(p['price']))}</div>
      <div class="soldby">Sold by {SELLER} ({ORIGIN}) via this specialist storefront</div>
      <p>{escape(p.get('blurb') or title)}</p>
      <ul class="bullets">
        <li>Real manufacturer: <strong>{escape(p.get('vendor') or '')}</strong> {material}</li>
        <li>SKU {escape(p.get('sku') or '—')} · trade-grade unbreakable {escape(cat_label.lower())}</li>
        <li>Ships from {ORIGIN} via {SELLER}</li>
        <li>{CATCHLINE}</li>
      </ul>
      <button class="btn is-disabled" disabled type="button">Add to bag</button>
      <p class="note-soft">Concept store — not taking payment yet. Enquire via <a href="{rel(depth,'contact/index.html')}">contact</a>.</p>
      <p class="note-soft"><a href="{rel(depth, f'shop/{cat}/index.html')}">More {escape(cat_label.lower())}</a> · <a href="{rel(depth,'shop/index.html')}">All products</a></p>
    </div>
  </div>
</div>
"""
    return page_shell(t, f"product/{p['handle']}/index.html", f"{title} — {t['name']}", body, schema)


def about_page(t: dict) -> str:
    depth = 1
    n = escape(t["name"])
    body = f"""
<div class="wrap section prose">
  <div class="kicker">About</div>
  <h1>About the {n} face</h1>
  <p>{escape(t['voice']['about_lede'])}</p>
  <p><strong>{n}</strong> is a concept face — colour, type and voice for this bakeoff storefront. It is not a private-label product brand on the ware.</p>
  <p>Every product title names the real manufacturer: <strong>Superware</strong> melamine or <strong>Polysafe</strong> polycarbonate. Sold by <strong>{SELLER}</strong> ({ORIGIN}) via this specialist storefront.</p>
  <p>{CATCHLINE}</p>
  <p><a class="btn" href="{rel(depth,'shop/index.html')}">{escape(t['voice']['cta_shop'])}</a></p>
</div>
"""
    return page_shell(t, "about/index.html", f"About {t['name']}", body)


def shipping_page(t: dict) -> str:
    body = f"""
<div class="wrap section prose">
  <div class="kicker">Shipping</div>
  <h1>Shipping from {ORIGIN}</h1>
  <p>Orders are fulfilled by {SELLER} from {ORIGIN}. Concept rates below — live carrier quotes unlock with checkout.</p>
  <table class="table">
    <thead><tr><th>Zone</th><th>Placeholder</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>SEQ / Gold Coast</td><td>from $9.90</td><td>Fastest lane from Yatala</td></tr>
      <tr><td>Metro AU</td><td>from $12.90</td><td>Sydney, Melbourne, Brisbane, Adelaide, Perth metro</td></tr>
      <tr><td>Regional AU</td><td>from $18.90</td><td>Extra transit days</td></tr>
      <tr><td>Remote AU</td><td>Quote</td><td>Contact before order</td></tr>
      <tr><td>New Zealand</td><td>Coming</td><td>NZ not live on this concept store</td></tr>
    </tbody>
  </table>
  <p>Sold by {SELLER} via this specialist storefront.</p>
</div>
"""
    return page_shell(t, "shipping/index.html", f"Shipping — {t['name']}", body)


def returns_page(t: dict) -> str:
    body = f"""
<div class="wrap section prose">
  <div class="kicker">Returns</div>
  <h1>Returns &amp; breakage</h1>
  <p><strong>30-day concept returns.</strong> Change of mind within 30 days of delivery on unused items in original condition — draft policy for bakeoff only.</p>
  <p><strong>Breakage in transit.</strong> Photograph the carton and the piece within 48 hours of delivery and email {escape(t['email'])}.</p>
  <p>Sold by {SELLER}, {ORIGIN}.</p>
</div>
"""
    return page_shell(t, "returns/index.html", f"Returns — {t['name']}", body)


def faq_page(t: dict) -> str:
    n = t["name"]
    faqs = [
        (f"Is {n} the product brand on the box?",
         f"No. {n} is the concept face (colour, type, voice). Product titles use real manufacturers — Superware melamine and Polysafe polycarbonate."),
        ("Who is the seller?", f"{SELLER} ({ORIGIN}) sells via this specialist storefront."),
        ("Is this china?", "No. Melamine and polycarbonate unbreakable ware for rooms that punish porcelain."),
        ("Can I buy today?", "Concept store — payment disabled. Use Contact to register interest."),
        ("Do you ship to New Zealand?", "NZ is marked coming. Australian zones are on Shipping."),
        ("Is it dishwasher safe?", "Yes for everyday commercial-style cycles."),
        ("What if a piece arrives damaged?", "Photograph carton and piece within 48 hours — see Returns."),
        ("Where are orders fulfilled from?", f"{ORIGIN}, by {SELLER}."),
    ]
    items = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs)
    body = f"""
<div class="wrap section">
  <div class="kicker">FAQ</div>
  <h1>Questions</h1>
  <div class="faq">{items}</div>
</div>
"""
    return page_shell(t, "faq/index.html", f"FAQ — {n}", body)


def contact_page(t: dict) -> str:
    n = escape(t["name"])
    body = f"""
<div class="wrap section">
  <div class="kicker">Contact</div>
  <h1>Talk to us</h1>
  <p class="lede">Concept inbox for the {n} face. Seller: {SELLER}, {ORIGIN}. Email <a href="mailto:{escape(t['email'])}">{escape(t['email'])}</a>.</p>
  <form class="form" onsubmit="event.preventDefault();alert('Concept form only — email {escape(t['email'])}');">
    <label>Name<input type="text" name="name" required/></label>
    <label>Email<input type="email" name="email" required/></label>
    <label>Topic
      <select name="topic">
        <option>General</option>
        <option>Aged care</option>
        <option>Childcare / OSHC</option>
        <option>Marine / venue</option>
        <option>Wholesale interest</option>
      </select>
    </label>
    <label>Message<textarea name="message" rows="5" required></textarea></label>
    <button class="btn" type="submit">Send (mock)</button>
    <p class="note-soft">Sold by {SELLER}, {ORIGIN}.</p>
  </form>
</div>
"""
    return page_shell(t, "contact/index.html", f"Contact — {t['name']}", body)


def privacy_page(t: dict) -> str:
    body = f"""
<div class="wrap section prose">
  <div class="kicker">Privacy</div>
  <h1>Privacy (concept)</h1>
  <p>Short Australian-flavoured concept notice for the {escape(t['name'])} bakeoff store. Not final legal advice.</p>
  <p>Enquiry details are used to respond. We do not sell personal information. Seller: {SELLER}, {ORIGIN}.</p>
  <p>Contact {escape(t['email'])} about access or deletion of enquiry records.</p>
</div>
"""
    return page_shell(t, "privacy/index.html", f"Privacy — {t['name']}", body)


def terms_page(t: dict) -> str:
    body = f"""
<div class="wrap section prose">
  <div class="kicker">Terms</div>
  <h1>Terms (concept)</h1>
  <ul>
    <li>Prices in AUD are illustrative for bakeoff.</li>
    <li>No payment is taken on this site.</li>
    <li>Product names use real manufacturers (Superware / Polysafe).</li>
    <li>Governing law intended: Queensland, Australia.</li>
    <li>Seller: {SELLER}, {ORIGIN}. Concept face: {escape(t['name'])}.</li>
  </ul>
  <p>Questions: {escape(t['email'])}.</p>
</div>
"""
    return page_shell(t, "terms/index.html", f"Terms — {t['name']}", body)


def sector_page(t: dict, products: list[dict], slug: str, label: str, blurb: str) -> str:
    depth = 2
    prefer = {
        "aged-care": ["plates", "bowls", "mugs-cups", "drinkware"],
        "childcare-oshc": ["plates", "bowls", "mugs-cups", "drinkware"],
        "marine-galley": ["plates", "bowls", "drinkware", "platters-trays"],
        "camp-outdoor": ["plates", "bowls", "drinkware", "mugs-cups"],
        "cafes-venues": ["platters-trays", "plates", "drinkware", "mugs-cups"],
        "schools": ["plates", "bowls", "drinkware", "mugs-cups"],
    }
    order = prefer.get(slug, [c for c, _ in CATEGORIES])
    picked: list[dict] = []
    for cat in order:
        for p in products:
            if p["category"] == cat and p not in picked:
                picked.append(p)
            if len(picked) >= 12:
                break
        if len(picked) >= 12:
            break
    body = f"""
<div class="wrap section">
  <div class="kicker">Sector · {escape(label)}</div>
  <h1>{escape(label)}</h1>
  <p class="lede">{escape(blurb)} {RANGE_PROOF}. Sold by {SELLER} ({ORIGIN}).</p>
  <div class="prose">
    <p>The {escape(t['name'])} face skins this store — the ware itself is Superware melamine and Polysafe polycarbonate, titled honestly.</p>
  </div>
  {product_cards(picked, depth)}
  <p style="margin-top:1.4rem">
    <a class="btn" href="{rel(depth,'contact/index.html')}">Enquire for this sector</a>
    &nbsp; <a class="btn btn-ghost" href="{rel(depth,'shop/index.html')}">View full range</a>
  </p>
</div>
"""
    return page_shell(t, f"sectors/{slug}/index.html", f"{label} — {t['name']}", body)


def write_store(slug: str, products: list[dict]) -> int:
    t = load_tokens(slug)
    grouped = by_category(products)
    root = STORES / slug
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)

    pages: dict[str, str] = {
        "index.html": home_page(t, products, grouped),
        "shop/index.html": shop_page(t, products),
        "about/index.html": about_page(t),
        "shipping/index.html": shipping_page(t),
        "returns/index.html": returns_page(t),
        "faq/index.html": faq_page(t),
        "contact/index.html": contact_page(t),
        "privacy/index.html": privacy_page(t),
        "terms/index.html": terms_page(t),
    }
    for cat, _ in CATEGORIES:
        pages[f"shop/{cat}/index.html"] = shop_page(t, products, cat)
    for s, lab, blurb in SECTORS:
        pages[f"sectors/{s}/index.html"] = sector_page(t, products, s, lab, blurb)
    for p in products:
        title = display_title(p)
        if FAKE_PL_RE.search(title):
            raise SystemExit(f"Refusing fake PL: {title}")
        if not any(title.startswith(m) for m in MANUFACTURERS):
            raise SystemExit(f"Title missing manufacturer prefix: {title}")
        pages[f"product/{p['handle']}/index.html"] = pdp_page(t, p)

    count = 0
    for rel_path, html in pages.items():
        if FAKE_PL_RE.search(html):
            m = FAKE_PL_RE.search(html)
            raise SystemExit(f"Fake PL leaked into {slug}/{rel_path}: {m.group(0)}")
        dest = root / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        count += 1
    return count


def write_hub(sku_count: int) -> None:
    SITES.mkdir(parents=True, exist_ok=True)
    html = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Unbreakable crockery — Superware &amp; Polysafe concept stores</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700&display=swap" rel="stylesheet"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"DM Sans",system-ui,sans-serif;background:#0E1116;color:#F4F5F7;padding:2rem 1.25rem 3rem}}
h1{{font-size:clamp(1.6rem,3vw,2.2rem);margin-bottom:.4rem}}
.sub{{color:#9AA3B2;margin-bottom:1.75rem;max-width:62ch;line-height:1.5}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;max-width:960px}}
a.card{{display:block;text-decoration:none;color:inherit;border-radius:14px;padding:1.35rem 1.4rem;min-height:160px;transition:transform .15s ease}}
a.card:hover{{transform:translateY(-2px)}}
a.card strong{{display:block;font-size:1.35rem;margin-bottom:.35rem}}
a.card span{{display:block;font-size:.88rem;opacity:.85;line-height:1.4}}
a.card em{{display:block;margin-top:.85rem;font-style:normal;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;opacity:.7}}
.c3{{background:linear-gradient(145deg,#fff 55%,#fdeceb);color:#111;border:1px solid #ddd}}
.c3 strong{{font-family:ui-monospace,monospace;letter-spacing:.08em}}
.tu{{background:#0A0C10;color:#F2EDE4;border:4px solid #F2EDE4}}
.tu strong{{font-size:1.6rem;letter-spacing:.04em}}
.ib{{background:#E8DCC8;color:#2C1810;border:2px solid #2C1810}}
.ib strong{{font-family:Georgia,serif;font-size:1.5rem}}
.du{{background:#D8F0EA;color:#0F3D3E;border:1px solid #A8D0C8;border-radius:20px}}
.du strong{{font-family:Georgia,serif}}
.note{{margin-top:1.75rem;font-size:.8rem;color:#6B7280;max-width:70ch;line-height:1.45}}
.note a{{color:#9AA3B2}}
.law{{margin-top:1rem;padding:1rem 1.1rem;border:1px solid #2a313c;border-radius:10px;max-width:70ch;font-size:.82rem;color:#c5cbd4;line-height:1.45}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<h1>Unbreakable crockery — four concept faces</h1>
<p class="sub">{RANGE_PROOF} of real <strong>Superware</strong> melamine and <strong>Polysafe</strong> polycarbonate ({sku_count} SKUs with images). Sold by {SELLER} ({ORIGIN}) via specialist storefronts. Faces skin colour, type and voice only.</p>
<div class="grid">
  <a class="card c3" href="stores/c3n6/"><strong>C3N6</strong><span>Lab-precise face. Full range, six sectors, manufacturer-true titles.</span><em>Sage + Magician</em></a>
  <a class="card tu" href="stores/tusk/"><strong>TUSK</strong><span>Animal-tough face. Same honest Superware / Polysafe catalogue.</span><em>Warrior / Hero</em></a>
  <a class="card ib" href="stores/ironbark/"><strong>Ironbark</strong><span>AU timber face. Reference visual system · product truth identical.</span><em>Everyman + Explorer</em></a>
  <a class="card du" href="stores/duron/"><strong>Duron</strong><span>Calm toughness face. Same 80+ melamine &amp; polycarbonate lines.</span><em>Caregiver + Sage</em></a>
</div>
<div class="law"><strong>Hard law 17/09/2026:</strong> Never title products “Duron Dinner Plate”, “Ironbark Mug”, “Tusk Bowl”, or “C3N6 platter”. Titles start with Superware or Polysafe. Seller = {SELLER} ({ORIGIN}).</div>
<p class="note">Catchline: {CATCHLINE} Hub → <strong>stores/</strong>. Archive mocks at <a href="mocks/">mocks/</a> if present.</p>
</body>
</html>
"""
    (SITES / "index.html").write_text(html, encoding="utf-8")


def main() -> None:
    products = load_catalogue()
    products.sort(key=lambda p: (p["category"], display_title(p)))
    total = 0
    for slug in BRANDS:
        n = write_store(slug, products)
        total += n
        print(f"{slug}: {n} pages → {STORES / slug}")
    write_hub(len(products))
    print(f"hub → {SITES / 'index.html'}")
    print(f"SKU count: {len(products)}")
    print(f"TOTAL store pages: {total}")


if __name__ == "__main__":
    main()
