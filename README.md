# 楽天アフィリエイト「キーワード記事型」自動生成サイト v2.0

楽天市場の商品検索APIを活用し、SEOに最適化された「おすすめ記事」を自動生成するアフィリエイトサイトです。

## v2.0 の特徴

- **キーワード中心の設計**: カテゴリ一覧ではなく、「ドライヤー おすすめ10選」のような検索意図に対応した記事ページを生成。
- **SEO最適化**: H1タグ、メタディスクリプション、目次、選び方のポイント、ランキング構造を自動構成。
- **高成約率テンプレート**: 楽天レッドを基調としたデザイン、視認性の高いランキングバッジ、強力なCTA（Call to Action）ボタンを実装。
- **新システム対応**: 最新の楽天API仕様（UUID形式ID）に対応。
- **完全自動更新**: GitHub Actions により、毎日最新の価格・レビュー数に基づいたランキングを維持。

## ディレクトリ構造

- `config/articles.yaml`: 記事の構成、キーワード、検索条件を管理
- `config/article_blueprint.template.yaml`: AI が埋める記事テンプレート
- `config/article_quality_rules.yaml`: 機械検証用の品質ルール
- `src/fetch_products.py`: 楽天APIからデータを取得し `data/` に保存
- `src/build_site.py`: `templates/` を使用して `docs/` に静的サイトを生成
- `src/validate_articles.py`: 記事設定の構造と品質を検証
- `docs/`: 生成されたサイト（GitHub Pages 公開用）
- `docs/ai/`: モデル非依存の執筆ルールとプロンプト
- `templates/`: Jinja2 テンプレートファイル

## 運用方法

1. `Rule.md` と `docs/ai/README.md` を読む。
2. `config/article_blueprint.template.yaml` を使って `config/articles.yaml` に記事設定を追加する。
3. `python src/validate_articles.py` を実行する。
4. GitHub にプッシュすると、GitHub Actions が自動的にデータを取得し、サイトを更新・デプロイします。

## 免責事項
当サイトはアフィリエイトリンクを含みます。商品情報は楽天市場のAPIより取得しており、最新の情報はリンク先の各ショップにてご確認ください。
