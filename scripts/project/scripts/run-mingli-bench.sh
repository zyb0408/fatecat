#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
runtime_root="$(cd -- "${script_dir}/.." && pwd)"
bench_dir="${runtime_root}/assets/vendor/github/MingLi-Bench-main"
python_bin="${PYTHON:-${runtime_root}/.venv/bin/python}"

mode="stats"
year=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/run-mingli-bench.sh [--stats] [--year YYYY]

说明:
  - 默认只执行 MingLi-Bench 离线统计，不调用任何外部模型 API。
  - 该脚本用于验证外部 benchmark 资产可读取，生产模型评测需另行提供真实 API key。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stats)
      mode="stats"
      shift
      ;;
    --year)
      [[ $# -ge 2 ]] || { echo "--year 缺少参数" >&2; exit 2; }
      year="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "未知参数: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -d "${bench_dir}" ]] || { echo "MingLi-Bench 缺失: ${bench_dir}" >&2; exit 1; }
[[ -x "${python_bin}" ]] || python_bin="python3"

"${python_bin}" - "${bench_dir}/data/data.json" "${year}" <<'PY'
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

data_path = Path(sys.argv[1])
selected_year = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None
payload = json.loads(data_path.read_text(encoding="utf-8"))
questions = payload.get("questions")
if not isinstance(questions, list):
    raise SystemExit(f"MingLi-Bench 数据结构异常: {data_path}")

filtered = []
for item in questions:
    if not isinstance(item, dict):
        continue
    question_number = int(item.get("question_number", 0) or 0)
    year = 2022 + ((question_number - 1) // 40) if question_number > 0 else None
    if selected_year is None or year == selected_year:
        filtered.append(item)

categories = Counter(str(item.get("category", "未分类")) for item in filtered)
available_years = sorted({2022 + ((int(item.get("question_number", 0) or 0) - 1) // 40) for item in questions})

print("")
print("Dataset Statistics:")
print("  Name: FortuneTellingBench")
print("  Version: unknown")
print("  Available Years: " + ", ".join(str(item) for item in available_years if item is not None))
if selected_year is not None:
    print(f"  Selected Year: {selected_year}")
print(f"  Total Questions: {len(filtered)}")
print("")
print("  Categories:")
for category, count in sorted(categories.items()):
    print(f"    - {category}: {count}")
PY
