import os
import json
import yaml

def run_full_audit():
    print("=== LTS Full Quality Audit (Spec v8.2) ===")
    
    with open("config/articles.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    articles = config['articles']
    data_dir = "data/products"
    
    errors = 0
    passed = 0
    
    for art in articles:
        art_id = art['id']
        print(f"\n[Auditing] {art_id}...")
        
        # 1. データファイルの存在チェック
        file_path = os.path.join(data_dir, f"{art_id}.json")
        if not os.path.exists(file_path):
            print(f"  [ERR] Data file missing: {file_path}")
            errors += 1
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data.get('items', [])
            
        # 2. 解析データ(products_extra)との整合性チェック
        extra = art.get('products_extra', [])
        if not extra:
            print("  [WARN] No products_extra defined (Ranking style?)")
            continue
            
        matched_count = 0
        missing_keywords = []
        for ex in extra:
            found = False
            for item in items:
                if ex['keyword'].lower() in item['name'].lower():
                    found = True
                    break
            if found:
                matched_count += 1
            else:
                missing_keywords.append(ex['keyword'])
        
        if matched_count == len(extra):
            print(f"  [OK] All {len(extra)} products matched perfectly.")
            passed += 1
        else:
            print(f"  [ERR] Integrity mismatch! Matched: {matched_count}/{len(extra)}")
            print(f"  [ERR] Missing keywords: {missing_keywords}")
            errors += 1
            
        # 3. プレースホルダチェック (HTML生成前にデータ構造で確認)
        # build_site.py のロジックにより、これらはビルドをブロックする
    
    print("\n" + "="*40)
    print(f"AUDIT COMPLETE")
    print(f"PASSED: {passed}")
    print(f"FAILED: {errors}")
    print("="*40)
    
    if errors > 0:
        print("\nACTION REQUIRED: Please fix the missing keywords or re-fetch products.")

if __name__ == "__main__":
    run_full_audit()
