# LTS（LifeTech Select）運用ワークフロー

本ドキュメントは、軽量モデルを含むすべての生成系 AI が同じ品質で記事を作るための標準手順です。

## 0. 入口
作業前に必ず以下を読むこと。

1. `Rule.md`
2. `docs/ai/CONTENT_CONTRACT.md`
3. `docs/ai/PROMPT_PACK.md`
4. `config/article_blueprint.template.yaml`

## 1. 収益最大化の PDCA

### Check
月 2 回、以下の CSV を人間がエクスポートし、AI に渡す。

1. Google Search Console
   検索クエリ、掲載順位、CTR。
2. 楽天アフィリエイト
   クリック数、CVR、発生報酬。

### Action
- 表示は多いが CTR が低い記事:
  `title`, `h1`, `meta_description` を改善。
- クリックはあるが売れない記事:
  `best_for`, `critical_cons`, `cost_performance` を改善。
- 在庫切れやノイズ流入がある記事:
  `rakuten_params.keyword`, `qa_config.forbidden_words` を見直す。

## 2. 新規記事 SOP

### Step 1: 検索意図を 1 つに固定
- 1 記事 1 意図。
- 高単価本体の比較であること。
- 周辺アクセサリ混入テーマは禁止。

### Step 2: 名機を先に決める
- 楽天 API に汎用語を直接投げない。
- 先にブランド名と型番を絞る。
- 比較対象は通常 2〜4 機種。

### Step 3: 評価軸を定義
- `test_criteria` は 2〜4 個。
- そのカテゴリに固有の判断軸だけを置く。
- `満足度`, `人気`, `総合力` のような抽象語は避ける。

### Step 4: テンプレートに落とす
- `config/article_blueprint.template.yaml` をコピーして埋める。
- すべての `products_extra` に対して以下を必須とする。
  - `best_for`
  - `scores`
  - `analysis_why`
  - `pros`
  - `critical_cons`
  - `maintenance_reality`
  - `cost_performance`

### Step 5: 機械検証
公開前に必ず以下を順に実行する。

1. `python src/validate_articles.py`
2. `python src/fetch_products.py`
3. `python src/build_site.py`

## 3. 品質ゲート

### 商品選定
- `中古`, `訳あり`, `ジャンク`, `ふるさと納税`, `返礼品` は禁止。
- アクセサリ、部品、ケース、カバーの混入は禁止。
- 価格下限はカテゴリのノイズが消える水準に置く。

### 文章品質
- `intro` は悩みと約束を書く。
- `analysis_insight` は後悔ポイントを言い切る。
- `critical_cons` は購入判断に効く現実を書く。
- `cost_performance` は価格の高さを論理で回収する。

### 画像品質
- 抽象的な雰囲気画像は禁止。
- 可能ならローカル管理の画像を使う。
- 商品本体が分かるアイキャッチを優先する。

## 4. 日次運用

### 計画公開
- 未来日付の記事ストックを維持する。
- 記事が不足したら、新テーマを追加して補充する。

### 突発公開
- 海外 SNS や Reddit で急騰したトレンドは `type: sns` で別枠公開する。
- トレンド記事でも、比較対象と除外条件は同じ厳密さで扱う。

## 5. 重複防止（チェックリスト）

新規記事の作成・登録前に、必ず以下の項目を確認すること。

- [ ] **ID/Slug/H1/Title の物理的重複:** 
  - `config/articles.yaml` を検索し、同じ値が使われていないか。
  - 特に `slug` は URL になるため、短く一意であること。
- [ ] **検索意図の重複:**
  - 既存記事と「解決したい悩み」が被っていないか。
  - （例：「高級ドライヤー」があるのに「3万円以上のドライヤー」を作るのは禁止。既存記事を更新すること）
- [ ] **キーワードの重複:**
  - `rakuten_params.keyword` が既存記事と酷似していないか。
  - 同一の検索結果を奪い合うのを避ける。
- [ ] **公開日の整合性:**
  - `release_date` が過去のままストックされていないか。
  - 予約投稿（未来日付）の場合は、他の記事と日付が重なっていないか。
- [ ] **バリデーションの実行:**
  - `python src/validate_articles.py` を実行し、エラーがないことを確認済みか。
