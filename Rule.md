# プロジェクト概要
楽天アフィリエイトを活用した高単価特化型の厳選メディア `LifeTech Select (LTS)` のプロジェクトです。

## 作業開始時

すべての作業で `Rule.md` と `docs/STATE.md` を読む。

- PDCA、収益分析、開始票、レポート: `$monetization-pdca` と `docs/pdca_profile.md` を読む。記事仕様はActが記事・商品・生成物を変更する場合だけ読む。
- 記事・商品・生成サイトを変更する作業: `workflow.md`、`docs/ai/CONTENT_CONTRACT.md`、`docs/ai/QUALITY_GATE.md`、`config/article_quality_rules.yaml` を読む。

これ以外の巨大な履歴、原本、品質文書は、preflightまたは必要な疑義がある場合だけ読む。

## 絶対方針
- 汎用的なアフィリエイト記事の量産は禁止。
- 比較対象は、検索者が指名買い候補にする `名機` に限定する。
- 商品本体ではないアクセサリ、補修部品、中古、訳あり、ふるさと納税を混ぜない。
- 各記事には必ず独自の評価軸、推奨理由、欠点、運用の現実を書く。
- モデルの気分に任せず、テンプレートとバリデータを通す。

## 生成の原則
- 先に検索意図を固定する。
- 次に評価軸を 2〜4 個に絞る。
- その後で候補機種を決める。
- 最後に `config/article_blueprint.template.yaml` を埋める。

## 公開前の必須チェック
- `python src/validate_articles.py`
- `python src/fetch_products.py`
- `python src/build_site.py`
- `python src/audit_site.py`

この 4 つを通らない記事は公開不可とする。
