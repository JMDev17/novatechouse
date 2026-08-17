#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
html_files = sorted(ROOT.rglob('*.html'))
broken = []

for f in html_files:
    # Skip raw source templates/ and content/ files (which contain template placeholders)
    if "templates" in f.parts or "content" in f.parts:
        continue
    txt = f.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'href="([^"]+)"', txt):
        href = m.group(1)
        if href.startswith(('http://', 'https://', '#', 'tel:', 'mailto:', 'javascript:')):
            continue
        clean = href.split('#')[0]
        if not clean:
            continue
        if clean.startswith('/'):
            rel_path = clean.lstrip('/')
            target = ROOT / rel_path
            if clean.endswith('/'):
                target = target / 'index.html'
        else:
            target = (f.parent / clean).resolve()

        if not target.exists() and not (target.is_dir() and (target / 'index.html').exists()):
            broken.append((str(f.relative_to(ROOT)), href))

print(f"Total compiled HTML files checked: {len(html_files)}")
print(f"Broken internal links count: {len(broken)}")
if broken:
    for src, link in broken[:30]:
        print(f"  {src} -> {link}")
else:
    print("ALL COMPILED INTERNAL LINKS ARE 100% VALID!")

