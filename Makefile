.PHONY: venv rebuild-venv install install-dev install-locked install-dev-locked freeze preflight acceptance structure hygiene privacy governance export-lite export-hygiene lint format format-black typecheck test pre-commit build sdist wheel docs-serve clean-runtime clean-cache serve-api serve-bot container-build container-smoke container-release

PYTHON ?= python3
EXPORT_PARENT ?= /tmp/fatecat-export

venv:
	$(PYTHON) -m venv .venv

rebuild-venv:
	rm -rf .venv
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e '.[dev]'

install-locked:
	$(PYTHON) -m pip install -c requirements.lock.txt -r requirements.txt

install-dev-locked:
	$(PYTHON) -m pip install -c requirements-dev.lock.txt -r requirements-dev.txt

freeze:
	$(PYTHON) -m pip freeze > requirements.lock.txt

preflight:
	bash scripts/preflight.sh --mode pure --bootstrap --pretty

acceptance:
	bash scripts/acceptance.sh --with-dev

structure:
	bash scripts/check-structure.sh

hygiene:
	bash scripts/check-source-hygiene.sh

privacy:
	bash scripts/check-privacy-fixtures.sh

governance:
	python3 governance/tools/validate_governance_package.py --project-root . --strict

export-lite:
	bash scripts/export-runtime.sh --output-parent $(EXPORT_PARENT) --mode lite

export-hygiene:
	bash scripts/check-export-hygiene.sh $(EXPORT_PARENT)/fatecat

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

format-black:
	$(PYTHON) -m black .

typecheck:
	$(PYTHON) -m mypy -p fate_core

test:
	$(PYTHON) -m pytest -q

pre-commit:
	$(PYTHON) -m pre_commit run --all-files

build:
	$(PYTHON) -m build

sdist:
	$(PYTHON) -m build --sdist

wheel:
	$(PYTHON) -m build --wheel

docs-serve:
	$(PYTHON) -m mkdocs serve

clean-runtime:
	bash scripts/clean-runtime.sh

clean-cache:
	$(PYTHON) -m pip cache purge
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name build -o -name dist -o -name '*.egg-info' \) -prune -exec rm -rf {} +

serve-api:
	bash scripts/serve-api.sh

serve-bot:
	bash scripts/serve-bot.sh

container-build:
	bash scripts/container-build.sh

container-smoke:
	bash scripts/container-smoke.sh

container-release:
	bash scripts/container-release.sh
