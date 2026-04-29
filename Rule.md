# プロジェクト概要
楽天アフィリエイトを活用した高単価特化型の厳選メディア `LifeTech Select (LTS)` のプロジェクトです。

## 最優先ルール
このプロジェクトを扱う AI は、作業前に必ず以下をこの順で確認すること。

1. `Rule.md`
2. `workflow.md`
3. `docs/ai/CONTENT_CONTRACT.md`
4. `config/article_quality_rules.yaml`

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

この 3 つを通らない記事は公開不可とする。
