import json
from pathlib import Path

import importlib.util


def _load_main_module():
    script = Path("20_project/22_src/main.py").resolve()
    spec = importlib.util.spec_from_file_location("app", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DummyResp:
    def __init__(self, status_code):
        self.status_code = status_code


def test_parse_price_ok():
    module = _load_main_module()
    assert module.parse_price("JPY 12,345") == 12345


def test_run_step0_once_success(monkeypatch, tmp_path: Path):
    cfg = {
        "notification": {
            "enabled": True,
            "provider": "slack",
            "webhook_url": "https://example.invalid/webhook",
            "channel": "#alerts",
            "test_message": "hello",
            "api_key": "",
        },
        "items": [],
    }
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    def fake_post(url, headers, json, timeout):
        assert url == cfg["notification"]["webhook_url"]
        assert json["text"] == "hello"
        return DummyResp(200)

    module = _load_main_module()
    monkeypatch.setattr(module.requests, "post", fake_post)
    ok, message = module.run_step0_once(str(cfg_path))
    assert ok is True
    assert "sent" in message


def test_run_step0_once_missing_webhook(tmp_path: Path):
    cfg = {"notification": {"enabled": True, "webhook_url": ""}, "items": []}
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    module = _load_main_module()
    ok, message = module.run_step0_once(str(cfg_path))
    assert ok is False
    assert "webhook_url is empty" in message
