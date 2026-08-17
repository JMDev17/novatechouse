#!/usr/bin/env python3
"""Static site build script for the white-label template.

Renders every page from templates/ + content/ using the config in config/*.json,
writing the output in place (same paths as the current committed HTML) so the
deploy mechanism (upload the repo root) never has to change.

Usage:
    python scripts/build.py
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
import templating as tpl

ROOT = Path(__file__).parent.parent
CONFIG_DIR = ROOT / "config"
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"


def load_json(relpath, default=None):
    path = CONFIG_DIR / relpath
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_template(relpath):
    return (TEMPLATES_DIR / relpath).read_text(encoding="utf-8")


def read_content(relpath, default=""):
    path = CONTENT_DIR / relpath
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8")


def write_output(relpath, content):
    out_path = ROOT / relpath
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"  wrote {relpath}")


def render_partial(name, ctx):
    return tpl.render(read_template(f"partials/{name}.html"), ctx)


def sorted_by(items, key):
    return sorted(items, key=lambda item: item.get(key, 0))


def wa_link(number, message=None):
    if message:
        return f"https://wa.me/{number}?text={quote(message)}"
    return f"https://wa.me/{number}"


class Site:
    """Loads all config once and exposes the shared, pre-sorted collections
    every page template/partial needs. One instance per build run."""

    def __init__(self):
        self.site = load_json("site.json")
        self.services = load_json("services.json", [])
        self.catalog = load_json("catalog.json", [])
        self.areas = load_json("areas.json", [])
        self.reviews = load_json("reviews.json", [])
        self.posts = load_json("blog/posts.json", [])

    def base_ctx(self):
        ctx = dict(self.site)
        ctx["services_nav"] = sorted_by(self.services, "nav_order")
        ctx["services_carousel"] = sorted_by(self.services, "card_order")
        ctx["services_footer_col1"] = sorted_by(
            [s for s in self.services if s.get("footer_group") == "col1"], "footer_order")
        ctx["services_footer_col2"] = sorted_by(
            [s for s in self.services if s.get("footer_group") == "col2"], "footer_order")
        ctx["services_nav_compact"] = sorted_by(
            [s for s in self.services if s.get("show_in_compact_mobile_menu")], "nav_order")
        ctx["catalog"] = self.catalog
        ctx["catalog_nav"] = sorted_by(self.catalog, "nav_order")
        ctx["areas_regions"] = self.areas
        ctx["reviews"] = self.reviews
        ctx["blog_teaser"] = self.posts[:3]
        ctx["blog_posts"] = self.posts
        return ctx

    def find_service(self, slug):
        return next(s for s in self.services if s["slug"] == slug)

    def find_catalog_item(self, slug):
        return next(c for c in self.catalog if c["slug"] == slug)

    def find_region(self, slug):
        return next(r for r in self.areas if r["slug"] == slug)


DEFAULT_FOOTER_CTA_HEADING = "Pronto para começar?"
DEFAULT_FOOTER_CTA_SUBTITLE = "Fale com a equipe da nossa empresa em {city} e descubra como podemos ajudar."
BLOG_FOOTER_CTA_HEADING = "Ficou com alguma dúvida?"
BLOG_FOOTER_CTA_SUBTITLE = "Fale com a nossa equipe em {city} e tire suas dúvidas."


def home_variant_ctx(site: Site, include_whatsapp_float=True, is_blog_section=False,
                      footer_cta_heading=None, footer_cta_subtitle=None):
    """Shared chrome for the 'home' navbar/footer variant, used by index.html
    AND every blog page (both share the same compact top-3 navbar + rich
    5-column footer — confirmed identical across index.html and blog/*).
    Every blog page (index + posts) uses its own footer CTA wording, distinct
    from the homepage's — confirmed identical across all 4 blog files."""
    ctx = site.base_ctx()
    ctx["is_blog_section"] = is_blog_section
    default_heading = BLOG_FOOTER_CTA_HEADING if is_blog_section else DEFAULT_FOOTER_CTA_HEADING
    default_subtitle = BLOG_FOOTER_CTA_SUBTITLE if is_blog_section else DEFAULT_FOOTER_CTA_SUBTITLE
    ctx["footer_cta_heading"] = footer_cta_heading or default_heading
    ctx["footer_cta_subtitle"] = (footer_cta_subtitle or default_subtitle).format(city=ctx["business"]["city"])
    ctx["navbar"] = render_partial("navbar_home", ctx)
    ctx["mobile_menu"] = render_partial("mobile_menu_home", ctx)
    ctx["footer"] = render_partial("footer_rich", ctx)
    ctx["whatsapp_float"] = render_partial("whatsapp_float", ctx) if include_whatsapp_float else ""
    return ctx


def render_home(site: Site):
    ctx = home_variant_ctx(site, include_whatsapp_float=True)
    html = tpl.render(read_template("pages/index.html"), ctx)
    write_output("index.html", html)


DEFAULT_AREAS_CTA_MESSAGE = "Olá, gostaria de mais informações."


def inner_page_ctx(site: Site, variant, current_service_slug=None,
                    footer_blurb=None, show_contato_link=True,
                    navbar_cta_message=None):
    """variant: 'default' (services/catalog pages) or 'areas'. Builds the
    shared chrome (navbar, mobile menu, footer, whatsapp float) for an inner
    page, honoring the current-page highlight + per-page footer blurb."""
    ctx = site.base_ctx()
    ctx["footer_blurb"] = footer_blurb or site.site.get("footer_simple_default_blurb", "")
    ctx["show_contato_link"] = show_contato_link

    services_nav = [dict(s) for s in ctx["services_nav"]]
    for s in services_nav:
        s["is_current"] = (s["slug"] == current_service_slug)
    ctx["services_nav"] = services_nav

    if variant == "default":
        ctx["navbar"] = render_partial("navbar_inner", ctx)
        ctx["mobile_menu"] = render_partial("mobile_menu_inner", ctx)
    elif variant == "areas":
        ctx["is_current_area"] = True
        ctx["navbar_cta_message"] = quote(navbar_cta_message or DEFAULT_AREAS_CTA_MESSAGE)
        ctx["navbar"] = render_partial("navbar_areas", ctx)
        ctx["mobile_menu"] = render_partial("mobile_menu_areas", ctx)
    else:
        raise ValueError(f"Unknown inner page variant: {variant!r}")

    ctx["footer"] = render_partial("footer_simple", ctx)
    ctx["whatsapp_float"] = render_partial("whatsapp_float", ctx)
    return ctx


def render_services(site: Site):
    if not site.site.get("modules", {}).get("services"):
        return
    tmpl_path = TEMPLATES_DIR / "pages" / "service.html"
    if not tmpl_path.exists():
        print("  (skip) templates/pages/service.html not created yet")
        return
    tmpl = tmpl_path.read_text(encoding="utf-8")
    for service in site.services:
        ctx = inner_page_ctx(
            site, "default",
            current_service_slug=service["slug"],
            footer_blurb=service.get("footer_blurb"),
        )
        ctx.update(service)
        ctx["whatsapp_link_plain"] = wa_link(ctx["contact"]["whatsapp_number"])
        ctx["body"] = tpl.render(read_content(f"services/{service['slug']}.html"), ctx)
        html = tpl.render(tmpl, ctx)
        write_output(f"servicos/{service['slug']}/index.html", html)


def render_catalog(site: Site):
    if not site.site.get("modules", {}).get("catalog"):
        return
    tmpl_path = TEMPLATES_DIR / "pages" / "catalog_item.html"
    if not tmpl_path.exists():
        print("  (skip) templates/pages/catalog_item.html not created yet")
        return
    tmpl = tmpl_path.read_text(encoding="utf-8")
    for item in site.catalog:
        ctx = inner_page_ctx(
            site, "default",
            footer_blurb=item.get("footer_blurb"),
        )
        ctx.update(item)
        ctx["whatsapp_link_message"] = wa_link(ctx["contact"]["whatsapp_number"], item.get("whatsapp_message"))
        ctx["body"] = tpl.render(read_content(f"catalog/{item['slug']}.html"), ctx)
        html = tpl.render(tmpl, ctx)
        write_output(f"{ctx['url_slugs']['catalog']}/{item['slug']}/index.html", html)


def render_areas(site: Site):
    if not site.site.get("modules", {}).get("areas"):
        return
    hub_path = TEMPLATES_DIR / "pages" / "area_hub.html"
    region_path = TEMPLATES_DIR / "pages" / "area_region_index.html"
    sub_path = TEMPLATES_DIR / "pages" / "area_sub.html"

    if hub_path.exists():
        ctx = inner_page_ctx(site, "areas", footer_blurb=load_json("areas_hub_meta.json", {}).get("footer_blurb"), show_contato_link=False)
        hub_meta = load_json("areas_hub_meta.json", {})
        ctx.update(hub_meta)
        ctx["body"] = tpl.render(read_content("areas/index.html"), ctx)
        html = tpl.render(hub_path.read_text(encoding="utf-8"), ctx)
        write_output(f"{ctx['url_slugs']['areas']}/index.html", html)
    else:
        print("  (skip) templates/pages/area_hub.html not created yet")

    for region in site.areas:
        region_meta = read_content(f"areas/{region['slug']}/index.html")
        if region_path.exists():
            ctx = inner_page_ctx(site, "areas", footer_blurb=region.get("footer_blurb"), show_contato_link=False)
            ctx.update(region)
            ctx["body"] = tpl.render(region_meta, ctx)
            html = tpl.render(region_path.read_text(encoding="utf-8"), ctx)
            write_output(f"{ctx['url_slugs']['areas']}/{region['slug']}/index.html", html)
        elif region_meta:
            print(f"  (skip) templates/pages/area_region_index.html not created yet")

        if not sub_path.exists():
            continue
        for sub in region.get("neighborhoods", []):
            ctx = inner_page_ctx(
                site, "areas",
                footer_blurb=sub.get("footer_blurb"),
                navbar_cta_message=sub.get("navbar_cta_message"),
                show_contato_link=False,
            )
            ctx.update(sub)
            ctx["region"] = region
            ctx["body"] = tpl.render(read_content(f"areas/{region['slug']}/{sub['slug']}.html"), ctx)
            html = tpl.render(sub_path.read_text(encoding="utf-8"), ctx)
            write_output(f"{ctx['url_slugs']['areas']}/{region['slug']}/{sub['slug']}/index.html", html)


def render_blog(site: Site):
    if not site.site.get("modules", {}).get("blog"):
        return
    index_path = TEMPLATES_DIR / "pages" / "blog_index.html"
    post_path = TEMPLATES_DIR / "pages" / "blog_post.html"

    if index_path.exists():
        ctx = home_variant_ctx(site, include_whatsapp_float=False, is_blog_section=True)
        ctx["blog_categories"] = load_json("blog/categories.json", [])
        ctx.update(load_json("blog/index_meta.json", {}))
        html = tpl.render(index_path.read_text(encoding="utf-8"), ctx)
        write_output(f"{ctx['url_slugs']['blog']}/index.html", html)
    else:
        print("  (skip) templates/pages/blog_index.html not created yet")

    if not post_path.exists():
        print("  (skip) templates/pages/blog_post.html not created yet")
        return
    tmpl = post_path.read_text(encoding="utf-8")
    for post in site.posts:
        ctx = home_variant_ctx(
            site, include_whatsapp_float=True, is_blog_section=True,
            footer_cta_heading=post.get("footer_cta_heading"),
            footer_cta_subtitle=post.get("footer_cta_subtitle"),
        )
        ctx.update(post)
        ctx["body"] = tpl.render(read_content(f"blog/{post['slug']}.html"), ctx)
        html = tpl.render(tmpl, ctx)
        write_output(f"{ctx['url_slugs']['blog']}/{post['slug']}/index.html", html)


def render_sitemap(site: Site):
    ctx = site.base_ctx()
    domain = ctx["seo"]["base_url"].rstrip("/")
    urls = [("/", "1.0", "weekly")]
    if ctx["modules"].get("blog"):
        urls.append((f"/{ctx['url_slugs']['blog']}/", "0.8", "weekly"))
        for post in site.posts:
            urls.append((f"/{ctx['url_slugs']['blog']}/{post['slug']}/", "0.6", "monthly"))
    if ctx["modules"].get("areas"):
        urls.append((f"/{ctx['url_slugs']['areas']}/", "0.8", "monthly"))
        for region in site.areas:
            urls.append((f"/{ctx['url_slugs']['areas']}/{region['slug']}/", "0.7", "monthly"))
            for sub in region.get("neighborhoods", []):
                urls.append((f"/{ctx['url_slugs']['areas']}/{region['slug']}/{sub['slug']}/", "0.6", "monthly"))
    if ctx["modules"].get("catalog"):
        for item in site.catalog:
            urls.append((f"/{ctx['url_slugs']['catalog']}/{item['slug']}/", "0.8", "monthly"))
    if ctx["modules"].get("services"):
        for service in site.services:
            urls.append((f"/{ctx['url_slugs']['services']}/{service['slug']}/", "0.8", "monthly"))

    entries = "\n".join(
        f"  <url>\n    <loc>{domain}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for path, prio, freq in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    write_output("sitemap.xml", xml)


def main():
    print("Loading config...")
    site = Site()

    print("Rendering style.css...")
    style_ctx = dict(site.base_ctx())
    style_ctx["colors"] = style_ctx["branding"]["colors"]
    style_css = tpl.render(read_template("partials/style.css.tmpl"), style_ctx)
    write_output("style.css", style_css)

    print("Rendering homepage...")
    render_home(site)

    print("Rendering service pages...")
    render_services(site)

    print("Rendering catalog pages...")
    render_catalog(site)

    print("Rendering area (como-chegar) pages...")
    render_areas(site)

    print("Rendering blog...")
    render_blog(site)

    print("Rendering sitemap.xml...")
    render_sitemap(site)

    print("Done.")


if __name__ == "__main__":
    main()
