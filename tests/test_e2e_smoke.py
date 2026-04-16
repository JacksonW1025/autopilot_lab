from __future__ import annotations

import json
from pathlib import Path

from linearity_study.linearity_run_study import run_study
from linearity_core.config import load_study_config
from tests.support import write_synthetic_config


ROOT = Path(__file__).resolve().parents[1]


def test_backendless_end_to_end_smoke(tmp_path: Path) -> None:
    config = load_study_config(write_synthetic_config(tmp_path, filename="base_config.json"))
    payload = config.to_dict()
    payload["repeat_count"] = 1
    payload["model"] = ["ols_affine"]
    payload["pooling_mode"] = "pooled"
    payload["ablation_plan"] = None
    payload["reporting"] = {"stability_repeats": 1}
    payload["synthetic"] = {"sample_count": 96, "noise_std": 0.02, "sparse_matrix_density": 0.18}
    config_path = tmp_path / "tiny_study.json"
    config_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    raw_dirs, study_dir = run_study(
        config_path,
        output_root=tmp_path / "studies",
        skip_analysis=False,
    )
    assert raw_dirs
    assert study_dir is not None
    assert study_dir.exists()
    assert (study_dir / "reports/summary.md").exists()
    assert (study_dir / "reports/baseline_stability.md").exists()
    assert (study_dir / "reports/diagnostic_gate.md").exists()
    assert (study_dir / "reports/matrix_gallery.md").exists()
    assert (study_dir / "reports/state_evolution_audit.md").exists()
    assert (study_dir / "reports/sparsity_overlap.md").exists()
    assert (study_dir / "summary/study_summary.json").exists()
    assert (study_dir / "summary/baseline_stability.json").exists()
    assert (study_dir / "summary/diagnostic_gate.json").exists()
    assert (study_dir / "summary/matrix_gallery.json").exists()
    assert (study_dir / "summary/state_evolution_audit.json").exists()
    assert (study_dir / "summary/sparsity_overlap.json").exists()
