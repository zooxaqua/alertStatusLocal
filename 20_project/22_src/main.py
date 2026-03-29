import argparse
import datetime as dt
import json
import os
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from flask import Flask, redirect, render_template_string, request, url_for

CONFIG_ENV = "ALERTSTATUS_CONFIG_PATH"
DEFAULT_CONFIG = Path(__file__).resolve().parent / "config.json"


HTML_INDEX = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>alertStatusLocal</title>
  <style>
    body { font-family: sans-serif; margin: 24px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background: #f5f5f5; }
    .msg { margin: 12px 0; color: #0a5; }
    .err { margin: 12px 0; color: #b00; }
    form.inline { display: inline; }
    .actions { display: flex; gap: 8px; margin-bottom: 12px; }
  </style>
</head>
<body>
  <h1>alertStatusLocal</h1>
  {% if message %}<div class=\"msg\">{{ message }}</div>{% endif %}
  {% if error %}<div class=\"err\">{{ error }}</div>{% endif %}

  <div class=\"actions\">
    <a href=\"{{ url_for('new_item') }}\">+ Add Item</a>
    <form class=\"inline\" method=\"post\" action=\"{{ url_for('run_once') }}\"><button>Run --once</button></form>
    <form class=\"inline\" method=\"post\" action=\"{{ url_for('run_test_notify') }}\"><button>Run --test-notify</button></form>
  </div>

  <table>
    <thead>
      <tr>
        <th>Name</th><th>URL</th><th>Target</th><th>Last Price</th><th>Last Checked</th><th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {% for item in items %}
      <tr>
        <td>{{ item['name'] }}</td>
        <td>{{ item['url'] }}</td>
        <td>{{ item['target_price'] }}</td>
        <td>{{ item.get('last_price') }}</td>
        <td>{{ item.get('last_checked_at') }}</td>
        <td>
          <a href=\"{{ url_for('edit_item', item_id=item['id']) }}\">Edit</a>
          <form class=\"inline\" method=\"post\" action=\"{{ url_for('delete_item', item_id=item['id']) }}\">
            <button>Delete</button>
          </form>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""


HTML_FORM = """
<!doctype html>
<html>
<head><meta charset=\"utf-8\"><title>{{ title }}</title></head>
<body>
  <h1>{{ title }}</h1>
  {% if error %}<div style=\"color:#b00\">{{ error }}</div>{% endif %}
  <form method=\"post\">
    <label>Name <input name=\"name\" value=\"{{ item.get('name','') }}\" required maxlength=\"100\"></label><br>
    <label>URL <input name=\"url\" value=\"{{ item.get('url','') }}\" required maxlength=\"500\"></label><br>
    <label>Target Price <input name=\"target_price\" value=\"{{ item.get('target_price','') }}\" required></label><br>
    <label>Price Selector <input name=\"price_selector\" value=\"{{ item.get('price_selector','#price') }}\"></label><br>
    <button>Save</button>
  </form>
  <a href=\"{{ url_for('index') }}\">Back</a>
</body>
</html>
"""


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def resolve_config_path(config_path: str | None = None) -> Path:
    if config_path:
        return Path(config_path)
    env = os.getenv(CONFIG_ENV)
    if env:
        return Path(env)
    return DEFAULT_CONFIG


def load_config(config_path: str | None = None) -> Dict[str, Any]:
    path = resolve_config_path(config_path)
    return json.loads(path.read_text(encoding="utf-8"))


def save_config(config: Dict[str, Any], config_path: str | None = None) -> None:
    path = resolve_config_path(config_path)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def parse_price(text: str) -> int:
    digits = re.sub(r"[^0-9]", "", text)
    if not digits:
        raise ValueError("price text has no digits")
    return int(digits)


def _notification_headers(notification_cfg: Dict[str, Any]) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    api_key = (notification_cfg.get("api_key") or "").strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def send_slack_notification(
    notification_cfg: Dict[str, Any],
    message: str,
    post_func=None,
    timeout: int = 10,
) -> Tuple[bool, str]:
    if not notification_cfg.get("enabled", True):
        return False, "notification is disabled"

    webhook = (notification_cfg.get("webhook_url") or "").strip()
    if not webhook:
        return False, "webhook_url is empty"

    payload = {"text": message}
    channel = (notification_cfg.get("channel") or "").strip()
    if channel:
        payload["channel"] = channel

    try:
        if post_func is None:
            post_func = requests.post
        resp = post_func(
            webhook,
            headers=_notification_headers(notification_cfg),
            json=payload,
            timeout=timeout,
        )
        if 200 <= resp.status_code < 300:
            return True, f"slack notification sent: {resp.status_code}"
        return False, f"slack notification failed: {resp.status_code}"
    except Exception as exc:  # pragma: no cover
        return False, f"slack notification error: {exc}"


def run_step0_once(config_path: str | None = None) -> Tuple[bool, str]:
    config = load_config(config_path)
    notification = config.get("notification", {})
    message = notification.get("test_message") or "[Step0] alertStatusLocal test"
    return send_slack_notification(notification, message)


def _validate_item(name: str, url: str, target_price: str, existing_urls: List[str], current_id: str | None = None) -> Tuple[bool, str]:
    if not (1 <= len(name) <= 100):
        return False, "name must be 1-100 chars"
    if not re.match(r"^https?://", url):
        return False, "url must start with http:// or https://"
    try:
        val = float(target_price)
    except ValueError:
        return False, "target_price must be numeric"
    if val < 0:
        return False, "target_price must be >= 0"
    if url in [u for u in existing_urls if u != current_id]:
        return False, "duplicate url"
    return True, ""


def create_app(config_path: str | None = None) -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        cfg = load_config(config_path)
        items = sorted(cfg.get("items", []), key=lambda x: x.get("last_checked_at") or "", reverse=True)
        return render_template_string(HTML_INDEX, items=items, message=request.args.get("message"), error=request.args.get("error"))

    @app.route("/items/new", methods=["GET", "POST"])
    def new_item():
        if request.method == "GET":
            return render_template_string(HTML_FORM, title="Add Item", item={}, error=None)

        cfg = load_config(config_path)
        item = {
            "id": f"item-{int(dt.datetime.now().timestamp())}",
            "name": request.form.get("name", "").strip(),
            "url": request.form.get("url", "").strip(),
            "target_price": request.form.get("target_price", "").strip(),
            "price_selector": request.form.get("price_selector", "#price").strip(),
            "last_price": None,
            "last_checked_at": None,
        }
        ok, err = _validate_item(item["name"], item["url"], item["target_price"], [x.get("url", "") for x in cfg.get("items", [])])
        if not ok:
            return render_template_string(HTML_FORM, title="Add Item", item=item, error=err)
        item["target_price"] = float(item["target_price"])
        cfg.setdefault("items", []).append(item)
        save_config(cfg, config_path)
        return redirect(url_for("index", message="item created"))

    @app.route("/items/<item_id>/edit", methods=["GET", "POST"])
    def edit_item(item_id: str):
        cfg = load_config(config_path)
        items = cfg.get("items", [])
        item = next((x for x in items if x.get("id") == item_id), None)
        if not item:
            return redirect(url_for("index", error="item not found"))

        if request.method == "GET":
            return render_template_string(HTML_FORM, title="Edit Item", item=item, error=None)

        item2 = deepcopy(item)
        item2["name"] = request.form.get("name", "").strip()
        item2["url"] = request.form.get("url", "").strip()
        item2["target_price"] = request.form.get("target_price", "").strip()
        item2["price_selector"] = request.form.get("price_selector", "#price").strip()

        ok, err = _validate_item(item2["name"], item2["url"], item2["target_price"], [x.get("url", "") for x in items], current_id=item.get("url", ""))
        if not ok:
            return render_template_string(HTML_FORM, title="Edit Item", item=item2, error=err)

        item2["target_price"] = float(item2["target_price"])
        idx = items.index(item)
        items[idx] = item2
        save_config(cfg, config_path)
        return redirect(url_for("index", message="item updated"))

    @app.post("/items/<item_id>/delete")
    def delete_item(item_id: str):
        cfg = load_config(config_path)
        cfg["items"] = [x for x in cfg.get("items", []) if x.get("id") != item_id]
        save_config(cfg, config_path)
        return redirect(url_for("index", message="item deleted"))

    @app.post("/run-once")
    def run_once():
        ok, msg = run_step0_once(config_path)
        return redirect(url_for("index", message=msg if ok else None, error=None if ok else msg))

    @app.post("/test-notify")
    def run_test_notify():
        ok, msg = run_step0_once(config_path)
        return redirect(url_for("index", message=msg if ok else None, error=None if ok else msg))

    return app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="alertStatusLocal runner")
    parser.add_argument("--config", default=None, help="config.json path")
    parser.add_argument("--once", action="store_true", help="Step0: send Slack notification only")
    parser.add_argument("--test-notify", action="store_true", help="send Slack test notification")
    parser.add_argument("--web", action="store_true", help="run local web admin UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.web:
        app = create_app(args.config)
        app.run(host=args.host, port=args.port)
        return 0

    if args.once or args.test_notify:
        ok, message = run_step0_once(args.config)
        print(message)
        return 0 if ok else 1

    print("No action selected. Use --once, --test-notify, or --web.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
