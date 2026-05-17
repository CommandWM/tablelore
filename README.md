# TableLore

Practical data analysis hygiene for AI agents.

TableLore is a Codex/Claude-compatible skill for disciplined data science workflows: inspect first, profile before modeling, choose DuckDB/Polars/Pandas deliberately, keep notebooks and scripts clean, and report findings with caveats.

See [PRD.md](PRD.md) for the initial product requirements.

## Status

v1.0 skill-first release.

## What It Provides

- `tablelore/SKILL.md` with the core agent workflow and trigger guidance.
- Reference checklists for profiling, engine selection, notebook/script hygiene, modeling guardrails, and examples.
- Optional local profiling helper for CSV/TSV files.
- Fixture-backed tests for the helper.

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

Release notes live in [docs/releases/v1.0.md](docs/releases/v1.0.md).

## License

MIT. See [LICENSE](LICENSE).
