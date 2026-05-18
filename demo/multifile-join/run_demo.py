#!/usr/bin/env python3
"""Generate the TableLore multi-file join demo artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import duckdb
except ImportError as exc:  # pragma: no cover - exercised only without dev deps
    raise SystemExit(
        "duckdb is required for this demo. Run `python3 -m pip install -r requirements-dev.txt`."
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = REPO_ROOT / "demo" / "multifile-join"
DATA_ROOT = DEMO_ROOT / "data"
DEFAULT_OUTPUT_DIR = DEMO_ROOT / "output"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def csv_literal(path: Path) -> str:
    return str(path).replace("'", "''")


def build_connection() -> duckdb.DuckDBPyConnection:
    connection = duckdb.connect(database=":memory:")
    connection.execute(
        f"""
        create view customers as
        select * from read_csv_auto('{csv_literal(DATA_ROOT / "customers.csv")}');

        create view orders as
        select * from read_csv_auto('{csv_literal(DATA_ROOT / "orders.csv")}');

        create view refunds as
        select * from read_csv_auto('{csv_literal(DATA_ROOT / "refunds.csv")}');
        """
    )
    return connection


def scalar(connection: duckdb.DuckDBPyConnection, query: str) -> int:
    value = connection.execute(query).fetchone()[0]
    return int(value or 0)


def build_join_audit(connection: duckdb.DuckDBPyConnection, output_dir: Path) -> str:
    customer_rows = scalar(connection, "select count(*) from customers")
    order_rows = scalar(connection, "select count(*) from orders")
    refund_rows = scalar(connection, "select count(*) from refunds")
    duplicate_customer_keys = scalar(
        connection,
        """
        select count(*)
        from (
            select customer_id
            from customers
            group by customer_id
            having count(*) > 1
        )
        """,
    )
    orphan_orders = scalar(
        connection,
        """
        select count(*)
        from orders o
        left join customers c using (customer_id)
        where c.customer_id is null
        """,
    )
    orphan_refunds = scalar(
        connection,
        """
        select count(*)
        from refunds r
        left join orders o using (order_id)
        where o.order_id is null
        """,
    )
    joined_rows = scalar(
        connection,
        """
        select count(*)
        from orders o
        left join customers c using (customer_id)
        left join refunds r using (order_id)
        """,
    )

    return f"""# Join Audit

## Inputs

| file | rows | grain |
| --- | ---: | --- |
| `demo/multifile-join/data/customers.csv` | {customer_rows} | one row per customer, expected |
| `demo/multifile-join/data/orders.csv` | {order_rows} | one row per order |
| `demo/multifile-join/data/refunds.csv` | {refund_rows} | one row per refund event |

## Key Checks

- duplicate customer keys: {duplicate_customer_keys}
- orphan orders: {orphan_orders}
- orphan refunds: {orphan_refunds}
- joined rows after order-centered left joins: {joined_rows}

## Interpretation

The safest grain for the first pass is one row per order. The duplicate customer key can cause join explosion if customers are joined without deduplication. The orphan order and orphan refund need owner confirmation before revenue or refund-rate claims are treated as final.

## Artifacts

- Revenue summary: `{display_path(output_dir / "customer_revenue_summary.csv")}`
- Follow-up prompt: `{display_path(output_dir / "analysis_prompt.md")}`
"""


def write_revenue_summary(connection: duckdb.DuckDBPyConnection, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = connection.execute(
        """
        with customer_deduped as (
            select customer_id, min(account_name) as account_name, min(segment) as segment
            from customers
            group by customer_id
        ),
        refund_totals as (
            select order_id, sum(amount) as refunded_amount
            from refunds
            group by order_id
        )
        select
            coalesce(c.customer_id, o.customer_id) as customer_id,
            coalesce(c.account_name, 'UNKNOWN CUSTOMER') as account_name,
            count(o.order_id) as order_count,
            sum(o.amount) as gross_revenue,
            coalesce(sum(r.refunded_amount), 0) as refunded_amount,
            sum(o.amount) - coalesce(sum(r.refunded_amount), 0) as net_revenue
        from orders o
        left join customer_deduped c using (customer_id)
        left join refund_totals r using (order_id)
        group by 1, 2
        order by net_revenue desc
        """
    ).fetchall()

    lines = ["customer_id,account_name,order_count,gross_revenue,refunded_amount,net_revenue"]
    for row in rows:
        lines.append(",".join(str(value) for value in row))
    write_text(output_path, "\n".join(lines))


def analysis_prompt(output_dir: Path) -> str:
    return f"""Use $tablelore to review this multi-file join audit before summarizing revenue.

Inputs:
- Join audit: `{display_path(output_dir / "join_audit.md")}`
- Revenue summary: `{display_path(output_dir / "customer_revenue_summary.csv")}`
- Source files: `demo/multifile-join/data/`

Please:
1. Explain the row grain and join keys.
2. Call out duplicate keys, orphan orders, orphan refunds, and any join explosion risk.
3. Recommend whether the revenue summary is safe for directional use.
4. List the next data-owner questions before a final report.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create TableLore multi-file join demo artifacts.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    connection = build_connection()

    join_audit_path = output_dir / "join_audit.md"
    revenue_summary_path = output_dir / "customer_revenue_summary.csv"
    prompt_path = output_dir / "analysis_prompt.md"

    write_revenue_summary(connection, revenue_summary_path)
    write_text(join_audit_path, build_join_audit(connection, output_dir))
    write_text(prompt_path, analysis_prompt(output_dir))

    print("TableLore multi-file join demo artifacts written:")
    for path in [join_audit_path, revenue_summary_path, prompt_path]:
        print(f"- {display_path(path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
