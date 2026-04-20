# 楽天アフィリエイト自動更新サイト 要件定義書 v1.0

## 1. システム概要
楽天市場の商品データを毎日自動取得し、アフィリエイトリンク付きの静的HTMLサイトを自動生成・デプロイする。

## 2. ディレクトリ構成 (実装用)
- `src/`: スクリプト本体
- `templates/`: Jinja2テンプレート
- `output/site/`: 生成されたHTML（GitHub Pagesの公開対象）
- `data/products/`: 取得したJSONデータの一次保存

## 3. 実装フェーズ (Phase 1: MVP)
- [ ] `config/categories.yaml` の作成（kitchenカテゴリのみ有効化）
- [ ] `src/fetch_products.py` の実装
- [ ] `templates/` 以下のHTMLテンプレート作成
- [ ] `src/build_site.py` の実装
- [ ] `src/generate_sitemap.py` の実装
- [ ] GitHub Actions ワークフローの構築

## 4. 特記事項
- GitHub Pages の設定で、公開フォルダを `output/site/` に指定すること。
- 楽天APIの Credential は GitHub Secrets に保存すること。
