# プロジェクト法律: rakuten-affiliate-site

## 1. プロジェクトの目的
楽天市場の商品検索APIを活用し、完全自動で更新されるアフィリエイト静的サイトを構築・運用する。GitHub Actions を利用した「不労所得」モデルのプロトタイプとする。

## 2. 基本原則
- **完全自動化**: データの取得、HTMLの生成、デプロイまでを GitHub Actions で完結させる。
- **低コスト運用**: サーバー費用、API費用を一切かけず、無料枠の範囲内で最大化する。
- **LLM不使用**: 実行時の動的な生成に LLM (OpenAI, Gemini 等) を使用せず、テンプレートエンジン (Jinja2) による高速・確実な生成を行う。

## 3. ディレクトリ構造の定義 (GEMINI.md準拠)
全体憲法に従い、以下の構造を維持する。

- `Rule.md`: 本ファイル（プロジェクトの法律）
- `docs/`: 開発記録、設計書、タスク管理（GitHub Pages公開用ではない）
- `output/`: 
    - `site/`: 生成された静的サイト（GitHub Pages の公開対象）
    - `logs/`: 実行ログ
- `src/`: Pythonソースコード
- `templates/`: Jinja2テンプレート
- `config/`: カテゴリ設定等の設定ファイル
- `data/`: 一時的な商品データ (git ignore対象)

## 4. 技術スタック
- 言語: Python 3.11
- テンプレート: Jinja2
- インフラ: GitHub Actions, GitHub Pages
- API: 楽天商品検索API

## 5. 禁止事項
- Cドライブへのデータ保存（必ず D:\嘉秋\Antigravity 配下を使用）。
- 有料サービスの利用。
- セキュアな情報（API Key等）のコードへの直書き（GitHub Secretsを使用）。
