import yaml
import os

def migrate():
    file_path = "config/articles.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    for art in config['articles']:
        # 1. qa_config の整理
        if 'qa_config' not in art:
            art['qa_config'] = {}
        
        # トップレベルにあるパラメータを qa_config に移動
        for key in ['min_price', 'genre_id', 'required_words', 'forbidden_words']:
            if key in art:
                art['qa_config'][key] = art.pop(key)
        
        # デフォルト値の補完
        if 'min_price' not in art['qa_config']:
            art['qa_config']['min_price'] = 10000 # Default
        
        # 2. 検索キーワードの改善 (rakuten_params.keyword)
        kw = art.get('rakuten_params', {}).get('keyword', "")
        
        if art['id'] == 'premium-rice-cooker':
            art['rakuten_params']['keyword'] = "炎舞炊き, 土鍋ご泡火炊き, パナソニック 炊飯器 ビストロ, 本炭釜"
        elif art['id'] == 'audio-glasses-ranking':
            art['rakuten_params']['keyword'] = "HUAWEI Eyewear 2, Soundcore Frames, オーディオグラス"
        elif art['id'] == 'office-chair-ranking':
            art['rakuten_params']['keyword'] = "アーロンチェア, エルゴヒューマン プロ"
        elif art['id'] == 'toothbrush-ranking':
            art['rakuten_params']['keyword'] = "ソニッケアー, オーラルB iO, 電動歯ブラシ"
        elif art['id'] == 'monitor-arm':
            art['rakuten_params']['keyword'] = "エルゴトロン LX, Pixio モニターアーム"
        elif art['id'] == 'smart-home-kit':
            art['rakuten_params']['keyword'] = "SwitchBot ハブ2, Nature Remo 3"
        elif art['id'] == 'ai-voice-recorder':
            art['rakuten_params']['keyword'] = "PLAUD NOTE, VOITER, ソニー ICD-TX660"

    with open(file_path, "w", encoding="utf-8") as f:
        # yaml.dump だとコメントが消えるが、現状は正確な構造化を優先
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print("Migration completed.")

if __name__ == "__main__":
    migrate()
