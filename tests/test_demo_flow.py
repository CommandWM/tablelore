import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = REPO_ROOT / "demo" / "customer-churn" / "run_demo.py"
MULTIFILE_JOIN_SCRIPT = REPO_ROOT / "demo" / "multifile-join" / "run_demo.py"
NOTEBOOK_RESCUE_SCRIPT = REPO_ROOT / "demo" / "notebook-rescue" / "run_demo.py"
MODELING_READINESS_SCRIPT = REPO_ROOT / "demo" / "modeling-readiness" / "run_demo.py"


def test_customer_churn_demo_writes_expected_artifacts(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(DEMO_SCRIPT),
            "--output-dir",
            str(tmp_path),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stderr

    profile = tmp_path / "profile.md"
    analysis_prompt = tmp_path / "analysis_prompt.md"
    leakage_prompt = tmp_path / "leakage_prompt.md"
    summary = tmp_path / "demo_summary.md"

    for artifact in [profile, analysis_prompt, leakage_prompt, summary]:
        assert artifact.exists()
        assert str(artifact) in result.stdout

    profile_text = profile.read_text(encoding="utf-8")
    assert "Rows: 8" in profile_text
    assert "Potential leakage candidates: churn_reason, leaky_cancel_date." in profile_text

    analysis_text = analysis_prompt.read_text(encoding="utf-8")
    assert "Use $tablelore" in analysis_text
    assert "Do not train a model yet" in analysis_text

    leakage_text = leakage_prompt.read_text(encoding="utf-8")
    assert "Prediction point" in leakage_text
    assert "split strategy" in leakage_text


def run_demo(script: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(script),
            "--output-dir",
            str(output_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_multifile_join_demo_writes_join_audit(tmp_path: Path) -> None:
    result = run_demo(MULTIFILE_JOIN_SCRIPT, tmp_path)

    assert result.returncode == 0, result.stderr

    join_audit = tmp_path / "join_audit.md"
    revenue_summary = tmp_path / "customer_revenue_summary.csv"
    prompt = tmp_path / "analysis_prompt.md"

    for artifact in [join_audit, revenue_summary, prompt]:
        assert artifact.exists()
        assert str(artifact) in result.stdout

    audit_text = join_audit.read_text(encoding="utf-8")
    assert "Join Audit" in audit_text
    assert "duplicate customer keys" in audit_text
    assert "orphan orders" in audit_text
    assert "orphan refunds" in audit_text

    prompt_text = prompt.read_text(encoding="utf-8")
    assert "Use $tablelore" in prompt_text
    assert "join explosion" in prompt_text


def test_notebook_rescue_demo_writes_clean_artifacts(tmp_path: Path) -> None:
    result = run_demo(NOTEBOOK_RESCUE_SCRIPT, tmp_path)

    assert result.returncode == 0, result.stderr

    cleaned_script = tmp_path / "clean_revenue_analysis.py"
    manifest = tmp_path / "artifact_manifest.md"
    report = tmp_path / "rescue_report.md"

    for artifact in [cleaned_script, manifest, report]:
        assert artifact.exists()
        assert str(artifact) in result.stdout

    script_text = cleaned_script.read_text(encoding="utf-8")
    assert "def load_revenue" in script_text
    assert "if __name__ == \"__main__\"" in script_text

    report_text = report.read_text(encoding="utf-8")
    assert "Notebook Rescue Report" in report_text
    assert "hidden state" in report_text
    assert "reproducible script" in report_text


def test_modeling_readiness_demo_blocks_unsafe_modeling(tmp_path: Path) -> None:
    result = run_demo(MODELING_READINESS_SCRIPT, tmp_path)

    assert result.returncode == 0, result.stderr

    profile = tmp_path / "profile.md"
    readiness_report = tmp_path / "modeling_readiness_report.md"
    prompt = tmp_path / "baseline_prompt.md"

    for artifact in [profile, readiness_report, prompt]:
        assert artifact.exists()
        assert str(artifact) in result.stdout

    report_text = readiness_report.read_text(encoding="utf-8")
    assert "Modeling Readiness Report" in report_text
    assert "Blocked" in report_text
    assert "churn_reason" in report_text
    assert "leaky_cancel_date" in report_text

    prompt_text = prompt.read_text(encoding="utf-8")
    assert "Use $tablelore" in prompt_text
    assert "Do not train" in prompt_text
