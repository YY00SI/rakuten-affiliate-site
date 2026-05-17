"""Google Sitemap Ping - サイトマップ更新をGoogleに通知するスクリプト"""
import requests
import sys

SITEMAP_URL = "https://yy00si.github.io/rakuten-affiliate-site/sitemap.xml"
PING_URL = f"https://www.google.com/ping?sitemap={SITEMAP_URL}"

def main():
    print(f"[INFO] Google Ping 送信中...")
    print(f"  Sitemap: {SITEMAP_URL}")
    print(f"  Ping URL: {PING_URL}")
    
    try:
        response = requests.get(PING_URL, timeout=10)
        if response.status_code == 200:
            print(f"[OK] Google Ping 成功 (HTTP {response.status_code})")
            print("  → Googleにサイトマップの更新を通知しました。")
            print("  → クロールは数時間〜数日以内に行われます。")
        else:
            print(f"[WARN] Google Ping 応答: HTTP {response.status_code}")
            print(f"  Body: {response.text[:200]}")
    except Exception as e:
        print(f"[ERROR] Google Ping 失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
