import yaml
import os
import shutil

config_path = 'config/articles.yaml'
docs_dir = 'docs'

def main():
    # 1. YAMLの読み込み
    with open(config_path, 'r', encoding='utf-8') as f:
        articles = yaml.safe_load(f)

    # 2. release_date を未来（非公開）に変更 (hair-dryer-ranking以外)
    updated_count = 0
    day = 1
    for article in articles:
        if article.get('id') != 'hair-dryer-ranking':
            # 2026年5月以降にスケジュールを再設定
            article['release_date'] = f'2026-05-{day:02d}'
            day += 1
            updated_count += 1

    # 3. YAMLの保存
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(articles, f, allow_unicode=True, sort_keys=False)
    
    print(f"[INFO] {updated_count}件の記事を未公開（2026年5月以降）に差し戻しました。")

    # 4. 既存の生成済みHTML（docsディレクトリ内のゴミ）の完全クリーンアップ
    # assets, beauty/dryer-ranking, CNAME 以外を削除
    if os.path.exists(docs_dir):
        for item in os.listdir(docs_dir):
            item_path = os.path.join(docs_dir, item)
            # 必要なアセットとトップページ周り、beauty(ドライヤー)以外を一旦削除してクリーンビルドさせる
            if item in ['trend', 'home']: 
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"[INFO] 削除完了: 古いディレクトリ {item_path}")

if __name__ == "__main__":
    main()
