#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

cd "${skill_root}"

violations_file="$(mktemp)"
warnings_file="$(mktemp)"
trap 'rm -f "${violations_file}" "${warnings_file}"' EXIT

required_roots=(
  apps
  ai
  domains
  platform
  infra
  contracts
  catalog
  governance
  shared
  tools
  docs
  scripts
  tests
)

for root in "${required_roots[@]}"; do
  if [[ ! -d "${root}" ]]; then
    printf 'missing canonical root: %s\n' "${root}" >> "${violations_file}"
  fi
done

required_service_files=(
  domains/fate-analysis/services/fate-core/README.md
  domains/fate-analysis/services/fate-core/AGENTS.md
  domains/fate-analysis/services/fate-core/service.yaml
  domains/fate-analysis/services/fate-core/src/fate_core/__init__.py
  domains/fate-analysis/services/fate-core/tests/test_service_contract.py
  domains/experience-delivery/services/fatecat-delivery/README.md
  domains/experience-delivery/services/fatecat-delivery/AGENTS.md
  domains/experience-delivery/services/fatecat-delivery/service.yaml
  domains/experience-delivery/services/fatecat-delivery/src/_paths.py
  domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py
  catalog/components/fate-core.yaml
  catalog/components/fatecat-delivery.yaml
)

for path in "${required_service_files[@]}"; do
  if [[ ! -f "${path}" ]]; then
    printf 'missing service contract file: %s\n' "${path}" >> "${violations_file}"
  fi
done

required_root_files=(
  .auto-github.json
  .dockerignore
  .editorconfig
  .gitignore
  .gitmodules
  .pre-commit-config.yaml
  .python-version
  CHANGELOG.md
  CONSTITUTION.md
  LICENSE
  Makefile
  compose.yaml
  mkdocs.yml
  pyproject.toml
  requirements.txt
  requirements-dev.txt
  requirements.lock.txt
)

required_container_files=(
  infra/docker/AGENTS.md
  infra/docker/Dockerfile.delivery
  infra/docker/entrypoint.delivery.sh
  infra/environments/production/AGENTS.md
  infra/environments/production/.env.production.example
  scripts/container-build.sh
  scripts/container-smoke.sh
  scripts/container-release.sh
  .github/workflows/container.yml
)

for path in "${required_container_files[@]}"; do
  if [[ ! -f "${path}" ]]; then
    printf 'missing container release file: %s\n' "${path}" >> "${violations_file}"
  fi
done

for path in "${required_root_files[@]}"; do
  if [[ ! -f "${path}" ]]; then
    printf 'missing root maintenance file: %s\n' "${path}" >> "${violations_file}"
  fi
done

retired_roots=(
  services
  products
  assets
  config
  libs
  middle-platform
  internal-platform
)

for root in "${retired_roots[@]}"; do
  if [[ -e "${root}" ]]; then
    printf 'retired root exists at repository top level: %s\n' "${root}" >> "${violations_file}"
  fi
done

if [[ -d "scripts/project" ]]; then
  printf 'retired compatibility box still exists: scripts/project\n' >> "${violations_file}"
fi

if ! grep -q 'source_root: domains/fate-analysis/services/fate-core/src' domains/fate-analysis/services/fate-core/service.yaml; then
  printf 'fate-core service.yaml does not point source_root at canonical service src\n' >> "${violations_file}"
fi

if grep -q 'legacy_source_root:' domains/fate-analysis/services/fate-core/service.yaml; then
  printf 'fate-core service.yaml still declares legacy_source_root\n' >> "${violations_file}"
fi

if ! grep -q 'source_root: domains/experience-delivery/services/fatecat-delivery/src' domains/experience-delivery/services/fatecat-delivery/service.yaml; then
  printf 'fatecat-delivery service.yaml does not point source_root at canonical service src\n' >> "${violations_file}"
fi

if grep -q 'legacy_source_root:' domains/experience-delivery/services/fatecat-delivery/service.yaml; then
  printf 'fatecat-delivery service.yaml still declares legacy_source_root\n' >> "${violations_file}"
fi

if [[ -s "${violations_file}" ]]; then
  echo "structure gate failed:" >&2
  sed 's/^/  - /' "${violations_file}" >&2
  exit 1
fi

if [[ -s "${warnings_file}" ]]; then
  echo "structure gate warnings:" >&2
  sed 's/^/  - /' "${warnings_file}" >&2
fi

echo "structure gate ok"
