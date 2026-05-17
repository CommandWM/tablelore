# TableLore PRD

## Summary

TableLore is a purpose-built data science and data analysis skill for AI coding agents. It gives an agent a disciplined default workflow for working with datasets: inspect first, profile before modeling, choose the right local engine, produce reproducible scripts or notebooks, and explain results without overstating certainty.

The skill should wrap practical open-source tools rather than invent new analysis machinery:

- DuckDB for SQL over local files and larger-than-memory-ish analytical workflows.
- Polars as the fast default dataframe engine.
- Pandas when compatibility, ecosystem support, or user context makes it the better choice.
- Matplotlib, Seaborn, Plotly, or Altair for plots, selected by task and project conventions.
- Jupyter notebooks when exploration is the deliverable; scripts when repeatability is the deliverable.

## Name

- Display name: **TableLore**
- Skill/package/repo name: `tablelore`
- Positioning line: Practical data analysis hygiene for AI agents.

The name is intentionally fantasy-adjacent without depending on Tolkien-owned terminology. It also hints at the core product: finding useful lore in tables without pretending the table tells the whole story.

## Problem

General coding agents can write dataframe code, but they often skip the boring, important parts of data analysis:

- They jump into modeling before understanding the dataset.
- They infer schemas from tiny samples and miss nulls, joins, leakage, units, time windows, or duplicated entities.
- They mix exploratory one-off work with production scripts.
- They produce plots without checking whether the chart answers the actual question.
- They overstate conclusions from incomplete or messy data.
- They leave behind notebooks or scripts that are hard to rerun.

TableLore should make the careful path the default path.

## Target Users

- Data scientists using Codex, Claude Code, or similar coding agents.
- Analysts who want reliable local-first exploration of CSV, Parquet, JSON, Excel, SQLite, DuckDB, and database extracts.
- Engineers adding analytical checks, reports, or model-prep pipelines to existing repos.
- Agent builders who want a reusable skill for dataset triage and reproducible analysis.

## Goals

1. Make "profile the dataset before modeling" the agent's default behavior.
2. Choose DuckDB, Polars, Pandas, and plotting libraries deliberately based on task constraints.
3. Produce reproducible artifacts: scripts, notebooks, saved plots, and concise findings.
4. Detect common data quality risks early: missingness, duplicates, type drift, outliers, leakage, time-window mistakes, label imbalance, and join explosions.
5. Keep exploratory and production work separate.
6. Support local-first analysis without requiring paid APIs or external data exfiltration.

## Non-Goals

- TableLore is not an AutoML framework.
- It should not choose or train complex models before the dataset is understood.
- It should not upload datasets to external services by default.
- It should not replace domain expertise or statistical review.
- It should not prescribe one dataframe library for every project.

## Core Principle

Inspect before transform. Profile before model. Explain uncertainty.

Every TableLore workflow should start by answering:

- What files/tables are present?
- What are the row counts, columns, types, ranges, and missingness?
- What is the grain of the data?
- What does one row represent?
- Are there identifiers, timestamps, labels, target variables, or leakage-prone columns?
- What assumptions are being made?
- What artifact should be left behind: notebook, script, report, chart, test, or dataset?

## Default Workflow

### 1. Orient

- Read repo docs, existing notebooks, schemas, or analysis scripts before creating new work.
- Identify available data files and database connections.
- Do not print sensitive raw data unless needed and safe.
- Prefer metadata, schema, aggregates, and small samples over dumping full rows.

### 2. Profile

Produce an initial profile covering:

- File format, size, row count, column count.
- Column names, inferred types, null counts, distinct counts.
- Numeric distributions and suspicious values.
- Date/time ranges and timezone clues.
- Category cardinality and top values.
- Duplicate rows and duplicate entity keys.
- Potential primary keys and join keys.
- Target variable distribution if a target is specified.
- Leakage candidates if modeling is requested.

### 3. Choose Engine

Use DuckDB when:

- Querying CSV/Parquet directly.
- Joining multiple files.
- Running SQL-style aggregation.
- Working with data that is large enough to make eager Pandas awkward.

Use Polars when:

- Building fast dataframe transformations.
- Reading/writing Parquet or CSV locally.
- Lazy evaluation helps keep transformation logic clear.

Use Pandas when:

- Existing project code already uses Pandas.
- A library requires Pandas.
- The dataset is small and compatibility matters more than speed.

Use notebooks when:

- The deliverable is exploratory reasoning, charts, or an analysis narrative.

Use scripts when:

- The deliverable should be rerunnable, reviewed, scheduled, or committed as project logic.

### 4. Analyze

- Start with descriptive statistics and visual checks.
- Use simple baselines before advanced models.
- Keep transformations explicit and named.
- Save intermediate assumptions in comments or markdown.
- For modeling, separate train/test data in a way that respects time, groups, and leakage risks.

### 5. Report

Every finished analysis should include:

- Question answered.
- Data used.
- Method.
- Key findings.
- Caveats and data quality risks.
- Reproducibility instructions.
- Paths to generated notebooks, scripts, charts, or outputs.

## Functional Requirements

### FR1: Dataset Discovery

The skill must guide the agent to discover local data assets before analysis. Supported inputs should include:

- CSV and TSV
- Parquet
- JSON and JSONL
- Excel
- SQLite
- DuckDB
- Existing database extracts
- Existing project-specific data loaders

### FR2: Profiling Defaults

The skill must require a profile pass before modeling or heavy transformation unless the user explicitly asks to skip it.

Minimum profile output:

- Shape
- Schema
- Missingness
- Distinct counts
- Numeric summary
- Date/time ranges
- Duplicate checks
- Candidate keys
- Warnings

### FR3: Tool Selection Rules

The skill must document when to use DuckDB, Polars, Pandas, and plotting libraries. It should prefer existing project conventions when present.

### FR4: Notebook and Script Hygiene

The skill must push agents toward clean artifacts:

- Notebooks should have a short question, setup cell, profile section, analysis section, findings section, and caveats section.
- Scripts should expose functions, avoid hidden global state, accept input/output paths, and be runnable from the command line when useful.
- Generated outputs should go under an obvious folder such as `analysis/`, `reports/`, `outputs/`, or the repo's existing convention.

### FR5: Plotting Standards

The skill must guide agents to create plots that answer a specific question.

Plot defaults:

- Use readable titles and axis labels.
- Avoid decorative charts.
- Save plot files when they are part of the deliverable.
- Prefer simple, interpretable visualizations before complex ones.

### FR6: Modeling Guardrails

If modeling is requested, the skill must force a pre-modeling checklist:

- Define the prediction target.
- Identify the observation grain.
- Check label distribution.
- Check leakage candidates.
- Choose split strategy.
- Establish a simple baseline.
- Pick metrics that match the decision problem.

### FR7: Privacy and Safety

The skill must default to local execution and avoid uploading private data. If a task requires external services, the agent must ask first.

## Suggested Skill Structure

~~~text
tablelore/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── engine-selection.md
│   ├── profiling-checklist.md
│   ├── notebook-hygiene.md
│   └── modeling-guardrails.md
└── scripts/
    ├── table_profile.py
    └── init_analysis.py
~~~

`SKILL.md` should stay concise. Detailed checklists and examples should live in `references/` so an agent only loads them when needed.

## MVP Scope

The first version should ship as a Codex/Claude-compatible skill, not a full Python package.

MVP includes:

- `SKILL.md` with the core workflow and trigger description.
- Profiling checklist reference.
- Engine selection reference.
- Notebook/script hygiene reference.
- One optional profiling helper script using DuckDB plus Polars or Pandas.
- Example prompts and expected outputs inside references only if they materially improve agent behavior.

MVP does not include:

- Full CLI packaging.
- AutoML.
- Hosted services.
- Complex report generation.
- Database credential management.

## Later Versions

Potential v2 features:

- `tablelore profile path/to/file.csv` CLI.
- HTML profile report.
- Great Expectations or Pandera validation template generation.
- dbt source/model inspection.
- Time-series checklist.
- Causal inference checklist.
- Experiment analysis checklist.
- Geospatial data checklist.
- LLM-generated analysis review rubric.

## Acceptance Criteria

TableLore v1 is successful when an AI agent using the skill can:

1. Inspect an unfamiliar dataset without jumping straight to modeling.
2. Produce a useful profile summary with data quality warnings.
3. Choose DuckDB, Polars, or Pandas for defensible reasons.
4. Create a clean exploratory notebook or rerunnable script.
5. Save charts and outputs in a predictable location.
6. Explain findings with caveats.
7. Leave the repo cleaner than it found it.

## Example User Requests

- "Analyze this CSV and tell me what drives churn."
- "Profile this Parquet dataset before we build a model."
- "Create a clean notebook exploring revenue by cohort."
- "Convert this messy notebook into a reproducible script."
- "Check this dataset for leakage before training."
- "Use DuckDB to join these extracts and summarize anomalies."

## Open Questions

- Should `tablelore` be a pure skill first, or should it immediately include a small CLI?
- Should the helper script depend on DuckDB plus Polars, or DuckDB plus Pandas for broader install compatibility?
- Should the public repo target Codex skills, Claude skills, or both from day one?
- What license should be used?
- Should generated artifacts use `analysis/`, `reports/`, or defer entirely to repo convention?

## Recommended First Build

Build the skill in this order:

1. Draft `SKILL.md`.
2. Add `references/profiling-checklist.md`.
3. Add `references/engine-selection.md`.
4. Add `references/notebook-hygiene.md`.
5. Add `references/modeling-guardrails.md`.
6. Add a small `scripts/table_profile.py` only after the written workflow is solid.

The written skill matters more than the helper script. The real product is the agent behavior: slow down, profile the table, then analyze with discipline.
