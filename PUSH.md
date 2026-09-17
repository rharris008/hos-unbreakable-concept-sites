# Push + Foundation sync

## GitHub (ready on box — push blocked: `gh` not authenticated)
Checkout: `/workspace/hos-unbreakable-concept-sites`
Remote: `https://github.com/rharris008/hos-unbreakable-concept-sites.git`
Branch: `main` ahead of origin (commits include `055f08c` hard-law rebuild + `402d1ce` PUSH note)

```bash
cd /workspace/hos-unbreakable-concept-sites
gh auth login   # or use Mac gh
git push origin main
# Pages: https://rharris008.github.io/hos-unbreakable-concept-sites/
```

## Mac Foundation (machineId `dd15696b-c949-4726-8425-8e1cd341e673`)
```bash
FOUND="/Users/robertharris/Library/CloudStorage/OneDrive-ABHGROUP/Documents/Hospitality Products/Unbreakable Crockery Launch/Foundation"
# Sync Launchpad/ + Sites/ from box `/workspace/hos-launchpad/` or tarball, then:
python3 "$FOUND/Launchpad/DLL/spawn.py"
```

Box mirror: `/workspace/hos-launchpad/`
Tarball: `/workspace/hos-launchpad-deliverable.tgz`
