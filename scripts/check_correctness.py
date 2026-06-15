"""Run each problem's official HumanEval test against both the human (canonical)
and Claude-generated solutions, in an isolated subprocess, and record pass/fail.
"""
import json, os, subprocess, sys, tempfile

ROOT = "/home/claude/repo"
subset = json.load(open(f"{ROOT}/data/subset.json"))

RUNNER = """
{prog}

{test}

check({entry_point})
"""

def run_one(tid, prog, test, entry_point):
    src = RUNNER.format(prog=prog, test=test, entry_point=entry_point)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(src)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=10)
        ok = r.returncode == 0
        err = "" if ok else (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown error")
        return ok, err
    except subprocess.TimeoutExpired:
        return False, "timeout"
    finally:
        os.unlink(path)


results = {}
for p in subset:
    tid = p["task_id"]
    fname = tid.replace("/", "_") + ".py"
    human_src = open(f"{ROOT}/solutions/human/{fname}").read()
    claude_src = open(f"{ROOT}/solutions/claude/{fname}").read()

    h_ok, h_err = run_one(tid, human_src, p["test"], p["entry_point"])
    c_ok, c_err = run_one(tid, claude_src, p["test"], p["entry_point"])

    results[tid] = {
        "human_pass": h_ok, "human_err": h_err,
        "claude_pass": c_ok, "claude_err": c_err,
    }
    print(f"{tid:18s} human={'PASS' if h_ok else 'FAIL':4s}  claude={'PASS' if c_ok else 'FAIL':4s}"
          + ("" if c_ok else f"   ({c_err})"))

n = len(results)
h_pass = sum(r["human_pass"] for r in results.values())
c_pass = sum(r["claude_pass"] for r in results.values())
print(f"\nTotals: human {h_pass}/{n} pass, claude {c_pass}/{n} pass")

json.dump(results, open(f"{ROOT}/results/correctness.json", "w"), indent=2)
