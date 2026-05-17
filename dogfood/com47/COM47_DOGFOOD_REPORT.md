# COM-47 Dogfood Report

This dogfood pass used the TableLore v1 workflow against local representative analysis tasks.

## Checks Run

1. CSV profiling: `support_tickets.csv` was profiled with `tablelore/scripts/table_profile.py`.
2. Multi-file inspection: customer/order Parquet extracts were inspected before joining.
3. Notebook deliverable: `notebooks/revenue_by_cohort.ipynb` was created with question, setup, profile, analysis, findings, caveats, and reproducibility notes.
4. Rerunnable script deliverable: `scripts/build_cohort_report.py` generated a cohort summary CSV and saved chart.
5. Leakage check: `leakage_check.md` documented target, grain, leakage candidates, split strategy, baseline, metrics/caveat posture.

## Commands

```bash
python3 dogfood/com47/run_dogfood.py
python3 -m pytest tests -q
```

## Artifacts

- `dogfood/com47/evidence/support_tickets_profile.md`
- `dogfood/com47/evidence/multifile_parquet_inspection.md`
- `dogfood/com47/notebooks/revenue_by_cohort.ipynb`
- `dogfood/com47/scripts/build_cohort_report.py`
- `dogfood/com47/evidence/cohort_revenue_summary.csv`
- `dogfood/com47/evidence/cohort_revenue_by_month.png`
- `dogfood/com47/evidence/leakage_check.md`

## Findings

- The skill made profiling the first step before modeling and before interpreting joins.
- The profiling helper produced useful local warnings for missingness, duplicate rows, negative values, missing candidate keys, and leakage candidates.
- The first dogfood run showed that free-text note values should not be rendered as category examples; the helper was tightened to suppress note-like free text and flag status/note fields as leakage candidates.
- The engine-selection guidance correctly identified DuckDB as the preferred larger-data engine for multi-file Parquet joins, while allowing a dependency-light Pandas/PyArrow fallback for this small fixture.
- Notebook and script guidance separated exploratory narrative from rerunnable output generation.
- Modeling guardrails stopped short of fitting a model because leakage columns and duplicate grain issues were present.

## Follow-Up Issues

- Consider adding optional DuckDB support to the helper after v1 if COM-51 moves forward.
- Consider adding a native notebook validation script only if notebook dogfooding becomes a recurring release gate.
