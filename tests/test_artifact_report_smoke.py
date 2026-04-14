from __future__ import annotations

import json
from pathlib import Path

from linearity_analysis.linearity_analyze import run_analysis
from linearity_core.config import load_study_config
from linearity_core.synthetic import generate_synthetic_raw_runs
from tests.support import write_synthetic_config


ROOT = Path(__file__).resolve().parents[1]


def test_artifact_and_report_generation_smoke(tmp_path: Path) -> None:
    config = load_study_config(write_synthetic_config(tmp_path, filename="base_config.json"))
    payload = config.to_dict()
    payload["repeat_count"] = 1
    payload["model"] = ["ols_affine"]
    payload["pooling_mode"] = "pooled"
    payload["ablation_plan"] = None
    payload["reporting"] = {"stability_repeats": 1}
    payload["synthetic"] = {"sample_count": 96, "noise_std": 0.02, "sparse_matrix_density": 0.18}
    tiny_config_path = tmp_path / "tiny_config.json"
    tiny_config_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    config = load_study_config(tiny_config_path)
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path / "raw")
    study_dir = run_analysis(run_dirs, config, output_root=tmp_path / "studies")

    assert (study_dir / "prepared/sample_table.csv").exists()
    assert (study_dir / "prepared/schema_inventory.yaml").exists()
    assert (study_dir / "reports/summary.md").exists()
    assert (study_dir / "reports/schema_comparison.md").exists()
    assert (study_dir / "reports/baseline_stability.md").exists()
    assert (study_dir / "reports/diagnostic_gate.md").exists()
    assert (study_dir / "reports/matrix_gallery.md").exists()
    assert (study_dir / "reports/state_evolution_audit.md").exists()
    assert (study_dir / "reports/scenario_holdout.md").exists()
    assert (study_dir / "reports/sparsity_overlap.md").exists()
    assert (study_dir / "summary/study_summary.json").exists()
    assert (study_dir / "summary/baseline_stability.json").exists()
    assert (study_dir / "summary/diagnostic_gate.json").exists()
    assert (study_dir / "summary/matrix_gallery.json").exists()
    assert (study_dir / "summary/state_evolution_audit.json").exists()
    assert (study_dir / "summary/scenario_holdout.json").exists()
    assert (study_dir / "summary/sparsity_overlap.json").exists()
    assert list((study_dir / "fits").rglob("matrix_f.csv"))
    assert list((study_dir / "fits").rglob("bias_b.csv"))
    assert list((study_dir / "fits").rglob("sparsity_mask.csv"))
    assert list((study_dir / "fits").rglob("metrics.json"))
    gallery_payload = json.loads((study_dir / "summary/matrix_gallery.json").read_text(encoding="utf-8"))
    if gallery_payload["status"] == "gallery_available":
        assert list((study_dir / "fits").rglob("matrix_heatmap_abs.png"))
        assert list((study_dir / "fits").rglob("matrix_heatmap_signed.png"))
    else:
        assert gallery_payload["status"] == "no_supported_results"
