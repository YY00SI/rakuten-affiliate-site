import yaml
import urllib.request
import urllib.error
import time
import os

def check_url(url):
    # Handle local domain check for pre-deployment verification
    site_prefix = "https://yy00si.github.io/rakuten-affiliate-site/"
    if url.startswith(site_prefix):
        local_path = url.replace(site_prefix, "docs/")
        if os.path.exists(local_path):
            return True
        else:
            print(f"  [DEBUG] Local file not found: {local_path}")
            return False

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        return response.getcode() == 200
    except Exception as e:
        return False

def run_qa():
    print("=== LTS All-Article QA Check Started ===")
    try:
        with open('config/articles.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"YAML Parse Error: {e}")
        return

    articles = data.get('articles', [])
    print(f"Total articles found: {len(articles)}")
    
    errors = 0
    warnings = 0

    for idx, art in enumerate(articles):
        art_id = art.get('id', f'Unknown-{idx}')
        print(f"\n[{idx+1}/{len(articles)}] Checking: {art_id} ({art.get('title', 'No Title')})")
        
        # 1. URL Check
        url = art.get('eye_catch')
        if not url:
            print(f"  [ERROR] No eye_catch URL")
            errors += 1
        elif not url.startswith('http'):
            print(f"  [ERROR] Invalid eye_catch URL format: {url}")
            errors += 1
        else:
            if not check_url(url):
                print(f"  [ERROR] Dead or Unreachable URL: {url}")
                errors += 1
            else:
                print(f"  [OK] Image URL is reachable")

        # 2. rakuten_params check
        params = art.get('rakuten_params')
        if not params:
            print(f"  [ERROR] rakuten_params is missing")
            errors += 1
            continue
        
        keywords_str = params.get('keyword', '')
        if not keywords_str:
            print(f"  [ERROR] rakuten_params.keyword is missing")
            errors += 1
            continue
            
        param_keywords = [k.strip() for k in keywords_str.split(',')]
        
        # 3. products_extra check
        pe = art.get('products_extra', [])
        if len(pe) == 0:
            print(f"  [ERROR] products_extra is empty")
            errors += 1
            continue
            
        if len(param_keywords) != len(pe):
            print(f"  [ERROR] Mismatch! rakuten_params keywords ({len(param_keywords)}) != products_extra count ({len(pe)})")
            errors += 1
            
        # 4. KBF and Structure check
        criteria = art.get('test_criteria', [])
        if not criteria:
            print(f"  [ERROR] test_criteria is missing")
            errors += 1
        else:
            criteria_ids = [c['id'] for c in criteria]
            for p_idx, p in enumerate(pe):
                p_kw = p.get('keyword', f'Item-{p_idx}')
                
                # Check required fields
                required = ['best_for', 'scores', 'analysis_why', 'pros', 'critical_cons', 'maintenance_reality', 'cost_performance']
                missing = [r for r in required if r not in p or not p[r]]
                if missing:
                    print(f"  [ERROR] {p_kw} is missing fields: {missing}")
                    errors += 1
                
                # Check scores against criteria
                scores = p.get('scores', {})
                for c_id in criteria_ids:
                    if c_id not in scores:
                        print(f"  [ERROR] {p_kw} is missing score for criteria: {c_id}")
                        errors += 1

        if errors == 0:
            print(f"  => PASS")
            
    print("\n========================================")
    print(f"QA Check Completed.")
    print(f"Total Errors Found: {errors}")
    if errors > 0:
        print("ACTION REQUIRED: Fix the errors above before running git_push.bat.")
    else:
        print("SUCCESS: All articles passed the LTS Quality Gate.")

if __name__ == '__main__':
    run_qa()
