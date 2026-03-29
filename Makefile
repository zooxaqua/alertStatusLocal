PYTHON ?= python3
CONFIG ?= /workspaces/alertStatusLocal/20_project/22_src/config.json

run-once:
	$(PYTHON) 20_project/22_src/main.py --config $(CONFIG) --once

test-run:
	$(PYTHON) -m pytest -q 30_test/31_unit/logic

run-web:
	$(PYTHON) 20_project/22_src/main.py --config $(CONFIG) --web --host 0.0.0.0 --port 8000

integration-test:
	$(PYTHON) -m pytest -q 30_test/32_integration/logic

system-test:
	$(PYTHON) -m pytest -q 30_test/33_system/logic
