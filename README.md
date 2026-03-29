# alertStatusLocal

## プロジェクト概要
ECサイト価格監視ツールのローカル運用版です。Step0として`--once`で通知疎通のみを先に確認し、その後価格監視機能を拡張します。

## 主要機能
- Step0: `--once` でSlack通知のみ実行
- 監視対象の設定管理（`config.json`）
- ローカル定期実行（cron）
- ブラウザ管理画面（一覧・追加/編集/削除・通知テスト）

## 技術スタック
- Python
- Playwright
- Flask
- Slack Webhook
- ローカル cron

## セットアップ手順
1. 依存関係をインストール
```bash
python3 -m pip install -r 20_project/22_src/requirements.txt
```
2. 設定ファイルを編集
- `20_project/22_src/config.json` の `notification.webhook_url` を実値に更新

## 環境変数
- `ALERTSTATUS_CONFIG_PATH` (任意): `config.json` のパスを上書き

## フォルダ構成
- `20_project/21_document/`: 工程成果物
- `20_project/22_src/`: 実装
- `30_test/`: テスト資産

## 定期実行設定
ローカル cron 例（毎時0分）:
```cron
0 * * * * cd /workspaces/alertStatusLocal && /usr/bin/python3 20_project/22_src/main.py --config /workspaces/alertStatusLocal/20_project/22_src/config.json --once >> /tmp/alertstatus.log 2>&1
```

## テスト実行
- 単体テスト: `make test-run`
- 結合テスト: `make integration-test`
- システムテスト: `make system-test`
- 手動通知テスト: `make run-once`

## 対象サイト別カスタマイズ
`config.json` の `items[].price_selector` をサイトごとに調整してください。
Amazon向けは `#corePrice_desktop` を基準に実装できます。

## ライセンス
社内検証用（未定義）