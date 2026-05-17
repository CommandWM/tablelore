# Engine Selection

TableLore should choose analysis tools deliberately. Prefer the project's existing conventions when they are clear, then document any departure with the data size, file format, dependency, performance, or deliverable constraint that makes the exception worthwhile.

## Selection Order

1. Check repo conventions first: existing notebooks, scripts, `pyproject.toml`, `requirements.txt`, lockfiles, utility modules, chart styles, and output folders.
2. Identify the deliverable: exploratory notebook, rerunnable script, saved report, chart, dataset, or production logic.
3. Profile the data shape before committing to an engine: file format, row count, column count, nulls, cardinality, join keys, and memory pressure.
4. Choose the smallest tool that gives a clear, reproducible result.
5. State the tradeoff in the artifact when the choice is not obvious.

## DuckDB

Use DuckDB when the work is naturally analytical SQL over local files or tables.

Good fit:

- Querying CSV, TSV, Parquet, JSON, DuckDB, or SQLite-style extracts without first loading everything into a dataframe.
- Joining multiple local files or database exports.
- Aggregating, filtering, sampling, deduplicating, and profiling large local datasets.
- Reading Parquet metadata or partitioned files efficiently.
- Creating intermediate tables or views for repeatable analysis steps.
- Producing an Arrow, Polars, or Pandas result after reducing the data.

Tradeoffs:

- SQL can hide row-level transformation logic if the query becomes too large; break complex work into named views or scripts.
- Python-centric feature engineering, custom functions, and library integrations may be clearer in Polars or Pandas after DuckDB reduces the data.
- DuckDB is not a production database service; avoid implying concurrency, access control, or operational guarantees it does not provide.
- If a repo already has a mature dataframe pipeline, use DuckDB only where SQL-over-files materially simplifies discovery, joins, or aggregation.

Default pattern:

```python
import duckdb

con = duckdb.connect()
summary = con.execute(
    """
    select category, count(*) as rows, avg(amount) as avg_amount
    from read_parquet(?)
    group by 1
    order by rows desc
    """,
    ["data/events.parquet"],
).fetchdf()
```

## Polars

Use Polars as the fast default dataframe engine when the project has no stronger convention.

Good fit:

- Local CSV or Parquet transformation pipelines.
- Medium-to-large datasets where eager Pandas would be slow or memory-heavy.
- Typed column operations, lazy evaluation, predicate pushdown, and repeatable feature preparation.
- Clear transformation chains that can be reviewed as code.
- Producing clean Parquet, CSV, or Arrow outputs for downstream steps.

Tradeoffs:

- Some statistics, modeling, plotting, and domain packages still expect Pandas objects.
- Team familiarity may matter more than speed for small, collaborative analyses.
- Lazy execution is useful, but it requires explicit collection and can make debugging less immediate if overused.
- Convert to Pandas only at the boundary where a library requires it, and note that boundary.

Default pattern:

```python
import polars as pl

summary = (
    pl.scan_parquet("data/events.parquet")
    .filter(pl.col("amount").is_not_null())
    .group_by("category")
    .agg(
        rows=pl.len(),
        avg_amount=pl.col("amount").mean(),
    )
    .sort("rows", descending=True)
    .collect()
)
```

## Pandas

Use Pandas when compatibility, existing project context, or small-data ergonomics matter more than speed.

Good fit:

- Existing repo code, notebooks, tests, or project helpers already use Pandas.
- The dataset is small enough to fit comfortably in memory.
- A required library expects Pandas, such as many statistics, modeling, geospatial, or plotting packages.
- The user specifically asks for Pandas or needs a familiar handoff artifact.
- Quick inspection where the overhead of a new dependency is not justified.

Tradeoffs:

- Eager execution can be memory-heavy on wide, long, or messy files.
- Pandas joins and group-bys can become slow enough to obscure the real analysis task.
- Type inference can surprise you; inspect dtypes, nulls, dates, categorical values, and numeric ranges explicitly.
- Do not choose Pandas only from habit when DuckDB or Polars would make a larger local workflow safer and clearer.

Default pattern:

```python
import pandas as pd

df = pd.read_csv("data/events.csv")
summary = (
    df.dropna(subset=["amount"])
    .groupby("category", as_index=False)
    .agg(rows=("category", "size"), avg_amount=("amount", "mean"))
    .sort_values("rows", ascending=False)
)
```

## Notebooks

Use notebooks when the deliverable is exploratory reasoning, iterative profiling, charts, and an analysis narrative.

Good fit:

- The user asked for exploration, a walkthrough, or a chart-backed explanation.
- The notebook itself is the reviewable artifact.
- Intermediate tables and visual checks help explain the reasoning path.
- The question is still being refined and the next step depends on what the profile reveals.

Tradeoffs:

- Hidden state and out-of-order cells can make results hard to trust.
- Production logic should not live only in notebooks.
- Long notebooks are difficult to review; extract stable transformations into scripts or project modules.
- A notebook should still be restartable and should save important outputs to predictable paths.

## Scripts

Use scripts when the deliverable should be rerunnable, reviewed, scheduled, tested, or committed as project logic.

Good fit:

- Profiling or transformations need to be repeated on refreshed data.
- The output is a report, chart, cleaned dataset, feature table, or validation result.
- The work belongs in CI, a scheduled job, or a documented local workflow.
- The user asks to convert messy exploration into a reproducible artifact.

Tradeoffs:

- Scripts are less comfortable for exploratory narrative and iterative chart review.
- Over-engineering a one-off question can slow down analysis; start with a notebook when the question is still unclear.
- Scripts should take input and output paths rather than depending on hidden working-directory state.

Practical pattern: explore in a notebook, then move stable loading, profiling, cleaning, and plotting logic into a script or module. Keep the notebook as the narrative layer, not the only source of truth.

## Plotting Libraries

Follow existing project chart conventions first. If there is no convention, choose the simplest plotting library that answers the question and produces the required artifact.

### Matplotlib

Use Matplotlib for stable static charts, publication-style control, simple saved PNG/SVG/PDF outputs, and compatibility with the Python data stack.

Tradeoff: it can be verbose for statistical defaults and interactive exploration.

### Seaborn

Use Seaborn for quick statistical plots over Pandas-compatible data: distributions, box plots, heatmaps, faceted comparisons, and relationship checks.

Tradeoff: it usually expects Pandas-like inputs and is less suitable for large data before aggregation or sampling.

### Plotly

Use Plotly when interactivity is part of the deliverable, such as hover details, zooming, filtering, or a shareable HTML chart.

Tradeoff: interactive files can be heavier and less ideal for static reports, diffs, and lightweight review.

### Altair

Use Altair when declarative chart grammar improves clarity, especially for compact exploratory charts and notebook narratives.

Tradeoff: large datasets often need aggregation or sampling first, and some users may be less familiar with the Vega-Lite model.

### Built-In Dataframe Plots

Use Pandas or Polars built-in plotting only for quick diagnostics. For deliverable charts, switch to the repo's chart library or one of the libraries above so titles, labels, sizing, saved outputs, and styling are explicit.

## Common Decisions

- Local SQL over several Parquet files: DuckDB first, then Polars or Pandas for narrowed results.
- Fast dataframe transformation with no project convention: Polars first.
- Existing Pandas notebook in a small-data repo: Pandas first, unless profiling shows memory or speed problems.
- Exploratory question with charts and caveats: notebook first, with clean sections and saved outputs.
- Repeatable report or data product: script first, optionally paired with a short notebook or Markdown summary.
- Static report chart: Matplotlib or Seaborn, depending on whether low-level control or statistical defaults matter more.
- Interactive stakeholder review: Plotly, saved as HTML, only when interactivity is useful.

## Required Explanation

When leaving behind an analysis artifact, include a short note such as:

> Engine choice: DuckDB was used to join and aggregate three Parquet extracts without loading full raw tables into memory. The reduced result was converted to Pandas for Seaborn plotting because the project already uses Seaborn for report charts.

That note should name the project convention, the selected engine, and the tradeoff accepted.
