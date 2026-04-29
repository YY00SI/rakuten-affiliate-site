import os
import time
import json
import yaml
import requests
from dotenv import load_dotenv
from datetime import datetime
import re
import urllib.parse
from article_contract import merged_forbidden_words

# 環境変数の読み込み
load_dotenv()

RAKUTEN_APP_ID = os.getenv("RAKUTEN_APP_ID")
RAKUTEN_ACCESS_KEY = os.getenv("RAKUTEN_ACCESS_KEY")
RAKUTEN_AFFILIATE_ID = os.getenv("RAKUTEN_AFFILIATE_ID")

API_ENDPOINT = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"

MAJOR_BRANDS = [
    "パナソニック", "Panasonic", "ダイソン", "Dyson", "シャープ", "SHARP", "日立", "HITACHI",
    "ソニー", "SONY", "東芝", "TOSHIBA", "リファ", "ReFa", "ヤーマン", "YA-MAN", "ブラウン", "BRAUN", 
    "バルミューダ", "BALMUDA", "アラジン", "Aladdin", "象印", "ZOJIRUSHI", "タイガー", "TIGER",
    "デロンギ", "DeLonghi", "ハーマンミラー", "Herman Miller", "エルゴヒューマン", "Ergohuman",
    "オカムラ", "OKAMURA", "Anker", "アンカー", "Apple", "アップル", "ロジクール", "Logicool", 
    "シロカ", "siroca", "ルンバ", "iRobot", "テスコム", "TESCOM", "コイズミ", "KOIZUMI", 
    "MTG", "KINUJO", "リュミエリーナ", "Lumielina", "ヘアビューロン", "オーラルB",
    "HUAWEI", "ファーウェイ", "Soundcore", "SwitchBot", "Nature", "PLAUD", "VOITER", "XGIMI", "Nebula"
]

def fetch_items_for_keyword(keyword, params_config, qa_config, article_id):
    min_price = qa_config.get('min_price', params_config.get('min_price', 500))
    max_price = params_config.get('max_price', 9999999)
    
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "accessKey": RAKUTEN_ACCESS_KEY,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "keyword": keyword[:100], # Limit keyword length
        "hits": 30, 
        "sort": params_config.get('sort', 'standard'),
        "imageFlag": 1,
        "minPrice": min_price,
        "maxPrice": max_price,
        "format": "json"
    }
    
    # genre_id = qa_config.get('genre_id', params_config.get('genre_id', ''))
    # if genre_id:
    #     params['genreId'] = genre_id

    try:
        headers = {"Referer": "https://github.com", "Origin": "https://github.com"}
        # パラメータを個別にエンコードするのは requests に任せるが、念のため検証
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
        
        # 重要な修正: response.text (unicode) を直接使うのではなく、
        # content (bytes) を utf-8 でデコードしてからパースする
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            data = json.loads(content)
            return data.get("Items", [])
        elif response.status_code == 429:
            time.sleep(2)
            return fetch_items_for_keyword(keyword, params_config, qa_config, article_id)
        else:
            print(f"  [API ERR] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  [ERROR] API Exception for {keyword}: {str(e)}")
    return []

def fetch_article_items(article):
    article_id = article['id']
    params_config = article.get('rakuten_params')
    if not params_config: return []
        
    keywords = params_config['keyword'].split(',')
    max_total_hits = params_config.get('hits', 10)
    
    all_raw_items = []
    qa_config = article.get('qa_config', {})
    
    for kw in keywords:
        kw = kw.strip()
        items = fetch_items_for_keyword(kw, params_config, qa_config, article_id)
        all_raw_items.extend(items)
        time.sleep(0.5)

    best_offers = {}
    seen_urls = set()
    
    products_extra = article.get('products_extra', [])
    extra_keywords = [ex.get('keyword') for ex in products_extra if ex.get('keyword')]
    forbidden_words = merged_forbidden_words(article)
    required_words = qa_config.get('required_words', [])

    for item_raw in all_raw_items:
        item = item_raw.get("Item", item_raw)
        url = item.get("affiliateUrl") or item.get("itemUrl")
        if url in seen_urls: continue
        
        name = item.get("itemName", "")
        caption = item.get("itemCaption", "")
        # 禁止ワードチェック
        if any(fw.lower() in name.lower() for fw in forbidden_words):
            continue
        if required_words:
            haystack = f"{name} {caption}".lower()
            if not any(req.lower() in haystack for req in required_words):
                continue

        is_major = any(brand.lower() in name.lower() for brand in MAJOR_BRANDS)
        
        rev_avg = float(item.get("reviewAverage", 0))
        rev_count = int(item.get("reviewCount", 0))
        price = int(item.get("itemPrice", 0))
        
        offer_score = rev_avg * (1.0 + (min(rev_count, 1000) / 500))
        if "公式" in name or "official" in name.lower():
            offer_score *= 1.2 

        item_data = {
            "name": name, "price": price, "url": url, "affiliateUrl": item.get("affiliateUrl"),
            "image": "", "reviewCount": rev_count, "reviewAverage": rev_avg,
            "quality_score": offer_score, "offer_score": offer_score,
            "shopName": item.get("shopName"), "caption": caption[:300],
            "is_major": is_major
        }

        images = item.get("mediumImageUrls", [])
        if images:
            img_url = images[0].get("imageUrl") if isinstance(images[0], dict) else images[0]
            item_data["image"] = img_url.split("?")[0]

        # 重複はスコアが高い方を優先
        if name not in best_offers or item_data['offer_score'] > best_offers[name]['offer_score']:
            best_offers[name] = item_data
        seen_urls.add(url)

    # マスターピース照合 (照合率向上のため、あいまい一致)
    processed_items = []
    selected_urls = set()
    for ekw in extra_keywords:
        found_item = None
        max_score = -1
        for name, item_data in best_offers.items():
            haystack = f"{item_data.get('name', '')} {item_data.get('caption', '')}".lower()
            # 大文字小文字を区別せず、かつキーワードが含まれているか
            if ekw.lower() in haystack:
                if item_data['offer_score'] > max_score:
                    max_score = item_data['offer_score']
                    found_item = item_data
        
        if found_item:
            item_url = found_item.get("url")
            if item_url not in selected_urls:
                processed_items.append(found_item)
                selected_urls.add(item_url)
        else:
            print(f"  [MISS] Keyword '{ekw}' not found in {len(best_offers)} results.")
            if best_offers:
                sample = list(best_offers.keys())[0][:30]
                # print(f"    (Example in results: {sample})")

    # もし extra_keywords が定義されていない場合は、スコア上位を返す
    if not extra_keywords:
        processed_items = list(best_offers.values())

    processed_items.sort(key=lambda x: (x['is_major'], x['quality_score']), reverse=True)
    return processed_items[:max_total_hits]

def main():
    config_path = os.path.join("config", "articles.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_dir = os.path.join("data", "products")
    os.makedirs(data_dir, exist_ok=True)

    for article in config.get("articles", []):
        print(f"[FETCHING] {article['id']}...")
        items = fetch_article_items(article)
        if items:
            output_data = {"article_id": article['id'], "updated_at": datetime.now().isoformat(), "items": items}
            with open(os.path.join(data_dir, f"{article['id']}.json"), "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
        else:
            print(f"  [WARNING] No items fetched for {article['id']}")

if __name__ == "__main__":
    main()
