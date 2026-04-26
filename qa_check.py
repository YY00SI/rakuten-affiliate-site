import os
import json
import yaml
import sys

# Ensure UTF-8 output for console
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older python versions if necessary
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_full_audit():
    print("=== LTS Full Quality Audit (Spec v8.3) ===")
    
    config_path = "config/articles.yaml"
    if not os.path.exists(config_path):
        print(f"[ERR] Config file not found: {config_path}")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    articles = config.get('articles', [])
    data_dir = "data/products"
    
    total_errors = 0
    total_passed = 0
    
    for art in articles:
        art_id = art['id']
        print(f"\n[Auditing] {art_id}...")
        
        # 1. データファイルの存在チェック
        file_path = os.path.join(data_dir, f"{art_id}.json")
        if not os.path.exists(file_path):
            print(f"  [ERR] Data file missing: {file_path}")
            total_errors += 1
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data.get('items', [])
            
        if not items:
            print(f"  [ERR] No items found in data file.")
            total_errors += 1
            continue

        # 2. qa_config に基づく個別チェック
        qa_config = art.get('qa_config', {})
        min_price = qa_config.get('min_price') or art.get('min_price', 0)
        forbidden_words = qa_config.get('forbidden_words', [])
        required_words = qa_config.get('required_words', [])
        
        art_errors = 0
        
        for item in items:
            name = item.get('name', '')
            price = item.get('price', 0)
            
            # 価格チェック
            if price < min_price:
                print(f"  [ERR] Price too low: {price} < {min_price} ({name[:30]}...)")
                art_errors += 1
                
            # NGワードチェック
            for fw in forbidden_words:
                if fw in name:
                    print(f"  [ERR] Forbidden word '{fw}' found in item name: {name[:30]}...")
                    art_errors += 1
            
            # 必須ワードチェック
            if required_words and not all(rw in name for rw in required_words):
                print(f"  [ERR] Missing required words {required_words} in: {name[:30]}...")
                art_errors += 1
        
        # 3. 解析データ(products_extra)との整合性チェック
        extra = art.get('products_extra', [])
        if extra:
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
                print(f"  [OK] All {len(extra)} masterpieces matched perfectly.")
            else:
                print(f"  [ERR] Integrity mismatch! Matched: {matched_count}/{len(extra)}")
                print(f"  [ERR] Missing keywords: {missing_keywords}")
                art_errors += 1
        else:
            print("  [WARN] No products_extra defined (Ranking style?)")

        if art_errors == 0:
            print(f"  [PASS] {art_id} audit successful.")
            total_passed += 1
        else:
            total_errors += art_errors
            
    print("\n" + "="*40)
    print(f"AUDIT COMPLETE")
    print(f"ARTICLES PASSED: {total_passed}")
    print(f"TOTAL ERRORS FOUND: {total_errors}")
    print("="*40)
    
    if total_errors > 0:
        print("\nACTION REQUIRED: Please fix the errors or re-fetch products.")
        sys.exit(1)

if __name__ == "__main__":
    run_full_audit()
