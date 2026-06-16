# TP-10.03 BaziQA Admission Gate

## Result

PASS with WARN.

BaziQA remains `future_candidate/evaluation_only`.

It is not admitted as a runtime dependency, production rule source, formal release gate, public-report data source, or training corpus.

## Recheck Evidence

Remote source:

- Repo: `https://github.com/ChenJiangxi/BaziQA`
- Local review clone: `/tmp/fatecat-baziqa-admission`
- Current reviewed commit: `8ea8222f8bd8ef8a6f1a5fb012344935a66e7686`
- Commit time: `2026-03-08 23:07:31 +0800`
- Commit subject: `Fix URL formatting in README.md`

Commands:

```bash
rm -rf /tmp/fatecat-baziqa-admission
git clone --depth 1 https://github.com/ChenJiangxi/BaziQA /tmp/fatecat-baziqa-admission
git -C /tmp/fatecat-baziqa-admission rev-parse HEAD
git -C /tmp/fatecat-baziqa-admission log -1 --format='%H%n%ci%n%s'
find /tmp/fatecat-baziqa-admission -maxdepth 1 \( -iname 'LICENSE*' -o -iname 'COPYING*' -o -iname 'NOTICE*' \) -print
```

Root files observed:

```text
README.md
benchmark_report.md
dataset_and_input_format.md
data/celebrity50_zh.json
data/contest8_2021.json
data/contest8_2022.json
data/contest8_2023.json
data/contest8_2024.json
data/contest8_2025.json
```

No root `LICENSE`, `COPYING`, or `NOTICE` file was found.

## License Gate

WARN.

README includes an MIT badge and says the dataset uses MIT License, but the repository still has no license body file in the reviewed checkout.

Decision:

- Offline admission discussion can continue.
- Runtime, production dependency, vendoring, public redistribution, training use, and formal release-gate use remain blocked until the license evidence is complete.

## Data Shape Recheck

Command:

```bash
for f in /tmp/fatecat-baziqa-admission/data/*.json; do
  base=$(basename "$f")
  count=$(jq 'length' "$f")
  with_questions=$(jq '[.[] | select(.questions)] | length' "$f")
  questions=$(jq '[.[] | select(.questions) | .questions | length] | add // 0' "$f")
  options=$(jq '[.[] | select(.questions) | .questions[] | (.options | length)] | unique | @csv' -r "$f")
  answers=$(jq '[.[] | select(.questions) | .questions[] | select(has("answer"))] | length' "$f")
  printf '%s items=%s persons_with_questions=%s questions=%s option_counts=%s answers=%s\n' "$base" "$count" "$with_questions" "$questions" "$options" "$answers"
done
```

Observed counts:

| File | Items | Persons With Questions | Questions | Option Counts | Answers |
| --- | ---: | ---: | ---: | --- | ---: |
| `celebrity50_zh.json` | 50 | 50 | 488 | 4,5 | 488 |
| `contest8_2021.json` | 10 | 9 | 40 | 4 | 40 |
| `contest8_2022.json` | 9 | 8 | 40 | 4 | 40 |
| `contest8_2023.json` | 9 | 8 | 40 | 4 | 40 |
| `contest8_2024.json` | 9 | 8 | 40 | 4 | 40 |
| `contest8_2025.json` | 9 | 8 | 40 | 4 | 40 |

Schema risks:

- `Celebrity50` observed question count is 488, while README still claims 250.
- `Contest8 2021` has 9 persons with questions, while README claims 8 persons per year.
- All question rows include `answer`; adapters must keep gold labels outside prediction generation.
- Celebrity data contains real people and event timelines; it is not safe for public report/runtime by default.

## No-Runtime Gate

Command:

```bash
rg 'BaziQA|baziqa|Bazi-QA' domains/fate-analysis/services/fate-core/src domains/experience-delivery/services/fatecat-delivery/src apps ai scripts tests -n
```

Observed only:

```text
domains/fate-analysis/services/fate-core/src/fate_core/usecases/evaluators/AGENTS.md:44:- 禁止读取 MingLi/BaziQA 的 expected answer、question_id 或 scoring result。
```

Decision:

- PASS: no runtime code, test harness, script, Web, Bot, or API path currently consumes BaziQA data.
- The single match is a negative architecture rule, not a data integration.

## Admission Matrix

| Use | Decision | Reason |
| --- | --- | --- |
| Runtime dependency | BLOCK | License body missing; data contains answers and real people. |
| Production rule source | BLOCK | Would leak benchmark labels into domain rules. |
| Public Web/Bot/API report source | BLOCK | Real-person event data and answer labels are not suitable for runtime. |
| Formal release gate | BLOCK for now | License/schema/privacy gates remain unresolved. |
| Offline evaluation candidate | PASS with WARN | Can be evaluated later through an external data path and no-leak adapter. |
| Vendored dataset | BLOCK | No complete license evidence and no need to store benchmark data in repo. |

## Future Adapter Contract

If BaziQA is revisited, the only allowed shape is:

1. Data stays outside the repo and is selected by `FATECAT_BAZIQA_DATA_DIR`.
2. Adapter reads only birth profile, gender, question text, and options for prediction input.
3. Prediction output must not contain `answer`, `expected`, `correct`, `gold`, `label`, `question_id`, or scoring result.
4. Evaluation loads gold answers in a separate scorer process.
5. Every evaluation row records repo URL, commit hash, file hash, schema version, and admission status.
6. `celebrity50_zh.json` remains isolated/manual-review only unless privacy and redistribution rules are clarified.

## Gate

PASS with WARN: license, schema, adapter, privacy, and no-runtime review is complete for this task.

The gate result is intentionally conservative: BaziQA may stay on the roadmap as `future_candidate/evaluation_only`, but it is not allowed to unblock TP-09 corpus targets or TP-11 release readiness.
