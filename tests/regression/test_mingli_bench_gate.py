from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_mingli_bench_evaluation_smoke_computes_accuracy(tmp_path):
    predictions = tmp_path / "predictions.jsonl"
    output_json = tmp_path / "evaluation.json"
    rows = [
        {"question_id": "ftb_0001", "predicted_answer": "A"},
        {"question_id": "ftb_0002", "predicted_answer": "C"},
        {"question_id": "ftb_0003", "predicted_answer": "C"},
        {"question_id": "ftb_0004", "predicted_answer": "C"},
        {"question_id": "ftb_0005", "predicted_answer": "B"},
    ]
    predictions.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    subprocess.run(
        [
            "bash",
            "scripts/run-mingli-bench.sh",
            "--sample",
            "5",
            "--predictions-file",
            str(predictions),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["evaluation"]["total"] == 5
    assert report["evaluation"]["answered"] == 5
    assert report["evaluation"]["correct"] == 5
    assert report["evaluation"]["accuracy"] == 1.0


def test_mingli_bench_predictions_can_be_generated_from_fatecat(tmp_path):
    predictions = tmp_path / "fatecat-predictions.jsonl"
    output_json = tmp_path / "evaluation.json"

    generated = subprocess.run(
        [
            "bash",
            "scripts/generate-mingli-predictions.sh",
            "--year",
            "2025",
            "--sample",
            "2",
            "--output-jsonl",
            str(predictions),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(generated.stdout)
    assert payload["predictions"] == 2
    assert payload["source"] == "fatecat_scored_baseline_v1"

    rows = [json.loads(line) for line in predictions.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2
    assert {row["prediction_source"] for row in rows} == {"fatecat_scored_baseline_v1"}
    assert all(row["fatecat_evidence"]["fourPillars"] for row in rows)
    assert all(row["scoring_trace"]["optionScores"] for row in rows)
    assert all(row["scoring_trace"]["boundary"] for row in rows)
    assert all(row["predicted_answer"] in {"A", "B", "C", "D"} for row in rows)

    subprocess.run(
        [
            "bash",
            "scripts/run-mingli-bench.sh",
            "--year",
            "2025",
            "--sample",
            "2",
            "--predictions-file",
            str(predictions),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["evaluation"]["total"] == 2
    assert report["evaluation"]["answered"] == 2
    assert 0 <= report["evaluation"]["accuracy"] <= 1
