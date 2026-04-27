import yaml

def fix_final():
    # 完全に正しい構造と日本語で再構築する
    data = {
        "articles": [
            {
                "id": "hair-dryer-ranking",
                "rakuten_params": {"keyword": "リファ ドライヤー, ナノケア ドライヤー, Dyson Supersonic, KINUJO"},
                "qa_config": {"min_price": 30000, "required_words": ["ドライヤー"]},
                "products_extra": [
                    {"keyword": "リファ"}, {"keyword": "ナノケア"}, {"keyword": "Dyson"}, {"keyword": "KINUJO"}
                ]
            },
            {
                "id": "premium-rice-cooker",
                "rakuten_params": {"keyword": "炎舞炊き, ご泡火炊き, 炊飯器 ビストロ, 本炭釜"},
                "qa_config": {"min_price": 30000, "required_words": ["炊飯器"]},
                "products_extra": [
                    {"keyword": "炎舞"}, {"keyword": "土鍋"}, {"keyword": "ビストロ"}, {"keyword": "本炭釜"}
                ]
            },
            {
                "id": "audio-glasses-ranking",
                "rakuten_params": {"keyword": "HUAWEI Eyewear, Soundcore Frames, オーディオグラス"},
                "qa_config": {"min_price": 10000, "required_words": ["グラス"]},
                "products_extra": [
                    {"keyword": "HUAWEI"}, {"keyword": "Soundcore"}
                ]
            },
            {
                "id": "office-chair-ranking",
                "rakuten_params": {"keyword": "アーロンチェア リマスタード, エルゴヒューマン プロ"},
                "qa_config": {"min_price": 50000, "required_words": ["チェア"]},
                "products_extra": [
                    {"keyword": "アーロンチェア"}, {"keyword": "エルゴヒューマン"}
                ]
            },
            {
                "id": "toothbrush-ranking",
                "rakuten_params": {"keyword": "ソニッケアー プレステージ, オーラルB iO9"},
                "qa_config": {"min_price": 15000, "required_words": ["歯ブラシ"]},
                "products_extra": [
                    {"keyword": "ソニッケアー"}, {"keyword": "オーラルB"}
                ]
            },
            {
                "id": "smart-home-kit",
                "rakuten_params": {"keyword": "SwitchBot ハブ2, Nature Remo 3"},
                "qa_config": {"min_price": 3000, "required_words": ["リモコン", "ハブ"]},
                "products_extra": [
                    {"keyword": "SwitchBot"}, {"keyword": "Nature"}
                ]
            }
        ]
    }

    file_path = "config/articles.yaml"
    # 全てを書き換えると情報が失われるため、既存のファイルを読み込み、文字化け箇所だけを特定して直す
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 記事ごとの修正マッピング
    corrections = {
        "hair-dryer-ranking": ["リファ", "ナノケア", "Dyson", "KINUJO"],
        "premium-rice-cooker": ["炎舞", "土鍋", "ビストロ", "本炭釜"],
        "audio-glasses-ranking": ["HUAWEI", "Soundcore"],
        "office-chair-ranking": ["アーロンチェア", "エルゴヒューマン"],
        "toothbrush-ranking": ["ソニッケアー", "オーラルB"],
        "smart-home-kit": ["SwitchBot", "Nature"],
        "stick-vacuum-ranking": ["V10", "PV", "Shark"],
        "facial-device-ranking": ["ヤーマン", "バイタリフト"],
        "monitor-arm": ["エルゴトロン", "Pixio"],
        "ferrofluid-speaker": ["磁性流体"]
    }

    for art in config['articles']:
        # rakuten_params.keyword の文字化けを直す (手動定義に置換)
        if art['id'] == "hair-dryer-ranking":
            art['rakuten_params']['keyword'] = "リファ ドライヤー, ナノケア ドライヤー, Dyson Supersonic, KINUJO"
        elif art['id'] == "premium-rice-cooker":
            art['rakuten_params']['keyword'] = "炎舞炊き, ご泡火炊き, 炊飯器 ビストロ, 本炭釜"
        elif art['id'] == "audio-glasses-ranking":
            art['rakuten_params']['keyword'] = "HUAWEI Eyewear 2, Soundcore Frames, オーディオグラス"
        elif art['id'] == "office-chair-ranking":
            art['rakuten_params']['keyword'] = "アーロンチェア リマスタード, エルゴヒューマン プロ"
        elif art['id'] == "toothbrush-ranking":
            art['rakuten_params']['keyword'] = "ソニッケアー プレステージ, オーラルB iO"

        # products_extra の keyword を修正
        if art['id'] in corrections:
            new_keys = corrections[art['id']]
            for i, ex in enumerate(art.get('products_extra', [])):
                if i < len(new_keys):
                    ex['keyword'] = new_keys[i]

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print("YAML encoding/content fixed.")

if __name__ == "__main__":
    fix_final()
