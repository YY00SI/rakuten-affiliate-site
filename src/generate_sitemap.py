import os
import yaml
from datetime import datetime

def main():
    with open("config/categories.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    base_url = config['site']['base_url'].rstrip('/')
    today = datetime.now().strftime("%Y-%m-%d")
    
    urls = []
    
    # docs配下のindex.htmlを探索
    for root, dirs, files in os.walk("docs"):
        for file in files:
            if file == "index.html":
                # パスをURLに変換
                rel_path = os.path.relpath(root, "docs")
                if rel_path == ".":
                    url = f"{base_url}/"
                else:
                    url = f"{base_url}/{rel_path.replace(os.sep, '/')}/"
                urls.append(url)

    # sitemap.xmlの生成
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        sitemap_content += '  <url>\n'
        sitemap_content += f'    <loc>{url}</loc>\n'
        sitemap_content += f'    <lastmod>{today}</lastmod>\n'
        sitemap_content += '    <changefreq>daily</changefreq>\n'
        sitemap_content += '    <priority>0.8</priority>\n'
        sitemap_content += '  </url>\n'
    
    sitemap_content += '</urlset>'
    
    with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("[INFO] Generated: docs/sitemap.xml")

    # robots.txtの生成
    robots_content = f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml"
    with open("docs/robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("[INFO] Generated: docs/robots.txt")

if __name__ == "__main__":
    main()
