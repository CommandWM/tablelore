---
name: tablelore
description: Use when analyzing, profiling, transforming, cleaning, joining, visualizing, modeling, validating, or reporting on local datasets, including CSV, TSV, Parquet, JSON, JSONL, Excel, SQLite, DuckDB, database extracts, and project data loaders.
---

# TableLore

Practical data analysis hygiene for AI agents working with local datasets.

## Core Principle

Inspect before transform. Profile before model. Explain uncertainty.

## Workflow

1. Orient on the repo, existing docs, notebooks, schemas, scripts, and data-loading conventions before creating new analysis.
2. Discover local data assets and database extracts. Prefer metadata, schemas, aggregates, and small safe samples over raw row dumps.
3. Profile the data before modeling or heavy transformation unless the user explicitly asks to skip profiling.
4. Choose DuckDB, Polars, Pandas, notebooks, scripts, and plotting libraries based on task constraints and project conventions.
5. Analyze with explicit assumptions, named transformations, visual checks, and simple baselines before advanced models.
6. Report the question answered, data used, method, findings, caveats, data quality risks, reproducibility instructions, and output paths.

## Privacy And Safety

Default to local execution. Do not upload private datasets, use external services, or expose sensitive raw records unless the user explicitly approves that path. When in doubt, summarize with schemas, aggregates, redacted samples, or generated fixtures.

## Reference Loading

- Read `references/profiling-checklist.md` before profiling, modeling, heavy transformation, joins, or data quality claims.
- Read `references/engine-selection.md` when choosing DuckDB, Polars, Pandas, plotting libraries, notebooks, or scripts.
- Read `references/notebook-hygiene.md` before creating or editing notebooks, reusable scripts, reports, or saved outputs.
- Read `references/modeling-guardrails.md` before training, evaluating, tuning, or comparing models.
- Read `references/examples.md` when the user asks for examples, prompt patterns, expected outputs, or a style precedent for a dataset task.
- Load only the reference files needed for the current request; do not duplicate full checklists in the final answer.

## Final Response Expectations

End with a concise summary of the analysis or artifact, the data used, the method, key findings, caveats, reproducibility instructions, and paths to generated notebooks, scripts, charts, reports, or outputs. State clearly when a result is exploratory, when profiling was skipped by request, or when data quality limits the conclusion.
