# TableLore Demo Flow

This guide shows the best first user path for TableLore. Treat TableLore as an analysis hygiene skill: it helps an agent slow down before modeling, inspect the data, choose the right local tool, and report caveats clearly.

## Best Way To Use It

Use TableLore when you have a local table and want reliable analysis behavior from an AI agent.

Good first prompts:

```text
Use $tablelore to profile this CSV before analysis: path/to/file.csv
```

```text
Use $tablelore to inspect these Parquet extracts and recommend a safe join plan before summarizing anomalies.
```

```text
Use $tablelore to check this dataset for leakage before any model training.
```

Avoid starting with:

```text
Build the best model from this data.
```

That skips the inspection step where most avoidable mistakes happen.

## Runnable Customer-Churn Demo

From the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 demo/customer-churn/run_demo.py
```

Generated files:

- `demo/customer-churn/output/profile.md`: lightweight table profile.
- `demo/customer-churn/output/analysis_prompt.md`: copy/paste prompt for a first-pass readiness review.
- `demo/customer-churn/output/leakage_prompt.md`: copy/paste prompt for pre-model leakage review.
- `demo/customer-churn/output/demo_summary.md`: short explanation of the demo artifacts.

## What The Demo Teaches

The fixture at `tests/fixtures/customer_churn_sample.csv` intentionally includes common analysis traps:

- Missing values in spend and post-churn fields.
- Duplicate rows.
- Negative monthly spend.
- No clean single-column candidate key.
- Likely leakage columns such as churn reason and cancellation date.

A good TableLore-guided agent should identify those issues before claiming churn drivers or training a model.

## Demo Script Output

After running the demo script, start with:

```bash
cat demo/customer-churn/output/profile.md
cat demo/customer-churn/output/analysis_prompt.md
```

Then paste `analysis_prompt.md` into Codex or another skill-aware agent. The answer should include:

- Data inspected and profile path.
- Row count, column count, target distribution, and schema summary.
- Data quality risks.
- Leakage candidates.
- A clear recommendation for the next safe analysis step.

Before modeling, paste:

```bash
cat demo/customer-churn/output/leakage_prompt.md
```

The answer should produce a conservative modeling-readiness review: columns to exclude or confirm, timing questions for the data owner, and a split strategy.

## Practical User Pattern

For a real dataset, follow this loop:

1. Put the data in a local project folder.
2. Ask TableLore to inventory and profile before analysis.
3. Confirm row grain, keys, target definition, and prediction timing.
4. Ask for a transformation or join plan only after the profile is clear.
5. Ask for modeling only after leakage and split strategy are explicit.
6. Ask the agent to save outputs as scripts, notebooks, charts, or reports with reproducible commands.
