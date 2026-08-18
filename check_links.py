#!/usr/bin/env python3
import re
from pathlib import Path

BASE = Path('.')
SKIP_PREFIXES = ('http://', 'https://', 'tel:', 'mailto:', 'javascript:', '#', '/')

problems = []
for f in sorted(BASE.rglob('*.html')):
    txt = f.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(r'href="([^"]+)"', txt):
        href = m.group(1)
        if any(href.startswith(p) for p in SKIP_PREFIXES):
            continue
        if href == '':
            continue
        problems.append((str(f.relative_to(BASE)), href))

if problems:
    for path, href in problems[:30]:
        print(f'  {path}: {href!r}')
    print(f'\n  total: {len(problems)}')
else:
    print('All internal links are absolute. No remaining relative links.')
