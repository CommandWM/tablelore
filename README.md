<p align="center">
  <img src="tablelore/assets/tablelore-logo.png" alt="TableLore logo" width="220">
</p>

<p align="center">
  <strong>Practical data analysis hygiene for AI agents.</strong>
</p>

<p align="center">
  <a href="https://github.com/CommandWM/tablelore/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/CommandWM/tablelore/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue.svg">
  <img alt="Skill first" src="https://img.shields.io/badge/release-v1.0_skill--first-2D9CDB.svg">
</p>

TableLore is a Codex/Claude-compatible skill for disciplined data science workflows: inspect first, profile before modeling, choose DuckDB/Polars/Pandas deliberately, keep notebooks and scripts clean, and report findings with caveats.

See [PRD.md](PRD.md) for the initial product requirements.

## Status

v1.0 skill-first release.

## What It Provides

- `tablelore/SKILL.md` with the core agent workflow and trigger guidance.
- Reference checklists for profiling, engine selection, notebook/script hygiene, modeling guardrails, and examples.
- Optional local profiling helper for CSV/TSV files.
- Fixture-backed tests for the helper.
- GitHub Actions CI for tests, helper smoke checks, and dogfood evidence regeneration.

## Use the Skill

Install or reference the `tablelore/` folder in an agent environment that supports local skills. The skill is intentionally concise and loads detailed reference files only when needed.

The core behavior is:

1. Orient on the repo, available data, schemas, notebooks, and existing loaders.
2. Profile before modeling or heavy transformation unless explicitly skipped.
3. Choose DuckDB, Polars, Pandas, notebooks, scripts, and plotting libraries deliberately.
4. Keep exploratory and production artifacts separate.
5. Report findings with caveats, data quality risks, and reproducibility steps.

## Optional Profiling Helper

The helper is not a packaged CLI. Run it directly:

```bash
python3 -m pip install -r requirements.txt
python3 tablelore/scripts/table_profile.py tests/fixtures/customer_churn_sample.csv --target churned
```

Write a Markdown profile to a file:

```bash
python3 tablelore/scripts/table_profile.py path/to/file.csv --target target_column --output reports/profile.md
```

The helper currently supports CSV and TSV files and uses Pandas for broad local compatibility.

## Development

Run the tests:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests -q
```

Run the full local check set:

```bash
python3 -m pytest tests -q
python3 tablelore/scripts/table_profile.py tests/fixtures/customer_churn_sample.csv --target churned
python3 dogfood/com47/run_dogfood.py
git diff --check
```

## Project Layout

```text
tablelore/
├── SKILL.md
├── agents/openai.yaml
├── assets/tablelore-logo.png
├── references/
└── scripts/table_profile.py
dogfood/com47/
├── COM47_DOGFOOD_REPORT.md
├── data/
├── evidence/
├── notebooks/
└── scripts/
```

Release notes live in [docs/releases/v1.0.md](docs/releases/v1.0.md).

## License

MIT. See [LICENSE](LICENSE).
