# プロジェクト進捗状況 (2026-05-02)

## 1. 全体概要
Gemini Flash 級の軽量モデルでも破綻しにくい記事生成ルールと、収益化運用を支える公開監査・SEO基盤の整備を完了。品質保証フレームワーク（QUALITY_GATE.md）を新設し、モデル非依存の品質担保を体系化。

## 2. 現在のステータス
- **構成検証:** `src/validate_articles.py` で全記事検証（要実行確認）
- **生成監査:** `src/audit_site.py` で `errors=0 / warnings=0`
- **公開対象:** 29記事をビルド対象（5/13公開分までストック済み）
- **収益導線:** 楽天アフィリエイトリンク、canonical、OGP、JSON-LD、sitemap、robots、関連記事導線を実装済み
- **運用耐性:** 未来日・QA失敗記事の自動除外、staleページの自動削除、禁止商材語の共通適用を実装済み

## 3. 今回の改善
- **品質保証フレームワーク新設:** `docs/ai/QUALITY_GATE.md` を作成。軽量AIモデルでも品質を担保するための生成フロー、セルフチェックリスト、機械検証基準、重複防止プロトコルを体系化
- **ストック記事の補充:** 5/7〜5/13 の7記事を新規追加
  - 5/7: ワイヤレスイヤホン（work）
  - 5/8: 卓上食洗機（home）
  - 5/9: デスクライト（work）
  - 5/10: 空気清浄機（home）
  - 5/11: 4Kモニター（work）
  - 5/12: 電動シェーバー（beauty）
  - 5/13: マッサージガン（beauty）
- **ワークフロー更新:** `workflow.md` に QUALITY_GATE.md への参照と audit_site.py の実行ステップを追加

## 4. 残タスク
- [x] 1. `site.analytics.ga4_measurement_id` に本番の GA4 計測IDを入力
- [ ] 2. 新規記事追加後に `python src/validate_articles.py` → `python src/fetch_products.py` → `python src/build_site.py` → `python src/audit_site.py` を通す
- [ ] 3. 検索流入とクリック率を見ながら、各カテゴリの追加記事を補充
- [ ] 4. 新規7記事のバリデーション実行と商品データ取得
