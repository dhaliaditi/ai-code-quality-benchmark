"""Run Pylint and Radon over both solution sets and collect per-file metrics
into a single CSV for analysis.
"""
import csv, json, subprocess, sys, os
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze

ROOT = "/home/claude/repo"
subset = json.load(open(f"{ROOT}/data/subset.json"))


def pylint_metrics(path):
    r = subprocess.run(
        [sys.executable, "-m", "pylint", path, "--score=y",
         "--output-format=json"],
        capture_output=True, text=True
    )
    try:
        messages = json.loads(r.stdout)
    except json.JSONDecodeError:
        messages = []

    counts = {"convention": 0, "refactor": 0, "warning": 0, "error": 0}
    for m in messages:
        cat = m.get("type")
        if cat in counts:
            counts[cat] += 1

    score = None
    # score isn't in JSON output; rerun in text mode to grab it
    r2 = subprocess.run(
        [sys.executable, "-m", "pylint", path, "--score=y"],
        capture_output=True, text=True
    )
    for line in r2.stdout.splitlines():
        if "rated at" in line:
            try:
                score = float(line.split("rated at")[1].split("/")[0].strip())
            except (ValueError, IndexError):
                pass

    counts["score"] = score
    counts["total_messages"] = sum(v for k, v in counts.items() if k != "score")
    return counts


def radon_metrics(path):
    src = open(path).read()
    blocks = cc_visit(src)
    cc_values = [b.complexity for b in blocks]
    mi = mi_visit(src, multi=True)
    raw = analyze(src)
    return {
        "cyclomatic_complexity": max(cc_values) if cc_values else 0,
        "maintainability_index": round(mi, 2),
        "loc": raw.loc,
        "sloc": raw.sloc,
        "lloc": raw.lloc,
    }


rows = []
for p in subset:
    tid = p["task_id"]
    fname = tid.replace("/", "_") + ".py"
    for group in ("human", "claude"):
        path = f"{ROOT}/solutions/{group}/{fname}"
        pm = pylint_metrics(path)
        rm = radon_metrics(path)
        row = {"task_id": tid, "group": group, **pm, **rm}
        rows.append(row)
        print(f"{tid:18s} {group:7s} pylint={pm['score']:>5} "
              f"smells={pm['total_messages']:>2}  cc={rm['cyclomatic_complexity']:>2}  "
              f"mi={rm['maintainability_index']:>6}  sloc={rm['sloc']:>3}")

fieldnames = list(rows[0].keys())
with open(f"{ROOT}/results/metrics.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

print(f"\nwrote {len(rows)} rows to results/metrics.csv")
