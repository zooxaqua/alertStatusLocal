# system-test 成果物

## 1. 目的
システム全体要件をE2E観点で検証する。

## 2. 入力
- 前工程成果物: `20_project/21_document/integration-test/integration-test.md`
- テスト資産: `30_test/33_system/input/stc_matrix.csv`, `30_test/33_system/logic/test_system.py`

## 3. 全体構成
- STC-001: Web UI index応答
- STC-002: Web UI run-once導線

## 4. 詳細
- 正常系:
  - STC-001 pass
- 異常系:
  - STC-002 pass（エラー安全にリダイレクト）
- 実施率: 100%（2/2）
- 実行コマンド: `python3 -m pytest -q 30_test/33_system/logic`
- 実行結果: 2 passed in 0.27s
- 証跡: `30_test/33_system/output/system_pytest.txt`

## 6. 課題・リスク
- 実Slack到達性はシステムテスト環境ではモック前提。

## 7. 次工程への引き継ぎ
- releaseで運用方式（local cron）の妥当性を判定。
