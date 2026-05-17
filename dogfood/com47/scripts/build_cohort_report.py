#!/usr/bin/env python3
"""Build a rerunnable cohort revenue summary for COM-47 dogfooding."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build cohort revenue dogfood artifacts.")
    parser.add_argument("--customers", required=True, type=Path)
    parser.add_argument("--orders-q1", required=True, type=Path)
    parser.add_argument("--orders-q2", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def load_inputs(customers_path: Path, q1_path: Path, q2_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    customers = pd.read_parquet(customers_path)
    orders = pd.concat(
        [pd.read_parquet(q1_path), pd.read_parquet(q2_path)],
        ignore_index=True,
    )
    return customers, orders


def build_cohort_summary(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    customers = customers.copy()
    orders = orders.copy()
    customers["signup_month"] = pd.to_datetime(customers["signup_date"]).dt.to_period("M").astype(str)
    orders["order_month"] = pd.to_datetime(orders["order_date"]).dt.to_period("M").astype(str)
    joined = orders.merge(customers[["customer_id", "signup_month", "region"]], on="customer_id", how="left")
    return (
        joined.groupby(["signup_month", "order_month", "region"], dropna=False)
        .agg(
            orders=("order_id", "count"),
            revenue=("amount", "sum"),
            customers=("customer_id", "nunique"),
        )
        .reset_index()
        .sort_values(["signup_month", "order_month", "region"])
    )


def save_plot(summary: pd.DataFrame, output_path: Path) -> None:
    monthly = summary.groupby("order_month", as_index=False)["revenue"].sum()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(monthly["order_month"], monthly["revenue"], color="#2D9CDB")
    ax.set_title("Revenue by Order Month")
    ax.set_xlabel("Order month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    customers, orders = load_inputs(args.customers, args.orders_q1, args.orders_q2)
    summary = build_cohort_summary(customers, orders)
    summary_path = args.output_dir / "cohort_revenue_summary.csv"
    plot_path = args.output_dir / "cohort_revenue_by_month.png"
    summary.to_csv(summary_path, index=False)
    save_plot(summary, plot_path)
    print(f"Wrote {summary_path}")
    print(f"Wrote {plot_path}")


if __name__ == "__main__":
    main()
