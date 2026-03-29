import json
from pathlib import Path

import importlib.util


def _load_main():
    script = Path("20_project/22_src/main.py").resolve()
    spec = importlib.util.spec_from_file_location("app", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_stc_001_web_index(tmp_path: Path):
    module = _load_main()
    cfg = {"notification": {"enabled": True, "webhook_url": ""}, "items": []}
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    app = module.create_app(str(cfg_path))
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


def test_stc_002_run_once_redirect(tmp_path: Path):
    module = _load_main()
    cfg = {"notification": {"enabled": True, "webhook_url": ""}, "items": []}
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    app = module.create_app(str(cfg_path))
    client = app.test_client()
    resp = client.post("/run-once")
    assert resp.status_code == 302
