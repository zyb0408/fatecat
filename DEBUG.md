# DEBUG.md - bootstrap build isolation network failure

## Bug

`bash scripts/acceptance.sh --with-dev --with-mingli-bench --output /tmp/fatecat-acceptance-full-test` 在 `delivery-smoke` 的 `preflight --bootstrap` 阶段失败。

## Environment

- Repo: `/home/lenovo/.projects/fatecat`
- Runtime root: `/home/lenovo/.projects/fatecat`
- Python: `.venv/bin/python`
- Failure phase: `pip install -e .` during bootstrap called by delivery preflight

## Reproduction

Command:

```bash
bash scripts/acceptance.sh --with-dev --with-mingli-bench --output /tmp/fatecat-acceptance-full-test
```

Observed failure excerpt:

```text
ERROR: Could not find a version that satisfies the requirement hatchling
ERROR: Failed to build 'file:///home/lenovo/.projects/fatecat' when installing build dependencies
```

## Observations

- `pyproject.toml` uses `build-backend = "hatchling.build"`.
- `hatchling` editable installs require `editables` when build isolation is disabled.
- The active `.venv` did not have `hatchling` installed before the failed delivery smoke bootstrap.
- `requirements.txt`, `requirements-dev.txt`, and `requirements.lock.txt` did not declare `hatchling`.
- `pip install -e .` used build isolation, so pip tried to fetch `hatchling` from PyPI inside a temporary build environment.
- Network access to PyPI returned `ReadTimeoutError` / `SSLEOFError`, making the release gate flaky.

## Hypotheses

1. Build isolation is the root cause because editable install fetches build backend from PyPI during test execution.
   - Supports: failure is specifically inside "installing build dependencies" for `hatchling`.
   - Test: install build-system requirements in the venv first and run editable install with `--no-build-isolation`.
2. The failure is a transient PyPI outage only.
   - Supports: error includes network timeout and SSL EOF.
   - Conflicts: release gate should not require nested build dependency fetches once bootstrap has prepared the venv.
   - Test: rerun without changing bootstrap would likely be flaky rather than structurally fixed.
3. The package metadata is missing build backend declaration.
   - Conflicts: `pyproject.toml` correctly declares `hatchling`.
   - Test: inspect `pyproject.toml`.

## Root Cause

`bootstrap.sh` relied on PEP 517 build isolation for editable installs, but did not preinstall the declared build backend into the managed venv. This made delivery smoke depend on a nested online fetch of `hatchling`.

## Fix

- Install `pyproject.toml` build-system requirements into `.venv` during bootstrap.
- Use `pip install --no-build-isolation -e .` once build requirements are present.
- Add `hatchling` and `editables` to build-system/dev dependency declarations so developer environments expose the packaging backend explicitly.

## Regression Evidence

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/acceptance.sh --with-dev --with-mingli-bench --output /tmp/fatecat-acceptance-full-test
```

Result:

- `bootstrap.sh --with-dev` completed and `pip show hatchling editables` reported installed packages.
- The former failing path passed: `bash scripts/delivery-smoke.sh --target api --response-file /tmp/fatecat-delivery-api-after-build-fix.json`.
- Full acceptance with MingLi-Bench completed: `/tmp/fatecat-acceptance-full-test`.
