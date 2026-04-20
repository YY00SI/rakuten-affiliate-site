import os
import time
import json
import yaml
import requests
from dotenv import load_dotenv
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

# 最新のUUID形式IDとAccess Keyを読み込む
RAKUTEN_APP_ID = os.getenv("RAKUTEN_APP_ID")
RAKUTEN_ACCESS_KEY = os.getenv("RAKUTEN_ACCESS_KEY")
RAKUTEN_AFFILIATE_ID = os.getenv("RAKUTEN_AFFILIATE_ID")

# 【2025年最新】新ドメイン・新パスのエンドポイント
API_ENDPOINT = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"

print(f"[DEBUG] RAKUTEN_APP_ID: {RAKUTEN_APP_ID}")
print(f"[DEBUG] API_ENDPOINT: {API_ENDPOINT}")

def fetch_article_items(article):
    """記事単位で商品を取得する (min_review_countフィルタリング付き)"""
    items = []
    article_id = article['id']
    params_config = article['rakuten_params']
    
    print(f"[INFO] {article_id}: 取得開始 (キーワード: {params_config['keyword']})")

    params = {
        "applicationId": RAKUTEN_APP_ID,
        "accessKey": RAKUTEN_ACCESS_KEY,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "keyword": params_config['keyword'],
        "hits": 30,  # 予備を含めて多めに取得
        "sort": params_config['sort'],
        "imageFlag": 1,
        "minPrice": 500,
        "format": "json"
    }
    
    if 'genre_id' in params_config and params_config['genre_id']:
        params['genreId'] = params_config['genre_id']

    # API呼び出し（リトライ処理付き）
    retry_count = 0
    max_retries = 3
    while retry_count <= max_retries:
        try:
            headers = {
                "Referer": "https://github.com",
                "Referrer": "https://github.com",
                "Origin": "https://github.com"
            }
            
            response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                raw_items = data.get("Items", [])
                
                min_reviews = params_config.get('min_review_count', 0)
                max_hits = params_config.get('hits', 10)

                for item_raw in raw_items:
                    item = item_raw.get("Item", item_raw)
                    
                    review_count = item.get("reviewCount", 0)
                    if review_count < min_reviews:
                        continue

                    # 画像URLの取得
                    image_url = ""
                    images = item.get("mediumImageUrls", [])
                    if images and isinstance(images[0], dict):
                        image_url = images[0].get("imageUrl", "").split("?")[0]
                    elif images and isinstance(images[0], str):
                        image_url = images[0].split("?")[0]

                    items.append({
                        "name": item.get("itemName"),
                        "price": item.get("itemPrice"),
                        "url": item.get("affiliateUrl") or item.get("itemUrl"),
                        "affiliateUrl": item.get("affiliateUrl"),
                        "image": image_url,
                        "reviewCount": review_count,
                        "reviewAverage": item.get("reviewAverage"),
                        "shopName": item.get("shopName"),
                        "caption": item.get("itemCaption", "")[:200]
                    })
                    
                    if len(items) >= max_hits:
                        break
                
                print(f"[INFO] {article_id}: 取得成功 ({len(items)}件)")
                break
            elif response.status_code == 429:
                print(f"[WARN] Rate Limit exceeded. Waiting 3s... (Retry {retry_count+1}/{max_retries})")
                time.sleep(3)
                retry_count += 1
            else:
                print(f"[ERROR] {article_id}: HTTP {response.status_code}")
                print(f"[DEBUG] Response: {response.text}")
                break
        except Exception as e:
            print(f"[ERROR] {article_id}: Exception {str(e)}")
            break
    
    time.sleep(0.5)
    return items

def main():
    config_path = os.path.join("config", "articles.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_dir = os.path.join("data", "products")
    os.makedirs(data_dir, exist_ok=True)

    for article in config.get("articles", []):
        if not article.get("enabled", False):
            continue

        items = fetch_article_items(article)
        
        if items:
            output_data = {
                "article_id": article['id'],
                "updated_at": datetime.now().isoformat(),
                "items": items
            }
            output_path = os.path.join(data_dir, f"{article['id']}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] {article['id']}: {len(items)}件保存完了")

if __name__ == "__main__":
    main()
