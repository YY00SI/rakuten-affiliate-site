from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
STOCK_PATH = ROOT / "config" / "articles_stock.yaml"

FORBIDDEN = [
    "中古",
    "訳あり",
    "ジャンク",
    "ふるさと納税",
    "返礼品",
    "レンタル",
    "部品",
    "パーツ",
    "ケース",
    "カバー",
    "交換用",
    "フィルターのみ",
    "スタンドのみ",
    "ケーブルのみ",
]

CRITERIA = [
    ("fit", "用途との合いやすさ"),
    ("install", "設置と運用の現実"),
    ("value", "価格と長期満足"),
]

THEMES = [
    ("2026-07-01", "refrigerator-450l-ranking", "home", "refrigerator-450l", "450Lクラス冷蔵庫", "冷蔵庫", 100000, "パナソニック 冷蔵庫, 三菱 冷蔵庫", ["冷蔵庫 450L", "冷蔵庫 500L"], ["パナソニック", "三菱"]),
    ("2026-07-02", "upright-freezer-ranking", "home", "upright-freezer", "前開き冷凍庫", "冷凍庫", 30000, "アイリスオーヤマ 冷凍庫, 三菱 冷凍庫", ["前開き 冷凍庫", "家庭用 冷凍庫"], ["アイリスオーヤマ", "三菱"]),
    ("2026-07-03", "dehumidifier-dryer-ranking", "home", "dehumidifier-dryer", "衣類乾燥除湿機", "除湿", 25000, "パナソニック 除湿機, コロナ 除湿機", ["衣類乾燥除湿機", "除湿機 コンプレッサー"], ["パナソニック", "コロナ"]),
    ("2026-07-04", "premium-humidifier-ranking", "home", "premium-humidifier", "高性能加湿器", "加湿器", 15000, "ダイニチ 加湿器, 象印 加湿器", ["加湿器 大容量", "スチーム式 加湿器"], ["ダイニチ", "象印"]),
    ("2026-07-05", "water-purifier-ranking", "home", "water-purifier", "家庭用浄水器", "浄水器", 10000, "パナソニック 浄水器, 東レ トレビーノ 浄水器", ["浄水器 蛇口直結", "据置型 浄水器"], ["パナソニック", "トレビーノ"]),
    ("2026-07-06", "smart-toilet-seat-ranking", "home", "smart-toilet-seat", "温水洗浄便座", "温水洗浄便座", 25000, "TOTO 温水洗浄便座, パナソニック 温水洗浄便座", ["ウォシュレット", "温水洗浄便座"], ["TOTO", "パナソニック"]),
    ("2026-07-07", "induction-cooktop-ranking", "home", "induction-cooktop", "据置型IHクッキングヒーター", "IH", 20000, "パナソニック IHクッキングヒーター, アイリスオーヤマ IHクッキングヒーター", ["IHクッキングヒーター 2口", "据置 IH"], ["パナソニック", "アイリスオーヤマ"]),
    ("2026-07-08", "home-bakery-ranking", "home", "home-bakery", "ホームベーカリー", "ホームベーカリー", 10000, "パナソニック ホームベーカリー, シロカ ホームベーカリー", ["ホームベーカリー", "パン焼き機"], ["パナソニック", "シロカ"]),
    ("2026-07-09", "vacuum-sealer-ranking", "home", "vacuum-sealer", "真空パック機", "真空", 8000, "FoodSaver 真空パック, アイリスオーヤマ 真空パック", ["真空パック機", "フードシーラー"], ["FoodSaver", "アイリスオーヤマ"]),
    ("2026-07-10", "sous-vide-cooker-ranking", "home", "sous-vide-cooker", "低温調理器", "低温調理", 10000, "BONIQ 低温調理器, アイリスオーヤマ 低温調理器", ["低温調理器", "真空低温調理"], ["BONIQ", "アイリスオーヤマ"]),
    ("2026-07-11", "inverter-generator-ranking", "trend", "inverter-generator", "インバーター発電機", "発電機", 50000, "ホンダ 発電機, ヤマハ 発電機", ["インバーター発電機", "防災 発電機"], ["ホンダ", "ヤマハ"]),
    ("2026-07-12", "impact-driver-ranking", "work", "impact-driver", "充電式インパクトドライバー", "インパクト", 15000, "マキタ インパクトドライバー, HiKOKI インパクトドライバー", ["インパクトドライバー 充電式", "電動工具 インパクト"], ["マキタ", "HiKOKI"]),
    ("2026-07-13", "high-pressure-washer-ranking", "home", "high-pressure-washer", "高圧洗浄機", "高圧洗浄機", 15000, "ケルヒャー 高圧洗浄機, マキタ 高圧洗浄機", ["高圧洗浄機 家庭用", "洗車 高圧洗浄機"], ["ケルヒャー", "マキタ"]),
    ("2026-07-14", "robotic-lawn-mower-ranking", "home", "robotic-lawn-mower", "ロボット芝刈り機", "芝刈", 80000, "ハスクバーナ ロボット芝刈機, Navimow 芝刈り機", ["ロボット 芝刈り機", "自動 芝刈機"], ["ハスクバーナ", "Navimow"]),
    ("2026-07-15", "cordless-lawn-mower-ranking", "home", "cordless-lawn-mower", "充電式芝刈り機", "芝刈", 30000, "マキタ 芝刈り機, 京セラ 芝刈り機", ["充電式 芝刈り機", "電動 芝刈機"], ["マキタ", "京セラ"]),
    ("2026-07-16", "sewing-machine-ranking", "home", "sewing-machine", "コンピューターミシン", "ミシン", 30000, "JUKI ミシン, ブラザー ミシン", ["コンピューターミシン", "家庭用 ミシン"], ["JUKI", "ブラザー"]),
    ("2026-07-17", "overlock-sewing-machine-ranking", "home", "overlock-sewing-machine", "ロックミシン", "ロックミシン", 30000, "JUKI ロックミシン, ベビーロック ロックミシン", ["ロックミシン", "4本糸 ロックミシン"], ["JUKI", "ベビーロック"]),
    ("2026-07-18", "drawing-tablet-ranking", "work", "drawing-tablet", "液晶ペンタブレット", "液晶タブレット", 30000, "Wacom 液晶タブレット, XP-Pen 液晶タブレット", ["液晶ペンタブレット", "液タブ"], ["Wacom", "XP-Pen"]),
    ("2026-07-19", "tablet-pc-ranking", "work", "tablet-pc", "高性能タブレット", "タブレット", 40000, "iPad タブレット, Galaxy Tab タブレット", ["タブレット 11インチ", "高性能 タブレット"], ["iPad", "Galaxy Tab"]),
    ("2026-07-20", "gaming-router-ranking", "work", "gaming-router", "ゲーミングルーター", "ルーター", 15000, "ASUS ゲーミングルーター, TP-Link ゲーミングルーター", ["ゲーミングルーター", "WiFi 7 ルーター"], ["ASUS", "TP-Link"]),
    ("2026-07-21", "camera-gimbal-ranking", "trend", "camera-gimbal", "カメラ用ジンバル", "ジンバル", 20000, "DJI ジンバル, ZHIYUN ジンバル", ["カメラ ジンバル", "スタビライザー カメラ"], ["DJI", "ZHIYUN"]),
    ("2026-07-22", "astronomical-telescope-ranking", "trend", "astronomical-telescope", "天体望遠鏡", "天体望遠鏡", 20000, "ビクセン 天体望遠鏡, Celestron 天体望遠鏡", ["天体望遠鏡 初心者", "自動導入 天体望遠鏡"], ["ビクセン", "Celestron"]),
    ("2026-07-23", "premium-binoculars-ranking", "trend", "premium-binoculars", "高性能双眼鏡", "双眼鏡", 15000, "ニコン 双眼鏡, キヤノン 双眼鏡", ["双眼鏡 防振", "コンサート 双眼鏡"], ["ニコン", "キヤノン"]),
    ("2026-07-24", "treadmill-ranking", "beauty", "treadmill", "家庭用ルームランナー", "ルームランナー", 30000, "アルインコ ルームランナー, Horizon ルームランナー", ["ルームランナー 家庭用", "ランニングマシン"], ["アルインコ", "Horizon"]),
    ("2026-07-25", "exercise-bike-ranking", "beauty", "exercise-bike", "フィットネスバイク", "フィットネスバイク", 15000, "アルインコ フィットネスバイク, STEADY フィットネスバイク", ["フィットネスバイク 静音", "スピンバイク"], ["アルインコ", "STEADY"]),
    ("2026-07-26", "rowing-machine-ranking", "beauty", "rowing-machine", "ローイングマシン", "ローイングマシン", 20000, "Concept2 ローイングマシン, MERACH ローイングマシン", ["ローイングマシン", "家庭用 ローイング"], ["Concept2", "MERACH"]),
    ("2026-07-27", "foot-massager-ranking", "beauty", "foot-massager", "フットマッサージャー", "フットマッサージ", 15000, "フジ医療器 フットマッサージャー, スライヴ フットマッサージャー", ["フットマッサージャー", "足 マッサージ機"], ["フジ医療器", "スライヴ"]),
    ("2026-07-28", "massage-chair-ranking", "beauty", "massage-chair", "マッサージチェア", "マッサージチェア", 100000, "フジ医療器 マッサージチェア, パナソニック マッサージチェア", ["マッサージチェア", "高級 マッサージチェア"], ["フジ医療器", "パナソニック"]),
    ("2026-07-29", "automatic-pet-feeder-ranking", "home", "automatic-pet-feeder", "自動給餌器", "自動給餌器", 10000, "PETKIT 自動給餌器, うちのこエレクトリック 自動給餌器", ["自動給餌器 カメラ", "ペット 自動給餌器"], ["PETKIT", "うちのこエレクトリック"]),
    ("2026-07-30", "pet-camera-ranking", "home", "pet-camera", "ペットカメラ", "カメラ", 10000, "Furbo ペットカメラ, SwitchBot 見守りカメラ", ["ペットカメラ", "見守りカメラ ペット"], ["Furbo", "SwitchBot"]),
    ("2026-07-31", "sparkling-water-maker-ranking", "home", "sparkling-water-maker", "炭酸水メーカー", "炭酸水メーカー", 10000, "SodaStream 炭酸水メーカー, ドリンクメイト 炭酸水メーカー", ["炭酸水メーカー", "ソーダメーカー"], ["SodaStream", "ドリンクメイト"]),
    ("2026-08-01", "electric-hot-water-dispenser-ranking", "home", "electric-hot-water-dispenser", "高機能電気ポット", "電気ポット", 10000, "象印 電気ポット, タイガー 電気ポット", ["電気ポット 5L", "VE電気まほうびん"], ["象印", "タイガー"]),
    ("2026-08-02", "air-fryer-ranking", "home", "air-fryer", "ノンフライヤー", "ノンフライヤー", 10000, "COSORI ノンフライヤー, Ninja ノンフライヤー", ["ノンフライヤー 大容量", "エアフライヤー"], ["COSORI", "Ninja"]),
    ("2026-08-03", "garment-steamer-ranking", "home", "garment-steamer", "衣類スチーマー", "衣類スチーマー", 10000, "パナソニック 衣類スチーマー, ティファール 衣類スチーマー", ["衣類スチーマー", "スチームアイロン 衣類"], ["パナソニック", "ティファール"]),
    ("2026-08-04", "carpet-cleaner-ranking", "home", "carpet-cleaner", "リンサークリーナー", "リンサークリーナー", 10000, "アイリスオーヤマ リンサークリーナー, BISSELL リンサークリーナー", ["リンサークリーナー", "カーペットクリーナー"], ["アイリスオーヤマ", "BISSELL"]),
    ("2026-08-05", "photo-printer-ranking", "work", "photo-printer", "写真プリンター", "プリンター", 20000, "キヤノン プリンター, エプソン プリンター", ["写真プリンター", "A3 プリンター"], ["キヤノン", "エプソン"]),
    ("2026-08-06", "portable-solar-panel-ranking", "trend", "portable-solar-panel", "ポータブルソーラーパネル", "ソーラーパネル", 20000, "EcoFlow ソーラーパネル, Jackery ソーラーパネル", ["ポータブル ソーラーパネル", "折りたたみ ソーラーパネル"], ["EcoFlow", "Jackery"]),
    ("2026-08-07", "fish-finder-ranking", "trend", "fish-finder", "魚群探知機", "魚群探知機", 30000, "ホンデックス 魚群探知機, Garmin 魚群探知機", ["魚群探知機", "魚探 GPS"], ["ホンデックス", "Garmin"]),
]


def q(value):
    return "'" + str(value).replace("'", "''") + "'"


def block(text):
    return ">\n      " + text


def article_text(theme):
    date, article_id, category, slug, topic, required, min_price, keywords, discovery, products = theme
    product_names = "、".join(products)
    h1 = f"{topic} 厳選2選"
    title = f"【2026年最新】{topic} 厳選2選｜買ってから困る設置と維持費を比較"
    intro = (
        f"{topic}は価格やスペックだけで選ぶと、設置場所、メンテナンス、消耗品、保証条件で後悔しやすい商品です。"
        f"本記事では{product_names}を候補に、使い始めてから負担になりやすい点まで比較します。"
    )
    meta = (
        f"{product_names}の{topic}を比較。価格、設置、運用、メンテナンス、保証条件を整理し、"
        "楽天市場で新品購入前に必ず確認すべき落とし穴をまとめます。"
    )
    insight = (
        f"{topic}の後悔は、購入直後の性能よりも設置条件と維持の手間に出ます。"
        "公開レビュー評価・件数と商品説明の仕様表記を確認し、長く使える現実性を重視します。"
    )

    lines = [
        f"  - id: {article_id}",
        f"    category_id: {category}",
        "    type: daily",
        f"    slug: {slug}",
        f"    release_date: {q(date)}",
        f"    h1: {h1}",
        f"    title: {title}",
        f"    intro: {block(intro)}",
        f"    meta_description: {meta}",
        f"    analysis_insight: {block(insight)}",
        "    qa_config:",
        f"      min_price: {min_price}",
        "      required_words:",
        f"        - {required}",
        "      forbidden_words:",
    ]
    lines.extend(f"        - {word}" for word in FORBIDDEN)
    lines.extend([
        "    rakuten_params:",
        f"      keyword: {keywords}",
        "      discovery_keywords:",
    ])
    lines.extend(f"        - {word}" for word in discovery)
    lines.extend([
        "      hits: 20",
        "      sort: -reviewCount",
        "    test_criteria:",
    ])
    lines.extend(
        [f"      - id: {cid}", f"        name: {name}"]
        for cid, name in CRITERIA
    )
    flat_lines = []
    for item in lines:
        if isinstance(item, list):
            flat_lines.extend(item)
        else:
            flat_lines.append(item)
    flat_lines.append("    products_extra:")
    for idx, product in enumerate(products):
        scores = (4.7 - idx * 0.2, 4.2 + idx * 0.2, 4.4 - idx * 0.1)
        flat_lines.extend([
            f"      - keyword: {product}",
            f"        best_for: {product}の定番感を重視し、購入後の設置や維持まで無理なく続けたい人",
            "        scores:",
            f"          fit: {scores[0]:.1f}",
            f"          install: {scores[1]:.1f}",
            f"          value: {scores[2]:.1f}",
            f"        analysis_why: {product}は{topic}の比較候補として探しやすく、商品説明や公開レビュー件数から仕様と使い勝手を確認しやすい候補です。",
            "        pros:",
            "          - 定番候補として比較情報を集めやすい",
            "          - 価格と仕様のバランスを確認しやすい",
            "          - 楽天市場で保証や付属品を見比べやすい",
            "        critical_cons: 安さだけで選ぶと、設置条件、付属品、保証範囲が用途に合わない場合があります。",
            "        maintenance_reality: 購入前に本体サイズ、設置場所、消耗品、保証期間を商品ページで確認してください。",
            "        cost_performance: 毎日使う前提なら初期価格だけでなく、手入れの簡単さと長期保証まで含めて判断しやすい候補です。",
        ])
    return "\n".join(flat_lines)


def main():
    text = STOCK_PATH.read_text(encoding="utf-8")
    existing = set(re.findall(r"^\s+- id: ([^\n]+)$", text, flags=re.MULTILINE))
    additions = [article_text(theme) for theme in THEMES if theme[1] not in existing]
    if not additions:
        print("No stock articles to add.")
        return
    suffix = "\n\n" + "\n\n".join(additions) + "\n"
    STOCK_PATH.write_text(text.rstrip() + suffix, encoding="utf-8")
    print(f"Added {len(additions)} stock articles through {THEMES[-1][0]}.")


if __name__ == "__main__":
    main()
