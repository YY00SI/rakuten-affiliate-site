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

print(f"[DEBUG] RAKUTEN_APP_ID: {RAKUTEN_APP_ID[:8]}...")
print(f"[DEBUG] RAKUTEN_ACCESS_KEY: {RAKUTEN_ACCESS_KEY[:8]}...")

def fetch_category_items(category):
    """特定カテゴリの商品を取得する (2025年最新 openapi.rakuten.co.jp 対応)"""
    items = []
    category_id = category['id']
    keyword = category['keyword']
    genre_id = category['rakuten_genre_id']
    page_count = category.get('page_count', 1)

    print(f"[INFO] {category_id}: 取得開始 (キーワード: {keyword})")

    for page in range(1, page_count + 1):
        params = {
            "applicationId": RAKUTEN_APP_ID,
            "accessKey": RAKUTEN_ACCESS_KEY,
            "affiliateId": RAKUTEN_AFFILIATE_ID,
            "keyword": keyword,
            "genreId": genre_id,
            "hits": 30,
            "page": page,
            "sort": "-reviewCount",
            "imageFlag": 1,
            "minPrice": 500,
            "format": "json"
        }

        # API呼び出し（リトライ処理付き）
        retry_count = 0
        max_retries = 3
        while retry_count <= max_retries:
            try:
                # 新システムでは Referer チェックが厳しい
                headers = {
                    "Referer": "https://github.com",
                    "Referrer": "https://github.com",
                    "Origin": "https://github.com"
                }
                
                response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    # 新システムのレスポンス構造に合わせる（Items直下に商品があるか、Itemで包まれているか確認）
                    raw_items = data.get("Items", [])
                    for item_raw in raw_items:
                        # 構造が Item キーを持つ場合と持たない場合の両方に対応
                        item = item_raw.get("Item", item_raw)
                        
                        # 画像URLの取得（構造が少し変わっている可能性があるため安全に取得）
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
                            "reviewCount": item.get("reviewCount"),
                            "reviewAverage": item.get("reviewAverage"),
                            "shopName": item.get("shopName"),
                            "caption": item.get("itemCaption", "")[:200]
                        })
                    print(f"[INFO] {category_id}: Page {page} 取得成功 ({len(raw_items)}件)")
                    break
                elif response.status_code == 429:
                    print(f"[WARN] Rate Limit exceeded. Waiting 3s... (Retry {retry_count+1}/{max_retries})")
                    time.sleep(3)
                    retry_count += 1
                else:
                    print(f"[ERROR] {category_id}: HTTP {response.status_code}")
                    print(f"[DEBUG] Response: {response.text}")
                    break
            except Exception as e:
                print(f"[ERROR] {category_id}: Exception {str(e)}")
                break
        
        time.sleep(0.5)

    return items

def main():
    config_path = os.path.join("config", "categories.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_dir = os.path.join("data", "products")
    os.makedirs(data_dir, exist_ok=True)

    for category in config.get("categories", []):
        if not category.get("enabled", False):
            continue

        items = fetch_category_items(category)
        
        if items:
            output_data = {
                "category_id": category['id'],
                "category_name": category['name'],
                "updated_at": datetime.now().isoformat(),
                "items": items
            }
            output_path = os.path.join(data_dir, f"{category['id']}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] {category['id']}: {len(items)}件保存完了")

if __name__ == "__main__":
    main()
