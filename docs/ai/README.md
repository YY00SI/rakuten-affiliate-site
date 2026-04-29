# AI Authoring System

このディレクトリは、モデルの賢さに依存せず `LifeTech Select` 水準の記事を作るための共通基盤です。

## 読む順番
1. `Rule.md`
2. `workflow.md`
3. `docs/ai/CONTENT_CONTRACT.md`
4. `docs/ai/PROMPT_PACK.md`
5. `config/article_blueprint.template.yaml`

## 役割分担
- `Rule.md`
  プロジェクト全体の絶対方針。
- `workflow.md`
  企画から公開までの運用手順。
- `docs/ai/CONTENT_CONTRACT.md`
  記事1本に必要な入力、出力、禁止事項、品質条件。
- `docs/ai/PROMPT_PACK.md`
  Gemini Flash のような軽量モデルにもそのまま渡せる執筆指示。
- `config/article_blueprint.template.yaml`
  `articles.yaml` に貼るための雛形。
- `config/article_quality_rules.yaml`
  バリデータが参照する機械可読ルール。

## 最短フロー
1. テーマを決める。
2. `config/article_blueprint.template.yaml` をコピーする。
3. `docs/ai/PROMPT_PACK.md` を使って、必要項目をすべて埋める。
4. `python src/validate_articles.py`
5. `python src/fetch_products.py`
6. `python src/build_site.py`

## 原則
- モデルには自由作文させない。
- 先に `評価軸`, `読者`, `除外条件`, `推奨機種` を固定する。
- 公開前に必ず機械検証を通す。
