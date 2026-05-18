# Notebook Rescue Demo

This demo shows how TableLore should handle a messy exploratory notebook. The source notebook has hidden state, scratch cells, and a hard-coded filter. The demo turns that into durable analysis artifacts.

Run it from the repository root:

```bash
python3 -m pip install -r requirements-dev.txt
python3 demo/notebook-rescue/run_demo.py
```

Generated artifacts are written to `demo/notebook-rescue/output/`:

- `clean_revenue_analysis.py`: a reproducible script with explicit input and output paths
- `artifact_manifest.md`: a small map of source and generated files
- `rescue_report.md`: what changed, what hidden state was removed, and how to rerun

The lesson is that notebooks are useful for exploration, but TableLore should help convert important work into scripts and reports that another person can rerun.
