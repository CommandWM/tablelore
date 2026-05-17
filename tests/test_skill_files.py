from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "tablelore"


def test_skill_references_existing_files() -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert "name: tablelore" in content
    assert "description:" in content

    for reference in [
        "references/profiling-checklist.md",
        "references/engine-selection.md",
        "references/notebook-hygiene.md",
        "references/modeling-guardrails.md",
        "references/examples.md",
    ]:
        assert reference in content
        assert (SKILL_DIR / reference).exists()


def test_openai_metadata_names_tablelore_skill() -> None:
    metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert 'display_name: "TableLore"' in metadata
    assert "short_description:" in metadata
    assert 'icon_small: "./assets/tablelore-logo.png"' in metadata
    assert (SKILL_DIR / "assets" / "tablelore-logo.png").exists()
    assert 'default_prompt: "Use $tablelore' in metadata
