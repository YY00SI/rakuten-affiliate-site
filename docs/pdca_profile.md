# Rakuten PDCA Profile

共通判断は `$monetization-pdca` を正本とする。この文書はLifeTech Select固有のデータ定義と品質ゲートだけを定める。

## データ源と指標

| 指標ID | 正式な取得元 | 単位・定義 |
| :--- | :--- | :--- |
| `gsc_clicks` / `gsc_impressions` / `gsc_ctr` / `gsc_average_position` | Google Search Consoleの検索パフォーマンス | 同一の固定比較期間。上位クエリ・ページは補足資料。 |
| `ga4_active_users` / `ga4_page_views` | LifeTech SelectのGA4 | 固定比較期間。プロパティと期間を必ず記録。 |
| `rakuten_affiliate_clicks` / `rakuten_conversions` / `rakuten_sales` / `rakuten_rewards` | 楽天アフィリエイト管理画面 | 同一の固定比較期間。未取得は0に置換しない。 |
| `rakuten_affiliate_click_event` | GA4イベント `rakuten_affiliate_click` | 計測の健全性確認用。楽天管理画面のクリック数と同じ値として扱わない。 |

商品別クリックが現行UIで取得不能な場合は `未取得` とし、ショップ別値を代用しない。

## 初期の判断閾値

- SERP CTRの施策判断: GSC表示100以上、またはGSCクリック10以上。
- 楽天CVRの施策判断: 楽天クリック20以上。
- 下回る場合は `insufficient_sample` とし、露出・計測・導線の仮説に留める。

これは初期ガードレールであり、固定比較期間3回分の実測が揃った時点で見直す。

## 実行

1. `docs/pdca_metrics_input.template.json` をコピーし、取得済み値だけを更新する。
2. 次を実行して小型パケットを作る。

```powershell
python ../../skills/monetization-pdca/scripts/build_pdca_packet.py --project rakuten-affiliate-site --cycle mid --analysis-date YYYY-MM-DD --input docs/pdca_metrics_input.json --output output/pdca_preflight/YYYYMMDD/packet.json
python ../../skills/monetization-pdca/scripts/validate_pdca_packet.py output/pdca_preflight/YYYYMMDD/packet.json
```

3. パケット、直近の実験台帳、STATEだけで分析する。記事を変更するActのときだけ `workflow.md`、`CONTENT_CONTRACT.md`、`QUALITY_GATE.md`、`article_quality_rules.yaml` を読む。
4. 記事・商品・生成サイトを変更した場合は、`validate_articles.py`、必要な`fetch_products.py`、`build_site.py`、`audit_site.py`を全て通す。

## 保存先と復旧

- 入力・パケット・内部作業ログ: `output/pdca_preflight/YYYYMMDD/`
- 親向け決定レポート: `docs/monthly_pdca_YYYY_MM_[mid|end].md`
- 実験台帳: `docs/pdca_experiments.json`
- 公開物に問題がある場合は、変更した設定・記事を直前のGit版へ限定して戻し、全品質ゲートを再実行する。
