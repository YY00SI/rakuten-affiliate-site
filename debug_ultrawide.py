"""ultrawide-monitor-ranking の MISS 原因を特定する診断スクリプト"""
import os, json, time, yaml, requests
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"
APP_ID = os.getenv("RAKUTEN_APP_ID")
ACCESS_KEY = os.getenv("RAKUTEN_ACCESS_KEY")
AFF_ID = os.getenv("RAKUTEN_AFFILIATE_ID")

def search(keyword, min_price=50000):
    params = {
        "applicationId": APP_ID, "accessKey": ACCESS_KEY, "affiliateId": AFF_ID,
        "keyword": keyword[:100], "hits": 30, "sort": "-reviewCount",
        "imageFlag": 1, "minPrice": min_price, "maxPrice": 9999999, "format": "json"
    }
    headers = {"Referer": "https://github.com", "Origin": "https://github.com"}
    r = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return data.get("Items", [])
    else:
        print(f"  API ERR {r.status_code}: {r.text[:200]}")
        return []

# --- 現在の rakuten_params.keyword ---
current_keywords = [
    "Dell モニター ウルトラワイド",
    "LG ウルトラワイド",
    "BenQ モニター ワイド",
    "HUAWEI MateView",
]

# --- products_extra のキーワード ---
extra_kws = ["Dell", "LG", "BenQ", "HUAWEI"]

print("=" * 60)
print("STEP 1: 現在のキーワードごとの API 戻り件数と商品名サンプル")
print("=" * 60)
all_items = []
for kw in current_keywords:
    print(f"\n--- 検索: '{kw}' ---")
    items = search(kw)
    print(f"  ヒット数: {len(items)}")
    for i, raw in enumerate(items[:5]):
        item = raw.get("Item", raw)
        name = item.get("itemName", "")[:80]
        price = item.get("itemPrice", 0)
        print(f"  [{i+1}] ¥{price:,} | {name}")
    all_items.extend(items)
    time.sleep(1)

print(f"\n合計取得件数 (重複含む): {len(all_items)}")

print("\n" + "=" * 60)
print("STEP 2: 取得結果の中に extra_keywords が存在するか確認")
print("=" * 60)
for ekw in extra_kws:
    found = []
    for raw in all_items:
        item = raw.get("Item", raw)
        name = item.get("itemName", "")
        caption = item.get("itemCaption", "")
        haystack = f"{name} {caption}".lower()
        if ekw.lower() in haystack:
            found.append(name[:60])
    print(f"\n  '{ekw}': {len(found)} 件マッチ")
    for f in found[:3]:
        print(f"    -> {f}")

print("\n" + "=" * 60)
print("STEP 3: より広いキーワードでの代替テスト")
print("=" * 60)
alt_keywords = [
    "ウルトラワイドモニター",
    "ウルトラワイド 曲面",
    "Dell ウルトラワイド モニター",
    "MateView",
]
for kw in alt_keywords:
    print(f"\n--- 代替検索: '{kw}' ---")
    items = search(kw)
    print(f"  ヒット数: {len(items)}")
    for i, raw in enumerate(items[:3]):
        item = raw.get("Item", raw)
        name = item.get("itemName", "")[:80]
        print(f"  [{i+1}] {name}")
    # extra_keywords のマッチ状況
    for ekw in extra_kws:
        cnt = sum(1 for raw in items
                  if ekw.lower() in f"{raw.get('Item', raw).get('itemName','')} {raw.get('Item', raw).get('itemCaption','')}".lower())
        if cnt > 0:
            print(f"    -> '{ekw}' が {cnt} 件でマッチ")
    time.sleep(1)

print("\n診断完了。上記結果をコピーしてください。")
