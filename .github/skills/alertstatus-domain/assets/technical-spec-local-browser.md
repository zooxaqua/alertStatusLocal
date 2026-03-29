# Technical Spec (Local Browser Operations)

このファイルは、alertStatus 案件で利用する技術要件を集約する。
agent 定義側には詳細を重複記載せず、本ファイルを参照して適用する。

## 1. 実装技術の前提
- スクレイピング: Python + Playwright（ヘッドレスブラウザ）
- 通知: Slack Webhook
- 設定管理: `SLACK_WEBHOOK_URL` は環境変数で管理する
- 監視対象: `config.json` で商品名・URL・ターゲット価格を管理する

## 2. コア実装要件
- 価格取得処理は関数として共通化し、サイト差異を吸収する
- CSS セレクタは変数化し、後から調整可能にする
- 価格がターゲット価格以下なら Slack 通知する
- 単発実行（例: `--once`）を提供する
- 通知テスト（例: `--test-notify`）を提供する

## 3. ブラウザ管理画面要件
- ローカルWebサーバ（Flask または FastAPI など）でブラウザアクセス可能にする
- 監視対象一覧で以下を表示する
  - 商品名
  - URL
  - ターゲット価格
  - 最終取得価格
  - 最終実行時刻
  - 通知判定結果
- 監視対象の追加・編集・削除を画面から実行可能にする
- 画面上から「今すぐ監視実行」「通知テスト」を実行可能にする
- バリデーションを実装する
  - URL 形式（http/https）
  - 価格数値（0以上）
  - 必須項目
  - 同一URL重複

## 4. 成果物（実装工程）
- `20_project/22_src/main.py`
- `20_project/22_src/config.json`
- `20_project/22_src/requirements.txt`
- `20_project/22_src/.env.example`
- `30_test/31_unit/input/`
- `30_test/31_unit/logic/`
- `30_test/31_unit/output/`

## 5. 運用方式別ルール
### 5.1 ローカル cron 運用
- `README.md` に cron 設定例を記載する
- `README.md` に手動実行手順（`--once` / `--test-notify`）を記載する
- `release.md` に cron 設定の妥当性確認結果を記載する

### 5.2 GitHub Actions 運用
- `.github/workflows/price_check.yml` を用意する
- GitHub Secrets に `SLACK_WEBHOOK_URL` を登録する
- `release.md` に `workflow_dispatch` 実行結果を記載する

## 6. README 必須セクション
1. プロジェクト概要
2. 主要機能
3. 技術スタック
4. セットアップ手順
5. 環境変数
6. フォルダ構成
7. 定期実行設定
8. テスト実行
9. 対象サイト別カスタマイズ
10. ライセンス（任意）

## 7. リリース確認観点
- 運用方式（ローカル cron / GitHub Actions）と記載内容の整合
- 環境変数/Secrets 設定手順の明確性
- 手動実行結果の記録
- ロールバック方針の記載
