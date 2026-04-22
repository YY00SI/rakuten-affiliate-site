import os
import time
import json
import yaml
import requests
from dotenv import load_dotenv
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

RAKUTEN_APP_ID = os.getenv("RAKUTEN_APP_ID")
RAKUTEN_ACCESS_KEY = os.getenv("RAKUTEN_ACCESS_KEY")
RAKUTEN_AFFILIATE_ID = os.getenv("RAKUTEN_AFFILIATE_ID")

API_ENDPOINT = "https://openapi.openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"
# ※環境によりエンドポイントが異なる場合があるため、動作確認済みの方を使用
API_ENDPOINT = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"

MAJOR_BRANDS = [
    "パナソニック", "Panasonic", "ダイソン", "Dyson", "シャープ", "SHARP", "日立", "HITACHI",
    "ソニー", "SONY", "東芝", "TOSHIBA", "リファ", "ReFa", "ヤーマン", "YA-MAN", "ブラウン", "BRAUN", 
    "バルミューダ", "BALMUDA", "アラジン", "Aladdin", "象印", "ZOJIRUSHI", "タイガー", "TIGER",
    "デロンギ", "DeLonghi", "ハーマンミラー", "Herman Miller", "エルゴヒューマン", "Ergohuman",
    "オカムラ", "OKAMURA", "Anker", "アンカー", "Apple", "アップル", "ロジクール", "Logicool", 
    "シロカ", "siroca", "ルンバ", "iRobot", "テスコム", "TESCOM", "コイズミ", "KOIZUMI", 
    "MTG", "KINUJO", "リュミエリーナ", "Lumielina", "ヘアビューロン"
]

def fetch_items_for_keyword(keyword, params_config):
    """特定のキーワードで商品を取得する内部関数"""
    min_price = params_config.get('min_price', 500)
    max_price = params_config.get('max_price', 9999999)
    
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "accessKey": RAKUTEN_ACCESS_KEY,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "keyword": keyword,
        "hits": 20,
        "sort": params_config.get('sort', 'standard'),
        "imageFlag": 1,
        "minPrice": min_price,
        "maxPrice": max_price,
        "format": "json"
    }
    
    if 'genre_id' in params_config and params_config['genre_id']:
        params['genreId'] = params_config['genre_id']

    try:
        headers = {"Referer": "https://github.com", "Origin": "https://github.com"}
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("Items", [])
        elif response.status_code == 429:
            time.sleep(2)
            return fetch_items_for_keyword(keyword, params_config)
    except Exception as e:
        print(f"[ERROR] API Exception for {keyword}: {str(e)}")
    return []

def fetch_article_items(article):
    """記事単位で商品を取得する (複数ブランド・高精度版)"""
    article_id = article['id']
    params_config = article['rakuten_params']
    
    # 検索キーワードのリスト化 (カンマ区切りまたは単一)
    keywords = params_config['keyword'].split(',')
    max_total_hits = params_config.get('hits', 10)
    
    all_raw_items = []
    for kw in keywords:
        kw = kw.strip()
        print(f"[INFO] {article_id}: 取得中... キーワード: {kw}")
        items = fetch_items_for_keyword(kw, params_config)
        all_raw_items.extend(items)
        time.sleep(0.5)

    processed_items = []
    seen_urls = set()

    for item_raw in all_raw_items:
        item = item_raw.get("Item", item_raw)
        url = item.get("affiliateUrl") or item.get("itemUrl")
        if url in seen_urls:
            continue
        
        item_name = item.get("itemName", "")
        # 除外キーワードチェック
        if "dryer" in article_id and ("タオル" in item_name or "キャップ" in item_name or "スタンド" in item_name):
            continue

        is_major = any(brand.lower() in item_name.lower() for brand in MAJOR_BRANDS)
        
        # 画像URL
        image_url = ""
        images = item.get("mediumImageUrls", [])
        if images and isinstance(images[0], dict):
            image_url = images[0].get("imageUrl", "").split("?")[0]
        elif images and isinstance(images[0], str):
            image_url = images[0].split("?")[0]

        processed_items.append({
            "name": item_name,
            "price": item.get("itemPrice"),
            "url": url,
            "affiliateUrl": item.get("affiliateUrl"),
            "image": image_url,
            "reviewCount": item.get("reviewCount", 0),
            "reviewAverage": item.get("reviewAverage", 0),
            "shopName": item.get("shopName"),
            "caption": item.get("itemCaption", "")[:200],
            "is_major": is_major
        })
        seen_urls.add(url)

    # 1. メジャーブランド優先 2. 価格が高い順(高級記事の場合) 3. レビュー数
    # 高級記事の場合は価格が高いものを上に持ってくる
    processed_items.sort(key=lambda x: (x['is_major'], x['price']), reverse=True)
    
    final_items = processed_items[:max_total_hits]
    print(f"[INFO] {article_id}: 最終確定 {len(final_items)}件 (メジャーブランド数: {sum(1 for i in final_items if i['is_major'])})")
    return final_items

def main():
    config_path = os.path.join("config", "articles.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_dir = os.path.join("data", "products")
    os.makedirs(data_dir, exist_ok=True)

    for article in config.get("articles", []):
        if not article.get("enabled", True) or not article.get("auto_fetch", True):
            continue

        items = fetch_article_items(article)
        if items:
            output_data = {"article_id": article['id'], "updated_at": datetime.now().isoformat(), "items": items}
            with open(os.path.join(data_dir, f"{article['id']}.json"), "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
