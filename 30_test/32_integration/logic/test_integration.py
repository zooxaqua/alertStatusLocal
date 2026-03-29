import json
from pathlib import Path
import importlib.util


def _load_main_module():
    script = Path("20_project/22_src/main.py").resolve()
    spec = importlib.util.spec_from_file_location("app", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_itc_001_once_success(tmp_path: Path, monkeypatch):
    module = _load_main_module()
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

    class R:
        def __init__(self, code: int):
            self.status_code = code

    def fake_post(*args, **kwargs):
        return R(200)

    monkeypatch.setattr(module.requests, "post", fake_post)
    ok, message = module.run_step0_once(str(cfg_path))
    assert ok is True
    assert "sent" in message


def test_itc_002_once_missing_webhook(tmp_path: Path):
    module = _load_main_module()
    cfg = {"notification": {"enabled": True, "webhook_url": ""}, "items": []}
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    ok, message = module.run_step0_once(str(cfg_path))
    assert ok is False
    assert "webhook_url is empty" in message
