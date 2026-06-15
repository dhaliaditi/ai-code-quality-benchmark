# AI-Generated vs Human Code: Quality Comparison on HumanEval

Sample: 41 HumanEval problems (every 4th task, IDs 0–160).

## Correctness (official HumanEval unit tests)

| | Pass | Total | Pass rate |
|---|---|---|---|
| Human (canonical) | 41 | 41 | 100.0% |
| Claude-generated | 39 | 41 | 95.1% |

Claude-generated solutions that failed: HumanEval/84, HumanEval/140

## Static analysis (averages across the sample)

| Metric | Human | Claude | Difference (Claude − Human) |
|---|---|---|---|
| Pylint score (0–10, higher = fewer issues) | 4.32 | 5.35 | +1.03 |
| Code smells per file (Pylint messages) | 3.44 | 2.41 | -1.02 |
| Cyclomatic complexity (max per file) | 3.63 | 3.54 | -0.10 |
| Maintainability Index (Radon, 0–100) | 80.79 | 81.43 | +0.64 |
| Source lines of code (SLOC) | 7.37 | 7.12 | -0.24 |

## Per-problem detail

| Task | H pylint | C pylint | H CC | C CC | H MI | C MI | H SLOC | C SLOC | C correct |
|---|---|---|---|---|---|---|---|---|---|
| HumanEval/0 | 7.78 | 5.71 | 5 | 4 | 95.6 | 95.2 | 9 | 7 | yes |
| HumanEval/4 | 5.00 | 5.00 | 2 | 2 | 80.6 | 80.6 | 4 | 4 | yes |
| HumanEval/8 | 6.25 | 6.25 | 2 | 2 | 98.2 | 98.2 | 8 | 8 | yes |
| HumanEval/12 | 6.25 | 7.78 | 5 | 4 | 96.7 | 97.3 | 8 | 9 | yes |
| HumanEval/16 | 0.00 | 0.00 | 1 | 1 | 100.0 | 100.0 | 2 | 2 | yes |
| HumanEval/20 | 8.00 | 7.27 | 6 | 3 | 89.0 | 92.5 | 16 | 11 | yes |
| HumanEval/24 | 2.50 | 6.00 | 3 | 3 | 100.0 | 99.9 | 4 | 5 | yes |
| HumanEval/28 | 3.33 | 3.33 | 1 | 1 | 100.0 | 100.0 | 3 | 3 | yes |
| HumanEval/32 | 7.86 | 8.12 | 4 | 4 | 82.8 | 82.6 | 15 | 17 | yes |
| HumanEval/36 | 7.00 | 5.00 | 5 | 4 | 91.2 | 88.1 | 10 | 6 | yes |
| HumanEval/40 | 5.71 | 5.71 | 5 | 5 | 70.8 | 70.8 | 7 | 7 | yes |
| HumanEval/44 | 6.67 | 7.50 | 2 | 3 | 83.4 | 89.6 | 6 | 8 | yes |
| HumanEval/48 | 4.00 | 0.00 | 3 | 1 | 74.6 | 50.4 | 5 | 2 | yes |
| HumanEval/52 | 6.00 | 0.00 | 3 | 2 | 100.0 | 71.9 | 5 | 2 | yes |
| HumanEval/56 | 7.78 | 7.78 | 4 | 4 | 89.1 | 89.1 | 10 | 10 | yes |
| HumanEval/60 | 0.00 | 0.00 | 1 | 1 | 57.4 | 57.4 | 2 | 2 | yes |
| HumanEval/64 | 7.14 | 7.50 | 4 | 4 | 90.6 | 96.0 | 9 | 10 | yes |
| HumanEval/68 | 0.00 | 7.27 | 3 | 6 | 38.6 | 59.3 | 5 | 11 | yes |
| HumanEval/72 | 7.00 | 2.50 | 4 | 2 | 84.5 | 58.5 | 10 | 4 | yes |
| HumanEval/76 | 0.00 | 7.78 | 3 | 4 | 83.7 | 88.3 | 7 | 9 | yes |
| HumanEval/80 | 1.43 | 7.14 | 6 | 4 | 79.7 | 83.7 | 7 | 7 | yes |
| HumanEval/84 | 0.00 | 0.00 | 2 | 2 | 100.0 | 100.0 | 2 | 3 | no |
| HumanEval/88 | 0.00 | 5.00 | 2 | 3 | 50.1 | 75.5 | 2 | 6 | yes |
| HumanEval/92 | 3.33 | 2.50 | 7 | 5 | 79.7 | 66.4 | 6 | 4 | yes |
| HumanEval/96 | 7.27 | 8.18 | 5 | 5 | 94.3 | 91.3 | 11 | 11 | yes |
| HumanEval/100 | 0.00 | 6.00 | 2 | 2 | 53.6 | 71.3 | 2 | 5 | yes |
| HumanEval/104 | 6.67 | 6.67 | 4 | 4 | 89.3 | 89.3 | 6 | 6 | yes |
| HumanEval/108 | 5.56 | 7.14 | 2 | 3 | 88.4 | 88.5 | 8 | 7 | yes |
| HumanEval/112 | 0.00 | 0.00 | 3 | 3 | 57.2 | 57.2 | 3 | 3 | yes |
| HumanEval/116 | 0.00 | 5.00 | 1 | 1 | 100.0 | 100.0 | 2 | 4 | yes |
| HumanEval/120 | 6.67 | 5.00 | 2 | 2 | 63.1 | 49.3 | 6 | 4 | yes |
| HumanEval/124 | 7.50 | 8.33 | 13 | 13 | 81.7 | 82.5 | 16 | 18 | yes |
| HumanEval/128 | 2.00 | 8.33 | 4 | 5 | 64.6 | 89.8 | 4 | 12 | yes |
| HumanEval/132 | 7.50 | 8.18 | 6 | 8 | 87.4 | 87.1 | 17 | 11 | yes |
| HumanEval/136 | 5.00 | 6.67 | 3 | 7 | 69.7 | 86.2 | 4 | 6 | yes |
| HumanEval/140 | 8.95 | 8.82 | 7 | 7 | 80.7 | 88.1 | 21 | 18 | no |
| HumanEval/144 | 6.25 | 6.67 | 2 | 1 | 90.6 | 86.7 | 8 | 6 | yes |
| HumanEval/148 | 4.44 | 7.50 | 5 | 3 | 78.2 | 75.3 | 10 | 8 | yes |
| HumanEval/152 | 0.00 | 0.00 | 2 | 2 | 55.7 | 55.7 | 2 | 2 | yes |
| HumanEval/156 | 2.31 | 7.78 | 3 | 3 | 91.7 | 95.9 | 15 | 9 | yes |
| HumanEval/160 | 4.00 | 4.00 | 2 | 2 | 50.1 | 53.4 | 5 | 5 | yes |