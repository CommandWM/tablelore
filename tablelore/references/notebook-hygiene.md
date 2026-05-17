# Notebook and Script Hygiene

TableLore artifacts should be easy to rerun, review, and trust. Keep exploration useful, but do not let exploratory state become the only copy of production logic.

## Clean Notebook Structure

A notebook should have a visible structure that tells the reader what question was asked, what data was used, what changed during analysis, and what can be trusted.

Recommended sections:

1. Title and question
2. Setup
3. Data inventory
4. Profile summary
5. Analysis
6. Findings
7. Caveats and next steps
8. Reproducibility notes

### Title and Question

- State the analysis question in one or two sentences.
- Name the target dataset, date range, cohort, entity grain, or business context when known.
- Include the expected deliverable: findings, chart, cleaned dataset, profile, or modeling readiness check.

### Setup

- Put imports, display options, constants, input paths, output paths, random seeds, and chart defaults near the top.
- Avoid hidden notebook state. A clean restart-and-run-all should reproduce the same outputs.
- Do not hardcode user-specific absolute paths unless the repo already requires them.
- Prefer `pathlib.Path` and repo-relative paths.

### Data Inventory

- List the files, tables, or extracts used.
- Record file sizes, row counts, column counts, and last-modified clues when relevant.
- Avoid dumping sensitive raw rows. Prefer schemas, aggregates, and small masked samples.

### Profile Summary

- Include shape, schema, missingness, distinct counts, numeric summaries, date ranges, duplicate checks, candidate keys, and warnings.
- Capture assumptions about grain, identifiers, timestamps, labels, and leakage-prone columns.
- Profile before modeling or heavy transformations unless the user explicitly asked to skip profiling.

### Analysis

- Keep transformations explicit and named.
- Use markdown between major steps to explain why the step exists.
- Prefer simple baselines and descriptive checks before advanced modeling.
- If the notebook grows long or reusable logic emerges, extract stable functions into a script or project module.

### Findings

- Answer the original question directly.
- Link findings to specific tables, plots, or saved outputs.
- Include caveats, data quality risks, uncertainty, and what would change the conclusion.
- Do not overstate causality or model performance from exploratory evidence.

## Rerunnable Script Standards

Use scripts when the work needs to be repeated, reviewed, scheduled, tested, or reused by another agent or teammate.

A script should:

- Expose functions for loading, profiling, transforming, plotting, and writing outputs.
- Keep executable orchestration under `if __name__ == "__main__":`.
- Accept input and output paths through CLI arguments, configuration, or a clearly documented constant block.
- Avoid hidden global state and notebook-only variables.
- Create output directories if they do not exist.
- Write deterministic outputs when possible.
- Set random seeds when sampling, splitting, or modeling.
- Log or print concise progress messages, not full sensitive data dumps.
- Fail clearly when required inputs are missing.
- Preserve enough metadata for reruns: source paths, row counts, filters, parameters, and generation time when useful.

Minimal pattern:

```python
from pathlib import Path
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile a local dataset.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", default=Path("outputs/analysis"), type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Load, profile, analyze, and write outputs here.


if __name__ == "__main__":
    main()
```

## Output Folder Conventions

Use the repo's existing convention first. Look for folders such as `analysis/`, `reports/`, `outputs/`, `notebooks/`, `figures/`, `plots/`, `data/processed/`, or documented project paths.

If there is no convention, use predictable local folders:

- `analysis/` for exploratory notebooks and analysis notes.
- `outputs/` for generated tables, summaries, and machine-readable artifacts.
- `outputs/plots/` for generated chart images.
- `reports/` for polished Markdown, HTML, PDF, or presentation-ready summaries.
- `data/processed/` for derived datasets only when the repo already treats derived data as a committed or reproducible artifact.

Rules:

- Do not overwrite source data.
- Separate raw inputs from generated outputs.
- Use filenames that include the subject and purpose, such as `churn_profile_summary.csv` or `revenue_by_cohort.png`.
- Avoid timestamped filenames unless multiple historical runs must be preserved.
- Add a short README or report note when outputs need interpretation.
- Respect `.gitignore`; large generated artifacts may belong outside version control.

## Plot Standards

Every deliverable plot should answer a specific question.

Required defaults:

- Use a clear title that names the metric, group, and time window when relevant.
- Label axes with units.
- Use readable tick formatting and avoid clipped labels.
- Prefer simple interpretable charts before complex ones.
- Sort bars and categories intentionally.
- Use color to encode meaning, not decoration.
- Include sample size, filters, or caveats in the caption or surrounding text when they matter.
- Save plots that are part of the deliverable.

Suggested formats:

- PNG for common static review.
- SVG or PDF for publication-style vector output.
- HTML for Plotly or other interactive deliverables.

Avoid:

- Decorative charts that do not answer the question.
- 3D charts for ordinary tabular comparisons.
- Pie charts with many categories.
- Dual-axis charts unless there is no clearer alternative.
- Plotting millions of raw points when aggregation, binning, or sampling would show the pattern more honestly.

## Reproducibility Notes

Each notebook, script, or report should leave enough context for another worker to rerun the analysis.

Include:

- Command or notebook run instructions.
- Input data paths and any expected schema assumptions.
- Output paths.
- Engine and library choices when not obvious from project convention.
- Package manager or environment notes when the repo provides them.
- Random seeds and sampling rules.
- Date/time filtering rules and timezone assumptions.
- Known data quality risks.
- Any manual steps that were required.

Before calling work complete:

- Restart and run all notebook cells when feasible.
- Run scripts from the command line using the documented arguments.
- Confirm expected outputs are created.
- Confirm plots render and are saved where documented.
- Check that sensitive raw data was not printed or written unnecessarily.

## Keep Exploration Separate From Production Logic

Exploration is allowed to be messy while the question is forming. The committed artifact should not be.

Keep in notebooks:

- Narrative reasoning.
- Initial profiling.
- Diagnostic charts.
- Small experiments.
- Caveats and interpretation.

Move into scripts or modules:

- Reusable loading code.
- Cleaning and type normalization.
- Feature construction.
- Joins and business rules.
- Plot generation used in reports.
- Modeling preparation or scoring logic.

Do not leave production behavior dependent on:

- Cell execution order.
- Manual edits to intermediate files.
- Variables created in earlier notebook sessions.
- Hardcoded local machine paths.
- Unrecorded filters or exclusions.

Practical handoff: keep the notebook as a readable story, and make the script or module the repeatable source for loading, transformation, and saved outputs.
