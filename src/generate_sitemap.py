import os
from datetime import datetime

import yaml


def absolute_url(site_config, path=""):
    base_url = site_config["base_url"].rstrip("/")
    if not path:
        return f"{base_url}/"
    return f"{base_url}/{path.strip('/')}/"


def main():
    with open("config/articles.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    site_config = config["site"]
    today = datetime.now().strftime("%Y-%m-%d")
    urls = []

    for root, _, files in os.walk("docs"):
        if "index.html" not in files:
            continue
        rel_path = os.path.relpath(root, "docs")
        if rel_path == ".":
            urls.append(absolute_url(site_config))
        else:
            urls.append(absolute_url(site_config, rel_path.replace(os.sep, "/")))

    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in sorted(urls):
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{url}</loc>")
        sitemap_lines.append(f"    <lastmod>{today}</lastmod>")
        sitemap_lines.append("    <changefreq>daily</changefreq>")
        sitemap_lines.append("    <priority>0.8</priority>")
        sitemap_lines.append("  </url>")
    sitemap_lines.append("</urlset>")

    with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines))
    print("[INFO] Generated: docs/sitemap.xml")

    robots_content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {site_config['base_url'].rstrip('/')}/sitemap.xml",
        ]
    )
    with open("docs/robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("[INFO] Generated: docs/robots.txt")


if __name__ == "__main__":
    main()
