import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = REPO_ROOT / "demo" / "customer-churn" / "run_demo.py"


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
