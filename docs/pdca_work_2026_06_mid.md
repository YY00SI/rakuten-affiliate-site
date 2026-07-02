# 2026年6月 月央PDCA 作業ログ（途中再開用）

作成日: 2026-06-21
ブラウザポート: 9222（デバッグ用Chrome）

## 作業状況

- [x] A8ログイン → subsidy-saas-matcher の月次レポート取得完了
- [x] 楽天アフィリエイト レポート取得完了
- [x] GSC (rakuten-affiliate-site) パフォーマンス取得完了
- [x] GA4 (rakuten-affiliate-site) ホームデータ取得完了（過去7日のみ）
- [ ] GSC (subsidy-saas-matcher) 取得 ← 次の作業
- [ ] GA4 過去30日データ取得（レポートページへ移動が必要）
- [ ] rakuten-affiliate-site 月央PDCAレポート作成
- [ ] subsidy-saas-matcher 月央PDCAレポート作成
- [ ] rakuten-affiliate-site ストック記事追加（8/7分まで）
- [ ] git_push.bat 実行

---

## 取得済みデータ

### A8.net（subsidy-saas-matcher用）
- 対象期間: 2026年06月（今月）
- imp数（合計）: 9
- click数（合計）: 0
- CTR: -（クリックなし）
- 発生件数: 0
- 発生金額: 0円
- 未確定金額: 0円

案件別内訳:
| プログラム名 | imp前々月 | imp前月 | imp今月 | click数 | 発生件数 | 発生金額 |
|---|---|---|---|---|---|---|
| マネーフォワード クラウド確定申告 | 0 | 0 | 0 | 1 | 0 | 0 |
| 個人事業主特化ファクタリング | 0 | 0 | 0 | 0 | 0 | - |
| KANBEI SIGN（IT導入補助金対応）| 0 | 0 | 0 | 2 | 0 | 0 |
| CLOUDPHONE（IT導入補助金対応）| 0 | 0 | 0 | 2 | 0 | 0 |
| freee会計 | 0 | 0 | 0 | 2 | 0 | 0 |
| 弥生シリーズ | 0 | 0 | 0 | 2 | 0 | 0 |

※ imp数のカラムが前々月/前月/今月の3列になっているが全て0。click数は月全体の合計9。

---

### 楽天アフィリエイト（rakuten-affiliate-site用）
- 対象期間: 直近30日（2026年5月下旬〜6月21日）
- クリック数: **5**
- 売上件数（未確定）: 0
- 売上金額（未確定）: ¥0
- 成果報酬（未確定）: ¥0
- CVR: 0.00%

---

### Google Search Console（rakuten-affiliate-site）
- 対象期間: 2026/04/23 〜 2026/06/19（約2ヶ月）
- 合計クリック数: **10**
- 合計表示回数: **510**
- 平均CTR: **2%**
- 平均掲載順位: **16.3**

上位クエリ:
| クエリ | クリック | 表示 |
|---|---|---|
| ポータブルゲーミングpc 2026 | 1 | 17 |
| umpc ゲーミング 2026 | 1 | 4 |
| umpc 2026 | 1 | 1 |
| site:github.io "無料ギフト"... | 0 | 10 |
| ロボット掃除機 高級 | 0 | 6 |
| ai ドローン | 0 | 6 |
| ドライヤー 高級 | 0 | 4 |
| 27インチ 4k モニター おすすめ 2026 | 0 | 3 |
| 高級ドライヤー | 0 | 3 |
| 合計クエリ数: 47 |

---

### GA4（rakuten-affiliate-site / LifeTech Select）
- 対象期間: 過去7日間
- アクティブユーザー: **1**
- 表示回数: **1**
- イベント数: **4**
- 新規ユーザー: 1
- セッション: Organic Search 1, Direct 0

上位ページ（表示回数）:
| ページタイトル | 表示 |
|---|---|
| 【2026年最新】プロジェクター 厳選2選｜4Kとレーザーの極地 | 1 |

参照元:
| 参照元/メディア | アクティブユーザー |
|---|---|
| google / organic | 1 |
| (direct) / (none) | 0 |

---

## 次の作業手順

1. GSC (subsidy-saas-matcher) データ取得
   - タブID: 60D7FF95496BFF5EB473B4DFCE471C0F
   - URL: https://search.google.com/search-console/performance/search-analytics?resource_id=https%3A%2F%2Fyy00si.github.io%2Fsubsidy-saas-matcher%2F

2. GA4 過去30日データ取得（LifeTech Select）
   - タブID: 575A8197E2C93BD98AC43B13CA66291D

3. 月央PDCAレポート作成（両プロジェクト）

4. ストック記事追加（rakuten-affiliate-site、8/7分まで）
   - `config/articles_stock.yaml` に追記
   - `fetch_products.py` 実行
   - `validate_articles.py` → `build_site.py` → `audit_site.py` 実行

5. git_push.bat 実行

## Chromeデバッグ接続情報
- ポート: 9222
- プロファイル: D:\嘉秋\Antigravity\.browser_profiles\pdca_2026_05
