import yaml

def rewrite_keywords():
    file_path = "config/articles.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    updates = {
        "robot-vacuum-ranking": {
            "search": "ルンバ j9+, DEEBOT X2, Roborock S8",
            "extra": {"j9": "ルンバ"}
        },
        "ai-voice-recorder": {
            "search": "PLAUD NOTE, VOITER SR302, ICD-TX660, オリンパス WS-883",
            "extra": {"WS": "WS-883"}
        },
        "premium-rice-cooker": {
            "search": "象印 炎舞炊き, タイガー ご泡火炊き, 炊飯器 ビストロ, 三菱 本炭釜",
            "extra": {"繝薙せ繝医Ο": "ビストロ"} # 元のキーが文字化けしていても対応できるよう配慮
        },
        "audio-glasses-ranking": {
            "search": "HUAWEI Eyewear 2, Soundcore Frames Cafe, オーディオグラス",
            "extra": {"繧ｹ繝槭繝医げ繝ｩ繧ｹ": "HUAWEI", "Soundcore": "Soundcore"}
        },
        "stick-vacuum-ranking": {
            "search": "ダイソン V10, 日立 PV-BH900, Shark スティック掃除機",
            "extra": {"V10": "Dyson"}
        },
        "office-chair-ranking": {
            "search": "アーロンチェア リマスタード, エルゴヒューマン プロ",
            "extra": {"繧｢繝ｼ繝ｭ繝ｳ繝√ぉ繧｢ 繝ｪ繝槭せ繧ｿ繝ｼ繝": "アーロンチェア"}
        },
        "toothbrush-ranking": {
            "search": "ソニッケアー プレステージ 9900, オーラルB iO9",
            "extra": {"繧ｽ繝九ャ繧ｱ繧｢繝ｼ 繝励Ξ繧ｹ繝繧ｸ": "ソニッケアー"}
        },
        "facial-device-ranking": {
            "search": "ヤーマン フォトプラス, パナソニック バイタリフト RF",
            "extra": {"繝舌う繧ｿ繝ｪ繝輔ヨ RF": "バイタリフト"}
        },
        "monitor-arm": {
            "search": "エルゴトロン LX, Pixio PS2S モニターアーム",
            "extra": {"Pixio PS2S": "Pixio"}
        },
        "smart-home-kit": {
            "search": "SwitchBot ハブ2, Nature Remo 3",
            "extra": {"Nature Remo 3": "Nature"}
        }
    }

    for art in config['articles']:
        if art['id'] in updates:
            upd = updates[art['id']]
            art['rakuten_params']['keyword'] = upd['search']
            for ex in art['products_extra']:
                # 旧キーワード(文字化け含む)を新キーワードに置換
                for old_key, new_key in upd.get('extra', {}).items():
                    if ex['keyword'] == old_key:
                        ex['keyword'] = new_key

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print("Keywords rewritten.")

if __name__ == "__main__":
    rewrite_keywords()
