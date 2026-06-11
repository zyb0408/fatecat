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

## 2026-06-11 CI follow-up: setuptools.build_meta unavailable

### Bug

GitHub Actions run `27320894427` failed during `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-ci-acceptance`.

Observed failure excerpt:

```text
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta'
```

### Observations

- The failure happened in bootstrap before tests, immediately after CI created a fresh Python 3.12 venv.
- A clean local temp venv reproduced the environment property: `importlib.util.find_spec("setuptools.build_meta")` raised `ModuleNotFoundError: No module named 'setuptools'`.
- `bootstrap.sh` installed the project with `pip install --no-build-isolation -e .`, which also makes source builds in that install invocation depend on build backends already present in the venv.
- Local acceptance did not expose this because the existing local `.venv` already had `setuptools`.

### Hypotheses

1. The root cause is that project editable install used `--no-build-isolation` while still resolving dependencies.
   - Supports: CI fresh venv lacks `setuptools`, and the failure is `setuptools.build_meta` during dependency preparation.
   - Test: install dependencies in a normal pip step first, then install only the project editable with `--no-deps --no-build-isolation`.
2. The root cause is only a transient PyPI/network issue.
   - Conflicts: the reported backend is missing locally in a clean venv; this is structural for fresh Python 3.12 environments.
3. The root cause is an invalid project build backend.
   - Conflicts: the project backend is `hatchling.build`; the missing backend is `setuptools.build_meta` from a third-party source build.

### Root Cause

`bootstrap.sh` disabled build isolation for the project editable install before separating dependency installation. In a fresh CI venv, third-party source distributions that require `setuptools.build_meta` could not build because `setuptools` was not present in the active environment.

### Fix

- Upgrade `pip`, `setuptools`, and `wheel` as bootstrap seed tooling.
- Install `requirements.txt` or `requirements-dev.txt` in a normal pip dependency step.
- Install the local project editable with `--no-build-isolation --no-deps`, limiting no-build-isolation to FateCat itself.

### Regression Evidence

Completed:

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-ci-fix
```

Result:

- Fresh local `.venv` rebuild completed with the updated bootstrap flow.
- CI-parity acceptance passed end to end: 112 pytest tests, ruff, mypy, API/Bot smoke, export smoke, exported hygiene and strict validation.
- Evidence directory: `/tmp/fatecat-acceptance-ci-fix`.

## 2026-06-11 CI follow-up: iztro vendor hash drift

### Bug

After the bootstrap fix, local CI-parity acceptance reached `vendor-health` and failed:

```text
iztro sha256 mismatch:
expected=195f863dd4c66f3925a757ea0c23255803ac0a27aa831500bafefd87064370be
actual=3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325
```

### Observations

- `tools/reference-repos/github/iztro-main` had no working-tree diff after migration.
- The old manifest at `HEAD^:scripts/project/assets/vendor/vendor_sources.json` recorded `3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325`.
- The migration diff changed only the manifest value from `3817f93...` to `195f863...`.
- File count before and after migration was identical for the iztro snapshot: 338 files.

### Root Cause

The iztro vendor snapshot was migrated byte-for-byte, but `vendor_sources.json` regressed to an older snapshot hash during the path migration.

### Fix

Restore the iztro `snapshotSha256` to the pre-migration verified value `3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325`.

### Regression Evidence

Completed:

```bash
bash scripts/vendor-health.sh
bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-ci-fix
```

Result:

- `vendor-health` passed with `required=5 optionalFutureFeatures=10 hashed=15 licenseAuditRequired=5`.
- The same CI-parity acceptance passed end to end after the manifest correction.
