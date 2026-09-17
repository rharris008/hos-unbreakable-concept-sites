# Brand Launchpad — playbook

## Purpose
Bake off four full B2C storefront packs sharing one kit and catchline, with **distinct** visual systems.

## Hard law — 17/09/2026
- Melamine = **Superware**; polycarbonate = **Polysafe** (real names in title, H1, alt, schema).
- Concept faces (Duron / Ironbark / Tusk / C3N6) skin colour, type and voice ONLY.
- Seller line: sold by Hospitality Products (Yatala) via this specialist storefront.
- NEVER title “Duron Dinner Plate”, “Ironbark Mug”, “Tusk Bowl”, “C3N6 platter”.
- Catalogue: ≥80 SKUs with images from `DLL/catalogue.unbreakable.json`.

## Reference store
**Ironbark** is the reference full B2C pack (energy bar + complete page inventory). Other brands must match page depth; they must **not** share Ironbark CSS/voice.

## Generate
`python3 Launchpad/DLL/spawn.py` from Foundation / Launchpad root.

## Publish
Push `Sites/stores/**` + `Sites/index.html` to `rharris008/hos-unbreakable-concept-sites`.
