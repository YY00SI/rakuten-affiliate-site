import os
import json
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def main():
    # 設定読み込み
    with open("config/articles.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    site_config = config['site']
    categories = {c['id']: c for c in config['categories']}
    articles = config['articles']
    
    # テンプレート環境設定
    env = Environment(loader=FileSystemLoader("src/templates"))
    article_template = env.get_template("article.html")
    category_template = env.get_template("category.html")
    home_template = env.get_template("index.html")
    
    output_base = "docs"
    today_str = datetime.now().strftime("%Y年%m月%d日")
    
    processed_articles = []

    # 1. 各記事詳細ページの生成
    for art_conf in articles:
        if not art_conf.get('enabled', True):
            continue
            
        category = categories.get(art_conf['category_id'])
        if not category:
            continue
            
        # 記事ディレクトリの作成
        article_dir = os.path.join(output_base, category['slug'], art_conf['slug'])
        os.makedirs(article_dir, exist_ok=True)
        
        # 製品データの読み込み
        product_file = os.path.join("data/products", f"{art_conf['id']}.json")
        if not os.path.exists(product_file):
            print(f"[WARN] {art_conf['id']} の製品データが見つかりません。")
            continue
            
        with open(product_file, "r", encoding="utf-8") as f:
            product_data = json.load(f)
            
        # 関連記事の抽出 (同じカテゴリから)
        related_articles = []
        for rel_art in articles:
            if rel_art['id'] != art_conf['id'] and rel_art['category_id'] == art_conf['category_id']:
                rel_cat = categories.get(rel_art['category_id'])
                if rel_cat:
                    related_articles.append({
                        "h1": rel_art['h1'],
                        "url": f"../../{rel_cat['slug']}/{rel_art['slug']}/"
                    })

        # --- Spec v8.3: Ultimate QA Gate (Policy: Zero Trash Publication) ---
        qa_errors = []
        
        qa_config = art_conf.get('qa_config')
        if qa_config is None:
            print(f"[CRITICAL QA ERROR] {art_conf['id']}: qa_config が未定義です。ビルドをブロックしました。")
            continue
            
        min_price = qa_config.get('min_price', 0)
        if not min_price:
            print(f"[CRITICAL QA ERROR] {art_conf['id']}: qa_config.min_price が未設定です。")
            continue
            
        forbidden_words = qa_config.get('forbidden_words', [])
        
        items = product_data.get('items', [])
        products_extra = art_conf.get('products_extra', [])
        
        if not products_extra:
            qa_errors.append("products_extra が未定義です。商品定義なしには公開できません。")

        # 解析データに紐付く製品のみを抽出
        matched_items = []
        if not qa_errors and products_extra:
            for ex in products_extra:
                found_item = None
                for item in items:
                    # 1. キーワード一致
                    if ex['keyword'].lower() not in item['name'].lower():
                        continue
                    # 2. 禁止キーワード除外 (スタンド, フィルム等)
                    if any(f_kw in item['name'] for f_kw in forbidden_words):
                        continue
                    # 3. 価格下限チェック
                    if item.get('price', 0) < min_price:
                        continue
                    
                    item['_extra'] = ex
                    found_item = item
                    break
                
                if found_item:
                    matched_items.append(found_item)
                else:
                    qa_errors.append(f"キーワード '{ex['keyword']}' に合致する製品が見つかりません。")

        # 最終ブロック判定
        if qa_errors:
            print(f"[CRITICAL QA ERROR] {art_conf['id']} のビルドを以下の理由でブロックしました:")
            for err in qa_errors:
                print(f"  - {err}")
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
        
        # 最終防衛線: HTML全体のスキャン (Unsplash editor画像チェック)
        if "images.unsplash.com" in html_content:
            # 記事タイトルやアイキャッチでの使用は許可する場合があるが、基本はブロック
            # ただし LTS standards では editorアバターを img タグで直書きしているものを狙う
            if "unsplash.com/photo-" in html_content:
                 print(f"[CRITICAL QA ERROR] {art_conf['id']}: テンプレートにUnsplashプレースホルダーが残存しています。")
                 continue

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
            category=cat,
            articles=cat_processed_articles,
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
        articles=home_articles,
        categories=categories.values(),
        today=today_str
    )
    with open(os.path.join(output_base, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_html)
    
    print(f"ビルド完了: 全{len(processed_articles)}記事")

if __name__ == "__main__":
    main()
