# Modeling Readiness Demo

This demo shows how TableLore should respond when a user wants to move from profiling into modeling. It reuses the customer-churn fixture and deliberately stops before training because the data contains likely leakage and unresolved split questions.

Run it from the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 demo/modeling-readiness/run_demo.py
```

Generated artifacts are written to `demo/modeling-readiness/output/`:

- `profile.md`: the lightweight table profile
- `modeling_readiness_report.md`: why modeling is blocked and what must be confirmed
- `baseline_prompt.md`: copy/paste prompt for a TableLore-guided baseline planning pass

The lesson is that TableLore is not AutoML. It should help users define grain, timing, leakage exclusions, and split strategy before fitting even a simple model.
