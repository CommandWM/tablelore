# TableLore v0.1 Skill Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the TableLore v0.1 skill foundation from the PRD so agents reliably inspect, profile, choose tools deliberately, and report caveats before deeper data analysis.

**Architecture:** TableLore should ship as a concise skill with detailed guidance split into reference files. `SKILL.md` owns activation, workflow order, and guardrails; `references/` owns the detailed checklists; README/license work makes the repo shareable without pulling CLI packaging into v1.

**Tech Stack:** Markdown skill files, Codex/Claude-compatible skill conventions, shell verification, Linear project `TableLore - Data Analysis Hygiene Skill`.

---

## Linear Roadmap

Project: https://linear.app/commandwm/project/tablelore-data-analysis-hygiene-skill-6dd44ccc3bae

Project document: https://linear.app/commandwm/document/roadmap-and-agent-execution-map-345534a5a4d1

### v0.1 Skill Foundation

- COM-38 Create TableLore skill skeleton
- COM-39 Add profiling checklist reference
- COM-40 Add engine selection reference
- COM-41 Add notebook and script hygiene reference
- COM-42 Add modeling guardrails reference
- COM-43 Decide license and compatibility target

### v0.2 Profiling Helper

- COM-44 Implement optional local profiling helper
- COM-45 Add tests and fixtures for the profiling helper
- COM-46 Add example prompts and expected outputs

### v1.0 Release Readiness

- COM-47 Dogfood TableLore on representative analysis tasks
- COM-48 Verify Codex and Claude skill packaging
- COM-49 Polish README and release notes for v1
- COM-50 Prepare v1 release checklist

### v2 Backlog

- COM-51 Plan `tablelore profile` CLI
- COM-52 Evaluate validation templates and HTML profile report
- COM-53 Add specialized analysis checklist backlog

## File Structure

- Create: `tablelore/SKILL.md`
  - Owns trigger metadata, the default workflow, reference-loading rules, privacy posture, and final-report expectations.
- Create: `tablelore/references/profiling-checklist.md`
  - Owns the required initial profile pass.
- Create: `tablelore/references/engine-selection.md`
  - Owns DuckDB, Polars, Pandas, notebook/script, and plotting selection rules.
- Create: `tablelore/references/notebook-hygiene.md`
  - Owns artifact standards for exploratory notebooks and rerunnable scripts.
- Create: `tablelore/references/modeling-guardrails.md`
  - Owns the pre-modeling checklist.
- Modify: `README.md`
  - Replace PRD-only status once v0.1 files exist.
- Create: `LICENSE`
  - Add the chosen license after COM-43 is decided.

## Suggested First Sub-Agent Split

- Worker 1 owns COM-38 and writes `tablelore/SKILL.md`.
- Worker 2 owns COM-39 and writes `tablelore/references/profiling-checklist.md`.
- Worker 3 owns COM-40 and COM-41 and writes the engine and artifact hygiene references.
- Worker 4 owns COM-42 and writes `tablelore/references/modeling-guardrails.md`.

Run a review pass before COM-43 and before any helper script work. COM-44 should wait because the PRD explicitly says the written skill matters more than the helper script.

### Task 1: Create Skill Skeleton

**Files:**
- Create: `tablelore/SKILL.md`
- Create: `tablelore/references/.gitkeep`

- [ ] **Step 1: Create the feature branch**

Run:

```bash
git switch -c codex/com-38-tablelore-skill-skeleton
```

Expected: branch switches cleanly from `main`.

- [ ] **Step 2: Create the skill directories**

Run:

```bash
mkdir -p tablelore/references
touch tablelore/references/.gitkeep
```

Expected: `tablelore/` and `tablelore/references/` exist.

- [ ] **Step 3: Write the initial `SKILL.md`**

Use this as the first complete draft:

```markdown
---
name: tablelore
description: Use when analyzing, profiling, transforming, visualizing, modeling, validating, or reporting on local datasets such as CSV, TSV, Parquet, JSON, JSONL, Excel, SQLite, DuckDB, database extracts, or existing project data loaders.
---

# TableLore

TableLore is practical data analysis hygiene for AI agents.

## Core Principle

Inspect before transform. Profile before model. Explain uncertainty.

## Default Workflow

1. Orient on the repo, existing docs, notebooks, schemas, scripts, and data-loading conventions before creating new analysis.
2. Discover local data assets and database extracts without uploading private data.
3. Profile the data before modeling or heavy transformation unless the user explicitly asks to skip profiling.
4. Choose DuckDB, Polars, Pandas, notebooks, scripts, and plotting libraries based on task constraints and project conventions.
5. Analyze with explicit assumptions, simple baselines before advanced models, and named transformations.
6. Report the question answered, data used, method, findings, caveats, data quality risks, reproducibility instructions, and output paths.

## Reference Loading

- For profiling requirements, read `references/profiling-checklist.md`.
- For DuckDB, Polars, Pandas, notebook/script, and plotting selection, read `references/engine-selection.md`.
- For notebook and script standards, read `references/notebook-hygiene.md`.
- For modeling requests, read `references/modeling-guardrails.md` before training or evaluating models.

## Privacy and Safety

Default to local execution. Prefer metadata, schemas, aggregates, and small safe samples over raw data dumps. Ask before using external services or uploading data.

## Final Response Expectations

Every finished analysis should include the question answered, data used, method, key findings, caveats, reproducibility instructions, and paths to generated notebooks, scripts, charts, reports, or outputs.
```

- [ ] **Step 4: Verify the skeleton exists**

Run:

```bash
test -f tablelore/SKILL.md
test -d tablelore/references
rg -n "Inspect before transform|Profile before model|references/" tablelore/SKILL.md
```

Expected: all commands exit 0 and `rg` finds the core principle plus reference links.

- [ ] **Step 5: Commit COM-38**

Run:

```bash
git add tablelore/SKILL.md tablelore/references/.gitkeep
git commit -m "feat: add TableLore skill skeleton"
```

### Task 2: Add Profiling Checklist

**Files:**
- Create: `tablelore/references/profiling-checklist.md`

- [ ] **Step 1: Write `profiling-checklist.md`**

The document must include these sections in this order:

```markdown
# Profiling Checklist

Use this checklist before modeling or heavy transformation unless the user explicitly asks to skip profiling.

## 1. Data Inventory

- List available files, tables, extracts, loaders, and relevant repo docs.
- Record file format, file size, row count, and column count.
- Prefer schema, aggregates, and small safe samples over raw row dumps.

## 2. Schema and Types

- Capture column names and inferred types.
- Flag mixed types, unexpected strings in numeric columns, and date parsing ambiguity.
- Note units, identifiers, timestamps, labels, and target-like columns.

## 3. Missingness and Distinct Counts

- Count nulls and null percentages by column.
- Count distinct values for identifiers, categories, and target-like columns.
- Flag all-null, near-constant, and high-cardinality columns.

## 4. Numeric and Date Ranges

- Summarize numeric min, max, mean, median, and suspicious values.
- Summarize date/time min, max, gaps, and timezone clues.
- Flag impossible values, sentinel values, and outlier ranges.

## 5. Grain, Keys, and Duplicates

- State what one row appears to represent.
- Identify candidate primary keys and join keys.
- Check duplicate rows and duplicate entity keys.
- Warn about possible join explosions before joining tables.

## 6. Target and Leakage Scan

- If a target is specified, summarize label distribution and imbalance.
- Identify columns that may leak the target or future information.
- Identify whether time, group, or entity leakage affects split strategy.

## 7. Warnings and Next Step

- List data quality risks as warnings.
- State assumptions that need user or domain confirmation.
- Recommend the next analysis step only after the profile is complete.
```

- [ ] **Step 2: Verify checklist coverage**

Run:

```bash
rg -n "Data Inventory|Schema and Types|Missingness|Grain|Target and Leakage|Warnings" tablelore/references/profiling-checklist.md
```

Expected: every required section is present.

- [ ] **Step 3: Commit COM-39**

Run:

```bash
git add tablelore/references/profiling-checklist.md
git commit -m "docs: add TableLore profiling checklist"
```

### Task 3: Add Engine Selection and Artifact Hygiene References

**Files:**
- Create: `tablelore/references/engine-selection.md`
- Create: `tablelore/references/notebook-hygiene.md`

- [ ] **Step 1: Write `engine-selection.md`**

Required sections:

```markdown
# Engine Selection

Prefer existing project conventions when they are clear. When conventions are absent, choose the smallest tool that makes the analysis reproducible and understandable.

## DuckDB

Use DuckDB for SQL over CSV or Parquet, multi-file joins, large analytical scans, and aggregation-heavy work.

## Polars

Use Polars for fast local dataframe transformations, lazy pipelines, Parquet/CSV workflows, and typed transformation logic.

## Pandas

Use Pandas when existing project code uses Pandas, a required library expects Pandas, or the dataset is small enough that compatibility matters more than speed.

## Notebooks

Use notebooks when the deliverable is exploratory reasoning, charts, or a narrative analysis.

## Scripts

Use scripts when the deliverable should be rerunnable, reviewed, scheduled, tested, or committed as project logic.

## Plotting Libraries

Use plots to answer specific questions. Prefer simple, interpretable visualizations before complex ones. Use Matplotlib or Seaborn for static exploratory charts, Plotly for interactive inspection, and Altair when declarative charting fits the project.
```

- [ ] **Step 2: Write `notebook-hygiene.md`**

Required sections:

```markdown
# Notebook and Script Hygiene

Keep exploratory and production work separate. Choose the artifact based on what the user needs to reuse.

## Notebook Standard

A clean notebook should contain:

- Question
- Setup
- Profile
- Analysis
- Findings
- Caveats
- Reproducibility instructions

## Script Standard

A clean script should:

- Expose functions.
- Avoid hidden global state.
- Accept input and output paths.
- Use explicit transformations.
- Be runnable from the command line when useful.
- Save outputs under the repo's existing convention, or under `analysis/`, `reports/`, or `outputs/`.

## Plot Standard

Every saved plot should have a readable title, labeled axes, clear units, and a reason to exist. Avoid decorative charts.

## Final Artifact Notes

Record generated paths and commands needed to rerun the work.
```

- [ ] **Step 3: Verify reference coverage**

Run:

```bash
rg -n "DuckDB|Polars|Pandas|Notebooks|Scripts|Plotting" tablelore/references/engine-selection.md
rg -n "Notebook Standard|Script Standard|Plot Standard|Final Artifact Notes" tablelore/references/notebook-hygiene.md
```

Expected: every required section is present.

- [ ] **Step 4: Commit COM-40 and COM-41**

Run:

```bash
git add tablelore/references/engine-selection.md tablelore/references/notebook-hygiene.md
git commit -m "docs: add engine and artifact hygiene guidance"
```

### Task 4: Add Modeling Guardrails

**Files:**
- Create: `tablelore/references/modeling-guardrails.md`

- [ ] **Step 1: Write `modeling-guardrails.md`**

Required content:

```markdown
# Modeling Guardrails

Use this checklist before training, evaluating, or comparing models unless the user explicitly asks to skip it.

## Target Definition

- State the prediction target.
- State whether the target is observed, derived, delayed, or user-provided.
- Confirm the target is available at the time a prediction would be made.

## Observation Grain

- State what one row represents.
- Identify entity, timestamp, and grouping columns.
- Confirm whether multiple rows per entity create leakage risk.

## Label Distribution

- Summarize target counts, rates, class balance, and missing labels.
- Flag rare classes and target values that require special metrics or sampling.

## Leakage Candidates

- Identify future-looking columns, post-outcome fields, duplicate identifiers, aggregate features, and timestamps that could reveal the target.

## Split Strategy

- Choose time, group, stratified, or random splitting based on the data and decision problem.
- Explain why the split matches the prediction scenario.

## Baseline and Metrics

- Establish a simple baseline before advanced models.
- Pick metrics that match the decision problem and class balance.
- Report uncertainty and caveats with results.
```

- [ ] **Step 2: Verify modeling guardrail coverage**

Run:

```bash
rg -n "Target Definition|Observation Grain|Label Distribution|Leakage Candidates|Split Strategy|Baseline and Metrics" tablelore/references/modeling-guardrails.md
```

Expected: every required section is present.

- [ ] **Step 3: Commit COM-42**

Run:

```bash
git add tablelore/references/modeling-guardrails.md
git commit -m "docs: add modeling guardrails"
```

### Task 5: Resolve License and Compatibility Target

**Files:**
- Modify: `README.md`
- Create: `LICENSE`

- [ ] **Step 1: Decide license**

Default recommendation: MIT, because TableLore is a small reusable skill and the repo is intended to be shareable. If a different license is needed, choose it before editing.

- [ ] **Step 2: Update README**

Replace the PRD-only status with a v0.1 status once the skill files exist:

```markdown
## Status

v0.1 skill foundation in progress. TableLore currently targets Codex-compatible skill usage first, with Claude-compatible wording kept in mind where it does not complicate the repo.
```

- [ ] **Step 3: Add license**

If MIT is selected, add the standard MIT license text with the current year and copyright holder.

- [ ] **Step 4: Verify no TBD status remains**

Run:

```bash
rg -n "TBD|TODO|implement later|fill in details" README.md tablelore LICENSE
git diff --check
```

Expected: no placeholder wording remains except any intentional PRD open questions, and `git diff --check` passes.

- [ ] **Step 5: Commit COM-43**

Run:

```bash
git add README.md LICENSE
git commit -m "docs: clarify TableLore status and license"
```

### Task 6: Final Verification and Linear Update

**Files:**
- Verify all files touched above.
- Update Linear issues COM-38 through COM-43.

- [ ] **Step 1: Run final local verification**

Run:

```bash
test -f tablelore/SKILL.md
test -f tablelore/references/profiling-checklist.md
test -f tablelore/references/engine-selection.md
test -f tablelore/references/notebook-hygiene.md
test -f tablelore/references/modeling-guardrails.md
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 2: Review the combined diff**

Run:

```bash
git log --oneline --max-count=6
git status --short
```

Expected: the recent commits map to COM-38 through COM-43, and the worktree is clean.

- [ ] **Step 3: Update Linear**

Mark COM-38 through COM-43 Done after the branch is reviewed and merged. Leave COM-44 in Backlog until the written workflow has been reviewed.

## Review Checklist

- `SKILL.md` is concise and delegates detail to references.
- Profiling is required before modeling unless explicitly skipped.
- Engine selection explains tradeoffs and respects local project conventions.
- Notebook/script guidance keeps exploration and production logic separate.
- Modeling guardrails cover target, grain, leakage, split strategy, baseline, and metrics.
- README is no longer PRD-only.
- v1 scope does not include full CLI packaging, hosted services, AutoML, or database credential management.
