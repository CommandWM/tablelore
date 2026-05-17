# Multi-File Inspection

Question: inspect local customer and order extracts before summarizing cohort revenue.

Data inventory:
- `customers.parquet`: 5 rows x 4 columns.
- `orders_q1.parquet`: 4 rows.
- `orders_q2.parquet`: 3 rows.

Engine choice:
- DuckDB would be the preferred engine for a larger real extract because this is SQL-style aggregation over multiple Parquet files.
- This dogfood run used Pandas with PyArrow because the repo intentionally avoids adding DuckDB as a v1 runtime dependency.

Join checks:
- Join key: `customer_id`.
- Expected relationship: many orders to one customer.
- Order rows before join: 7.
- Rows after left join: 7.
- Duplicate order IDs: 0.
- Unmatched order rows: 1.

Warnings:
- One order references `A-006`, which is not present in `customers.parquet`; downstream cohort reporting should treat that row as unmatched until the extract is corrected.

Recommended next step:
- Use a rerunnable script for the cohort summary so join assumptions, unmatched counts, and outputs are reproducible.
