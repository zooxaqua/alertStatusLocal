# Domain Checklist

- `config.json` に商品名・URL・ターゲット価格のリストが定義されている
- `main.py` が `config.json` から監視対象を読み込んでいる
- CSSセレクタが変数化され、後から調整できる構造になっている
- 価格取得処理が関数として共通化されている
- 現在価格う7ーゲット価格以下の場合に Slack Webhook へ通知が送られる
- `SLACK_WEBHOOK_URL` が環境変数から取得される（ハードコードされていない）
- GitHub Actions ワークフローが毎日 JST 9:00/12:00/18:00/21:00 に起動する
- GitHub Secrets に `SLACK_WEBHOOK_URL` が登録されている
- 正常系/不正常系（価格取得失敗・ページの構造変化・Webhook失敗）を設計・評価している
