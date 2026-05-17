# Modeling Guardrails

Use this checklist whenever a user asks for modeling, prediction, scoring,
classification, regression, feature importance, or "what drives" an outcome.
Do not train a complex model until the dataset has been profiled and these
items are documented.

## 1. Target Definition

State the prediction target in plain language before writing model code.

- Name the target column or explain how it will be derived.
- Define the positive class for classification tasks.
- Define the prediction horizon, such as "within 30 days" or "next quarter."
- Confirm whether the target is known at prediction time or only after the
  outcome occurs.
- Identify rows where the target is missing, ambiguous, or not eligible for
  modeling.

If the target definition is unclear, stop and ask the user or inspect project
docs before modeling.

## 2. Observation Grain

Describe what one training example represents.

- One customer, account, event, transaction, session, claim, device, day, or
  other entity.
- Whether multiple rows can belong to the same entity.
- Whether rows are snapshots, events, aggregates, or labels joined onto another
  table.
- Whether the model will score the same grain at inference time.

The grain controls deduplication, feature aggregation, splitting, and metric
interpretation. Do not mix grains without making the transformation explicit.

## 3. Label Distribution

Profile the target before choosing models or metrics.

- Count labeled, unlabeled, and ineligible rows.
- For classification, report class counts and proportions.
- For regression, report the target range, missingness, outliers, and skew.
- For time-dependent labels, check whether distribution shifts across time.
- Flag severe imbalance, rare positive labels, or small sample sizes.

Do not treat label imbalance as a reason to resample automatically. First
explain how it affects baseline choice, metric choice, and uncertainty.

## 4. Leakage Candidates

Search for columns and joins that reveal the answer directly or indirectly.

Common leakage candidates:

- Columns recorded after the prediction point.
- Status, reason, resolution, outcome, payment, cancellation, or closure fields.
- Dates that occur after the label event.
- Aggregates computed using the full dataset instead of the training window.
- IDs or codes that encode the target.
- Features created by joining future records onto past observations.
- Duplicated entities that can appear in both train and test sets.
- Notebook or script variables created after the target was computed.

When leakage risk is found, do not silently drop columns and proceed. List the
risk, explain why it is risky, and either remove it with justification or ask for
domain confirmation.

## 5. Split Strategy

Choose a validation split that matches how the model will be used.

- Use a time-based split when predictions will be made on future data.
- Use a group split when the same entity can appear in multiple rows.
- Use stratification for classification only when it does not break time or
  group constraints.
- Keep the test set untouched until the final evaluation.
- Fit encoders, imputers, scalers, feature selectors, and resampling only on the
  training split.
- Record the split rule in the notebook or script, including date cutoffs or
  grouping keys.

Random row splits are acceptable only when rows are independent and there is no
time, group, or leakage concern.

## 6. Baseline

Establish a simple baseline before advanced modeling.

- Classification: majority class, stratified random, or a simple rule the user
  already uses.
- Regression: mean, median, last known value, or a domain rule.
- Ranking or prioritization: current ordering, random ordering, or a simple
  sortable risk signal.
- Time series: naive last value, seasonal naive, or moving average.

Report whether the candidate model improves on the baseline in the metric that
matches the decision problem. If it does not, say so plainly.

## 7. Metrics

Pick metrics based on the decision, not on convenience.

- Imbalanced classification: precision, recall, F1, PR AUC, lift, or recall at
  a review budget.
- Balanced classification: accuracy may be acceptable, but include confusion
  matrix details.
- Probability scoring: log loss, Brier score, and calibration checks.
- Regression: MAE for typical absolute error, RMSE for large-error penalty,
  MAPE only when zero or near-zero targets are not a problem.
- Ranking: top-k precision/recall, lift, NDCG, or business-relevant review rate.
- Time-dependent evaluation: metrics by time window, not only a pooled score.

State what a better value means and why the selected metric fits the user's
decision.

## 8. Uncertainty

Explain how stable the result is likely to be.

- Report sample size and label counts alongside metrics.
- Use confidence intervals, bootstrapping, or repeated validation when feasible.
- Compare train, validation, and test performance for overfitting signs.
- Show metric variation across important segments or time windows.
- Avoid overinterpreting small metric differences.
- Note when uncertainty is dominated by data quality, labeling, or sampling.

If uncertainty cannot be quantified within the task, name the limitation rather
than presenting the score as definitive.

## 9. Modeling Caveats

Every modeling report should include caveats that are specific to the data and
workflow.

Cover:

- Target definition assumptions.
- Observation grain assumptions.
- Excluded rows or columns.
- Leakage risks found and how they were handled.
- Split strategy and why it matches the use case.
- Baseline comparison.
- Metric limitations.
- Known data quality issues.
- Whether the result is exploratory or suitable for production review.

Do not imply causality from predictive feature importance. Use language such as
"associated with model predictions" unless the analysis was designed for causal
inference.

## Minimum Pre-Modeling Note

Before fitting a model, leave a short note in the notebook, script, or response:

```markdown
### Modeling Readiness

- Target: `<target definition and positive class or regression target>`
- Observation grain: `<one row represents ...>`
- Label distribution: `<counts/proportions or summary after profiling>`
- Leakage candidates: `<columns/joins reviewed and action taken>`
- Split strategy: `<time/group/random split rule and reason>`
- Baseline: `<simple baseline to beat>`
- Metrics: `<metric list and why they fit the decision>`
- Caveats: `<known limitations before modeling>`
```
