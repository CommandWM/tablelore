#!/usr/bin/env python3
"""Generate the TableLore customer-churn demo artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = REPO_ROOT / "tests" / "fixtures" / "customer_churn_sample.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "demo" / "customer-churn" / "output"

sys.path.insert(0, str(REPO_ROOT / "tablelore" / "scripts"))

from table_profile import build_profile, read_table  # noqa: E402


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def analysis_prompt(dataset: Path, profile_path: Path, target: str) -> str:
    return f"""Use $tablelore on this local customer-churn dataset.

Data:
- File: `{display_path(dataset)}`
- Target: `{target}`
- Existing profile: `{display_path(profile_path)}`

Please do a first-pass analysis readiness review:
1. Summarize the row grain, target distribution, and schema.
2. Call out data quality warnings that could affect analysis.
3. Identify likely leakage or post-outcome columns.
4. Recommend the next safe step before modeling.

Do not train a model yet. Keep the answer grounded in the profile and include reproducibility commands or artifact paths.
"""


def leakage_prompt(dataset: Path, target: str) -> str:
    return f"""Use $tablelore to check leakage before any churn model is trained.

Data:
- File: `{display_path(dataset)}`
- Target: `{target}`
- Prediction point: assume we want to predict churn before a cancellation or churn reason is known.

Please review column names, date columns, target timing, duplicate rows, and split strategy. Return:
- Columns to exclude or confirm.
- Questions still needed from the data owner.
- A safe baseline split recommendation.
"""


def next_steps_summary(dataset: Path, profile_path: Path, target: str) -> str:
    return f"""# TableLore Demo Summary

This demo shows the intended TableLore user flow:

1. Start with a local table, not a modeling request.
2. Generate a lightweight profile.
3. Ask the agent to interpret readiness, caveats, and leakage risk.
4. Only then decide whether modeling or deeper transformation is justified.

## Artifacts

- Dataset: `{display_path(dataset)}`
- Target: `{target}`
- Profile: `{display_path(profile_path)}`
- First-pass prompt: `analysis_prompt.md`
- Leakage prompt: `leakage_prompt.md`

## What To Notice

The fixture intentionally contains duplicate rows, missing values, negative spend, and likely leakage columns. A good TableLore-guided agent should notice those issues before making any claim about churn drivers.

## Next Command

```bash
cat {display_path(profile_path)}
```

Then paste `analysis_prompt.md` into Codex or another skill-aware agent session.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create TableLore customer-churn demo artifacts.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--target", default="churned")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset = args.dataset.resolve()
    output_dir = args.output_dir.resolve()
    profile_path = output_dir / "profile.md"

    dataframe = read_table(dataset)
    write_text(profile_path, build_profile(dataset, dataframe, target=args.target))
    write_text(output_dir / "analysis_prompt.md", analysis_prompt(dataset, profile_path, args.target))
    write_text(output_dir / "leakage_prompt.md", leakage_prompt(dataset, args.target))
    write_text(output_dir / "demo_summary.md", next_steps_summary(dataset, profile_path, args.target))

    print("TableLore demo artifacts written:")
    for path in [
        profile_path,
        output_dir / "analysis_prompt.md",
        output_dir / "leakage_prompt.md",
        output_dir / "demo_summary.md",
    ]:
        print(f"- {display_path(path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
