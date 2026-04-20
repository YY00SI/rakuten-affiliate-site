# Rakuten Affiliate Auto-Update Site

楽天商品検索APIを活用し、GitHub Actionsで毎日自動更新されるアフィリエイト静的サイトです。
GitHub Pagesで無料でホスティングされます。

## システム構成
- **データ取得**: `src/fetch_products.py` (楽天API)
- **サイト生成**: `src/build_site.py` (Jinja2)
- **SEO管理**: `src/generate_sitemap.py`
- **自動化**: GitHub Actions (`.github/workflows/build_and_deploy.yml`)

## セットアップ
1. 楽天デベロッパーアカウントでアプリIDを取得
2. 楽天アフィリエイトIDを取得
3. GitHubリポジトリのSecretsに以下を登録:
   - `RAKUTEN_APP_ID`
   - `RAKUTEN_AFFILIATE_ID`
4. GitHub Pagesの設定で `main` ブランチの `docs/` フォルダをソースに指定
