# Customer Churn Demo

This demo is the fastest way to experience TableLore as a user. It uses a tiny local churn fixture with intentionally messy data, then generates a profile and two copy/paste prompts for a skill-aware agent session.

## Run It

From the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 demo/customer-churn/run_demo.py
```

The script writes generated artifacts to `demo/customer-churn/output/`.

## Use It In Codex

1. Open `demo/customer-churn/output/analysis_prompt.md`.
2. Paste it into Codex with the TableLore skill available.
3. Review the answer for schema, row grain, quality warnings, leakage risk, and recommended next step.
4. Paste `demo/customer-churn/output/leakage_prompt.md` before any modeling work.

The expected behavior is not "train a churn model immediately." The expected behavior is: inspect first, identify risks, and make the next analysis step explicit.
