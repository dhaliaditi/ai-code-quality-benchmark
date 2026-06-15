import csv
from statistics import mean
import matplotlib.pyplot as plt

ROOT = "/home/claude/repo"
rows = list(csv.DictReader(open(f"{ROOT}/results/metrics.csv")))
for r in rows:
    r["score"] = float(r["score"])
    r["total_messages"] = int(r["total_messages"])
    r["cyclomatic_complexity"] = int(r["cyclomatic_complexity"])
    r["maintainability_index"] = float(r["maintainability_index"])

human = [r for r in rows if r["group"] == "human"]
claude = [r for r in rows if r["group"] == "claude"]

metrics = [
    ("Pylint score\n(0-10, higher better)", "score"),
    ("Code smells\nper file", "total_messages"),
    ("Cyclomatic\ncomplexity", "cyclomatic_complexity"),
    ("Maintainability\nIndex (0-100)", "maintainability_index"),
]

fig, axes = plt.subplots(1, 4, figsize=(11, 3.6))
for ax, (label, key) in zip(axes, metrics):
    h_val = mean(r[key] for r in human)
    c_val = mean(r[key] for r in claude)
    bars = ax.bar(["Human", "Claude"], [h_val, c_val], color=["#6b7280", "#3b82f6"], width=0.55)
    ax.set_title(label, fontsize=10)
    for b, v in zip(bars, [h_val, c_val]):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)

fig.suptitle("AI-generated vs human code, averaged over 41 HumanEval problems", fontsize=11)
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(f"{ROOT}/results/comparison.png", dpi=130)
print("saved results/comparison.png")
