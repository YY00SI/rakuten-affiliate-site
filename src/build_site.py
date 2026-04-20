import os
import json
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def main():
    # 設定の読み込み
    with open("config/categories.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    site_config = config['site']
    
    # Jinja2の設定
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")
    
    # データの読み込み
    categories_data = []
    data_dir = "data/products"
    
    # 設定ファイルにある順序でデータを読み込む
    for cat_conf in config['categories']:
        file_path = os.path.join(data_dir, f"{cat_conf['id']}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                categories_data.append({
                    "id": cat_conf['id'],
                    "name": cat_conf['name'],
                    "products": data['items']
                })
    
    if not categories_data:
        print("[ERROR] 表示するデータがありません。先に fetch_products.py を実行してください。")
        return

    # 出力ディレクトリの作成
    output_dir = "output/site"
    os.makedirs(output_dir, exist_ok=True)
    
    # HTMLの生成
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = template.render(
        title=site_config['name'],
        description=site_config['description'],
        site_name=site_config['name'],
        site_description=site_config['description'],
        canonical_url=site_config['base_url'],
        categories=categories_data,
        updated_at=now
    )
    
    # ファイル書き出し
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[INFO] サイト構築完了: {output_path}")

if __name__ == "__main__":
    main()
