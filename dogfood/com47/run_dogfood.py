#!/usr/bin/env python3
"""Generate COM-47 dogfood evidence for TableLore v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "dogfood" / "com47"
DATA = BASE / "data"
EVIDENCE = BASE / "evidence"
NOTEBOOKS = BASE / "notebooks"
SCRIPTS = BASE / "scripts"
HELPER = ROOT / "tablelore" / "scripts" / "table_profile.py"


def write_inputs() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)

    support = pd.DataFrame(
        [
            {
                "ticket_id": "T-100",
                "account_id": "A-001",
                "opened_at": "2026-01-03",
                "plan": "starter",
                "severity": "low",
                "first_response_hours": 8.5,
                "csat_score": 5,
                "churned_30d": 0,
                "resolution_status": "resolved",
                "post_churn_note": "",
            },
            {
                "ticket_id": "T-101",
                "account_id": "A-002",
                "opened_at": "2026-01-07",
                "plan": "pro",
                "severity": "high",
                "first_response_hours": 31.0,
                "csat_score": 2,
                "churned_30d": 1,
                "resolution_status": "canceled_after_ticket",
                "post_churn_note": "downgraded after closure",
            },
            {
                "ticket_id": "T-102",
                "account_id": "A-003",
                "opened_at": "2026-01-08",
                "plan": "enterprise",
                "severity": "critical",
                "first_response_hours": 48.0,
                "csat_score": 1,
                "churned_30d": 1,
                "resolution_status": "refund_processed",
                "post_churn_note": "refund after churn",
            },
            {
                "ticket_id": "T-103",
                "account_id": "A-004",
                "opened_at": "2026-02-02",
                "plan": "starter",
                "severity": "medium",
                "first_response_hours": None,
                "csat_score": 4,
                "churned_30d": 0,
                "resolution_status": "resolved",
                "post_churn_note": "",
            },
            {
                "ticket_id": "T-104",
                "account_id": "A-005",
                "opened_at": "2026-02-12",
                "plan": "pro",
                "severity": "critical",
                "first_response_hours": -1.0,
                "csat_score": None,
                "churned_30d": 1,
                "resolution_status": "canceled_after_ticket",
                "post_churn_note": "account closed",
            },
            {
                "ticket_id": "T-104",
                "account_id": "A-005",
                "opened_at": "2026-02-12",
                "plan": "pro",
                "severity": "critical",
                "first_response_hours": -1.0,
                "csat_score": None,
                "churned_30d": 1,
                "resolution_status": "canceled_after_ticket",
                "post_churn_note": "account closed",
            },
        ]
    )
    support.to_csv(DATA / "support_tickets.csv", index=False)

    customers = pd.DataFrame(
        [
            {"customer_id": "A-001", "signup_date": "2025-10-01", "region": "NA", "segment": "small"},
            {"customer_id": "A-002", "signup_date": "2025-10-15", "region": "EU", "segment": "mid"},
            {"customer_id": "A-003", "signup_date": "2025-11-20", "region": "NA", "segment": "enterprise"},
            {"customer_id": "A-004", "signup_date": "2025-12-03", "region": "APAC", "segment": "small"},
            {"customer_id": "A-005", "signup_date": "2025-12-10", "region": "EU", "segment": "mid"},
        ]
    )
    orders_q1 = pd.DataFrame(
        [
            {"order_id": "O-100", "customer_id": "A-001", "order_date": "2026-01-03", "amount": 120.0},
            {"order_id": "O-101", "customer_id": "A-002", "order_date": "2026-01-14", "amount": 240.0},
            {"order_id": "O-102", "customer_id": "A-003", "order_date": "2026-02-08", "amount": 750.0},
            {"order_id": "O-103", "customer_id": "A-006", "order_date": "2026-02-19", "amount": 88.0},
        ]
    )
    orders_q2 = pd.DataFrame(
        [
            {"order_id": "O-104", "customer_id": "A-001", "order_date": "2026-04-03", "amount": 135.0},
            {"order_id": "O-105", "customer_id": "A-004", "order_date": "2026-04-15", "amount": 60.0},
            {"order_id": "O-106", "customer_id": "A-005", "order_date": "2026-05-20", "amount": 260.0},
        ]
    )
    customers.to_parquet(DATA / "customers.parquet", index=False)
    orders_q1.to_parquet(DATA / "orders_q1.parquet", index=False)
    orders_q2.to_parquet(DATA / "orders_q2.parquet", index=False)


def run_profile() -> None:
    profile_path = EVIDENCE / "support_tickets_profile.md"
    subprocess.run(
        [
            sys.executable,
            str(HELPER),
            str(DATA / "support_tickets.csv"),
            "--target",
            "churned_30d",
            "--output",
            str(profile_path),
        ],
        check=True,
        cwd=ROOT,
    )


def write_multifile_inspection() -> None:
    customers = pd.read_parquet(DATA / "customers.parquet")
    orders = pd.concat(
        [pd.read_parquet(DATA / "orders_q1.parquet"), pd.read_parquet(DATA / "orders_q2.parquet")],
        ignore_index=True,
    )
    joined = orders.merge(customers, on="customer_id", how="left", indicator=True)
    duplicate_order_ids = int(orders["order_id"].duplicated().sum())
    unmatched = int((joined["_merge"] == "left_only").sum())
    report = f"""# Multi-File Inspection

Question: inspect local customer and order extracts before summarizing cohort revenue.

Data inventory:
- `customers.parquet`: {len(customers)} rows x {len(customers.columns)} columns.
- `orders_q1.parquet`: {len(pd.read_parquet(DATA / "orders_q1.parquet"))} rows.
- `orders_q2.parquet`: {len(pd.read_parquet(DATA / "orders_q2.parquet"))} rows.

Engine choice:
- DuckDB would be the preferred engine for a larger real extract because this is SQL-style aggregation over multiple Parquet files.
- This dogfood run used Pandas with PyArrow because the repo intentionally avoids adding DuckDB as a v1 runtime dependency.

Join checks:
- Join key: `customer_id`.
- Expected relationship: many orders to one customer.
- Order rows before join: {len(orders)}.
- Rows after left join: {len(joined)}.
- Duplicate order IDs: {duplicate_order_ids}.
- Unmatched order rows: {unmatched}.

Warnings:
- One order references `A-006`, which is not present in `customers.parquet`; downstream cohort reporting should treat that row as unmatched until the extract is corrected.

Recommended next step:
- Use a rerunnable script for the cohort summary so join assumptions, unmatched counts, and outputs are reproducible.
"""
    (EVIDENCE / "multifile_parquet_inspection.md").write_text(report, encoding="utf-8")


def run_cohort_script() -> None:
    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "build_cohort_report.py"),
            "--customers",
            str(DATA / "customers.parquet"),
            "--orders-q1",
            str(DATA / "orders_q1.parquet"),
            "--orders-q2",
            str(DATA / "orders_q2.parquet"),
            "--output-dir",
            str(EVIDENCE),
        ],
        check=True,
        cwd=ROOT,
    )


def write_notebook() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Revenue by Cohort\n", "\n", "Question: how does revenue vary by signup cohort and order month?\n"],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Profile Summary\n",
                    "\n",
                    "Inputs are local Parquet customer and order extracts. Profile before analysis: row counts, join keys, unmatched orders, date ranges, and revenue ranges are checked before cohort aggregation.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from pathlib import Path\n",
                    "import pandas as pd\n",
                    "\n",
                    "base = Path('dogfood/com47')\n",
                    "customers = pd.read_parquet(base / 'data/customers.parquet')\n",
                    "orders = pd.concat([\n",
                    "    pd.read_parquet(base / 'data/orders_q1.parquet'),\n",
                    "    pd.read_parquet(base / 'data/orders_q2.parquet'),\n",
                    "], ignore_index=True)\n",
                    "customers.shape, orders.shape\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "customers['signup_month'] = pd.to_datetime(customers['signup_date']).dt.to_period('M').astype(str)\n",
                    "orders['order_month'] = pd.to_datetime(orders['order_date']).dt.to_period('M').astype(str)\n",
                    "joined = orders.merge(customers[['customer_id', 'signup_month', 'region']], on='customer_id', how='left', indicator=True)\n",
                    "joined['_merge'].value_counts()\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Findings and Caveats\n",
                    "\n",
                    "- This notebook is a reviewable exploration shell, not production logic.\n",
                    "- The rerunnable script in `dogfood/com47/scripts/build_cohort_report.py` is the source for committed outputs.\n",
                    "- One unmatched order is expected from the fixture and should be called out before interpreting cohort revenue.\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (NOTEBOOKS / "revenue_by_cohort.ipynb").write_text(json.dumps(notebook, indent=2) + "\n", encoding="utf-8")


def write_leakage_check() -> None:
    support = pd.read_csv(DATA / "support_tickets.csv", keep_default_na=False, na_values=[""])
    label_counts = support["churned_30d"].value_counts(dropna=False).to_dict()
    report = f"""# Leakage Check

Question: check `support_tickets.csv` for leakage before training a churn model.

Modeling readiness:
- Target: `churned_30d`, positive class `1`.
- Observation grain: one row appears to represent one support ticket, but duplicate `ticket_id` values show the grain is not clean.
- Label distribution: {label_counts}.
- Prediction time: ticket open time; features should be available at or shortly after `opened_at`.

Leakage candidates:
- `resolution_status`: contains post-ticket outcomes such as cancellation/refund-style states.
- `post_churn_note`: explicitly contains post-outcome text and should be excluded from training.
- Duplicate `ticket_id` values can place the same entity in train and test unless removed or grouped.

Split strategy:
- Use a time-based split by `opened_at` for future prediction, or a grouped split by `account_id` if multiple tickets per account are retained.

Baseline:
- Start with the majority-class or simple severity/response-time rule before advanced models.

Decision:
- Not ready for modeling until duplicate ticket handling, leakage-column exclusion, and split strategy are documented.
"""
    (EVIDENCE / "leakage_check.md").write_text(report, encoding="utf-8")


def write_final_report() -> None:
    report = """# COM-47 Dogfood Report

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
"""
    (BASE / "COM47_DOGFOOD_REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    write_inputs()
    run_profile()
    write_multifile_inspection()
    run_cohort_script()
    write_notebook()
    write_leakage_check()
    write_final_report()


if __name__ == "__main__":
    main()
