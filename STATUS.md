# プロジェクト進捗状況 (2026-04-28)

## 1. 全体概要
Gemini Flash 級の軽量モデルでも破綻しにくい記事生成ルールと、収益化運用を支える公開監査・SEO基盤の整備を完了。

## 2. 現在のステータス
- **構成検証:** `src/validate_articles.py` で `errors=0 / warnings=0`
- **生成監査:** `src/audit_site.py` で `errors=0 / warnings=0`
- **公開対象:** 15記事をビルド対象として安定生成
- **収益導線:** 楽天アフィリエイトリンク、canonical、OGP、JSON-LD、sitemap、robots、関連記事導線を実装済み
- **運用耐性:** 未来日・QA失敗記事の自動除外、staleページの自動削除、禁止商材語の共通適用を実装済み

## 3. 今回の改善
- **単一商品記事の信頼性向上:** 1商品しか成立しない記事はランキング口調をやめ、選定理由中心の表現に自動切り替え
- **外部装飾アセットの排除:** Unsplash や Wikipedia の装飾画像をテンプレートから除去し、実商品画像中心の見せ方へ統一
- **計測設定の運用化:** Search Console 検証コードと GA4 ID を `config/articles.yaml` の `site` 設定から管理できる構成に変更

## 4. 残タスク
- [x] 1. `site.analytics.ga4_measurement_id` に本番の GA4 計測IDを入力
- [ ] 2. 新規記事追加時は `python src/validate_articles.py` → `python src/build_site.py` → `python src/audit_site.py` を必ず通す
3. 検索流入とクリック率を見ながら、各カテゴリの追加記事を補充
