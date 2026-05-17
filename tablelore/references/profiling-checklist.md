# Profiling Checklist

Use this checklist before modeling, heavy transformation, or analysis that depends
on assumptions about the data. Skip or shorten it only when the user explicitly
asks to skip profiling, and note that the skip increases data-quality risk.

Prefer metadata, schemas, aggregate summaries, and small safe samples over raw row
dumps. Do not print sensitive raw values unless the user has asked for them and it
is safe to do so.

## 1. Data Inventory

- List every input file, table, or extract being used.
- Capture format, path or connection name, file size when available, row count,
  column count, and read method.
- Note whether the source is local, generated, sampled, filtered, or a full
  production extract.
- Identify existing repo conventions for where analysis outputs, reports, or
  notebooks should be written.

## 2. Schema And Types

- Record column names and inferred types from the chosen engine.
- Compare inferred types with documented schemas, existing code, or domain
  expectations when available.
- Flag type drift such as IDs read as numbers, dates read as strings, numeric
  amounts read as text, booleans encoded as mixed strings, or high-precision
  values at risk of truncation.
- Note units and encoded meanings when they are visible from names or metadata.

## 3. Missingness And Distinct Counts

- For each column, compute null count, null percentage, and distinct count.
- Distinguish true nulls from empty strings, whitespace, sentinels such as
  `N/A`, `unknown`, `-1`, `999`, or zero values that may mean missing.
- Flag columns that are entirely missing, nearly constant, unexpectedly sparse,
  or unexpectedly dense.
- Check whether missingness differs by time period, source file, segment, or
  target class when relevant.

## 4. Numeric And Date Ranges

- For numeric columns, compute min, max, mean or median, quartiles, and counts of
  negative, zero, and extreme values when those checks are meaningful.
- Flag impossible or suspicious values such as negative ages, percentages outside
  `0..100`, future dates, impossible coordinates, or amounts with mixed signs.
- For date and timestamp columns, compute min, max, timezone clues, parse failure
  count, and frequency by natural period when useful.
- Confirm whether date ranges match the question, expected training window, and
  available outcome window.

## 5. Category Cardinality And Top Values

- For categorical columns, compute cardinality and top values with counts and
  percentages.
- Flag free-text columns, identifier-like categories, very high-cardinality
  fields, and categories with inconsistent casing, whitespace, spelling, or
  encoding.
- Look for dominant values, rare buckets, placeholder categories, and values that
  imply system defaults rather than observed behavior.
- Avoid dumping long value lists; summarize high-cardinality columns with counts,
  examples only when safe, and aggregation.

## 6. Grain, Keys, And Duplicates

- State the likely grain: what one row represents.
- Identify candidate primary keys, entity keys, timestamps, event IDs, and
  natural composite keys.
- Check duplicate rows and duplicate candidate keys.
- For entity-level data, verify whether multiple rows per entity are expected.
- For event-level or time-series data, check ordering, repeated timestamps, and
  multiple events per entity per period.

## 7. Join Explosion Checks

Before joining datasets:

- Profile each join key on both sides for nulls, distinct counts, and duplicate
  key counts.
- Classify the expected relationship: one-to-one, one-to-many, many-to-one, or
  many-to-many.
- Estimate output row count before the join when possible.
- After the join, compare actual row count, unmatched counts, duplicated entity
  counts, and aggregate totals against pre-join baselines.
- Treat unexpected row growth, dropped rows, or changed totals as warnings that
  must be explained before continuing.

## 8. Target Distribution

When a target, label, outcome, or metric of interest is specified:

- Confirm the target column, target definition, and prediction or analysis time.
- Compute target missingness, distinct values, class balance, numeric range, and
  distribution by time period when relevant.
- Check whether the target is measured after the features and whether the outcome
  window is valid.
- Flag severe imbalance, rare outcomes, constant targets, target encoding issues,
  or target values that are unavailable at decision time.

## 9. Leakage Scan

For modeling or causal-style analysis, scan for leakage before training:

- Identify columns that directly encode the target, post-outcome events, future
  timestamps, final statuses, resolutions, refunds, cancellations, or manual
  decisions made after the prediction point.
- Check IDs, names, notes, file names, and status fields for hidden target
  information.
- Confirm that train/test splits respect time, groups, entities, and repeated
  observations.
- Flag aggregate features that may have been computed using future data or the
  full dataset.
- If leakage cannot be ruled out, recommend a baseline or split strategy that
  isolates the risk before modeling.

## 10. Warnings

End the profile with a concise warning list. Each warning should include:

- What was observed.
- Why it matters.
- Whether it blocks analysis, requires a caveat, or suggests a follow-up check.

Common warnings include schema drift, unexpected nulls, high-cardinality IDs,
duplicate keys, join explosion risk, impossible ranges, time-window mismatch,
label imbalance, likely leakage, raw data sensitivity, and insufficient sample
size.

## 11. Recommended Next Step

Finish with one practical next step based on the profile:

- Continue with descriptive analysis when data quality is adequate.
- Clean or normalize specific fields before analysis.
- Resolve key or grain ambiguity before joining.
- Reframe the question if the available data cannot answer it.
- Create a notebook when exploration and narrative are the deliverable.
- Create a script when repeatability, review, or reuse is the deliverable.
- For modeling, define the target, split strategy, baseline, and metrics only
  after the profiling warnings are addressed or explicitly accepted.
