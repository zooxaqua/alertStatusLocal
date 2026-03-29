---
name: alertstatus-domain
description: "alertStatus 案件の専門情報を提供します。Use for domain constraints, price monitoring rules, Slack notification strategy, and local cron or GitHub Actions scheduling hints."
argument-hint: "参照したい工程と検討対象（価格取得セレクタ・通知条件・ECサイト別対応・スケジュールなど）"
user-invocable: true
---
# AlertStatus Domain

本 skill は本案件特有の専門情報を集約します。エージェント本体は汎用に保ち、ドメイン知識はこの skill を参照して適用します。

## ドメイン要件の核
- ECサイトの商品価格を定期的に監視し、基準価格以下になったら Slack で通知する。
- 監視対象は `config.json` で管理する（商品名・URL・ターゲット価格）。
- CSSセレクタは変数化し、後からサイトごとに調整できる構造にする。
- 価格取得処理は関数として共通化し、サイト構造の違いに対応する。

## 推奨技術スタック
- スクレイピング: Python + Playwright（ヘッドレスブラウザ）
- 通知: Slack Webhook（環境変数 `SLACK_WEBHOOK_URL` から取得）
- 定期実行: ローカル cron（必要に応じて GitHub Actions も選択可）
- 設定管理: ローカル環境変数（GitHub Actions 利用時は GitHub Secrets）

## 段階実装の推奨順
1. MVP: `main.py` + `config.json` + Slack 通知のコアロジック
2. ローカル定期実行（cron）と手動テスト実行導線の追加
3. ブラウザ管理画面の追加（監視対象管理、今すぐ実行、通知テスト）
4. Amazon.co.jp 他、特定サイト向けの価格パース最適化

## 対象サイト別対応方針
- **Amazon.co.jp**: `#corePrice_desktop` 内の価格テキストから数値のみを抽出する正規表現を含むパース関数を実装する。
- その他ECサイト: CSSセレクタ変数を切り替えることで対応する。

## 参照リソース
- [technical spec (local/browser)](./assets/technical-spec-local-browser.md)
- [domain checklist](./assets/domain-checklist.md)
- [mode policy](./assets/new-vs-delta-policy.md)
