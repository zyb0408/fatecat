#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
runtime_root="$(cd -- "${script_dir}/.." && pwd)"
bench_dir="${runtime_root}/assets/vendor/github/MingLi-Bench-main"
python_bin="${PYTHON:-${runtime_root}/.venv/bin/python}"

mode="stats"
year=""
sample_size=""
predictions_file=""
prompt_out=""
output_json=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/run-mingli-bench.sh [--stats] [--year YYYY] [--sample N]
  bash scripts/run-mingli-bench.sh --prompt-out prompts.jsonl [--year YYYY] [--sample N]
  bash scripts/run-mingli-bench.sh --predictions-file predictions.jsonl [--output-json report.json]

说明:
  - 默认执行 MingLi-Bench 离线统计，不调用任何外部模型 API。
  - --prompt-out 生成 FateCat 评测提示词 JSONL，供外部模型或人工评测使用。
  - --predictions-file 读取本项目/外部模型已生成答案并计算准确率；不会联网。
  - predictions 支持 JSONL 或 JSON，字段可用 question_id/id、predicted_answer/prediction/answer、response。
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
    --sample)
      [[ $# -ge 2 ]] || { echo "--sample 缺少参数" >&2; exit 2; }
      sample_size="$2"
      shift 2
      ;;
    --predictions-file)
      [[ $# -ge 2 ]] || { echo "--predictions-file 缺少参数" >&2; exit 2; }
      predictions_file="$2"
      mode="evaluate"
      shift 2
      ;;
    --prompt-out)
      [[ $# -ge 2 ]] || { echo "--prompt-out 缺少参数" >&2; exit 2; }
      prompt_out="$2"
      mode="prompt"
      shift 2
      ;;
    --output-json)
      [[ $# -ge 2 ]] || { echo "--output-json 缺少参数" >&2; exit 2; }
      output_json="$2"
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

"${python_bin}" - \
  "${bench_dir}/data/data.json" \
  "${year}" \
  "${sample_size}" \
  "${predictions_file}" \
  "${prompt_out}" \
  "${output_json}" \
  "${mode}" <<'PY'
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

data_path = Path(sys.argv[1])
selected_year = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None
sample_size = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
predictions_file = Path(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None
prompt_out = Path(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] else None
output_json = Path(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] else None
mode = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] else "stats"
payload = json.loads(data_path.read_text(encoding="utf-8"))
questions = payload.get("questions")
if not isinstance(questions, list):
    raise SystemExit(f"MingLi-Bench 数据结构异常: {data_path}")


def benchmark_year(item: dict) -> int | None:
    question_number = int(item.get("question_number", 0) or 0)
    return 2022 + ((question_number - 1) // 40) if question_number > 0 else None


filtered = []
for item in questions:
    if not isinstance(item, dict):
        continue
    year = benchmark_year(item)
    if selected_year is None or year == selected_year:
        filtered.append(item)
if sample_size is not None:
    filtered = filtered[:sample_size]

categories = Counter(str(item.get("category", "未分类")) for item in filtered)
available_years = sorted({benchmark_year(item) for item in questions if benchmark_year(item) is not None})


def build_prompt(item: dict) -> str:
    birth_info = item.get("birth_info") if isinstance(item.get("birth_info"), dict) else {}
    options = item.get("options") if isinstance(item.get("options"), list) else []
    option_lines = "\n".join(f"{opt.get('letter')}. {opt.get('text')}" for opt in options if isinstance(opt, dict))
    return (
        "以下是一道关于中国传统命理的选择题。请基于题目给出的出生信息与选项判断，"
        "最后只用“答案：X”的格式给出 A/B/C/D。\n\n"
        f"命主信息：\n{birth_info.get('raw', birth_info)}\n\n"
        f"问题：{item.get('question', '')}\n\n"
        f"选项：\n{option_lines}"
    )


def write_prompts(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for item in items:
            row = {
                "question_id": item.get("id"),
                "question_number": item.get("question_number"),
                "benchmark_year": benchmark_year(item),
                "category": item.get("category"),
                "prompt": build_prompt(item),
            }
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_predictions(path: Path) -> dict[str, dict]:
    if not path.exists():
        raise SystemExit(f"predictions 文件不存在: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    if path.suffix == ".jsonl":
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        data = json.loads(text)
        if isinstance(data, dict) and isinstance(data.get("predictions"), list):
            rows = data["predictions"]
        elif isinstance(data, dict):
            rows = [{"question_id": key, **value} if isinstance(value, dict) else {"question_id": key, "answer": value} for key, value in data.items()]
        elif isinstance(data, list):
            rows = data
        else:
            raise SystemExit(f"predictions 数据结构异常: {path}")
    result: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        qid = str(row.get("question_id") or row.get("id") or "").strip()
        if qid:
            result[qid] = row
    return result


def extract_answer(row: dict) -> str | None:
    direct = row.get("predicted_answer") or row.get("prediction") or row.get("answer")
    if direct:
        match = re.search(r"\b([A-D])\b", str(direct).strip().upper())
        if match:
            return match.group(1)
    response = str(row.get("response") or "")
    match = re.search(r"答案\s*[:：]\s*([A-D])", response.upper())
    if match:
        return match.group(1)
    match = re.search(r"\b([A-D])\b", response.upper())
    return match.group(1) if match else None


evaluation = None
if prompt_out is not None:
    write_prompts(prompt_out, filtered)

if predictions_file is not None:
    predictions = load_predictions(predictions_file)
    rows = []
    for item in filtered:
        qid = str(item.get("id"))
        prediction_row = predictions.get(qid, {})
        predicted = extract_answer(prediction_row) if prediction_row else None
        expected = item.get("answer")
        rows.append(
            {
                "question_id": qid,
                "category": item.get("category"),
                "benchmark_year": benchmark_year(item),
                "expected": expected,
                "predicted": predicted,
                "correct": bool(predicted and expected and predicted == expected),
                "missingPrediction": not bool(prediction_row),
            }
        )
    answered = [row for row in rows if not row["missingPrediction"] and row["predicted"]]
    correct = [row for row in answered if row["correct"]]
    by_category = {}
    for category in sorted({str(row["category"]) for row in rows}):
        cat_rows = [row for row in rows if str(row["category"]) == category]
        cat_answered = [row for row in cat_rows if not row["missingPrediction"] and row["predicted"]]
        cat_correct = [row for row in cat_answered if row["correct"]]
        by_category[category] = {
            "total": len(cat_rows),
            "answered": len(cat_answered),
            "correct": len(cat_correct),
            "accuracy": round(len(cat_correct) / len(cat_answered), 4) if cat_answered else 0,
        }
    evaluation = {
        "total": len(rows),
        "answered": len(answered),
        "missing": len(rows) - len(answered),
        "correct": len(correct),
        "accuracy": round(len(correct) / len(answered), 4) if answered else 0,
        "byCategory": by_category,
        "results": rows,
    }

report = {
    "dataset": "FortuneTellingBench",
    "availableYears": available_years,
    "selectedYear": selected_year,
    "totalQuestions": len(filtered),
    "categories": dict(sorted(categories.items())),
    "promptOut": str(prompt_out) if prompt_out else None,
    "evaluation": evaluation,
}
if output_json is not None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("")
print("Dataset Statistics:")
print("  Name: FortuneTellingBench")
print("  Version: unknown")
print("  Available Years: " + ", ".join(str(item) for item in available_years if item is not None))
if selected_year is not None:
    print(f"  Selected Year: {selected_year}")
print(f"  Total Questions: {len(filtered)}")
if prompt_out is not None:
    print(f"  Prompt Out: {prompt_out}")
print("")
print("  Categories:")
for category, count in sorted(categories.items()):
    print(f"    - {category}: {count}")
if evaluation is not None:
    print("")
    print("Evaluation:")
    print(f"  Answered: {evaluation['answered']}/{evaluation['total']}")
    print(f"  Correct: {evaluation['correct']}")
    print(f"  Accuracy: {evaluation['accuracy']:.2%}")
PY
