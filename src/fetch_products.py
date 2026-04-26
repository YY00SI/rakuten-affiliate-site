import os
import time
import json
import yaml
import requests
from dotenv import load_dotenv
from datetime import datetime
import re

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
    "MTG", "KINUJO", "リュミエリーナ", "Lumielina", "ヘアビューロン", "オーラルB"
]

def fetch_items_for_keyword(keyword, params_config, qa_config, article_id):
    """特定のキーワードで商品を取得する内部関数"""
    min_price = qa_config.get('min_price', params_config.get('min_price', 500))
    max_price = params_config.get('max_price', 9999999)
    
    # qa_config から必須ワードと除外ワードを取得
    core_kws = qa_config.get('required_words', [])
    final_neg_kws = qa_config.get('forbidden_words', [])

    params = {
        "applicationId": RAKUTEN_APP_ID,
        "accessKey": RAKUTEN_ACCESS_KEY,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "keyword": keyword,
        "hits": 30, 
        "sort": params_config.get('sort', 'standard'),
        "imageFlag": 1,
        "minPrice": min_price,
        "maxPrice": max_price,
        "format": "json"
    }
    
    genre_id = qa_config.get('genre_id', params_config.get('genre_id', ''))
    if genre_id:
        params['genreId'] = genre_id

    try:
        headers = {"Referer": "https://github.com", "Origin": "https://github.com"}
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            raw_items = response.json().get("Items", [])
            valid_items = []
            for item_raw in raw_items:
                item = item_raw.get("Item", item_raw)
                name = item.get("itemName", "")
                rev_count = int(item.get("reviewCount", 0))
                
                # 1. 徹底排除キーワードチェック
                if any(neg in name for neg in final_neg_kws):
                    continue
                
                # 2. 記事のテーマが含まれているか
                if core_kws and not any(ck in name for ck in core_kws):
                    continue

                # 3. 信頼性チェック
                is_major = any(brand.lower() in name.lower() for brand in MAJOR_BRANDS)
                if not is_major and rev_count == 0:
                    continue

                valid_items.append(item_raw)
            return valid_items
        elif response.status_code == 429:
            time.sleep(2)
            return fetch_items_for_keyword(keyword, params_config, qa_config, article_id)
    except Exception as e:
        print(f"[ERROR] API Exception for {keyword}: {str(e)}")
    return []

def normalize_item_name(name):
    """商品名から装飾語を除去し、製品のコア名（型番等）を抽出する"""
    patterns = [
        r"【[^】]+】", r"\[[^\]]+\]", r"送料無料", r"ポイント\d+倍", r"あす楽", 
        r"公式", r"国内正規品", r"正規販売店", r"限定", r"最大\d+%Pバック"
    ]
    norm_name = name
    for p in patterns:
        norm_name = re.sub(p, "", norm_name)
    return re.sub(r"\s+", "", norm_name).lower()

def fetch_article_items(article):
    """記事単位で商品を取得する"""
    article_id = article['id']
    params_config = article.get('rakuten_params')
    
    if not params_config:
        return []
        
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

    for item_raw in all_raw_items:
        item = item_raw.get("Item", item_raw)
        url = item.get("affiliateUrl") or item.get("itemUrl")
        if url in seen_urls: continue
        
        name = item.get("itemName", "")
        
        # 悪質なノイズ商品を完全に排除 (YAMLから取得した禁止ワードを使用)
        forbidden_words = qa_config.get('forbidden_words', [])
        if any(kw in name for kw in forbidden_words):
            continue

        norm_name = normalize_item_name(name)
        is_major = any(brand.lower() in name.lower() for brand in MAJOR_BRANDS)
        
        rev_avg = float(item.get("reviewAverage", 0))
        rev_count = int(item.get("reviewCount", 0))
        price = int(item.get("itemPrice", 0))
        
        offer_score = rev_avg * (1.0 + (min(rev_count, 1000) / 500))
        if "公式" in name or "official" in name.lower():
            offer_score *= 1.2 

        item_data = {
            "name": name,
            "price": price,
            "url": url,
            "affiliateUrl": item.get("affiliateUrl"),
            "image": "", 
            "reviewCount": rev_count,
            "reviewAverage": rev_avg,
            "quality_score": offer_score, 
            "offer_score": offer_score,   
            "shopName": item.get("shopName"),
            "caption": item.get("itemCaption", "")[:300],
            "is_major": is_major
        }

        images = item.get("mediumImageUrls", [])
        if images:
            item_data["image"] = (images[0].get("imageUrl") if isinstance(images[0], dict) else images[0]).split("?")[0]

        product_key = norm_name[:15]
        
        for ekw in extra_keywords:
            clean_ekw = re.sub(r"[^a-zA-Z0-9ぁ-んァ-ン一-龥]", "", ekw).lower()
            clean_name = re.sub(r"[^a-zA-Z0-9ぁ-んァ-ン一-龥]", "", name).lower()
            
            if clean_ekw in clean_name or ekw.lower() in name.lower():
                product_key = f"MASTERPIECE_{ekw}"
                break
                
        if product_key not in best_offers or item_data["offer_score"] > best_offers[product_key]["offer_score"]:
            best_offers[product_key] = item_data
        
        seen_urls.add(url)

    if extra_keywords:
        processed_items = []
        for ekw in extra_keywords:
            m_key = f"MASTERPIECE_{ekw}"
            if m_key in best_offers:
                processed_items.append(best_offers[m_key])
            else:
                print(f"  [MISS] Keyword '{ekw}' not found in results.")
    else:
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
        if not article.get("enabled", True) or not article.get("auto_fetch", True):
            continue

        print(f"[FETCHING] {article['id']}...")
        items = fetch_article_items(article)
        if items:
            output_data = {"article_id": article['id'], "updated_at": datetime.now().isoformat(), "items": items}
            with open(os.path.join(data_dir, f"{article['id']}.json"), "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
