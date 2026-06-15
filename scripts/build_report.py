"""Combine correctness + static analysis results into results/REPORT.md."""
import csv, json
from statistics import mean, median

ROOT = "/home/claude/repo"
rows = list(csv.DictReader(open(f"{ROOT}/results/metrics.csv")))
correctness = json.load(open(f"{ROOT}/results/correctness.json"))

for r in rows:
    for k in ("convention", "refactor", "warning", "error", "total_messages",
              "cyclomatic_complexity", "loc", "sloc", "lloc"):
        r[k] = int(r[k])
    r["score"] = float(r["score"])
    r["maintainability_index"] = float(r["maintainability_index"])

human = [r for r in rows if r["group"] == "human"]
claude = [r for r in rows if r["group"] == "claude"]
n = len(human)

def summarize(group):
    return {
        "pylint_score": mean(r["score"] for r in group),
        "code_smells": mean(r["total_messages"] for r in group),
        "cyclomatic_complexity": mean(r["cyclomatic_complexity"] for r in group),
        "maintainability_index": mean(r["maintainability_index"] for r in group),
        "sloc": mean(r["sloc"] for r in group),
    }

h_sum = summarize(human)
c_sum = summarize(claude)

h_pass = sum(v["human_pass"] for v in correctness.values())
c_pass = sum(v["claude_pass"] for v in correctness.values())

lines = []
lines.append("# AI-Generated vs Human Code: Quality Comparison on HumanEval\n")
lines.append(f"Sample: {n} HumanEval problems (every 4th task, IDs 0\u2013160).\n")

lines.append("## Correctness (official HumanEval unit tests)\n")
lines.append("| | Pass | Total | Pass rate |")
lines.append("|---|---|---|---|")
lines.append(f"| Human (canonical) | {h_pass} | {n} | {h_pass/n:.1%} |")
lines.append(f"| Claude-generated | {c_pass} | {n} | {c_pass/n:.1%} |")
lines.append("")
lines.append("Claude-generated solutions that failed: " +
              ", ".join(tid for tid, v in correctness.items() if not v["claude_pass"]) + "\n")

lines.append("## Static analysis (averages across the sample)\n")
lines.append("| Metric | Human | Claude | Difference (Claude \u2212 Human) |")
lines.append("|---|---|---|---|")
lines.append(f"| Pylint score (0\u201310, higher = fewer issues) | {h_sum['pylint_score']:.2f} | {c_sum['pylint_score']:.2f} | {c_sum['pylint_score']-h_sum['pylint_score']:+.2f} |")
lines.append(f"| Code smells per file (Pylint messages) | {h_sum['code_smells']:.2f} | {c_sum['code_smells']:.2f} | {c_sum['code_smells']-h_sum['code_smells']:+.2f} |")
lines.append(f"| Cyclomatic complexity (max per file) | {h_sum['cyclomatic_complexity']:.2f} | {c_sum['cyclomatic_complexity']:.2f} | {c_sum['cyclomatic_complexity']-h_sum['cyclomatic_complexity']:+.2f} |")
lines.append(f"| Maintainability Index (Radon, 0\u2013100) | {h_sum['maintainability_index']:.2f} | {c_sum['maintainability_index']:.2f} | {c_sum['maintainability_index']-h_sum['maintainability_index']:+.2f} |")
lines.append(f"| Source lines of code (SLOC) | {h_sum['sloc']:.2f} | {c_sum['sloc']:.2f} | {c_sum['sloc']-h_sum['sloc']:+.2f} |")
lines.append("")

# per-problem table
lines.append("## Per-problem detail\n")
lines.append("| Task | H pylint | C pylint | H CC | C CC | H MI | C MI | H SLOC | C SLOC | C correct |")
lines.append("|---|---|---|---|---|---|---|---|---|---|")
by_task = {}
for r in rows:
    by_task.setdefault(r["task_id"], {})[r["group"]] = r
for tid, g in by_task.items():
    h, c = g["human"], g["claude"]
    ok = "yes" if correctness[tid]["claude_pass"] else "no"
    lines.append(f"| {tid} | {h['score']:.2f} | {c['score']:.2f} | {h['cyclomatic_complexity']} | {c['cyclomatic_complexity']} "
                  f"| {h['maintainability_index']:.1f} | {c['maintainability_index']:.1f} | {h['sloc']} | {c['sloc']} | {ok} |")

open(f"{ROOT}/results/REPORT.md", "w").write("\n".join(lines))
print("\n".join(lines[:20]))
print("...")
print(f"\nwrote results/REPORT.md ({len(lines)} lines)")
