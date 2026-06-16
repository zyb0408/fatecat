# TP-09.01 Golden Corpus Target Gap Evidence

## Result

BLOCK.

当前仓库没有达到 TP-09.01 定义的 corpus 数量 gate，不能标记为 Done。

## Current Counts

| Corpus | Current | Target | Status |
| --- | ---: | ---: | --- |
| calendar boundary | 51 | 50 | PASS |
| rule-depth runtime cases | 8 | 120 | BLOCK |
| statement cases | 5 | 80 | BLOCK |
| P0 topic cases / topic | 0 | 20 | BLOCK |

## Evidence

```bash
jq '{calendar:.caseCount, calendarCases:(.cases|length)}' domains/fate-analysis/data-products/bazi/golden/calendar_boundary_cases.json
jq '{ruleDepthCases:(.cases|length), advancedPattern:(.advancedPatternGoldenMatrix|length), combineCounterexamples:(.combineTransformCounterexampleMatrix|length), yongCounterexamples:(.yongShenCounterexampleMatrix|length)}' domains/fate-analysis/data-products/bazi/golden/rule_depth_cases.json
jq '{statementCases:(.cases|length)}' domains/fate-analysis/data-products/bazi/golden/statement_cases.json
find domains/fate-analysis/data-products/bazi/golden -maxdepth 1 -type f -name '*topic*' -o -name '*profile*'
```

Observed:

- calendar: `51`
- rule-depth runtime cases: `8`
- statement cases: `5`
- topic/profile golden files: none

## Minimal Fix

- Generate or admit at least 120 rule-depth cases with source, expected, failureExplanation and no runtime oracle leakage.
- Expand statement cases to at least 80, with high-risk wording regression.
- Add topic profile golden corpus with at least 20 cases per P0 topic.
- Keep quick CI on representative/sharded subsets; full corpus belongs to release/deep gate.

## Guardrail

Do not manufacture “professional truth” labels. Synthetic fixtures may lock current behavior and boundaries, but expert/real case admission requires license/source/privacy review.
