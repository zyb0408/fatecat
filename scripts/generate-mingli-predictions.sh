#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
bench_dir="${runtime_root}/tools/reference-repos/github/MingLi-Bench-main"
python_bin="${PYTHON:-${runtime_root}/.venv/bin/python}"
year=""
sample_size=""
output_jsonl=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/generate-mingli-predictions.sh --output-jsonl predictions.jsonl [--year YYYY] [--sample N]

说明:
  - 读取本地 MingLi-Bench 数据，调用 FateCat pure-analysis 生成可评测 predictions。
  - 不调用外部模型 API，不宣称专业准确率；输出是 scored FateCat baseline。
  - 生成结果可交给 scripts/run-mingli-bench.sh --predictions-file 做 accuracy/coverage 统计。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --year)
      [[ $# -ge 2 ]] || usage_error "--year 缺少参数"
      year="$2"
      shift 2
      ;;
    --sample)
      [[ $# -ge 2 ]] || usage_error "--sample 缺少参数"
      sample_size="$2"
      shift 2
      ;;
    --output-jsonl)
      [[ $# -ge 2 ]] || usage_error "--output-jsonl 缺少参数"
      output_jsonl="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage_error "未知参数: $1"
      ;;
  esac
done

[[ -n "${output_jsonl}" ]] || usage_error "必须提供 --output-jsonl"
[[ -d "${bench_dir}" ]] || die "MingLi-Bench 缺失: ${bench_dir}"
[[ -x "${python_bin}" ]] || python_bin="python3"
ensure_parent_dir "${output_jsonl}"

args=(
  -m fate_core.evaluation.mingli_baseline
  --data "${bench_dir}/data/data.json"
  --output-jsonl "${output_jsonl}"
)
if [[ -n "${year}" ]]; then
  args+=(--year "${year}")
fi
if [[ -n "${sample_size}" ]]; then
  args+=(--sample "${sample_size}")
fi

PYTHONPATH="${runtime_root}/domains/fate-analysis/services/fate-core/src${PYTHONPATH:+:${PYTHONPATH}}" \
  "${python_bin}" "${args[@]}"
