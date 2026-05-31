import os
import json
import shutil
import yaml
import re
import time
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from article_contract import (
    build_article_intro,
    is_published_article,
    merged_forbidden_words,
    resolve_eye_catch,
)
from config_loader import load_config


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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
    last_error = None
    for _ in range(5):
        try:
            if os.path.exists(path):
                os.chmod(path, 0o666)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return
        except PermissionError as exc:
            last_error = exc
            time.sleep(0.25)
    raise last_error


def build_display_date(release_date):
    try:
        dt = datetime.strptime(release_date, "%Y-%m-%d")
        return dt.strftime("%Y年%m月%d日")
    except Exception:
        return release_date


def load_product_data(article_id):
    product_file = os.path.join(PROJECT_ROOT, "data", "products", f"{article_id}.json")
    if not os.path.exists(product_file):
        print(f"[WARN] {article_id} の製品データが見つかりません。")
        return None
    with open(product_file, "r", encoding="utf-8") as f:
        return json.load(f)


def compact_text(value, max_length=120):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."


def build_spec_evidence(item):
    caption = item.get("caption", "")
    signal_terms = [
        "重量",
        "サイズ",
        "容量",
        "消費電力",
        "保証",
        "温度",
        "風量",
        "バッテリー",
        "連続",
        "給電",
        "洗浄",
        "自動",
        "対応",
        "ノイズ",
        "静音",
        "防水",
        "解像度",
        "周波数",
        "センサー",
        "フィルター",
        "メンテナンス",
    ]
    hits = [term for term in signal_terms if term in caption]
    return {
        "signals": hits[:4],
        "caption_excerpt": compact_text(caption, 140),
    }


def build_product_evidence(item, article_config):
    review_count = int(item.get("reviewCount") or 0)
    review_average = float(item.get("reviewAverage") or 0)
    spec_evidence = build_spec_evidence(item)

    if review_count >= 300:
        review_strength = "レビュー母数が大きく、評価のブレを比較的読みやすい"
    elif review_count >= 50:
        review_strength = "一定数のレビューがあり、傾向把握に使える"
    elif review_count > 0:
        review_strength = "レビュー母数は少なめ。仕様と販売元の情報も併せて確認"
    else:
        review_strength = "レビュー情報が不足。仕様・価格・販売元を中心に確認"

    selection_reason = item.get("selection_reason", "curated_masterpiece")
    if selection_reason == "hidden_gem":
        selection_label = "口コミ評価から拾った掘り出し物候補"
    else:
        selection_label = "指名買い候補として事前選定"

    return {
        "selection_label": selection_label,
        "review_basis": f"楽天市場の公開レビュー評価 {review_average:.2f} / 件数 {review_count:,}件。{review_strength}。",
        "spec_basis": "商品説明内の仕様シグナル: " + ("、".join(spec_evidence["signals"]) if spec_evidence["signals"] else "明確な仕様語は少なめ"),
        "caption_excerpt": spec_evidence["caption_excerpt"],
        "source_note": "レビュー本文の引用ではなく、楽天APIで取得できる評価・件数・商品説明・価格を根拠にしています。",
    }


def build_generated_hidden_extra(item, article_config):
    return {
        "keyword": item.get("match_keyword") or item.get("name", "")[:20],
        "best_for": "有名ブランド以外も含め、レビュー評価と価格のバランスで候補を広げたい方",
        "scores": {
            criteria.get("id"): min(
                5.0,
                round(float(item.get("reviewAverage") or 0) + min(int(item.get("reviewCount") or 0), 300) / 1000, 1),
            )
            for criteria in article_config.get("test_criteria", [])
            if criteria.get("id")
        },
        "analysis_why": "指名買い候補ではありませんが、楽天市場上のレビュー評価・件数・価格条件を満たしたため、掘り出し物候補として別枠で確認しています。",
        "pros": [
            "レビュー評価と価格のバランスが良い",
            "主要候補より予算を抑えやすい",
        ],
        "critical_cons": "トップメーカー品ほど長期レビューや周辺情報が豊富ではないため、保証条件と販売元の信頼性を必ず確認してください。",
        "maintenance_reality": "消耗品・交換部品・清掃方法が商品ページで明記されているかを購入前に確認する必要があります。",
        "cost_performance": "価格差が明確な場合に限り有力ですが、保証やサポートを含めた総額で判断すべき候補です。",
    }


def build_hidden_gem_views(article_config, product_data, matched_items):
    selected_urls = {item.get("affiliateUrl") or item.get("url") or item.get("name") for item in matched_items}
    hidden_gems = []
    for candidate in product_data.get("hidden_gem_candidates", []):
        dedupe_key = candidate.get("affiliateUrl") or candidate.get("url") or candidate.get("name")
        if not dedupe_key or dedupe_key in selected_urls:
            continue
        item = {
            **candidate,
            "_extra": build_generated_hidden_extra(candidate, article_config),
            "selection_reason": "hidden_gem",
        }
        item["_evidence"] = build_product_evidence(item, article_config)
        hidden_gems.append(item)
        selected_urls.add(dedupe_key)
        if len(hidden_gems) >= 3:
            break
    return hidden_gems


def summarize_article_evidence(article_config, matched_items):
    review_total = sum(int(item.get("reviewCount") or 0) for item in matched_items)
    weighted_total = sum(float(item.get("reviewAverage") or 0) * int(item.get("reviewCount") or 0) for item in matched_items)
    weighted_average = weighted_total / review_total if review_total else 0
    prices = [int(item.get("price") or 0) for item in matched_items if item.get("price")]
    curated_count = sum(1 for item in matched_items if item.get("selection_reason", "curated_masterpiece") != "hidden_gem")
    hidden_count = sum(1 for item in matched_items if item.get("selection_reason") == "hidden_gem")
    keywords = [extra.get("keyword") for extra in article_config.get("products_extra", []) if extra.get("keyword")]

    return {
        "item_count": len(matched_items),
        "review_total": review_total,
        "weighted_average": round(weighted_average, 2) if weighted_average else None,
        "price_min": min(prices) if prices else None,
        "price_max": max(prices) if prices else None,
        "curated_count": curated_count,
        "hidden_count": hidden_count,
        "covered_keywords": keywords,
        "source_types": [
            "楽天市場の商品情報",
            "レビュー評価・件数",
            "商品説明内の仕様表記",
            "編集部の購入後リスク評価",
        ],
    }


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
    hidden_candidates = product_data.get("hidden_gem_candidates", [])
    searchable_items = items + [
        candidate for candidate in hidden_candidates
        if candidate.get("url") not in {item.get("url") for item in items}
    ]
    products_extra = article_config.get("products_extra", [])

    if not products_extra:
        qa_errors.append("products_extra が未定義です。商品定義なしには公開できません。")
        return [], qa_errors

    matched_items = []
    for extra in products_extra:
        found_item = None
        keyword = extra.get("keyword", "").strip().lower()
        for item in searchable_items:
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

            found_item = {
                **item,
                "_extra": extra,
                "selection_reason": item.get("selection_reason", "curated_masterpiece"),
            }
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

    for item in deduped_items:
        item["_evidence"] = build_product_evidence(item, article_config)

    return deduped_items, qa_errors


def build_article_view(article_config, matched_items, product_data=None):
    return {
        **article_config,
        "intro": build_article_intro(article_config),
        "resolved_eye_catch": resolve_eye_catch(article_config, matched_items),
        "display_date": build_display_date(article_config.get("release_date", "2000-01-01")),
        "evidence_summary": summarize_article_evidence(article_config, matched_items),
        "hidden_gem_candidates": build_hidden_gem_views(article_config, product_data or {}, matched_items),
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
                "conf": build_article_view(article_config, matched_items, product_data),
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
    config = load_config()
    
    site_config = config['site']
    categories = {c['id']: category_view(c) for c in config['categories']}
    articles = config['articles']
    categories_list = list(categories.values())
    
    # テンプレート環境設定
    env = Environment(loader=FileSystemLoader(os.path.join(PROJECT_ROOT, "templates")))
    article_template = env.get_template("article.html")
    category_template = env.get_template("category_list.html")
    home_template = env.get_template("index.html")
    
    output_base = os.path.join(PROJECT_ROOT, "docs")
    override_today = os.getenv("LTS_TODAY", "").strip()
    now = datetime.strptime(override_today, "%Y-%m-%d") if override_today else datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    today_str = now.strftime("%Y年%m月%d日")

    prune_stale_article_dirs(output_base, categories, articles, today_date)
    processed_articles = prepare_articles(articles, categories, today_date)
    target_ids = {
        item.strip()
        for item in os.getenv("LTS_ARTICLE_IDS", "").split(",")
        if item.strip()
    }
    if target_ids:
        processed_articles = [
            entry for entry in processed_articles
            if entry["conf"].get("id") in target_ids
        ]

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

        write_text_file(os.path.join(article_dir, "index.html"), html_content)
        print(f"[INFO] 記事生成完了: {category['slug']}/{article_view['slug']}/index.html")

    if target_ids:
        print(f"[INFO] 対象記事のみ生成完了: {', '.join(sorted(target_ids))}")
        return

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
        write_text_file(os.path.join(cat_dir, "index.html"), cat_html)

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
    write_text_file(os.path.join(output_base, "index.html"), home_html)

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
