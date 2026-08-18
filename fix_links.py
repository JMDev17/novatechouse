#!/usr/bin/env python3
"""
Fix all internal href links to use absolute clean URLs.

Root cause: mobile menus in iphones/ and servicos/ pages use
  ../iphones/iphone-X/index.html  (one level up, wrong)
instead of
  ../../iphones/iphone-X/index.html  (two levels up, correct)
producing doubled paths like /iphones/iphones/iphone-X/.

Solution: convert every internal href to a canonical absolute URL.
"""

import re
import os
from pathlib import Path

BASE = Path(r"c:\Users\User\OneDrive\Área de Trabalho\PROJETOS IA ANTIGRAVITY\FERRARI CELL").resolve()

# Known slug patterns — matched against the raw href string
IPHONE_MODELS = [
    'iphone-17-pro-max', 'iphone-17', 'iphone-16', 'iphone-15',
    'iphone-14', 'iphone-13', 'iphone-12', 'iphone-11',
]
SERVICE_SLUGS = [
    'conserto-de-celular-iphone', 'conserto-de-celular-android',
    'troca-de-tela', 'troca-de-bateria', 'conserto-de-placa',
    'micro-solda', 'reparo-de-software', 'conserto-de-ipad',
    'conserto-de-notebook', 'reparo-face-id', 'reparo-de-camera',
]
BLOG_SLUGS = [
    'iphone-nao-carrega-o-que-fazer',
    'celular-caiu-na-agua-o-que-fazer',
    'saude-da-bateria-mitos-e-verdades-sobre-carregamento',
]
# Sublocations for como-chegar
PINDA_SUBS = [
    'araretama', 'boa-vista', 'cidade-nova', 'crispim', 'mombaca',
    'residencial-pasin', 'santana', 'sao-benedito', 'vila-rica',
]
TAUBATE_SUBS = [
    'barranco', 'belem', 'estiva', 'independencia', 'jardim-das-nacoes',
    'monte-belo', 'parque-senhor-do-bonfim', 'quiririm', 'vila-sao-jose',
]
# centro appears in both cities; resolve by checking which city appears in href
AMBIGUOUS_SUBS = ['centro']

# Fragments known to live on the home page
ROOT_FRAGMENTS = {'#especialistas', '#contato', '#contato-info', '#servicos', '#hero', '#iphones'}


def canonical(href, file_path):
    """
    Return the canonical absolute clean URL for an internal href.
    Returns None if the href should not be changed.
    """
    if not href:
        return None

    # Leave external, protocol-relative, and anchor-only links untouched
    if href.startswith(('http://', 'https://', 'tel:', 'mailto:', 'javascript:')):
        return None
    if href.startswith('#'):
        return None

    # Leave asset references (CSS, JS, images) untouched
    if re.search(r'\.(css|js|png|jpg|jpeg|webp|avif|svg|ico|woff|woff2|ttf)$', href, re.IGNORECASE):
        return None

    # --- Split off fragment ---
    fragment = ''
    if '#' in href:
        idx = href.index('#')
        fragment = href[idx:]
        href = href[:idx]
        if not href:
            return None  # just a fragment, leave alone

    # --- Already absolute: just strip /index.html ---
    if href.startswith('/'):
        clean = href
        if clean.endswith('/index.html'):
            clean = clean[: -len('index.html')]
        if clean != '/' and not clean.endswith('/'):
            clean += '/'
        result = clean + fragment
        return result if result != href + fragment else None

    # ---- Slug-based pattern matching ----

    for model in IPHONE_MODELS:
        if model in href:
            return f'/iphones/{model}/' + fragment

    for slug in SERVICE_SLUGS:
        if slug in href:
            return f'/servicos/{slug}/' + fragment

    for slug in BLOG_SLUGS:
        if slug in href:
            return f'/blog/{slug}/' + fragment

    # blog index
    if 'blog/index.html' in href or re.search(r'^\.\./?blog/?$', href):
        return '/blog/' + fragment

    # como-chegar sub-locations (check longer paths first to disambiguate)
    if 'pindamonhangaba/centro' in href:
        return '/como-chegar/pindamonhangaba/centro/' + fragment
    if 'taubate/centro' in href:
        return '/como-chegar/taubate/centro/' + fragment

    for sub in PINDA_SUBS:
        if sub in href:
            return f'/como-chegar/pindamonhangaba/{sub}/' + fragment
    for sub in TAUBATE_SUBS:
        if sub in href:
            return f'/como-chegar/taubate/{sub}/' + fragment

    if 'como-chegar/pindamonhangaba' in href:
        return '/como-chegar/pindamonhangaba/' + fragment
    if 'como-chegar/taubate' in href:
        return '/como-chegar/taubate/' + fragment
    if re.search(r'como-chegar/?(?:index\.html)?$', href):
        return '/como-chegar/' + fragment

    # ---- Filesystem-based resolution for everything else ----

    file_dir = file_path.parent
    try:
        resolved = Path(os.path.normpath(file_dir / href)).resolve()
    except Exception:
        return None

    # If resolved points outside site root, skip
    try:
        rel = resolved.relative_to(BASE)
    except ValueError:
        return None

    # Build candidate paths to check
    candidates = [resolved]
    if resolved.suffix == '.html':
        candidates.append(resolved)
    else:
        candidates.append(resolved / 'index.html')

    target_exists = any(c.exists() for c in candidates)

    if target_exists:
        posix = '/' + rel.as_posix()
        # Path('.') means site root
        if posix in ('/.', '/'):
            posix = '/'
        if posix.endswith('/index.html'):
            posix = posix[: -len('index.html')]
        elif posix == '/index.html':
            posix = '/'
        if posix != '/' and not posix.endswith('/'):
            if '.' not in posix.split('/')[-1]:
                posix += '/'
        result = posix + fragment
        orig = ('/' + rel.as_posix()) + fragment
        return result if result != orig else None
    else:
        # Target doesn't exist — broken relative link
        # Common case: mobile menu uses ../index.html#fragment on depth-2 pages
        # where the intended target is the home page
        if fragment in ROOT_FRAGMENTS:
            return '/' + fragment
        # ../index.html pointing to non-existent dir/index.html
        if href.endswith('index.html'):
            # Treat as home
            return '/' + fragment
        return None


def process_file(file_path):
    try:
        with open(file_path, encoding='utf-8') as f:
            original = f.read()
    except UnicodeDecodeError:
        with open(file_path, encoding='latin-1') as f:
            original = f.read()

    changes = []

    def replacer(m):
        old_href = m.group(1)
        new_href = canonical(old_href, file_path)
        if new_href is not None and new_href != old_href:
            changes.append((old_href, new_href))
            return f'href="{new_href}"'
        return m.group(0)

    updated = re.sub(r'href="([^"]*)"', replacer, original)

    if updated != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated)

    return changes


# ---- Run ----
print('=== Fixing internal links to absolute clean URLs ===\n')
total = 0
for html in sorted(BASE.rglob('*.html')):
    changes = process_file(html)
    if changes:
        rel = html.relative_to(BASE)
        print(f'{rel}  ({len(changes)} changes)')
        for old, new in changes[:8]:
            print(f'    {old!r}')
            print(f'  -> {new!r}')
        if len(changes) > 8:
            print(f'  ... and {len(changes) - 8} more')
        total += len(changes)
        print()

print(f'Total: {total} links fixed across {sum(1 for _ in BASE.rglob("*.html"))} HTML files')
