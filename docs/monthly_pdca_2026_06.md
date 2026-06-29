# 2026年6月 月末PDCA

作成日: 2026-06-29
更新日: 2026-06-29

## 対象期間

- 楽天アフィリエイト: 直近30日
- Google Search Console: 2026-04-23 〜 2026-06-26
- GA4: 過去7日間

## Plan

- 主ボトルネック `楽天クリックあり成果0` に対して、`portable-gaming-pc` の購入直前不安解消を補強する。
- CTA と比較表周辺で、販売元、保証、在庫、発送条件の確認文脈を明確にする。
- `ロボット掃除機 高級` と `ai ドローン` の表示ありクリック0クエリに対して、既存記事の title / meta を検索意図へ寄せる。
- 反応が出ている `portable-gaming-pc` を中心に関連記事導線を優先表示し、勝ち筋クラスターを明確化する。
- `rakuten_affiliate_click` は GA4 管理画面のキーイベント化までは行わず、まずサイト側の発火ロジックを補強する。

## Do

- `portable-gaming-pc` の `analysis_insight`、`best_for`、`critical_cons`、`maintenance_reality`、`cost_performance` を、互換性、更新、携帯時の負担、買った後に触らなくなる失敗回避へ寄せて更新。
- `robot-vacuum-ranking` の title / meta_description を `ロボット掃除機 高級` の検索意図へ合わせて調整。
- `ai-drone-ranking` の title / meta_description を `ai ドローン` の検索意図へ合わせて調整。
- [article.html](/D:/嘉秋/OneDrive/04_嘉秋/Antigravity/projects/rakuten-affiliate-site/templates/article.html) の CTA 文脈を更新し、価格、在庫、保証、販売元、発送条件の確認を促す導線に調整。
- [build_site.py](/D:/嘉秋/OneDrive/04_嘉秋/Antigravity/projects/rakuten-affiliate-site/src/build_site.py) で関連記事の明示オーバーライドを先に採用するよう変更し、`portable-gaming-pc` 中心の内部リンクを実際に表示側へ反映させる。
- [base.html](/D:/嘉秋/OneDrive/04_嘉秋/Antigravity/projects/rakuten-affiliate-site/templates/base.html) の `rakuten_affiliate_click` 送信を補強し、通常クリックに加えて補助クリックとキーボード操作でも `beacon` 送信するよう調整。
- Step 7として `validate_articles.py`、変更記事3本の `fetch_products.py`、全件 `build_site.py`、`audit_site.py` を実行した。`validate_articles.py` は `errors=0/warnings=0`、`fetch_products.py` は再取得完了、`build_site.py` は全76記事ビルド完了、`audit_site.py` は `errors=0/warnings=0`。OneDrive 配下の stale ディレクトリ削除警告は出るが非致命で、生成結果と監査結果には影響しない。

## Check

| 項目 | 結果 |
| --- | --- |
| 楽天クリック数 | 5 |
| 楽天成果件数 | 0 |
| 楽天売上 | 0円 |
| 楽天報酬 | 0円 |
| GSC合計クリック | 10 |
| GSC合計表示 | 528 |
| GSC平均CTR | 1.9% |
| GSC平均掲載順位 | 16.0 |
| GA4 PV | 1 |
| GA4アクティブユーザー | 1 |
| GA4主な参照元 | `Direct` 1 |
| `rakuten_affiliate_click` イベント数 | 0 |
| インデックス登録済み | 19 |
| 未インデックス | 15 |
| 公開URL確認 | トップ / `laser-printer` / `projector-ranking` が `200 OK` |
| ストック記事の最終公開予定日 | `2026-08-07` |
| 変更記事 | `portable-gaming-pc` / `robot-vacuum-ranking` / `ai-drone-ranking` |
| 品質ゲート | `validate_articles.py` `errors=0/warnings=0` / `fetch_products.py` 再取得完了 / `build_site.py` 全76記事ビルド完了 / `audit_site.py` `errors=0/warnings=0` |
| GA4キーイベント化 | 未実施 |

## 収益・検索データ

### 楽天アフィリエイト

| 指標 | 値 |
| --- | ---: |
| クリック数 | 5 |
| 成果件数 | 0 |
| 売上 | 0円 |
| 報酬 | 0円 |
| 成果商品 | なし |
| 商品別クリック | 未取得 |

補足:
- 現行の楽天管理画面では `レポート > ショップ別` まで取得可能で、内訳は `Panasonic Store Plus 楽天市場店 1`、`KINUJO【公式】楽天市場店 1`、`ひかりTVショッピング 楽天市場店 2`、`長野県筑北村 1` だった。
- `ショップ別` の展開で確認できたのは日別クリック数までで、商品単位へのドリルダウンは確認できなかった。

### Google Search Console

| 指標 | 値 |
| --- | ---: |
| 合計クリック | 10 |
| 合計表示 | 528 |
| 平均CTR | 1.9% |
| 平均掲載順位 | 16.0 |
| 上位クエリ | `ポータブルゲーミングpc 2026` / `umpc ゲーミング 2026` / `umpc 2026` |
| 上位ページ | `portable-gaming-pc` / `massage-gun` / `smart-home-kit` / `drum-washer` / `projector-ranking` |
| 未インデックスURL | 15 |

### GA4

| 指標 | 値 |
| --- | ---: |
| PV | 1 |
| アクティブユーザー | 1 |
| 主な参照元 | `Direct` 1 |
| `rakuten_affiliate_click` | 0 |

### 公開・供給状態

| 指標 | 値 |
| --- | --- |
| 公開URL確認 | トップ / `laser-printer` / `projector-ranking` が `200 OK` |
| ストック記事の最終公開予定日 | `2026-08-07` |

## 判断

- 主ボトルネックは `楽天クリックあり成果0` のまま。クリックは発生しているため、今回は購入直前の不安解消とCTA文脈の明確化を優先して実装した。
- 副ボトルネックは `表示ありクリック0`。`ロボット掃除機 高級` と `ai ドローン` は表示があるのにクリックが取れていないため、今回の title / meta 調整対象にした。
- 勝ち筋は引き続き `portable-gaming-pc`。上位ページで 5クリック / 49表示と最も反応しているため、関連記事導線もこのクラスターを優先する判断に寄せた。
- `rakuten_affiliate_click` は GA4 上で 0 のままだが、今回はまずサイト側の送信ロジックを補強した。管理画面でのキーイベント化と実数確認は次段階に残る。
- 楽天の注文明細は `対象データが見つかりませんでした` のため `成果商品: なし`。一方で `商品別クリック` は未取得のため、個別商品の入れ替え判断は保留のまま。
- 公開URL確認は取得済みで `200 OK`、ストックも `2026-08-07` まであるため、今回の主因は公開停止や供給不足ではない。
- 品質ゲート4本は完了し、`build_site.py` の stale ディレクトリ削除警告は非致命と確認できたため、今回のActは公開前品質ゲート通過と扱う。

## Act

### 今回実装したAct

1. `portable-gaming-pc` の購入直前不安解消を補強
2. 楽天リンク直前CTAと比較表周辺の購入前確認文脈を再調整
3. `robot-vacuum-ranking` の title / meta 見直し
4. `ai-drone-ranking` の title / meta 見直し
5. `portable-gaming-pc` 中心の内部リンク導線を実際の表示優先順へ反映
6. `rakuten_affiliate_click` の発火ロジックを補強

### 今回未実装のAct

1. 未インデックスURL 15件の個別URL検査・再クロール依頼
理由: 今回は成果化導線とCTR改善を優先し、ブラウザ依存の個別検査は Step 7 以降へ回したため。
2. 商品別クリックに基づく商品入れ替え
理由: `商品別クリック` が未取得で、商品単位の判断根拠が不足しているため。
3. GA4 管理画面での `rakuten_affiliate_click` キーイベント化
理由: 今回はサイト側の発火ロジック補強までに留め、管理画面設定は別運用タスクとして残したため。
4. 2026-08-07以降の新規記事大量追加
理由: ストックは確保済みで、翌月は既存記事の成果化と検索改善を優先するため。

### 翌月KPI案

| 指標 | 2026-06実績 | 2026-07案 |
| --- | ---: | ---: |
| GSC合計クリック | 10 | 20 |
| GSC合計表示 | 528 | 1,000 |
| GSC平均CTR | 1.9% | 2.5% |
| 楽天クリック数 | 5 | 10 |
| 楽天成果件数 | 0 | 1 |
| 楽天CVR | 0.00% | 3.0% |
| GA4 PV | 1 | 20 |
| GA4アクティブユーザー | 1 | 10 |
| `rakuten_affiliate_click` イベント数 | 0 | 1 |
| インデックス登録済みページ | 19 | 25 |
| 未インデックスURL | 15 | 10以下 |

### 記事追加方針

- 2026-07前半は新規記事を増やさず、既存の収益導線、CTR、内部リンク、計測を優先する。
- 新規記事を出す場合は、`portable-gaming-pc` 周辺のようにクリック増または成果発生が確認できたカテゴリへ限定する。
- 低反応カテゴリは、未インデックス解消と title / meta 改善の結果を見てから追加判断する。

### 撤退または方針転換ライン

- 2026-07月末で GSC合計表示が 800 未満なら、記事追加よりインデックス導線改善を優先する。
- 2026-07月末で GSC平均CTRが 1.5% 未満なら、title / meta の再設計を優先する。
- 2026-07月末で楽天クリックが 5 未満なら、CTA位置、商品リンクの視認性、比較表の構成を再設計する。
- 2026-07月末で楽天クリック10以上かつ成果0なら、商品選定と購入直前不安解消の見直しを最優先にする。
- 2026-07月末で `rakuten_affiliate_click` が 0 のままなら、GA4計測の信頼を置かず実装確認を先に行う。
- 2026-07月末で `商品別クリック` が未取得のままなら、商品単位の入れ替えではなく記事単位の導線改善に留める。

## KPI対比

| 指標 | 6月目標 | 6月実績 | 判定 |
| --- | ---: | ---: | --- |
| GSC合計クリック | 30 | 10 | 未達 |
| GSC合計表示 | 1,500 | 528 | 未達 |
| 楽天クリック数 | 10 | 5 | 未達 |
| 楽天成果件数 | 1 | 0 | 未達 |
| GA4アクティブユーザー | 50 | 1 | 未達 |
| インデックス登録済み記事数 | 25以上を目安 | 19 | 未達 |

## 未取得値

- 商品別クリック

## 次回取得テンプレート

```text
対象期間:
楽天クリック数:
楽天成果件数:
楽天売上:
楽天報酬:
成果商品:
商品別クリック:
GSC合計クリック:
GSC合計表示:
GSC平均CTR:
GSC平均掲載順位:
上位クエリ:
上位ページ:
未インデックスURL:
GA4 PV:
GA4アクティブユーザー:
GA4主な参照元:
rakuten_affiliate_click イベント数:
公開URL確認:
ストック記事の最終公開予定日:
```

## 次のアクション

1. GA4 管理画面で `rakuten_affiliate_click` を確認し、キーイベント化する。
2. 未取得の `商品別クリック` を楽天管理画面の別導線から取得する。
3. 2026-07中旬時点で `portable-gaming-pc` 周辺のクリック推移を見て、型番別・悩み別記事追加の可否を判断する。
