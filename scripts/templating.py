"""Minimal, dependency-free template engine used by build.py.

Supports only what the site templates need:
  {{ path.to.value }}          -- raw substitution (no HTML-escaping: values are
                                   trusted config/content authored by the site owner,
                                   and often already contain markup, e.g. rendered
                                   partials or <br/> in an address).
  {{#each list}}...{{/each}}    -- iterate a list of dicts (fields available directly
                                   in the block scope) or scalars (available as {{.}});
                                   {{@index}}/{{@first}}/{{@last}} are set per iteration.
                                   {{else}} inside an #each renders when the list is
                                   empty/missing.
  {{#if expr}}...{{else}}...{{/if}} -- truthy check on a dotted path.

A custom `{{ }}` token syntax (rather than str.format/string.Template) is used on
purpose: these HTML pages embed literal `{`/`}` pervasively (CSS, GSAP object
literals), which would collide with str.format's brace parsing.
"""
import re

_TAG_RE = re.compile(r'\{\{(#each|#if|/each|/if|else)?\s*([^}]*?)\s*\}\}')


class Node:
    __slots__ = ('kind', 'expr', 'children', 'else_children')

    def __init__(self, kind, expr=None):
        self.kind = kind  # 'root' | 'text' | 'var' | 'each' | 'if'
        self.expr = expr
        self.children = []
        self.else_children = []


def _get(ctx, path):
    if path == '.':
        if isinstance(ctx, dict) and '.' in ctx:
            return ctx['.']
        return ctx
    cur = ctx
    for part in path.split('.'):
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, (list, tuple)):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            cur = getattr(cur, part, None)
    return cur


def _truthy(value):
    if isinstance(value, (list, tuple, dict, str)):
        return len(value) > 0
    return bool(value)


def parse(template):
    root = Node('root')
    stack = [root]
    in_else = [False]
    pos = 0
    for m in _TAG_RE.finditer(template):
        node_top = stack[-1]
        target = node_top.else_children if in_else[-1] else node_top.children
        if m.start() > pos:
            target.append(Node('text', template[pos:m.start()]))
        tagtype, expr = m.group(1), m.group(2).strip()
        if tagtype in ('#each', '#if'):
            child = Node('each' if tagtype == '#each' else 'if', expr)
            target.append(child)
            stack.append(child)
            in_else.append(False)
        elif tagtype == 'else':
            in_else[-1] = True
        elif tagtype in ('/each', '/if'):
            if len(stack) == 1:
                raise ValueError(f"Unmatched {{{{{tagtype}}}}} in template")
            stack.pop()
            in_else.pop()
        else:
            target.append(Node('var', expr))
        pos = m.end()
    if len(stack) != 1:
        raise ValueError(f"Unclosed {{{{#{stack[-1].kind}}}}} block (expr={stack[-1].expr!r})")
    node_top = stack[-1]
    target = node_top.else_children if in_else[-1] else node_top.children
    if pos < len(template):
        target.append(Node('text', template[pos:]))
    return root


def _render_nodes(nodes, ctx):
    return ''.join(_render_node(n, ctx) for n in nodes)


def _render_node(node, ctx):
    if node.kind == 'root':
        return _render_nodes(node.children, ctx)
    if node.kind == 'text':
        return node.expr
    if node.kind == 'var':
        value = _get(ctx, node.expr)
        return '' if value is None else str(value)
    if node.kind == 'if':
        value = _get(ctx, node.expr)
        return _render_nodes(node.children if _truthy(value) else node.else_children, ctx)
    if node.kind == 'each':
        items = _get(ctx, node.expr)
        if not items:
            return _render_nodes(node.else_children, ctx)
        out = []
        n = len(items)
        for i, item in enumerate(items):
            if isinstance(item, dict):
                item_ctx = dict(ctx)
                item_ctx.update(item)
            else:
                item_ctx = dict(ctx)
                item_ctx['.'] = item
            item_ctx['@index'] = i
            item_ctx['@first'] = (i == 0)
            item_ctx['@last'] = (i == n - 1)
            out.append(_render_nodes(node.children, item_ctx))
        return ''.join(out)
    raise ValueError(f"Unknown node kind {node.kind!r}")


def render(template, context):
    return _render_node(parse(template), context)
