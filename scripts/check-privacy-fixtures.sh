#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
cd "${skill_root}"

first_party_pattern='济南|历下区|耿至宇|张三|张三丰|深圳南山|深圳市|深圳'
vendor_pattern='济南|历下区|耿至宇|深圳南山'

violations_file="$(mktemp)"
vendor_hits_file="$(mktemp)"
trap 'rm -f "${violations_file}" "${vendor_hits_file}"' EXIT

is_first_party_scan_target() {
  local path="$1"
  case "${path}" in
    README.md|SKILL.md|references/*)
      return 0
      ;;
    AGENTS.md|apps/*|ai/*|domains/*|contracts/*|catalog/*|docs/*|governance/*)
      return 0
      ;;
    scripts/*)
      [[ "${path#scripts/}" != */* ]] && return 0
      ;;
  esac
  return 1
}

is_first_party_excluded() {
  local path="$1"
  case "${path}" in
    scripts/check-privacy-fixtures.sh)
      return 0
      ;;
    # 历史归档、第三方快照和地理数据是隔离证据，不作为一线用户示例扫描。
    docs/reference-materials/archive/*|\
    docs/reference-materials/vendor/*|\
    tools/reference-repos/*|\
    domains/fate-analysis/data-products/*|\
    domains/experience-delivery/services/fatecat-delivery/src/location.py)
      return 0
      ;;
  esac
  return 1
}

while IFS= read -r path; do
  [[ -f "${path}" ]] || continue
  if ! is_first_party_scan_target "${path}"; then
    continue
  fi
  if is_first_party_excluded "${path}"; then
    continue
  fi
  if grep -nH -I -E "${first_party_pattern}" "${path}" >> "${violations_file}"; then
    :
  fi
done < <(git ls-files)

if [[ -s "${violations_file}" ]]; then
  echo "隐私示例扫描失败：一线代码、文档或测试中出现真实感地点/姓名示例。" >&2
  sed 's/^/  - /' "${violations_file}" >&2
  exit 1
fi

vendor_web_paths=()
vendor_root="$(runtime_vendor_dir "${runtime_root}")"
vendor_web_root="${vendor_root}/web"
if [[ -d "${vendor_web_root}" ]]; then
  vendor_web_paths+=("${vendor_web_root#${skill_root}/}")
fi
if [[ -d "tools/reference-repos/web" ]]; then
  vendor_web_paths+=(tools/reference-repos/web)
fi

if [[ "${#vendor_web_paths[@]}" -gt 0 ]]; then
  if git grep -n -I -E "${vendor_pattern}" -- "${vendor_web_paths[@]}" > "${vendor_hits_file}"; then
    while IFS= read -r line; do
      path="${line%%:*}"
      case "${path}" in
        tools/reference-repos/web/pcbz-monolith.html|\
        tools/reference-repos/web/pcbz-singlefile.html|\
        tools/reference-repos/web/pcbz-paipan/*|\
        tools/reference-repos/web/pcbz-wget/*|\
        tools/reference-repos/web/lifekline-main/components/BaziForm.tsx)
          ;;
        *)
          echo "vendor web 示例扫描失败：发现未登记的真实感占位数据。" >&2
          IFS=: read -r hit_path hit_line _rest <<< "${line}"
          echo "  - ${hit_path}:${hit_line}" >&2
          exit 1
          ;;
      esac
    done < "${vendor_hits_file}"
    echo "[privacy-fixtures] vendor web 存在已隔离的第三方示例占位，未作为生产入口使用。"
  fi
fi

echo "privacy fixtures ok"
