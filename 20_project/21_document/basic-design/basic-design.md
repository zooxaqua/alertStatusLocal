# basic-design 成果物

## 1. 目的
requirements を満たすための全体設計を定義する。

## 2. 入力
- 前工程成果物: `20_project/21_document/requirements/requirements.md`
- 要求/制約: ローカル cron、Step0通知先行、`config.json`設定管理

## 3. 全体構成
- CLI層: `main.py` (`--once`, `--test-notify`, `--web`)
- 通知層: Slack送信関数
- 設定層: `config.json` ロード/保存
- UI層: Flask によるブラウザ管理画面
- 運用層: cron + README手順
- テスト層: unit/integration/system

## 4. 詳細
- 正常系:
  - CLI `--once` が通知関数を呼び成功終了
  - UIから通知テスト実行
  - cronで定期起動
- 異常系:
  - webhook未設定/失敗をエラーとして返す
  - UI入力バリデーション違反
- インターフェース:
  - config notification: `provider`, `webhook_url`, `api_key`, `channel`, `test_message`, `enabled`
  - items: `id`, `name`, `url`, `target_price`, `price_selector`, `last_price`, `last_checked_at`

## 6. 課題・リスク
- `config.json` に機密情報を置くためアクセス制御が必要。
- ローカル環境依存（OS/cron/ネットワーク）。

## 7. 次工程への引き継ぎ
- 詳細設計でCLI引数、関数I/F、UIルート、テストケースを明記する。
