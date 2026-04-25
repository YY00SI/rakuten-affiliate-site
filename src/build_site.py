import os
import json
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def main():
    # 設定の読み込み
    with open("config/articles.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    site_config = config['site']
    categories = {cat['id']: cat for cat in config['categories']}
    articles = config['articles']
    
    # Jinja2の設定
    env = Environment(loader=FileSystemLoader("templates"))
    article_template = env.get_template("article.html")
    category_list_template = env.get_template("category_list.html")
    index_template = env.get_template("index.html")
    
    # 出力ディレクトリのベース (指示書に従い docs/ を使用)
    output_base = "docs"
    os.makedirs(output_base, exist_ok=True)
    
    data_dir = "data/products"
    now = datetime.now()
    today_str = now.strftime("%Y年%m月%d日")
    today_iso = now.strftime("%Y-%m-%d") # 比較用の日付
    
    # 1. 記事ページの生成
    processed_articles = []
    for art_conf in articles:
        if not art_conf.get("enabled", True):
            continue
            
        # 予約公開チェック: release_date が今日より後ならスキップ
        release_date_raw = str(art_conf.get("release_date", "2000-01-01")).strip()
        if release_date_raw > today_iso:
            print(f"[SKIP] 予約公開待ち: {art_conf['id']} (公開予定: {release_date_raw} / 今日: {today_iso})")
            continue
        
        # 表示用の日付フォーマット変換 (2026-04-23 -> 2026年04月23日)
        try:
            rd_dt = datetime.strptime(release_date_raw, "%Y-%m-%d")
            art_conf['display_date'] = rd_dt.strftime("%Y年%m月%d日")
        except:
            art_conf['display_date'] = release_date_raw

        print(f"[DEBUG] 処理対象記事: {art_conf['id']} (公開日: {art_conf['display_date']})")
            
        file_path = os.path.join(data_dir, f"{art_conf['id']}.json")
        if not os.path.exists(file_path):
            print(f"[WARN] データが見つからないためスキップ: {art_conf['id']}")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            product_data = json.load(f)
            
        category = categories.get(art_conf['category_id'])
        if not category:
            print(f"[ERROR] カテゴリが見つかりません: {art_conf['category_id']} (記事ID: {art_conf['id']})")
            continue
            
        print(f"[DEBUG] カテゴリ一致: {category['id']} -> {category['name']}")
            
        # 出力先ディレクトリ作成
        article_dir = os.path.join(output_base, category['slug'], art_conf['slug'])
        os.makedirs(article_dir, exist_ok=True)
        
        # 関連記事の情報を収集
        related_articles = []
        for rel_id in art_conf.get("related_article_ids", []):
            rel_art = next((a for a in articles if a['id'] == rel_id), None)
            if rel_art:
                rel_cat = categories.get(rel_art['category_id'])
                if rel_cat:
                    # 記事詳細から別の記事詳細への相対パス (../../cat/art/)
                    related_articles.append({
                        "h1": rel_art['h1'],
                        "url": f"../../{rel_cat['slug']}/{rel_art['slug']}/"
                    })
        # Spec v8.2: Strict Product Filter & QA Gate
        items = product_data.get('items', [])
        products_extra = art_conf.get('products_extra', [])
        
        # 解析データに紐付く製品のみを抽出
        matched_items = []
        if products_extra:
            for ex in products_extra:
                found_item = None
                for item in items:
                    if ex['keyword'].lower() in item['name'].lower():
                        item['_extra'] = ex
                        found_item = item
                        break
                
                if found_item:
                    matched_items.append(found_item)
                else:
                    print(f"[CRITICAL ERROR] {art_conf['id']} でキーワード '{ex['keyword']}' に合致する製品が見つかりません。")
                    art_conf['_qa_failed'] = True

        # 2. 全量一致チェック (LTS CEO Policy: 100% Data Integrity)
        if art_conf.get('_qa_failed') or (products_extra and len(matched_items) != len(products_extra)):
            print(f"[BLOCK] {art_conf['id']} のビルドを不完全なマッチングによりブロックしました。")
            continue

        # HTML生成 (matched_items のみを使用)
        html_content = article_template.render(
            site=site_config,
            category=category,
            article=art_conf,
            items=matched_items,
            related_articles=related_articles,
            today=today_str
        )
        
        with open(os.path.join(article_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        
        processed_articles.append({
            "conf": art_conf,
            "category": category,
            "url": f"./{category['slug']}/{art_conf['slug']}/" # トップから見た相対パス
        })
        print(f"[INFO] 記事生成完了: {category['slug']}/{art_conf['slug']}/index.html")
    
    # 処理済み記事を日付順（降順）にソート
    processed_articles.sort(key=lambda x: x['conf'].get('release_date', '2000-01-01'), reverse=True)
    print(f"[DEBUG] トップページ用記事リスト: {[a['conf']['id'] for a in processed_articles]}")

    # 2. カテゴリ一覧ページの生成
    for cat_id, cat in categories.items():
        cat_articles = [a for a in processed_articles if a['category']['id'] == cat_id]
        if not cat_articles:
            continue
            
        cat_dir = os.path.join(output_base, cat['slug'])
        os.makedirs(cat_dir, exist_ok=True)
        
        # カテゴリ一覧から記事詳細への相対パス修正
        cat_processed_articles = []
        for a in cat_articles:
            cat_processed_articles.append({
                "conf": a['conf'],
                "url": f"./{a['conf']['slug']}/"
            })
        
        html_content = category_list_template.render(
            site=site_config,
            category=cat,
            articles=cat_processed_articles,
            today=today_str
        )
        
        with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[INFO] カテゴリページ生成完了: {cat['slug']}/index.html")

    # 3. トップページの生成
    html_content = index_template.render(
        site=site_config,
        categories=categories.values(),
        all_articles=processed_articles,
        today=today_str
    )
    
    with open(os.path.join(output_base, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[INFO] トップページ生成完了: index.html")

    # 4. 固定ページの生成 (About, Privacy Policy, How We Test)
    static_pages = [
        {"tpl": "about.html", "dir": "about"},
        {"tpl": "privacy-policy.html", "dir": "privacy-policy"},
        {"tpl": "how-we-test.html", "dir": "how-we-test"}
    ]
    
    for page in static_pages:
        template = env.get_template(page['tpl'])
        page_dir = os.path.join(output_base, page['dir'])
        os.makedirs(page_dir, exist_ok=True)
        
        html_content = template.render(
            site=site_config,
            today=today_str
        )
        
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[INFO] 固定ページ生成完了: {page['dir']}/index.html")

if __name__ == "__main__":
    main()
