# Stock Article Factory

この手順書は、軽量モデルでも `LifeTech Select` のストック記事を再現性高く作るための正本です。

## 目的

- 楽天アフィリエイトで購入直前の読者に刺さる比較記事を継続投入する。
- 6/14までと同じ品質で、公開前に商品取得・QA・静的監査まで完了させる。
- レビュー本文を取得していない状態で、口コミ本文を読んだような断定を書かない。

## 追加先

- 通常記事: `config/articles.yaml`
- 未来公開のストック記事: `config/articles_stock.yaml`
- 商品データ: `data/products/{article_id}.json`

`src/config_loader.py` が2つのYAMLを結合するため、未来記事は `articles_stock.yaml` に入れる。

## テーマ選定

優先順は以下。

1. 価格が高く、楽天アフィリエイトの成果単価が見込める商品
2. 購入後の後悔ポイントが明確な商品
3. トップメーカーを3から4社並べられる商品
4. 楽天市場で新品在庫があり、商品名と商品説明からQA条件を満たせる商品
5. レビュー評価・件数が取れる、または仕様差だけでも比較価値がある商品

避けるテーマ:

- 安価な消耗品、部品、アクセサリ中心のテーマ
- 中古在庫しか取れないテーマ
- 医療・法務・金融など、断定のリスクが高いテーマ
- 公式情報や楽天商品説明だけで差別化できないテーマ

## 必須フィールド

各記事には必ず以下を入れる。

- `id`, `category_id`, `type`, `slug`, `release_date`
- `h1`, `title`, `intro`, `meta_description`, `analysis_insight`
- `qa_config`
- `rakuten_params`
- `test_criteria`
- `products_extra`

`products_extra` は各商品ごとに以下を必須にする。

- `keyword`
- `best_for`
- `scores`
- `analysis_why`
- `pros`
- `critical_cons`
- `maintenance_reality`
- `cost_performance`

## 根拠ルール

楽天商品検索APIで取得できる主な根拠は以下。

- 商品名
- 商品説明
- 価格
- レビュー評価
- レビュー件数
- 商品画像
- ショップ名
- アフィリエイトURL

レビュー本文は取得できない。したがって、以下は禁止。

- 「口コミでは静かという声が多い」など本文を読んだ断定
- 「低評価レビューを分析した」など未取得データを根拠にする表現
- メーカー公式の主張を検証済みの事実として書く表現

使ってよい表現:

- 「公開レビュー評価・件数を見る限り」
- 「商品説明の仕様表記では」
- 「レビュー母数が少ないため、仕様と保証条件も併せて確認」
- 「購入前に商品ページで型番・付属品・保証を確認」

## QA設定

`qa_config.required_words` は、商品本体だけを通すための語にする。表記ゆれを想定し、必要なら複数入れる。

例:

- Webカメラ: `WEBカメラ`, `Webカメラ`, `ウェブカメラ`
- ゲーミングモニター: `モニター`, `ディスプレイ`
- ウルトラワイド: `ウルトラワイド`, `UltraWide`, `'21:9'`, `曲面`

`21:9` のような値は YAML が数値解釈するため、必ずクォートする。

`forbidden_words` にはテーマ固有の除外語を入れる。全体で避けるべき語は `config/article_quality_rules.yaml` に集約する。

## 商品取得

新規ストック記事だけ取得する場合:

```powershell
$env:PYTHONPATH='D:\嘉秋\Antigravity\projects\rakuten-affiliate-site\.codex_python_deps;D:\嘉秋\Antigravity\projects\rakuten-affiliate-site\src'
$env:LTS_ARTICLE_IDS='article-id-1,article-id-2'
& 'C:\Users\yoshi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'src/fetch_products.py'
```

取得後、`[MISS]` が出た商品は公開しない。次のいずれかで直す。

- 楽天市場で新品在庫があるブランド・型番に差し替える
- `keyword` を実際の商品名に合わせて緩和する
- `required_words` の表記ゆれを追加する
- どうしても取得できない商品は `products_extra` から外し、記事タイトルの選数も合わせる

## 公開前検証

未来日を指定して全公開予定をシミュレーションする。

```powershell
$env:PYTHONPATH='D:\嘉秋\Antigravity\projects\rakuten-affiliate-site\.codex_python_deps;D:\嘉秋\Antigravity\projects\rakuten-affiliate-site\src'
& 'C:\Users\yoshi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'src/validate_articles.py'
$env:LTS_TODAY='2026-06-14'
& 'C:\Users\yoshi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'src/build_site.py'
& 'C:\Users\yoshi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'src/audit_site.py'
```

合格条件:

- `validate_articles.py`: errors=0, warnings=0
- `build_site.py`: 公開対象記事がすべて生成され、CRITICAL QA ERROR が0
- `audit_site.py`: errors=0, warnings=0

## 公開後PDCA

記事を追加したら、7日後・14日後・30日後に以下を見る。

- Google Search Console: 表示回数、クリック数、CTR、平均掲載順位、インデックス状況
- 楽天アフィリエイト: クリック数、成果件数、売上、報酬、商品別クリック
- GitHub Pages: デプロイ成功と公開URL確認

改善の優先順位:

1. インデックスされていない記事をGSCで登録依頼
2. 表示ありクリックなしの記事はタイトルとメタを検索意図に寄せる
3. クリックあり成果なしの記事は導入文、比較軸、CTA、商品選定を見直す
4. 成果が出た記事は周辺ロングテール記事を追加する
