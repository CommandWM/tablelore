#!/usr/bin/env python3
"""Generate the TableLore modeling-readiness demo artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = REPO_ROOT / "tests" / "fixtures" / "customer_churn_sample.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "demo" / "modeling-readiness" / "output"
DEFAULT_TARGET = "churned"

sys.path.insert(0, str(REPO_ROOT / "tablelore" / "scripts"))

from table_profile import build_profile, candidate_keys, leakage_candidates, read_table  # noqa: E402


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def readiness_report(dataset: Path, profile_path: Path, target: str, output_dir: Path) -> str:
    frame = read_table(dataset)
    leaks = leakage_candidates(frame, target)
    keys = candidate_keys(frame)
    duplicate_rows = int(frame.duplicated().sum())
    target_counts = frame[target].value_counts(dropna=False).to_dict() if target in frame.columns else {}
    missing_columns = [column for column in frame.columns if frame[column].isna().any()]
    excluded_columns = [target, *leaks]
    remaining_columns = [column for column in frame.columns if column not in excluded_columns]

    status = "Blocked"
    return f"""# Modeling Readiness Report

Status: **{status}**

Dataset: `{display_path(dataset)}`
Profile: `{display_path(profile_path)}`
Target: `{target}`

## What We Know

- Rows: {len(frame)}
- Columns: {len(frame.columns)}
- Target distribution: {target_counts}
- Candidate keys: {", ".join(keys) if keys else "none found"}
- Duplicate rows: {duplicate_rows}
- Missing-value columns: {", ".join(missing_columns) if missing_columns else "none detected"}

## Why Modeling Is Blocked

Modeling is blocked until the data owner confirms target timing, leakage exclusions, and split strategy.

Columns that must be excluded or confirmed before any baseline:

{chr(10).join(f"- `{column}`" for column in leaks) if leaks else "- No obvious leakage columns from lightweight name checks."}

## Remaining Columns For Review After Exclusions

{chr(10).join(f"- `{column}`" for column in remaining_columns) if remaining_columns else "- No remaining columns identified."}

## Recommended Baseline Plan

1. Confirm one row represents one customer at one observation point.
2. Remove `churn_reason` and `leaky_cancel_date` unless the data owner proves they are known before prediction.
3. Resolve duplicate rows before splitting.
4. Prefer a time-aware split using `last_seen_date` after the prediction point is defined.
5. Train only a simple baseline first, and report it as exploratory.

## Generated Artifacts

- Profile: `{display_path(profile_path)}`
- Baseline prompt: `{display_path(output_dir / "baseline_prompt.md")}`
"""


def baseline_prompt(dataset: Path, profile_path: Path, readiness_path: Path, target: str) -> str:
    return f"""Use $tablelore to prepare a conservative churn baseline plan.

Data:
- Dataset: `{display_path(dataset)}`
- Profile: `{display_path(profile_path)}`
- Modeling readiness report: `{display_path(readiness_path)}`
- Target: `{target}`

Do not train a model yet. First confirm:
1. Prediction point and target timing.
2. Whether `churn_reason` and `leaky_cancel_date` are post-outcome leakage.
3. How duplicate rows should be resolved.
4. Whether a time-aware split using `last_seen_date` is appropriate.

Return the smallest safe baseline plan and the exact columns to exclude before training.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create TableLore modeling-readiness demo artifacts.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--target", default=DEFAULT_TARGET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset = args.dataset.resolve()
    output_dir = args.output_dir.resolve()
    profile_path = output_dir / "profile.md"
    readiness_path = output_dir / "modeling_readiness_report.md"
    prompt_path = output_dir / "baseline_prompt.md"

    frame = read_table(dataset)
    write_text(profile_path, build_profile(dataset, frame, target=args.target))
    write_text(readiness_path, readiness_report(dataset, profile_path, args.target, output_dir))
    write_text(prompt_path, baseline_prompt(dataset, profile_path, readiness_path, args.target))

    print("TableLore modeling-readiness demo artifacts written:")
    for path in [profile_path, readiness_path, prompt_path]:
        print(f"- {display_path(path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
