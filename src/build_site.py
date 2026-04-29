import os
import json
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from article_contract import (
    build_article_intro,
    is_published_article,
    merged_forbidden_words,
    resolve_eye_catch,
)


CATEGORY_DESCRIPTIONS = {
    "beauty": "高価格帯の美容家電とセルフケア機器を、仕上がり・使い勝手・後悔ポイントまで踏み込んで比較します。",
    "home": "掃除・調理・スマートホーム領域の中でも、生活効率を大きく変える高単価家電だけを厳選して検証します。",
    "trend": "海外SNSや動画で注目を集めた新奇ガジェットを、実用性と日本での買いやすさの両面から見極めます。",
    "work": "長時間のデスクワークや制作環境を底上げする機材を、疲労軽減と投資価値の観点で比較します。",
}

STATIC_PAGES = [
    {
        "slug": "about",
        "template": "about.html",
        "title": "当サイトについて",
        "description": "LifeTech Select の運営方針と、レビュー解析を重視する理由を紹介します。",
    },
    {
        "slug": "privacy-policy",
        "template": "privacy-policy.html",
        "title": "プライバシーポリシー",
        "description": "LifeTech Select における個人情報とアフィリエイト広告の取り扱いについて説明します。",
    },
    {
        "slug": "how-we-test",
        "template": "how-we-test.html",
        "title": "検証・評価基準",
        "description": "LifeTech Select が商品を比較する際の評価基準と、データ分析の考え方を公開しています。",
    },
]


def prune_stale_article_dirs(output_base, categories, articles, today_date):
    active_dirs = set()
    managed_category_slugs = set()

    for article in articles:
        category = categories.get(article.get("category_id"))
        if not category:
            continue
        managed_category_slugs.add(category["slug"])
        release_date = article.get("release_date", "2000-01-01")
        if article.get("enabled", True) and release_date <= today_date:
            active_dirs.add(os.path.join(output_base, category["slug"], article["slug"]))

    for category_slug in managed_category_slugs:
        category_dir = os.path.join(output_base, category_slug)
        if not os.path.isdir(category_dir):
            continue
        for entry in os.scandir(category_dir):
            if not entry.is_dir():
                continue
            if entry.path not in active_dirs:
                shutil.rmtree(entry.path)
                print(f"[CLEAN] Removed stale article directory: {entry.path}")


def absolute_url(site_config, path=""):
    base_url = site_config["base_url"].rstrip("/")
    if not path:
        return f"{base_url}/"
    return f"{base_url}/{path.strip('/')}/"


def build_page_meta(site_config, *, title, description, path="", image="", kind="website"):
    return {
        "title": title,
        "description": description,
        "url": absolute_url(site_config, path),
        "image": image,
        "kind": kind,
        "og_type": "article" if kind == "article" else "website",
    }


def website_schema(site_config):
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_config["name"],
        "url": absolute_url(site_config),
        "description": site_config["description"],
    }


def breadcrumb_schema(site_config, crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "name": crumb["name"],
                "item": absolute_url(site_config, crumb["path"]),
            }
            for idx, crumb in enumerate(crumbs, start=1)
        ],
    }


def collection_schema(site_config, title, description, path):
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": absolute_url(site_config, path),
        "isPartOf": {"@type": "WebSite", "name": site_config["name"], "url": absolute_url(site_config)},
    }


def article_schema(site_config, article, category, path, image):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.get("h1") or article["title"],
        "description": article["meta_description"],
        "datePublished": article["release_date"],
        "dateModified": datetime.now().strftime("%Y-%m-%d"),
        "image": [image] if image else [],
        "mainEntityOfPage": absolute_url(site_config, path),
        "author": {"@type": "Organization", "name": site_config["name"]},
        "publisher": {"@type": "Organization", "name": site_config["name"]},
        "articleSection": category["name"],
    }


def item_list_schema(site_config, path, items):
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "url": absolute_url(site_config, path),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "name": item["name"],
                "url": item.get("affiliateUrl") or item.get("url", ""),
            }
            for idx, item in enumerate(items, start=1)
        ],
    }


def category_view(category):
    return {
        **category,
        "description": category.get("description") or CATEGORY_DESCRIPTIONS.get(category["id"], ""),
    }


def write_text_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_display_date(release_date):
    try:
        dt = datetime.strptime(release_date, "%Y-%m-%d")
        return dt.strftime("%Y年%m月%d日")
    except Exception:
        return release_date


def load_product_data(article_id):
    product_file = os.path.join("data/products", f"{article_id}.json")
    if not os.path.exists(product_file):
        print(f"[WARN] {article_id} の製品データが見つかりません。")
        return None
    with open(product_file, "r", encoding="utf-8") as f:
        return json.load(f)


def match_article_items(article_config, product_data):
    qa_errors = []

    qa_config = article_config.get("qa_config")
    if qa_config is None:
        qa_errors.append("qa_config が未定義です。")
        return [], qa_errors

    min_price = qa_config.get("min_price", 0)
    if not min_price:
        qa_errors.append("qa_config.min_price が未設定です。")
        return [], qa_errors

    forbidden_words = merged_forbidden_words(article_config)
    required_words = qa_config.get("required_words", [])
    items = product_data.get("items", [])
    products_extra = article_config.get("products_extra", [])

    if not products_extra:
        qa_errors.append("products_extra が未定義です。商品定義なしには公開できません。")
        return [], qa_errors

    matched_items = []
    for extra in products_extra:
        found_item = None
        keyword = extra.get("keyword", "").strip().lower()
        for item in items:
            name = item.get("name", "")
            caption = item.get("caption", "")
            haystack = f"{name} {caption}".lower()

            if keyword and keyword not in haystack:
                continue
            if any(term.lower() in name.lower() for term in forbidden_words):
                continue
            if required_words and not any(req.lower() in haystack for req in required_words):
                continue
            if item.get("price", 0) < min_price:
                continue

            found_item = {**item, "_extra": extra}
            break

        if found_item:
            matched_items.append(found_item)
        else:
            qa_errors.append(f"キーワード '{extra.get('keyword', '')}' に合致する製品が見つかりません。")

    deduped_items = []
    seen_urls = set()
    for item in matched_items:
        dedupe_key = item.get("affiliateUrl") or item.get("url") or item.get("name")
        if dedupe_key in seen_urls:
            continue
        seen_urls.add(dedupe_key)
        deduped_items.append(item)

    return deduped_items, qa_errors


def build_article_view(article_config, matched_items):
    return {
        **article_config,
        "intro": build_article_intro(article_config),
        "resolved_eye_catch": resolve_eye_catch(article_config, matched_items),
        "display_date": build_display_date(article_config.get("release_date", "2000-01-01")),
    }


def prepare_articles(articles, categories, today_date):
    prepared = []

    for article_config in articles:
        if not is_published_article(article_config, today_date):
            continue

        category = categories.get(article_config["category_id"])
        if not category:
            continue

        product_data = load_product_data(article_config["id"])
        if not product_data:
            continue

        matched_items, qa_errors = match_article_items(article_config, product_data)
        if qa_errors:
            print(f"[CRITICAL QA ERROR] {article_config['id']} のビルドを以下の理由でブロックしました:")
            for error in qa_errors:
                print(f"  - {error}")
            continue

        prepared.append(
            {
                "conf": build_article_view(article_config, matched_items),
                "category": category,
                "items": matched_items,
                "path": f"{category['slug']}/{article_config['slug']}/",
                "url": f"./{category['slug']}/{article_config['slug']}/",
            }
        )

    prepared.sort(key=lambda x: x["conf"].get("release_date", "2000-01-01"), reverse=True)
    return prepared


def generate_sitemap_and_robots(site_config, output_base, today_date):
    urls = []
    for root, _, files in os.walk(output_base):
        if "index.html" not in files:
            continue
        rel_path = os.path.relpath(root, output_base)
        if rel_path == ".":
            urls.append(absolute_url(site_config))
        else:
            urls.append(absolute_url(site_config, rel_path.replace(os.sep, "/")))

    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in sorted(urls):
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{url}</loc>")
        sitemap_lines.append(f"    <lastmod>{today_date}</lastmod>")
        sitemap_lines.append("    <changefreq>daily</changefreq>")
        sitemap_lines.append("    <priority>0.8</priority>")
        sitemap_lines.append("  </url>")
    sitemap_lines.append("</urlset>")
    write_text_file(os.path.join(output_base, "sitemap.xml"), "\n".join(sitemap_lines))

    robots_content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {site_config['base_url'].rstrip('/')}/sitemap.xml",
        ]
    )
    write_text_file(os.path.join(output_base, "robots.txt"), robots_content)

def main():
    # 設定読み込み
    with open("config/articles.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    site_config = config['site']
    categories = {c['id']: category_view(c) for c in config['categories']}
    articles = config['articles']
    categories_list = list(categories.values())
    
    # テンプレート環境設定
    env = Environment(loader=FileSystemLoader("templates"))
    article_template = env.get_template("article.html")
    category_template = env.get_template("category_list.html")
    home_template = env.get_template("index.html")
    
    output_base = "docs"
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    today_str = now.strftime("%Y年%m月%d日")

    prune_stale_article_dirs(output_base, categories, articles, today_date)
    processed_articles = prepare_articles(articles, categories, today_date)

    # 1. 各記事詳細ページの生成
    for article_entry in processed_articles:
        article_view = article_entry["conf"]
        category = article_entry["category"]
        matched_items = article_entry["items"]
        article_path = article_entry["path"]
        article_dir = os.path.join(output_base, category["slug"], article_view["slug"])
        os.makedirs(article_dir, exist_ok=True)

        related_articles = []
        for related_entry in processed_articles:
            if related_entry["conf"]["id"] == article_view["id"]:
                continue
            if related_entry["category"]["id"] != category["id"]:
                continue
            related_articles.append(
                {
                    "h1": related_entry["conf"]["h1"],
                    "title": related_entry["conf"]["title"],
                    "eye_catch": related_entry["conf"].get("resolved_eye_catch")
                    or related_entry["conf"].get("eye_catch", ""),
                    "url": f"../../{related_entry['category']['slug']}/{related_entry['conf']['slug']}/",
                }
            )
        related_articles = related_articles[:3]

        html_content = article_template.render(
            site=site_config,
            category=category,
            categories_list=categories_list,
            article=article_view,
            items=matched_items,
            related_articles=related_articles,
            page_meta=build_page_meta(
                site_config,
                title=article_view["title"],
                description=article_view["meta_description"],
                path=article_path,
                image=article_view["resolved_eye_catch"],
                kind="article",
            ),
            page_schemas=[
                website_schema(site_config),
                breadcrumb_schema(
                    site_config,
                    [
                        {"name": "トップ", "path": ""},
                        {"name": category["name"], "path": category["slug"]},
                        {"name": article_view["h1"], "path": article_path},
                    ],
                ),
                article_schema(site_config, article_view, category, article_path, article_view["resolved_eye_catch"]),
                item_list_schema(site_config, article_path, matched_items),
            ],
            today=today_str
        )

        with open(os.path.join(article_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[INFO] 記事生成完了: {category['slug']}/{article_view['slug']}/index.html")

    # 2. カテゴリ一覧ページの生成
    for cat_id, cat in categories.items():
        cat_articles = [a for a in processed_articles if a['category']['id'] == cat_id]
        if not cat_articles:
            continue
            
        cat_dir = os.path.join(output_base, cat['slug'])
        os.makedirs(cat_dir, exist_ok=True)
        
        cat_processed_articles = []
        for a in cat_articles:
            cat_processed_articles.append({
                "conf": a['conf'],
                "url": f"./{a['conf']['slug']}/"
            })

        cat_html = category_template.render(
            site=site_config,
            categories_list=categories_list,
            category=cat,
            articles=cat_processed_articles,
            page_meta=build_page_meta(
                site_config,
                title=f"{cat['name']} のおすすめ記事 | {site_config['name']}",
                description=cat['description'],
                path=f"{cat['slug']}/",
                image=cat_articles[0]['conf'].get('resolved_eye_catch', ''),
                kind="category",
            ),
            page_schemas=[
                website_schema(site_config),
                breadcrumb_schema(
                    site_config,
                    [
                        {"name": "トップ", "path": ""},
                        {"name": cat["name"], "path": cat["slug"]},
                    ],
                ),
                collection_schema(
                    site_config,
                    f"{cat['name']} のおすすめ記事",
                    cat['description'],
                    f"{cat['slug']}/",
                ),
            ],
            today=today_str
        )
        with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(cat_html)

    # 3. トップページの生成
    home_articles = []
    for a in processed_articles:
        home_articles.append({
            "conf": a['conf'],
            "category": a['category'],
            "url": a['url']
        })
        
    home_html = home_template.render(
        site=site_config,
        all_articles=home_articles,
        categories=categories_list,
        categories_list=categories_list,
        page_meta=build_page_meta(
            site_config,
            title=site_config["name"],
            description=site_config["description"],
            path="",
            image=home_articles[0]['conf'].get('resolved_eye_catch', '') if home_articles else "",
            kind="website",
        ),
        page_schemas=[website_schema(site_config), collection_schema(site_config, site_config["name"], site_config["description"], "")],
        today=today_str
    )
    with open(os.path.join(output_base, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_html)

    # 4. 静的ページの再生成
    for page in STATIC_PAGES:
        template = env.get_template(page["template"])
        output_path = os.path.join(output_base, page["slug"], "index.html")
        html = template.render(
            site=site_config,
            categories_list=categories_list,
            page_meta=build_page_meta(
                site_config,
                title=f"{page['title']} | {site_config['name']}",
                description=page["description"],
                path=f"{page['slug']}/",
                image=home_articles[0]['conf'].get('resolved_eye_catch', '') if home_articles else "",
                kind="page",
            ),
            page_schemas=[
                website_schema(site_config),
                breadcrumb_schema(
                    site_config,
                    [
                        {"name": "トップ", "path": ""},
                        {"name": page["title"], "path": page["slug"]},
                    ],
                ),
                collection_schema(site_config, page["title"], page["description"], f"{page['slug']}/"),
            ],
        )
        write_text_file(output_path, html)

    generate_sitemap_and_robots(site_config, output_base, today_date)
    
    print(f"ビルド完了: 全{len(processed_articles)}記事")

if __name__ == "__main__":
    main()
