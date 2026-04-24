import re
import os
import shutil

config_path = 'config/articles.yaml'
docs_dir = 'docs'

def main():
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 'hair-dryer-ranking' 以外の release_date を 2026-05-xx に変更する
    # articles.yaml はリスト構造。単純な正規表現だと hair-dryer-ranking まで変わる恐れがあるため、慎重に分割処理
    sections = content.split('- id: ')
    
    new_sections = [sections[0]]
    day = 1
    
    for section in sections[1:]:
        if section.startswith('"hair-dryer-ranking"'):
            new_sections.append('- id: ' + section)
        else:
            # release_date: "2026-04-xx" を置換
            new_section = re.sub(
                r'release_date:\s*"[^"]+"',
                f'release_date: "2026-05-{day:02d}"',
                section
            )
            new_sections.append('- id: ' + new_section)
            day += 1
            if day > 30: day = 1

    new_content = ''.join(new_sections)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("[INFO] articles.yaml の日付リセット完了")

    # 2. 既存の生成済みHTMLのクリーンアップ
    # trend と home ディレクトリを削除
    for d in ['trend', 'home']:
        dir_path = os.path.join(docs_dir, d)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"[INFO] 削除完了: {dir_path}")
            except Exception as e:
                print(f"[ERROR] 削除失敗: {e}")

if __name__ == "__main__":
    main()
