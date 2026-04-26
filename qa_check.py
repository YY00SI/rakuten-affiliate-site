import os
import json
import yaml

def run_full_audit():
    print("=== LTS Full Quality Audit (Spec v8.3) ===")
    
    with open("config/articles.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    articles = config['articles']
    data_dir = "data/products"
    
    errors = 0
    passed = 0
    
    for art in articles:
        art_id = art['id']
        print(f"\n[Auditing] {art_id}...")
        
        # 1. qa_config の存在チェック
        qa_config = art.get('qa_config')
        if qa_config is None:
            print(f"  [ERR] qa_config is missing.")
            errors += 1
            continue
            
        min_price = qa_config.get('min_price', 0)
        if not min_price:
            print(f"  [ERR] qa_config.min_price is missing or 0.")
            errors += 1
            continue
            
        forbidden_words = qa_config.get('forbidden_words', [])

        # 2. データファイルの存在チェック
        file_path = os.path.join(data_dir, f"{art_id}.json")
        if not os.path.exists(file_path):
            print(f"  [ERR] Data file missing: {file_path}")
            errors += 1
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data.get('items', [])
            
        # 3. 解析データ(products_extra)との整合性チェック
        extra = art.get('products_extra', [])
        if not extra:
            print("  [ERR] No products_extra defined. Cannot publish without products.")
            errors += 1
            continue
            
        matched_count = 0
        missing_keywords = []
        for ex in extra:
            found = False
            for item in items:
                # 1. キーワード一致
                if ex['keyword'].lower() not in item['name'].lower():
                    continue
                # 2. 禁止キーワード除外
                if any(f_kw in item['name'] for f_kw in forbidden_words):
                    continue
                # 3. 価格下限チェック
                if item.get('price', 0) < min_price:
                    continue
                
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
            print(f"  [ERR] Only {matched_count}/{len(extra)} matched. Missing: {missing_keywords}")
            errors += 1

    print("\n" + "="*40)
    print(f"Audit Result: PASSED={passed}, ERRORS={errors}")
    print("="*40)
    
    if errors > 0:
        exit(1)

if __name__ == "__main__":
    run_full_audit()
