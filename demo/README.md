# TableLore Demo Suite

The demos are small, runnable product examples. Each one is built to show a behavior TableLore should make normal in agent-assisted data work.

## 1. Customer Churn

Path: `demo/customer-churn/`

Teaches the first 15 minutes of TableLore: profile a messy table, inspect target distribution, identify data quality warnings, and ask a safer follow-up prompt.

```bash
python3 demo/customer-churn/run_demo.py
```

## 2. Multi-File Join

Path: `demo/multifile-join/`

Teaches join hygiene: inspect file grains, check duplicate keys, find orphan records, and explain join explosion risk before summarizing revenue.

```bash
python3 demo/multifile-join/run_demo.py
```

## 3. Notebook Rescue

Path: `demo/notebook-rescue/`

Teaches reproducibility: turn a messy exploratory notebook into a clean script, an artifact manifest, and a report that explains hidden state.

```bash
python3 demo/notebook-rescue/run_demo.py
```

## 4. Modeling Readiness

Path: `demo/modeling-readiness/`

Teaches restraint before modeling: block unsafe baseline training until target timing, leakage columns, duplicate rows, and split strategy are explicit.

```bash
python3 demo/modeling-readiness/run_demo.py
```

## Suggested User Path

Run the demos in this order:

1. Customer churn for basic profiling behavior.
2. Multi-file join for relational analysis and DuckDB-style audit trails.
3. Notebook rescue for making exploratory work durable.
4. Modeling readiness for turning profile findings into safe baseline planning.

Generated outputs live under each demo's `output/` folder and are ignored by git so the demos can be rerun freely.
