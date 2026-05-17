import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tablelore" / "scripts" / "table_profile.py"
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "customer_churn_sample.csv"


def run_profile(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_profiles_csv_with_core_quality_warnings() -> None:
    result = run_profile(str(FIXTURE), "--target", "churned")

    assert result.returncode == 0, result.stderr
    output = result.stdout

    assert "# Table Profile" in output
    assert "Format: CSV" in output
    assert "File size:" in output
    assert "Rows: 8" in output
    assert "Columns: 9" in output
    assert "| region | object | 0 | 0.0% | 4 |" in output
    assert "monthly_spend" in output
    assert "Missing values found in: monthly_spend, churn_reason, leaky_cancel_date." in output
    assert "Duplicate rows: 1" in output
    assert "Candidate key: customer_id" not in output
    assert "Target distribution: churned" in output
    assert "Potential leakage candidates: churn_reason, leaky_cancel_date." in output
    assert "negative values" in output
    assert "C006: 2" not in output
    assert "2025-01-12: 2" not in output


def test_writes_profile_to_output_path(tmp_path: Path) -> None:
    output_path = tmp_path / "profile.md"

    result = run_profile(str(FIXTURE), "--target", "churned", "--output", str(output_path))

    assert result.returncode == 0, result.stderr
    assert output_path.exists()
    written = output_path.read_text(encoding="utf-8")
    assert "# Table Profile" in written
    assert "Target distribution: churned" in written
    assert str(output_path) in result.stdout


def test_rejects_missing_input() -> None:
    result = run_profile("tests/fixtures/does-not-exist.csv")

    assert result.returncode == 2
    assert "Input file not found" in result.stderr


def test_rejects_unsupported_extension() -> None:
    result = run_profile("PRD.md")

    assert result.returncode == 2
    assert "Unsupported file type" in result.stderr


def test_profiles_tsv_input(tmp_path: Path) -> None:
    tsv_path = tmp_path / "sample.tsv"
    tsv_path.write_text("account_id\tsegment\tamount\nA1\tcore\t10\nA2\texpansion\t20\n", encoding="utf-8")

    result = run_profile(str(tsv_path))

    assert result.returncode == 0, result.stderr
    assert "Format: TSV" in result.stdout
    assert "Rows: 2" in result.stdout
    assert "| amount | int64 | 0 | 0.0% | 2 |" in result.stdout


def test_header_only_file_does_not_report_candidate_keys() -> None:
    result = run_profile("tests/fixtures/empty_headers.csv")

    assert result.returncode == 0, result.stderr
    assert "Rows: 0" in result.stdout
    assert "Candidate key: none found" in result.stdout
    assert "Candidate key: customer_id" not in result.stdout


def test_markdown_table_cells_are_escaped(tmp_path: Path) -> None:
    csv_path = tmp_path / "pipes.csv"
    csv_path.write_text(
        "customer|id,segment,amount\nA|1,\"core\nsegment\",10\nB|2,expansion,20\n",
        encoding="utf-8",
    )

    result = run_profile(str(csv_path))

    assert result.returncode == 0, result.stderr
    assert "customer\\|id" in result.stdout
    assert "core segment" in result.stdout


def test_free_text_values_are_not_rendered_as_category_top_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "notes.csv"
    csv_path.write_text(
        "ticket_id,resolution_status,post_churn_note,churned_30d\n"
        "T1,resolved,,0\n"
        "T2,refund_processed,refund after churn,1\n",
        encoding="utf-8",
    )

    result = run_profile(str(csv_path), "--target", "churned_30d")

    assert result.returncode == 0, result.stderr
    assert "refund after churn" not in result.stdout
    assert "Potential leakage candidates: resolution_status, post_churn_note." in result.stdout
