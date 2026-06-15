"""Generate solutions for the problem subset using the Anthropic API.

This script is provided so others can reproduce or extend this benchmark with
their own model of choice. It was NOT used to produce the `solutions/claude/`
directory in this repo -- those solutions were written directly by Claude as
part of a conversation, which better reflects how a developer actually
receives and uses AI-generated code (no special prompting for benchmarks).

Usage:
    1. Either set your key below (ANTHROPIC_API_KEY = "sk-ant-...")
       OR export it as an environment variable before running:
           export ANTHROPIC_API_KEY=sk-ant-...
    2. python scripts/generate_solutions.py --model claude-sonnet-4-6 --out solutions/my_model

WARNING: if you paste your key into this file, do NOT commit it to a public
repo. Either leave it blank here and use the environment variable, or add
this file to .gitignore before committing.
"""
import argparse, json, os, re
import anthropic

# --------------------------------------------------------------------------
# Paste your Anthropic API key here, between the quotes, if you don't want to
# set it as an environment variable. Leave it as "" to use the
# ANTHROPIC_API_KEY environment variable instead (recommended).
# --------------------------------------------------------------------------
ANTHROPIC_API_KEY = ""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROMPT_TEMPLATE = """Complete the following Python function. Return ONLY the \
function body's continuation as Python code, with no explanation, no markdown \
fences, and no repetition of the signature or docstring.

{prompt}"""


def extract_code(text):
    # Strip markdown fences if the model adds them anyway.
    text = re.sub(r"^```(?:python)?\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text.strip())
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--out", default="solutions/generated")
    ap.add_argument("--subset", default="data/subset.json")
    args = ap.parse_args()

    api_key = ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit(
            "No API key found. Either paste it into ANTHROPIC_API_KEY at the "
            "top of this script, or set it as an environment variable:\n"
            "    export ANTHROPIC_API_KEY=sk-ant-..."
        )

    client = anthropic.Anthropic(api_key=api_key)
    subset = json.load(open(os.path.join(ROOT, args.subset)))
    outdir = os.path.join(ROOT, args.out)
    os.makedirs(outdir, exist_ok=True)

    for p in subset:
        tid = p["task_id"]
        msg = client.messages.create(
            model=args.model,
            max_tokens=512,
            messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(prompt=p["prompt"])}],
        )
        body = extract_code(msg.content[0].text)
        # Ensure the body is indented as a function body.
        if not body.startswith("    ") and not body.startswith("\t"):
            body = "\n".join("    " + line if line.strip() else line for line in body.splitlines())

        fname = tid.replace("/", "_") + ".py"
        with open(os.path.join(outdir, fname), "w") as f:
            f.write(p["prompt"] + body + "\n")
        print("wrote", fname)


if __name__ == "__main__":
    main()
