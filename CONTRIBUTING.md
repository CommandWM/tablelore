# Contributing to TableLore

TableLore is a skill-first repo. The core product is better agent behavior: inspect before transform, profile before model, and explain uncertainty.

## Development Setup

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests -q
```

## Local Checks

Run these before opening a pull request:

```bash
python3 -m pytest tests -q
python3 tablelore/scripts/table_profile.py tests/fixtures/customer_churn_sample.csv --target churned
python3 dogfood/com47/run_dogfood.py
git diff --check
```

## Contribution Guidelines

- Keep `tablelore/SKILL.md` concise; detailed guidance belongs in `tablelore/references/`.
- Keep the default workflow local-first and privacy-preserving.
- Add tests for helper behavior and metadata wiring.
- Keep examples small, synthetic, and safe to commit.
- Do not add AutoML, hosted services, database credential management, or full CLI packaging without explicitly scoping that work.

## Dogfood Evidence

When changing the skill workflow, update or add dogfood evidence under `dogfood/` so behavior changes are visible and reproducible.
