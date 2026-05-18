# Multi-File Join Demo

This demo shows how TableLore should behave before joining multiple extracts. It uses tiny customer, order, and refund CSVs with deliberate data quality traps:

- duplicate customer keys
- an order with no customer match
- a refund with no order match

Run it from the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 demo/multifile-join/run_demo.py
```

Generated artifacts are written to `demo/multifile-join/output/`:

- `join_audit.md`: row counts, key checks, and join-risk interpretation
- `customer_revenue_summary.csv`: order-centered directional revenue summary
- `analysis_prompt.md`: copy/paste prompt for a TableLore-guided agent review

The lesson is that joins need an audit trail. A useful agent should explain grain, keys, orphan records, and join explosion risk before summarizing revenue.
