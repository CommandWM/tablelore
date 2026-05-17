# Example Prompts and Response Shapes

These examples show the kind of user request TableLore should handle and the
shape of a useful response. The placeholders are intentional. Do not invent
analysis results; replace placeholders only after inspecting the real data.

## CSV Profiling

Example prompt:

> Analyze this CSV and tell me what drives churn.

Expected response shape:

```markdown
I will profile the CSV before modeling or claiming drivers.

Data inspected:
- Path: `<path/to/file.csv>`
- Shape: `<rows>` rows x `<columns>` columns
- Inferred engine: `<DuckDB/Polars/Pandas>` because `<reason>`

Profile summary:
- Schema: `<column/type summary>`
- Missingness: `<highest-null columns and notable patterns>`
- Candidate keys: `<possible IDs or none found>`
- Date ranges: `<timestamp columns and ranges>`
- Target check: `<target column, positive class, label distribution>`
- Data quality warnings: `<duplicates, suspicious values, type drift, etc.>`

Next step:
- If modeling is still requested, I will run the modeling guardrails checklist
  before fitting a baseline.
```

## Parquet or Multi-File Inspection

Example prompt:

> Profile this Parquet dataset before we build a model.

Expected response shape:

```markdown
I will inspect file metadata and row-group/schema consistency before loading
everything eagerly.

Data inventory:
- Root/path: `<dataset path>`
- Files found: `<file count and formats>`
- Partition columns: `<partition fields if present>`
- Schema consistency: `<same schema / drift detected>`
- Approximate rows: `<row count from metadata or query>`

Profile summary:
- Columns and types: `<schema summary>`
- Nulls and distincts: `<summary from aggregate queries>`
- Date/time coverage: `<ranges by relevant timestamp columns>`
- Join or entity keys: `<candidate keys>`
- Modeling readiness: `<target/grain/leakage questions still open>`

Recommended engine:
- `<DuckDB/Polars>` because `<file count, format, size, query pattern>`
```

## Notebook Exploration

Example prompt:

> Create a clean notebook exploring revenue by cohort.

Expected response shape:

```markdown
I will create an exploratory notebook with a reproducible structure:

Notebook outline:
1. Question and scope
2. Setup and imports
3. Data inventory
4. Profile: shape, schema, missingness, date coverage, cohort keys
5. Cohort construction with explicit assumptions
6. Revenue summaries and plots
7. Findings
8. Caveats and reproducibility notes

Artifacts:
- Notebook: `<path/to/notebook.ipynb>`
- Optional plots: `<paths if saved>`

I will not report findings until the notebook cells have been run against the
actual data.
```

## Messy Notebook Conversion

Example prompt:

> Convert this messy notebook into a reproducible script.

Expected response shape:

```markdown
I will preserve the analysis intent, remove hidden state, and make inputs and
outputs explicit.

Conversion plan:
- Source notebook: `<path/to/source.ipynb>`
- Target script: `<path/to/script.py>`
- Main inputs: `<input paths or parameters>`
- Main outputs: `<tables, charts, reports, or files>`
- Reusable functions: `<load/profile/transform/analyze/save>`
- Removed or isolated cells: `<scratch, failed attempts, display-only cells>`

Reproducibility checks:
- Script accepts input/output paths.
- Transformations are ordered and named.
- Generated artifacts go under `<analysis/reports/outputs or repo convention>`.
- The script can be run with `<command>`.

Caveats:
- `<assumptions or cells requiring user confirmation>`
```

## Leakage Check

Example prompt:

> Check this dataset for leakage before training.

Expected response shape:

```markdown
I will define the prediction point and review columns, joins, and split strategy
before any model training.

Modeling context:
- Target: `<target definition>`
- Observation grain: `<one row represents ...>`
- Prediction time: `<when features must be available>`
- Label distribution: `<counts/proportions after profiling>`

Leakage review:
- Direct target proxies: `<columns reviewed and concerns>`
- Post-outcome timestamps/statuses: `<columns reviewed and concerns>`
- Aggregates/window features: `<whether computed only from past data>`
- Entity duplication: `<whether same entity crosses splits>`
- Join timing: `<whether joined records are available at prediction time>`

Recommendation:
- Safe to proceed with baseline: `<yes/no/needs clarification>`
- Columns to exclude or confirm: `<list with reasons>`
- Split strategy: `<time/group/random rule and justification>`
```

## DuckDB Joins

Example prompt:

> Use DuckDB to join these extracts and summarize anomalies.

Expected response shape:

```markdown
I will inspect each extract first, then join with row-count checks to catch join
explosions or dropped records.

Inputs:
- `<extract A>`: `<shape/schema/key candidates>`
- `<extract B>`: `<shape/schema/key candidates>`
- `<additional extracts>`: `<shape/schema/key candidates>`

Join plan:
- Join keys: `<key columns>`
- Join type: `<inner/left/full>` because `<reason>`
- Grain after join: `<one output row represents ...>`
- Pre-join checks: `<duplicate keys, null keys, type mismatches>`
- Post-join checks: `<row counts, unmatched records, duplicated entities>`

Anomaly summary shape:
- Scope: `<what counts as anomalous and who defined it>`
- Aggregates: `<counts/rates by relevant dimensions>`
- Examples: `<small safe samples only if needed>`
- Caveats: `<data quality or join assumptions>`

Artifacts:
- Query or script: `<path>`
- Output table/report: `<path if produced>`
```
