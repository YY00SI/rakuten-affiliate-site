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

# 徹底排除キーワード (これらが含まれる場合は即座にスキップ)
NEGATIVE_KEYWORDS = [
    "ふるさと納税", "返礼品", "中古", "訳あり", "ジャンク", "部品", "パーツ", "クリーニング", "修理",
    "対応", "互換", "専用", "セット", "レンタル", "保証", "延長", "設置", "工事", "リサイクル",
    "目録", "景品", "カタログギフト", "パネル", "当選", "引換券",
    "シェーバー", "髭剃り", "バリカン", "脱毛器", "電池", "充電池", "バッテリー"
]

def fetch_items_for_keyword(keyword, params_config, article_id):
    """特定のキーワードで商品を取得する内部関数"""
    min_price = params_config.get('min_price', 500)
    max_price = params_config.get('max_price', 9999999)
    
    # 記事IDから主要キーワードを推測
    core_kws = []
    category_neg_kws = ["テーブル", "デスク", "マット", "カバー", "ケース", "フィルター", "ブラシ"]
    
    if "dryer" in article_id: core_kws = ["ドライヤー", "dryer", "ヘア"]
    elif "vacuum" in article_id: core_kws = ["掃除機", "ルンバ", "クリーナー"]
    elif "chair" in article_id: core_kws = ["チェア", "椅子", "デスクチェア"]
    elif "speaker" in article_id: core_kws = ["スピーカー"]
    elif "recorder" in article_id: core_kws = ["レコーダー", "録音"]
    elif "lock" in article_id: core_kws = ["ロック", "スマートロック", "鍵"]
    elif "coffee" in article_id: core_kws = ["コーヒー", "珈琲", "coffee"]

    # 記事テーマに関連する単語は除外ワードから外す
    final_neg_kws = NEGATIVE_KEYWORDS + category_neg_kws
    for cw in core_kws:
        if cw in final_neg_kws:
            final_neg_kws.remove(cw)

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
    
    if 'genre_id' in params_config and params_config['genre_id']:
        params['genreId'] = params_config['genre_id']

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

                # 3. 信頼性チェック (レビュー0件かつ高額な「景品ノイズ」を排除)
                # ただし、発売直後の新製品（is_major）の可能性もあるため、主要ブランド以外はレビュー必須
                is_major = any(brand.lower() in name.lower() for brand in MAJOR_BRANDS)
                if not is_major and rev_count == 0:
                    continue

                valid_items.append(item_raw)
            return valid_items
        elif response.status_code == 429:
            time.sleep(2)
            return fetch_items_for_keyword(keyword, params_config, article_id)
    except Exception as e:
        print(f"[ERROR] API Exception for {keyword}: {str(e)}")
    return []

import re

def normalize_item_name(name):
    """商品名から装飾語を除去し、製品のコア名（型番等）を抽出する"""
    # 除去する装飾語パターン
    patterns = [
        r"【[^】]+】", r"\[[^\]]+\]", r"送料無料", r"ポイント\d+倍", r"あす楽", 
        r"公式", r"国内正規品", r"正規販売店", r"限定", r"最大\d+%Pバック"
    ]
    norm_name = name
    for p in patterns:
        norm_name = re.sub(p, "", norm_name)
    # 空白除去と小文字化
    return re.sub(r"\s+", "", norm_name).lower()

def fetch_article_items(article):
    """記事単位で商品を取得する (重複排除・最良オファー選定版)"""
    article_id = article['id']
    params_config = article['rakuten_params']
    
    keywords = params_config['keyword'].split(',')
    max_total_hits = params_config.get('hits', 10)
    
    all_raw_items = []
    for kw in keywords:
        kw = kw.strip()
        items = fetch_items_for_keyword(kw, params_config, article_id)
        all_raw_items.extend(items)
        time.sleep(0.5)

    # 同一製品の名寄せ用辞書 {正規化名: 最良の商品データ}
    best_offers = {}
    seen_urls = set()

    for item_raw in all_raw_items:
        item = item_raw.get("Item", item_raw)
        url = item.get("affiliateUrl") or item.get("itemUrl")
        if url in seen_urls: continue
        
        name = item.get("itemName", "")
        norm_name = normalize_item_name(name)
        
        # 主要メーカー判定
        is_major = any(brand.lower() in name.lower() for brand in MAJOR_BRANDS)
        
        # スコア計算 (レビュー数・評価・価格のバランス)
        rev_avg = float(item.get("reviewAverage", 0))
        rev_count = int(item.get("reviewCount", 0))
        price = int(item.get("itemPrice", 0))
        
        # 最良オファー判定用の内部スコア (レビュー数重視)
        offer_score = rev_avg * (1.0 + (min(rev_count, 1000) / 500))
        if "公式" in name or "official" in name.lower():
            offer_score *= 1.2 # 公式ショップを優先

        item_data = {
            "name": name,
            "price": price,
            "url": url,
            "affiliateUrl": item.get("affiliateUrl"),
            "image": "", # 後ほど取得
            "reviewCount": rev_count,
            "reviewAverage": rev_avg,
            "quality_score": offer_score, # この製品自体の魅力度
            "offer_score": offer_score,   # 同一製品内での優位性
            "shopName": item.get("shopName"),
            "caption": item.get("itemCaption", "")[:300],
            "is_major": is_major
        }

        # 画像URL取得
        images = item.get("mediumImageUrls", [])
        if images:
            item_data["image"] = (images[0].get("imageUrl") if isinstance(images[0], dict) else images[0]).split("?")[0]

        # 同一製品（正規化名が前方一致または酷似）の重複排除
        # 簡易的に最初の15文字が一致すれば同一視（型番対応）
        product_key = norm_name[:15]
        if product_key not in best_offers or item_data["offer_score"] > best_offers[product_key]["offer_score"]:
            best_offers[product_key] = item_data
        
        seen_urls.add(url)

    # 最終的なリスト作成
    processed_items = list(best_offers.values())

    # ランキング全体のソート: 主要メーカーかつ総合スコアが高い順
    processed_items.sort(key=lambda x: (x['is_major'], x['quality_score']), reverse=True)
    
    final_items = processed_items[:max_total_hits]
    print(f"[INFO] {article_id}: 重複排除後 {len(final_items)}件 (全候補: {len(all_raw_items)})")
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
