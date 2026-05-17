#!/usr/bin/env python3
"""Generate a concise local profile for a CSV or TSV file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - exercised only without pandas
    raise SystemExit(
        "pandas is required for table_profile.py. Install it or run this helper in an "
        "environment where pandas is available."
    ) from exc


SUPPORTED_SUFFIXES = {".csv": ",", ".tsv": "\t"}
DATE_NAME_HINTS = ("date", "time", "timestamp", "_at")
LEAKAGE_NAME_HINTS = (
    "leak",
    "target",
    "label",
    "outcome",
    "status",
    "resolution",
    "cancel",
    "churn",
    "closed",
    "refund",
    "resolved",
    "future",
    "note",
)
FREE_TEXT_NAME_HINTS = ("note", "comment", "description", "message", "text")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile a local CSV or TSV file and emit a Markdown summary.",
    )
    parser.add_argument("input", type=Path, help="Path to a local CSV or TSV file.")
    parser.add_argument(
        "--target",
        help="Optional target column for label distribution and leakage checks.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path where the Markdown profile should be written.",
    )
    return parser.parse_args(list(argv))


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(f"Input file not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise ValueError(f"Unsupported file type: {suffix or '<none>'}. Supported: {supported}")

    return pd.read_csv(path, sep=SUPPORTED_SUFFIXES[suffix], keep_default_na=False, na_values=[""])


def as_percent(count: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{(count / total) * 100:.1f}%"


def markdown_cell(value: object) -> str:
    rendered = str(value)
    return rendered.replace("\n", " ").replace("|", "\\|")


def markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(markdown_cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(value) for value in row) + " |")
    return lines


def schema_rows(df: pd.DataFrame) -> list[list[object]]:
    rows = []
    for column in df.columns:
        missing = int(df[column].isna().sum())
        rows.append(
            [
                column,
                str(df[column].dtype),
                missing,
                as_percent(missing, len(df)),
                int(df[column].nunique(dropna=True)),
            ]
        )
    return rows


def numeric_rows(df: pd.DataFrame) -> list[list[object]]:
    rows = []
    numeric = df.select_dtypes(include="number")
    for column in numeric.columns:
        series = numeric[column].dropna()
        if series.empty:
            rows.append([column, "", "", "", ""])
            continue
        rows.append(
            [
                column,
                f"{series.min():.4g}",
                f"{series.median():.4g}",
                f"{series.mean():.4g}",
                f"{series.max():.4g}",
            ]
        )
    return rows


def likely_date_columns(df: pd.DataFrame) -> list[tuple[str, pd.Series]]:
    date_columns: list[tuple[str, pd.Series]] = []
    for column in df.columns:
        lowered = column.lower()
        if not any(hint in lowered for hint in DATE_NAME_HINTS):
            continue
        parsed = pd.to_datetime(df[column], errors="coerce")
        if parsed.notna().any():
            date_columns.append((column, parsed))
    return date_columns


def date_rows(df: pd.DataFrame) -> list[list[object]]:
    rows = []
    for column, parsed in likely_date_columns(df):
        valid = parsed.dropna()
        rows.append(
            [
                column,
                int(valid.count()),
                valid.min().date().isoformat() if not valid.empty else "",
                valid.max().date().isoformat() if not valid.empty else "",
            ]
        )
    return rows


def category_rows(df: pd.DataFrame) -> list[list[object]]:
    rows = []
    for column in df.select_dtypes(exclude="number").columns:
        lowered = column.lower()
        if "id" in lowered or any(hint in lowered for hint in DATE_NAME_HINTS):
            continue
        if any(hint in lowered for hint in FREE_TEXT_NAME_HINTS):
            continue
        distinct = int(df[column].nunique(dropna=True))
        if distinct == 0 or distinct > 20:
            continue
        top_values = df[column].value_counts(dropna=True).head(3)
        rendered = ", ".join(f"{value}: {count}" for value, count in top_values.items())
        rows.append([column, distinct, rendered])
    return rows


def candidate_keys(df: pd.DataFrame) -> list[str]:
    if len(df) == 0:
        return []
    return [
        column
        for column in df.columns
        if df[column].notna().all() and int(df[column].nunique(dropna=True)) == len(df)
    ]


def leakage_candidates(df: pd.DataFrame, target: str | None) -> list[str]:
    candidates = []
    for column in df.columns:
        lowered = column.lower()
        if target and column == target:
            continue
        if any(hint in lowered for hint in LEAKAGE_NAME_HINTS):
            candidates.append(column)
    return candidates


def warning_lines(df: pd.DataFrame, target: str | None) -> list[str]:
    warnings: list[str] = []

    missing_columns = [column for column in df.columns if df[column].isna().any()]
    if missing_columns:
        warnings.append(f"Missing values found in: {', '.join(missing_columns)}.")

    duplicate_rows = int(df.duplicated().sum())
    if duplicate_rows:
        warnings.append(f"Duplicate rows: {duplicate_rows}.")

    for column in df.select_dtypes(include="number").columns:
        negative_count = int((df[column] < 0).sum())
        if negative_count:
            warnings.append(f"{column} has {negative_count} negative values.")

    key_candidates = candidate_keys(df)
    if not key_candidates:
        warnings.append("No single-column candidate key found.")

    leaks = leakage_candidates(df, target)
    if leaks:
        warnings.append(f"Potential leakage candidates: {', '.join(leaks)}.")

    if target and target not in df.columns:
        warnings.append(f"Target column not found: {target}.")

    return warnings


def build_profile(path: Path, df: pd.DataFrame, target: str | None = None) -> str:
    file_format = path.suffix.lstrip(".").upper() or "UNKNOWN"
    file_size = path.stat().st_size if path.exists() else 0
    lines: list[str] = [
        "# Table Profile",
        "",
        f"Input: `{path}`",
        f"Format: {file_format}",
        f"File size: {file_size} bytes",
        f"Rows: {len(df)}",
        f"Columns: {len(df.columns)}",
        "",
        "## Schema",
        "",
        *markdown_table(
            ["column", "dtype", "missing", "missing_pct", "distinct"],
            schema_rows(df),
        ),
        "",
    ]

    numeric = numeric_rows(df)
    if numeric:
        lines.extend(
            [
                "## Numeric Summary",
                "",
                *markdown_table(["column", "min", "median", "mean", "max"], numeric),
                "",
            ]
        )

    dates = date_rows(df)
    if dates:
        lines.extend(
            [
                "## Date Ranges",
                "",
                *markdown_table(["column", "valid_values", "min", "max"], dates),
                "",
            ]
        )

    categories = category_rows(df)
    if categories:
        lines.extend(
            [
                "## Category Top Values",
                "",
                *markdown_table(["column", "distinct", "top_values"], categories),
                "",
            ]
        )

    duplicate_rows = int(df.duplicated().sum())
    lines.extend(["## Keys and Duplicates", "", f"Duplicate rows: {duplicate_rows}"])
    keys = candidate_keys(df)
    if keys:
        for key in keys:
            lines.append(f"Candidate key: {key}")
    else:
        lines.append("Candidate key: none found")
    lines.append("")

    if target:
        lines.extend([f"## Target distribution: {target}", ""])
        if target in df.columns:
            target_rows = [
                [value, count, as_percent(count, len(df))]
                for value, count in df[target].value_counts(dropna=False).items()
            ]
            lines.extend(markdown_table(["value", "count", "pct"], target_rows))
        else:
            lines.append(f"Target column not found: {target}")
        lines.append("")

    warnings = warning_lines(df, target)
    lines.extend(["## Warnings", ""])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- No obvious data quality warnings from this lightweight profile.")
    lines.extend(
        [
            "",
            "## Recommended Next Step",
            "",
            "Review the warnings and confirm the row grain, candidate keys, target definition, and split strategy before modeling or heavy transformation.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        df = read_table(args.input)
        profile = build_profile(args.input, df, target=args.target)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(profile, encoding="utf-8")
        print(f"Wrote profile to {args.output}")
    else:
        print(profile)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
