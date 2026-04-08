from __future__ import annotations

import json
from pathlib import Path

from linearity_analysis.linearity_analyze import run_analysis
from linearity_core.config import load_study_config
from linearity_core.io import read_yaml, write_yaml
from linearity_core.research_contract import apply_manifest_research_contract, build_acceptance_block, unavailable_acceptance_block
from linearity_core.synthetic import generate_synthetic_raw_runs


ROOT = Path(__file__).resolve().parents[1]


def _tiny_synthetic_config(tmp_path: Path):
    config = load_study_config(ROOT / "configs/studies/global_linear_commands_plus_state__delta_state.yaml")
    payload = config.to_dict()
    payload["repeat_count"] = 3
    payload["model"] = ["ols_affine"]
    payload["pooling_mode"] = "pooled"
    payload["ablation_plan"] = None
    payload["reporting"] = {"stability_repeats": 1}
    payload["synthetic"] = {"sample_count": 96, "noise_std": 0.02, "sparse_matrix_density": 0.18}
    config_path = tmp_path / "tiny_synthetic.json"
    config_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return load_study_config(config_path)


def test_manifest_research_contract_sets_required_fields() -> None:
    accepted = build_acceptance_block(
        experiment_started=True,
        active_phase_present=True,
        expected_active_samples=24,
        active_sample_count=24,
        active_nonzero_command_samples=24,
        failsafe_during_experiment=False,
        missing_topics_blocking=[],
        accepted=True,
        rejection_reasons=[],
    )
    payload = apply_manifest_research_contract(
        {"run_id": "px4_run", "backend": "px4", "status": "completed", "data_quality": {"topic_presence": {}}},
        research_tier="authoritative_research",
        acceptance=accepted,
    )
    assert payload["raw_schema_version"] == 2
    assert payload["research_acceptance"] == "accepted"
    assert payload["research_rejection_reasons"] == []
    assert payload["research_tier"] == "authoritative_research"
    assert payload["data_quality"]["acceptance"]["accepted"] is True

    unavailable = unavailable_acceptance_block()
    ardupilot_payload = apply_manifest_research_contract(
        {"run_id": "ardu_run", "backend": "ardupilot", "status": "completed"},
        research_tier="diagnostic_research",
        acceptance=unavailable,
    )
    assert ardupilot_payload["research_acceptance"] == "rejected"
    assert ardupilot_payload["research_rejection_reasons"] == ["acceptance_unavailable"]
    assert ardupilot_payload["research_tier"] == "diagnostic_research"
    assert ardupilot_payload["data_quality"]["acceptance"]["experiment_started"] is None


def test_analysis_filters_rejected_and_legacy_runs_by_default(tmp_path: Path) -> None:
    config = _tiny_synthetic_config(tmp_path)
    run_dirs = generate_synthetic_raw_runs(config, output_root=tmp_path / "raw")

    accepted_manifest = read_yaml(run_dirs[0] / "manifest.yaml")
    rejected_manifest = read_yaml(run_dirs[1] / "manifest.yaml")
    rejected_manifest["research_acceptance"] = "rejected"
    rejected_manifest["research_rejection_reasons"] = ["failsafe_during_experiment"]
    rejected_manifest["data_quality"]["acceptance"]["accepted"] = False
    rejected_manifest["data_quality"]["acceptance"]["rejection_reasons"] = ["failsafe_during_experiment"]
    write_yaml(run_dirs[1] / "manifest.yaml", rejected_manifest)

    legacy_manifest = read_yaml(run_dirs[2] / "manifest.yaml")
    legacy_manifest["raw_schema_version"] = 1
    legacy_manifest.pop("research_acceptance", None)
    legacy_manifest.pop("research_rejection_reasons", None)
    legacy_manifest.pop("research_tier", None)
    legacy_manifest["data_quality"] = {}
    write_yaml(run_dirs[2] / "manifest.yaml", legacy_manifest)

    study_dir = run_analysis(run_dirs, config, output_root=tmp_path / "studies")
    inventory = read_yaml(study_dir / "prepared" / "schema_inventory.yaml")
    assert inventory["run_count"] == 1
    assert inventory["runs"][0]["run_id"] == accepted_manifest["run_id"]
    assert len(inventory["excluded_runs"]) == 2
    assert {item["filter_reason"] for item in inventory["excluded_runs"]} == {"research_rejected", "legacy_manifest"}

    study_dir_all = run_analysis(run_dirs, config, output_root=tmp_path / "studies_all", include_rejected_runs=True)
    inventory_all = read_yaml(study_dir_all / "prepared" / "schema_inventory.yaml")
    assert inventory_all["run_count"] == 3
    assert inventory_all["analysis_filters"]["include_rejected_runs"] is True
    assert inventory_all["data_quality"]["accepted_run_count"] == 1
