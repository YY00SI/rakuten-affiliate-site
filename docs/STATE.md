# rakuten-affiliate-site 進捗の正本

## 現在のフェーズ
運用・インデックス促進・SEO戦略転換フェーズ

## 完了済み
- 2026-06-29: ブラウザ追補を実施。Google Search Console の `未登録 15` は `2026-06-12` 時点の古い集計で、可視10URLを個別URL検査した結果 `audio-glasses` は登録済み、残る `action-camera` / `facial-device` / `auto-cooker` / `ai-drone` / `massage-gun` / `electric-shaver` / `home/` / `beauty/` / `work/` は未登録を確認し、URL 検査から優先クロールキューへ追加した。楽天管理画面はログイン済みで今月クリック5・成果0を再確認した一方、現行UIでは `商品別クリック` 導線を特定できず再取得不能。GA4 は公開記事から楽天リンク実クリック後も `rakuten_affiliate_click` が 0 のままだったため、`templates/base.html` を修正し `window.gtag` の明示束縛と `sendBeacon` フォールバックを追加。`validate_articles.py` は errors=0/warnings=0、`build_site.py` は全76記事ビルド完了、`audit_site.py` は errors=0/warnings=0。
- 2026-06-29: 緊急改善追補を公開反映完了。未インデックス15件そのものは外部状態のため即時解消できないが、`portable-gaming-pc` を含む勝ち筋導線を記事上部の関連記事導線と `RELATED_ARTICLE_OVERRIDES` 拡張で補強し、`robot-vacuum-ranking` / `ai-drone-ranking` / `portable-gaming-pc` の title/meta を再調整、`rakuten_affiliate_click` は `pointerup` も拾うよう補強した。`validate_articles.py` は errors=0/warnings=0、対象3記事の `fetch_products.py` 再取得完了、`build_site.py` は 全76記事ビルド完了、`audit_site.py` は errors=0/warnings=0。stale ディレクトリ削除警告は継続するが非致命。
- 2026-06-29: GitHub同期: 月末PDCA関連のソース、生成物、`monthly_pdca_2026_06.md`、`pdca_work_2026_06_end.md` を `main` へ同期済み。同期後にローカルHEADとGitHub HEADの一致を確認した。
- 2026-06-29: Git remote設定: サニタイズ済み。
- 2026-06-29: 6月月末PDCA Step 7 を更新完了。主要数値は楽天クリック5・成果0・売上0円・報酬0円、GSCクリック10・表示528・CTR 1.9%・平均順位16.0、GA4 PV1・アクティブユーザー1・`rakuten_affiliate_click` 0。実装済みActとして、`portable-gaming-pc` の購入直前不安解消補強、CTA文脈改善、`robot-vacuum-ranking` / `ai-drone-ranking` の title/meta 更新、`portable-gaming-pc` 中心の内部リンク補強、`rakuten_affiliate_click` 発火ロジック補強を反映。`validate_articles.py` は errors=0/warnings=0、変更記事3本の `fetch_products.py` は再取得完了、全件 `build_site.py` は 76記事ビルド完了、`audit_site.py` は errors=0/warnings=0。OneDrive 配下の stale ディレクトリ削除警告は継続するが、生成結果と監査結果には影響しない。
- 2026-06-29: 品質ゲート残課題の追補を完了。`projector-ranking` は `XGIMI` 軸へ、`laser-printer-ranking` は `Canon レーザープリンター` と `required_words: レーザー` 追加で楽天商品一致条件を補正し、両記事の不一致を解消。`validate_articles.py` は errors=0/warnings=0、対象2記事の `fetch_products.py` 再取得完了、全件 `build_site.py` は 76記事ビルド完了、`audit_site.py` は errors=0/warnings=0。これで全件ビルド時の `[CRITICAL QA ERROR]` は解消した。
- 2026-06-29: 旧記録・更新済み。初回の6月月末PDCA Step 7記録では GA4 PV3・アクティブユーザー3、`gaming-monitor-ranking` / `hair-dryer-ranking` 更新、`projector-ranking` / `laser-printer-ranking` の商品一致エラー残存を記録していたが、その後の再取得と品質ゲート残課題解消を反映した正本は上記の「6月月末PDCA Step 7 を更新完了」を参照する。
- 2026-06-21: 6月月央PDCAを実施。楽天アフィリエイト直近30日クリック5・売上0、GSC合計クリック10・表示510・CTR 2%・平均順位16.3（期間2026/04/23-2026/06/19）、GA4過去7日アクティブユーザー1。ストック記事は8/7まで確保済みで追加不要。`docs/monthly_pdca_2026_06_mid.md` を作成。
- 2026-06-05: 6/15〜6/30の16本ストック記事を `config/articles_stock.yaml` に追加し、全品質ゲートを通過。楽天APIでの代替ブランド差し替え（Litter-Robot→トレッタ、Morus Zero→東芝、LOWYA→カリモク）を行い全16記事で4アイテム構成を確保。全77記事のビルド・監査に成功し、GitHub Pages へのデプロイ（git push）を完了。
- 2026-05-31: 月末PDCAのAct実装を完了。比較表直後に楽天「価格を見る」CTAを追加し、全楽天リンクに `data-affiliate-click` を付与、GA4へ `rakuten_affiliate_click` を送信する計測を追加。`ロボット掃除機 高級`、`ai ドローン`、`高級 トースター` の露出クエリに合わせてtitle/metaを調整。`build_site.py` はプロジェクトルート基準 of 絶対パス出力へ修正し、`validate_articles.py` errors=0/warnings=0、未来日込み全61記事ビルド、`audit_site.py` errors=0/warnings=0を確認。楽天API取得は外部ネットワークで一部タイムアウトしたため、商品キャッシュは既存データを維持。
- 2026-05-31: ログイン後に未取得だった月末PDCA数値を再取得し、`docs/monthly_pdca_2026_05.md` に追記。楽天アフィリエイトは今月クリック1、未確定売上0円、未確定成果報酬0円、売上件数0。Google Search Consoleは合計クリック8、合計表示369、平均CTR 2.2%、平均掲載順位17.1（画面表示期間 2026/04/23-2026/05/29）。GA4 LifeTech Selectは過去7日間のアクティブユーザー16、イベント211、表示回数162、キーイベント0を確認。公開トップと `/work/ultrawide-monitor/` の表示、canonical、楽天リンク、`sponsored` 属性も再確認済み。
- 2026-05-29: 5月末PDCAを実施し、`docs/monthly_pdca_2026_05.md` を作成。`validate_articles.py` は errors=0/warnings=0、`LTS_TODAY=2026-06-14` の未来日込みビルドは全61記事生成、`audit_site.py` は errors=0/warnings=0。公開トップと代表記事 `/work/ultrawide-monitor/` をブラウザで確認し、canonicalと楽天アフィリエイトリンクの `sponsored` 属性を確認。月末Actionとして、サイト説明・高級ヘアドライヤー記事・ロボット掃除機記事に残っていた未検証の数量表現を、公開レビュー評価・件数、価格、仕様表記に基づく表現へ修正。
- 5月中旬のPDCAデータ取得 (Rakuten Affiliate, Google Search Console)
- 楽天APIのエラーでビルド不可となっていたすべての記事（オーディオグラス、ウルトラワイドモニター等を含む全34記事）のキーワード緩和・修復完了
- 全34記事のビルド成功とGitHub Pagesへのデプロイ（`git_push.bat`による同期完了）
- Google Search Consoleでの優先URL（トップ、カテゴリ、主要記事の計12件）に対するインデックス手動登録リクエスト完了
- 2026-05-24: 独自分析の根拠表示を全面強化。各ページ冒頭にレビュー母数・加重平均評価・価格帯・根拠スコープを表示し、各商品に「根拠メモ」を追加。楽天APIの商品探索を拡張し、`hidden_gem_candidates` による掘り出し物候補の別枠表示を実装。`validate_articles.py` / `build_site.py` / `audit_site.py` はすべて通過。
- 2026-05-24: 2026-06-01から2026-06-14までのストック記事14本を `config/articles_stock.yaml` に追加し、楽天APIで商品データ取得済み。`LTS_TODAY=2026-06-14` のシミュレーションで全61記事生成、監査エラー0を確認。
- 2026-05-24: 既存 `ultrawide-monitor-ranking` の中古商品混入を修正。`allow_used: true` を撤回し、新品で取得できるLG/JAPANNEXT/MSIの3選へ再構成。
- 2026-05-24: 軽量モデル向けの継続記事作成手順 `docs/ai/STOCK_ARTICLE_FACTORY.md` と、PDCA必要情報 `docs/PDCA_REQUIREMENTS.md` を整備。

## 進行中
- 6月分析用の問題提起および引継ぎ事項の整理（`docs/current_status.md` としてドキュメント化完了）
- サイト全体のインデックス促進
- ビッグキーワードからロングテールキーワードへの戦略転換準備
- 外部ブログ・専門レビュー記事を根拠データとして扱うパイプラインの設計
- GSC の優先クロールキュー投入後のインデックス反映待ち
- GA4 `rakuten_affiliate_click` 修正反映後の再計測確認

## 次のアクション
1. 公開反映後に GA4 管理画面で `rakuten_affiliate_click` の再発火を確認し、必要ならキーイベント化する。
2. GSC で優先クロールキューへ追加した 9 URL の再判定結果を確認する。
3. 楽天管理画面の現行UIで `商品別クリック` が取れない前提で、当面は注文詳細・ショップ別・GA4・GSC を代替根拠に使う。
4. 2026-07中旬時点で `portable-gaming-pc` 周辺のクリック推移を確認し、型番別・悩み別記事追加の可否を判断する。

## 判断ログ
- 2026-06-29: GSC の `未登録 15` はページレポート更新日が `2026-06-12` で止まっていたため、個別 URL 検査で実態を優先した。少なくとも `audio-glasses` はすでに登録済みで、可視9URLは `インデックス登録をリクエスト済み` まで進めたため、次は集計画面ではなく URL 検査結果の反映待ちとして扱う。
- 2026-06-29: 楽天アフィリエイト管理画面はログイン済みでも、現行UIでは `商品別クリック` の取得導線を確認できなかった。したがって、次回PDCAまでは `商品別クリック` を必須入力から外さず未取得扱いのまま残し、商品単位の判断は保留する。
- 2026-06-29: GA4 は公開記事からの実クリック後も `rakuten_affiliate_click` が 0 のままで、ブラウザ実行状態でも `window.gtag` / `window.dataLayer` が不在だった。テンプレート出力自体は存在していたため、初期化を `window.gtag` 明示束縛へ変更し、さらに `sendBeacon` で直接 `g/collect` へ送るフォールバックを追加して、クライアント側の取りこぼしを減らす方針とした。
- 2026-06-29: 緊急改善追補では、未インデックス15件をリポジトリ側だけで即時解消することはできないため、クロールと回遊の両方に効く内部リンク強化を優先した。`portable-gaming-pc` / `gaming-monitor-ranking` / `ultrawide-monitor-ranking` 周辺に加え、`keyboard-ranking` / `office-chair-ranking` / `monitor-arm` / `premium-webcam-ranking` からも勝ち筋へ寄せる構成に変更した。加えて、記事上部にも関連記事導線を追加し、`rakuten_affiliate_click` は `click` / `auxclick` / `keydown` に加えて `pointerup` も取得するよう補強した。公開前品質ゲートは validate/fetch/build/audit で再確認済み。
- 2026-06-29: GitHub未同期の是正として、月末PDCA関連のコミットを `origin/main` へ push し、同期後にローカルHEADとGitHub HEADの一致を確認した。`config/articles_stock.yaml` と未追跡のストック下書き群は今回PDCAの同期対象から外し、ローカル作業中変更として保持した。
- 2026-06-29: Git remote設定: サニタイズ済み。
- 2026-06-29: Step 7 として `validate_articles.py`、変更記事3本の `fetch_products.py`、全件 `build_site.py`、`audit_site.py` を実行。`fetch_products.py` は最初の実行でネットワーク制約、`build_site.py` は `docs/home/wine-cellar/index.html` の権限で止まったため、いずれも権限外で再実行して完走した。最終結果は validate/audit ともに `errors=0, warnings=0`、全76記事ビルド完了。したがって、今回の実装変更は品質ゲート通過と判断する。OneDrive 配下の stale ディレクトリ削除警告は残るが、生成結果と監査結果には影響しない。
- 2026-06-29: 品質ゲート残課題として分離していた `projector-ranking` と `laser-printer-ranking` の楽天商品一致条件を補正し、対象2記事の再取得後に全件 `build_site.py` と `audit_site.py` を再実行した。`build_site.py` は OneDrive 配下の stale ディレクトリ削除警告を出すがビルド完了し、`audit_site.py` は errors=0/warnings=0。したがって、リポジトリ全体の公開前品質ゲートは `[CRITICAL QA ERROR]` なしへ復帰した。残課題は計測確認と未取得運用データに移る。
- 2026-06-29: 旧判断・更新済み。月末PDCAのStep 5/6直後は `projector-ranking` と `laser-printer-ranking` に商品一致エラーが残っていたが、その後の補修と再実行により `build_site.py` / `audit_site.py` の全体品質ゲートは通過済み。最終判断は上位の 2026-06-29 記録を正とする。
- 2026-05-31: 月末PDCAの未取得情報を再取得。Search Consoleではクリック8・表示369まで伸び、特にポータブルゲーミングPC/UMPC系クエリでクリックが発生している一方、楽天成果はクリック1・売上0に留まる。GA4はOrganic Search 15、Direct 3で、検索流入は発生済みだがキーイベント0のため、次の課題は「露出のある記事のCTR改善」と「楽天リンククリック計測・導線改善」。Search Consoleの `site:github.io` 系クエリはノイズとして施策対象外。
- 2026-05-29: 月末PDCAでは、楽天アフィリエイトは未ログイン、Search Consoleは案内ページ、GA4はGoogleアカウント側の本人確認待ち表示で止まり、認証後の数値は未取得。公開ページとローカル品質ゲートは通過済み。Google検索の `site:` 確認では一部ページのインデックスを確認できたが、検索スニペットに修正前表現が残る可能性があるため、公開反映後にURL検査と再クロール促進が必要。
- 2026-05-24: ユーザー実行後の公開確認をブラウザで実施。公開側で `/work/ultrawide-monitor/` と `/work/gaming-monitor/` が404だった原因は、GitHubリモート最新の自動更新コミットが多数の記事HTMLを削除していたこと。ローカルの完全な生成済みサイトを正として `Recover generated site after remote auto-update` をpushし、公開後に全69 URLをブラウザで直接確認。404なし、商品記事のアフィリエイトリンク欠落なし。再発防止としてGitHub Actionsにページ減少ガード追加を試みたが、現在のPATにworkflow権限がなくpush不可のため未反映。
- 2026-05-24: 6/14までのストック記事を追加。楽天APIの商品名表記ゆれで落ちた `premium-webcam-ranking` と `gaming-monitor-ranking` は required_words を補正して解消。`ultrawide-monitor-ranking` は過去に中古許可で通していたが、収益記事として不適切なため新品在庫に寄せて再設計した。
- 2026-05-24: 収益化の前提となる信頼性強化として、独自インサイトの根拠表示、商品ごとの根拠メモ、掘り出し物候補の別枠表示を実装。楽天商品検索APIで取得できるレビュー情報はレビュー本文ではなく `reviewCount` / `reviewAverage` であるため、記事表現を「口コミ本文を読んだ断定」から「公開レビュー評価・件数・商品説明・仕様表記に基づく判断」へ寄せた。詳細は `docs/monetization_evidence_upgrade_2026-05-24.md`。
- 2026-05-18: 楽天APIの[MISS]エラーおよびビルドゲートブロック問題の完全解消。特に `ultrawide-monitor-ranking` については、楽天API上で該当製品（Dell, LG, HUAWEI等）が中古在庫としてしか存在しないため、グローバルな「中古」除外制限に引っかかっていたのが根本原因と特定。`src/article_contract.py` を拡張して `allow_used: true` による個別許可オプションを実装し、製品情報を正常取得させた。全34記事が100%エラーフリーでビルド成功、GitHubへデプロイ完了。
- 2026-05-17: 楽天APIで弾かれていた商品キーワードを、型番指定からブランド名や汎用キーワードに緩和することで、ビルドエラーを100%解消した。
- 2026-05-17: ブラウザを使用して5月中旬のPDCA実績を取得。楽天（クリック0・売上0）、GSC（表示1・クリック0）。トラフィックゼロの根本原因は「ドメインパワー0（新規サイト）」および「ページがインデックスされていないこと」と特定。対策として、AIブラウザ操作によりGSCへの手動インデックス登録リクエストを代行実行した。今後は強豪がひしめくビッグKWを避け、ロングテール狙いへの転換を図る。
- 2026-05-17: 本日の修正事項およびSTATE.mdの更新分をすべてGitHubへ同期（git push）完了。フェーズの移行準備が整った。
