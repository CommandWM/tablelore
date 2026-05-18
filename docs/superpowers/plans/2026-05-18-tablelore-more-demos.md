# TableLore More Demos Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three runnable demos that make TableLore feel real for join auditing, notebook rescue, and modeling readiness.

**Architecture:** Each demo lives under `demo/<name>/` with a README, static tiny fixture data where useful, a `run_demo.py` script, and generated outputs written to ignored `output/` folders. Tests call each script with a temporary output directory and assert the key artifacts and safety messages exist.

**Tech Stack:** Python 3.11+, Pandas for local table profiling/analysis, DuckDB for the multi-file join demo, stdlib JSON for notebook rescue, pytest for executable coverage.

---

### Task 1: Demo Coverage Tests

**Files:**
- Modify: `tests/test_demo_flow.py`
- Modify: `.gitignore`

- [ ] **Step 1: Add tests before implementation**

Add tests that run these commands with temporary output directories:

```bash
python3 demo/multifile-join/run_demo.py --output-dir <tmp>
python3 demo/notebook-rescue/run_demo.py --output-dir <tmp>
python3 demo/modeling-readiness/run_demo.py --output-dir <tmp>
```

Each test asserts that the script exits successfully and writes the expected report, prompt, or cleaned artifact.

- [ ] **Step 2: Verify tests fail**

Run:

```bash
python3 -m pytest tests/test_demo_flow.py -q
```

Expected: failures because the new demo scripts do not exist yet.

### Task 2: Multi-File Join Demo

**Files:**
- Create: `demo/multifile-join/README.md`
- Create: `demo/multifile-join/run_demo.py`
- Create: `demo/multifile-join/data/customers.csv`
- Create: `demo/multifile-join/data/orders.csv`
- Create: `demo/multifile-join/data/refunds.csv`
- Modify: `requirements-dev.txt`

- [ ] **Step 1: Add tiny fixture data**

Use small CSV files with duplicate customer rows, an orphan order, and an orphan refund so the join audit has real warnings.

- [ ] **Step 2: Implement script**

Use DuckDB to read the CSVs, write a Markdown join audit report, write a revenue summary CSV, and write an agent prompt for follow-up analysis.

- [ ] **Step 3: Verify**

Run:

```bash
python3 demo/multifile-join/run_demo.py
python3 -m pytest tests/test_demo_flow.py -q
```

### Task 3: Notebook Rescue Demo

**Files:**
- Create: `demo/notebook-rescue/README.md`
- Create: `demo/notebook-rescue/run_demo.py`
- Create: `demo/notebook-rescue/messy_revenue_exploration.ipynb`
- Create: `demo/notebook-rescue/data/monthly_revenue.csv`

- [ ] **Step 1: Add messy notebook fixture**

The notebook should include hidden assumptions, scratch variables, and display-only exploration cells so the demo has something to rescue.

- [ ] **Step 2: Implement script**

Generate a cleaned analysis script, an artifact manifest, and a rescue report that explains what changed and how to rerun.

- [ ] **Step 3: Verify**

Run:

```bash
python3 demo/notebook-rescue/run_demo.py
python3 -m pytest tests/test_demo_flow.py -q
```

### Task 4: Modeling Readiness Demo

**Files:**
- Create: `demo/modeling-readiness/README.md`
- Create: `demo/modeling-readiness/run_demo.py`

- [ ] **Step 1: Reuse customer churn fixture**

Use `tests/fixtures/customer_churn_sample.csv` and the existing `table_profile.py` helpers to keep this demo grounded in real repo behavior.

- [ ] **Step 2: Implement script**

Write a profile, a modeling-readiness report, and a baseline prompt. The report must state that modeling is blocked until leakage columns and split strategy are confirmed.

- [ ] **Step 3: Verify**

Run:

```bash
python3 demo/modeling-readiness/run_demo.py
python3 -m pytest tests/test_demo_flow.py -q
```

### Task 5: Demo Index And README

**Files:**
- Create: `demo/README.md`
- Modify: `docs/demo-flow.md`
- Modify: `README.md`

- [ ] **Step 1: Add demo index**

List the four demo flows and what each teaches.

- [ ] **Step 2: Update top-level docs**

Link the demo index from the README and make `docs/demo-flow.md` point to the expanded demo suite.

- [ ] **Step 3: Verify full checks**

Run:

```bash
python3 -m pytest tests -q
python3 demo/customer-churn/run_demo.py --output-dir /tmp/tablelore-customer-demo
python3 demo/multifile-join/run_demo.py --output-dir /tmp/tablelore-join-demo
python3 demo/notebook-rescue/run_demo.py --output-dir /tmp/tablelore-notebook-demo
python3 demo/modeling-readiness/run_demo.py --output-dir /tmp/tablelore-modeling-demo
python3 dogfood/com47/run_dogfood.py
python3 /Users/matthewdavis/.codex/skills/.system/skill-creator/scripts/quick_validate.py tablelore
git diff --check
```

Expected: all commands pass.
