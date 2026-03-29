# integration-test 成果物

## 1. 目的
実装済みコンポーネント間連携を検証する。

## 2. 入力
- 前工程成果物: `20_project/21_document/implementation/implementation.md`
- テスト資産: `30_test/32_integration/input/itc_matrix.csv`, `30_test/32_integration/logic/test_integration.py`

## 3. 全体構成
- ITC-001: Step0成功連携
- ITC-002: webhook未設定異常

## 4. 詳細
- 正常系:
  - ITC-001 実行結果: pass
- 異常系:
  - ITC-002 実行結果: pass（期待エラー）
- 実施率: 100%（2/2）
- 実行コマンド: `python3 -m pytest -q 30_test/32_integration/logic`
- 実行結果: 2 passed in 0.33s
- 証跡: `30_test/32_integration/output/integration_pytest.txt`

## 6. 課題・リスク
- 実外部通知到達性は環境依存。

## 7. 次工程への引き継ぎ
- STCでUI経由の動作確認を実施。
