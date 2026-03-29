# detailed-design 成果物

## 1. 目的
基本設計を実装可能な粒度へ分解する。

## 2. 入力
- 前工程成果物: `20_project/21_document/basic-design/basic-design.md`
- 要求/制約: Step0優先、newモード、ローカル運用

## 3. 全体構成
- BE(ロジック): `load_config`, `save_config`, `send_slack_notification`, `run_step0_once`
- FE(UI): Flask routes `/`, `/items/new`, `/items/<id>/edit`, `/items/<id>/delete`, `/run-once`, `/test-notify`
- CLI: `--once`, `--test-notify`, `--web`

## 4. 詳細
- 正常系:
  - `run_step0_once` -> 2xxで成功
  - UI操作でitem CRUD成功
- 異常系:
  - `webhook_url` 空で失敗
  - URL形式不正、価格数値不正、重複URLで失敗
- データ定義:
  - notification object, items array
- テスト設計:
  - UT-001 parse_price
  - UT-002 step0 success
  - UT-003 step0 missing webhook
  - ITC/STC マトリクス全件実行

## 6. 課題・リスク
- 実Slack接続試験は環境依存。
- 画面テンプレートの最小実装では見た目調整余地あり。

## 7. 次工程への引き継ぎ
- 実装ファイル/テストファイル/READMEを作成する。
- 実行結果を output に残す。
