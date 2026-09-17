# Push + Foundation sync

## GitHub (ready on box, push blocked — no `gh` auth)
Checkout: `/workspace/hos-unbreakable-concept-sites`
Branch: `main` ahead of `origin/main` by **2** commits
Latest: `055f08c` — Rebuild stores under manufacturer-true hard law (17/09/2026)

```bash
cd /workspace/hos-unbreakable-concept-sites
gh auth login    # once
git push origin main
# Pages: https://rharris008.github.io/hos-unbreakable-concept-sites/
```

## Mac Foundation (machineId `dd15696b-c949-4726-8425-8e1cd341e673`)
```bash
FOUND="/Users/robertharris/Library/CloudStorage/OneDrive-ABHGROUP/Documents/Hospitality Products/Unbreakable Crockery Launch/Foundation"
# Sync Launchpad/ + Sites/ from box mirror or tarball, then:
python3 "$FOUND/Launchpad/DLL/spawn.py"
```

Box mirror: `/workspace/hos-launchpad/`
Tarball: `/workspace/hos-launchpad-deliverable.tgz`
