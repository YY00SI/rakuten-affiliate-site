# プロジェクト進捗状況 (2026-04-26)

## 1. 全体概要
楽天アフィリエイト「セレクトガイド型」サイトの品質向上作業中。
`qa_check.py` による品質監査を行い、不合格記事の修正およびマスターピース（特定商品）の照合精度を改善している。

## 2. 現在のステータス
- **品質監査 (QA Check):** 12/21 記事が [PASS]
- **サイト生成 (Build):** 実行済み
- **デプロイ (Deploy):** 2026-04-26 22:30 初回デプロイ完了（OK記事のみ公開中）
  - `audio-glasses-ranking` はマスターピース不一致によりビルドがブロックされた（仕様通り）。
  - 未来の日付の記事はビルドから自動的にスキップされている。

## 3. 合格記事 [PASS]
1. hair-dryer-ranking
2. ferrofluid-speaker
3. robot-vacuum-ranking
4. coffee-maker-ranking
5. ai-drone-ranking
6. smart-lock-ranking
7. keyboard-ranking
8. auto-cooker-ranking
9. toaster-ranking
10. facial-device-ranking
11. hair-iron-ranking
12. projector-ranking

## 4. 解決すべき課題 (不合格記事)
以下の記事でマスターピースのキーワード不一致、または価格・除外ワードによるエラーが発生中。
※カッコ内は照合を目指すマスターピース名

- **audio-glasses-ranking:** (HUAWEI Eyewear, Soundcore)
- **office-chair-ranking:** (アーロンチェア, エルゴヒューマン)
- **toothbrush-ranking:** (ソニッケアー, オーラルB)
- **monitor-arm:** (エルゴトロン, Pixio)
- **smart-home-kit:** (SwitchBot, Nature Remo)
- **premium-rice-cooker:** (炎舞炊き, 土鍋ご泡火炊き, ビストロ, 本炭釜)
- **ai-voice-recorder:** (PLAUD, VOITER) ※価格判定エラーあり

## 5. 実施済みの重要な修正
- `src/fetch_products.py` および `qa_check.py` を、各記事の `qa_config` (min_price, forbidden_words 等) を参照するように修正。
- サイト生成プログラム `src/build_site.py` を、マスターピース不一致時にビルドを停止するように強化。

## 6. 次の作業
1. `config/articles.yaml` のキーワードを慎重に修正（文字化けに注意）。
2. `python src/fetch_products.py` でデータを最新化。
3. `python qa_check.py` で全パスを確認。
4. `python src/build_site.py` で全記事を生成。
