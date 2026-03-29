# release 成果物

## 1. 目的
成果物と証跡を確認し、リリース可否を判定する。

## 2. 入力
- 前工程成果物: `20_project/21_document/system-test/system-test.md`
- 実装物: `20_project/22_src/*`
- テスト出力: `30_test/32_integration/output/*`, `30_test/33_system/output/*`

## 3. 全体構成
- 判定: Conditional Go（Webhook実値投入後に本番運用Go）
- 運用方式: local cron

## 4. 詳細
- integration 実施率: 100%（2/2）
- system 実施率: 100%（2/2）
- integration 証跡: `30_test/32_integration/output/integration_pytest.txt`（2 passed）
- system 証跡: `30_test/33_system/output/system_pytest.txt`（2 passed）
- Step0 証跡: `30_test/31_unit/output/step0_once_output.txt`（通知成功）
- local cron 運用要件:
  - READMEにcron例あり
  - READMEに手動テスト実行手順あり
- 未解決課題:
  - 本番Webhook未投入時は実通知到達性が未確認
- ロールバック方針:
  - `config.json` を直前版に戻し、安定コミットへ復帰

## 6. 課題・リスク
- `config.json` に機微情報が含まれるため権限管理が必要。

## 7. 次工程への引き継ぎ
- 運用開始前に実Webhookで `make run-once` を実行し、到達性を確認する。
