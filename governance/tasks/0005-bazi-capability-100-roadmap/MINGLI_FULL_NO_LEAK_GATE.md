# TP-10.01 MingLi Full No-Leak Gate Evidence

## Result

PASS.

MingLi-Bench full baseline evaluation completed locally without answer leakage.

## Commands

```bash
bash scripts/generate-mingli-predictions.sh --output-jsonl /tmp/fatecat-mingli-full.jsonl
bash scripts/run-mingli-bench.sh --predictions-file /tmp/fatecat-mingli-full.jsonl --output-json /tmp/fatecat-mingli-full.json
```

No-leak scan checked prediction rows for forbidden fields:

- `expected`
- `answer`
- `correct`
- `gold`
- `label`

## Observed Result

```json
{
  "predictions": 160,
  "answered": 160,
  "total": 160,
  "correct": 44,
  "accuracy": 0.275,
  "missing": 0,
  "leakCount": 0
}
```

## Gate

PASS: `answered=160/160` and predictions contain no expected/answer/correct/gold/label leakage fields.

## Guardrail

Accuracy is low at 27.50%. This proves the no-leak evaluation chain is real, not that professional reasoning is strong.

Runtime artifacts are in `/tmp/fatecat-mingli-full.jsonl` and `/tmp/fatecat-mingli-full.json`; they are not repository artifacts.
