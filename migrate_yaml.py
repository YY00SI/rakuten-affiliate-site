import os
import re

def migrate():
    config_path = 'config/articles.yaml'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    PRICE_FLOOR = {
        'portable-gaming-pc': 30000, 'ferrofluid-speaker': 10000, 'rice-cooker': 30000,
        'stick-vacuum': 15000, 'dryer-ranking': 20000, 'coffee-maker': 10000,
        'ai-drone': 10000, 'ai-voice-recorder': 5000, 'smart-lock': 8000,
        'monitor-arm': 5000, 'toaster-ranking': 10000, 'keyboard-ranking': 10000,
        'office-chair-ranking': 30000, 'facial-device-ranking': 20000, 'smart-home-kit': 3000,
        'toothbrush-ranking': 10000, 'hair-iron-ranking': 10000, 'projector-ranking': 30000
    }

    GENRE_MAP = {
        'portable-gaming-pc': '101240', 'ferrofluid-speaker': '100532', 'rice-cooker': '100233',
        'stick-vacuum': '100239', 'dryer-ranking': '100241', 'coffee-maker': '100236',
        'ai-drone': '100535', 'ai-voice-recorder': '100524', 'smart-lock': '567855'
    }

    REQ_WORDS_MAP = {
        'dryer': ['ドライヤー', 'ヘア'], 'vacuum': ['掃除機', 'クリーナー'], 'chair': ['チェア', '椅子'],
        'speaker': ['スピーカー'], 'recorder': ['レコーダー', '録音'], 'lock': ['スマートロック', '鍵'],
        'coffee': ['コーヒー', '珈琲'], 'rice-cooker': ['炊飯器', 'IH'], 'portable-gaming-pc': ['ゲーミングPC', 'UMPC'],
        'drone': ['ドローン', '空撮', 'drone']
    }

    FORBIDDEN_GLOBAL = ['フィルム', 'ケース', 'カバー', 'スタンド', '収納', '交換', '補修', '液体', 'オイル', 'ふるさと納税', '返礼品', '中古', '訳あり', 'ジャンク', '部品', 'パーツ', 'レンタル', '延長', '設置', '工事', '在庫処分', '3in1', 'アウトレット']

    FORBIDDEN_SPECIFIC = {
        'rice-cooker': ['ミル', 'グラインダー', 'コーヒー', '本', '絵本'],
        'portable-gaming-pc': ['保護フィルム', 'スキン', 'グリップ', '本', '絵本'],
        'stick-vacuum': ['スタンド', '収納ラック', '充電スタンド', '紙パック', 'フィルター単品']
    }

    new_lines = []
    in_article = False
    current_id = ""
    current_slug = ""
    qa_inserted = False

    for i, line in enumerate(lines):
        # 記事の開始を検知
        id_match = re.match(r'^  -\s*id:\s*"(.*?)"', line)
        if id_match:
            current_id = id_match.group(1)
            in_article = True
            qa_inserted = False
        
        slug_match = re.search(r'^    slug:\s*"(.*?)"', line)
        if in_article and slug_match:
            current_slug = slug_match.group(1)

        # トップレベルの min_price を検知して qa_config に置換
        min_price_match = re.match(r'^    min_price:\s*(\d+)', line)
        
        if in_article and min_price_match and not qa_inserted:
            # 既存の min_price の値を取得（あれば）
            file_min_price = int(min_price_match.group(1))
            min_price = PRICE_FLOOR.get(current_slug, file_min_price)
            if min_price == 0:
                min_price = file_min_price
                
            genre_id = GENRE_MAP.get(current_slug, '')
            
            req_words = []
            for k, v in REQ_WORDS_MAP.items():
                if k in current_id:
                    req_words = v
                    break
            req_words_str = '["' + '", "'.join(req_words) + '"]' if req_words else '[]'
            
            forbidden = list(FORBIDDEN_GLOBAL)
            if current_slug in FORBIDDEN_SPECIFIC:
                forbidden.extend(FORBIDDEN_SPECIFIC[current_slug])
            forbidden_str = '["' + '", "'.join(forbidden) + '"]'
            
            new_lines.append(f'    qa_config:\n')
            new_lines.append(f'      min_price: {min_price}\n')
            new_lines.append(f'      genre_id: "{genre_id}"\n')
            new_lines.append(f'      required_words: {req_words_str}\n')
            new_lines.append(f'      forbidden_words: {forbidden_str}\n')
            
            qa_inserted = True
            # 元の min_price 行は出力しない（削除扱い）
            continue
            
        new_lines.append(line)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Migration complete: Text-based replacement finished without losing comments.")

if __name__ == "__main__":
    migrate()
