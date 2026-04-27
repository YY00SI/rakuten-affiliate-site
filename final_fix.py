import yaml

def final_fix():
    file_path = "config/articles.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    for art in config['articles']:
        if art['id'] == "audio-glasses-ranking":
            art['rakuten_params']['keyword'] = "Anker スマートグラス, HUAWEI Eyewear, Soundcore"
            # 照合キーを Anker に広げる
            for ex in art['products_extra']:
                if ex['keyword'] == "Soundcore":
                    ex['keyword'] = "Anker"

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print("Final fix completed.")

if __name__ == "__main__":
    final_fix()
