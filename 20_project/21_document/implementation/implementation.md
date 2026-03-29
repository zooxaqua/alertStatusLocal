# implementation 成果物

## 1. 目的
Step0を含む実装と単体評価を完了する。

## 2. 入力
- 前工程成果物: `20_project/21_document/detailed-design/detailed-design.md`
- 要求/制約: `config.json`設定、ローカル運用、UI管理画面

## 3. 全体構成
- `20_project/22_src/main.py`
- `20_project/22_src/config.json`
- `20_project/22_src/requirements.txt`
- `20_project/22_src/.env.example`
- `30_test/31_unit/*`

## 4. 詳細
- 実装内容:
  - `--once` / `--test-notify` 実装（Step0通知のみ）
  - Slack送信関数（成功/失敗戻り値）
  - Flask管理画面とCRUD
  - Makefile/README整備
- 正常系観点:
  - Step0通知成功ケース
  - UIの一覧表示
- 異常系観点:
  - webhook空
  - 不正入力
- 単体評価:
  - 実行コマンド: `python3 -m pytest -q 30_test/31_unit/logic`
  - 結果: 3 passed in 0.23s
  - 証跡: `30_test/31_unit/output/unit_pytest.txt`
  - Step0通知証跡: `30_test/31_unit/output/step0_once_output.txt`（`slack notification sent: 200`）

## 6. 課題・リスク
- 実Webhook未投入では本番通知確認は未完了。
- `config.json` の権限管理が必要。

## 7. 次工程への引き継ぎ
- ITC/STCをフル実行し、結果をoutputへ残す。
