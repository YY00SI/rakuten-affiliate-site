import yaml

def final_polish():
    file_path = "config/articles.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    updates = {
        "robot-vacuum-ranking": {
            "search": "ルンバ j9, DEEBOT X2, Roborock S8, Dreame 掃除機",
            "extra": ["ルンバ", "DEEBOT", "j9", "Dreame"] # 照合キーを増やす
        },
        "audio-glasses-ranking": {
            "search": "HUAWEI Eyewear, Soundcore Frames, オーディオグラス",
            "extra": ["HUAWEI", "Soundcore"]
        },
        "smart-home-kit": {
            "search": "SwitchBot ハブ, Nature Remo, スマートリモコン",
            "extra": ["SwitchBot", "Nature"]
        }
    }

    for art in config['articles']:
        if art['id'] in updates:
            upd = updates[art['id']]
            art['rakuten_params']['keyword'] = upd['search']
            # products_extra の keyword を更新
            for i, ex in enumerate(art.get('products_extra', [])):
                if i < len(upd['extra']):
                    ex['keyword'] = upd['extra'][i]

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print("Final polish completed.")

if __name__ == "__main__":
    final_polish()
