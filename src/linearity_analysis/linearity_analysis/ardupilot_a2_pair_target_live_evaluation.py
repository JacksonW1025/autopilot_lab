from __future__ import annotations

import argparse
import copy
import json
import math
import shutil
import statistics
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ardupilot_mavlink_backend.matrix_runner import run_matrix
from linearity_core.io import ensure_study_directories, read_rows_csv, read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.paths import CONFIG_ROOT
from linearity_core.study_artifacts import build_guided_mode_smoke_payload, render_guided_mode_smoke_markdown

import linearity_analysis.ardupilot_a2_pair_target_algorithm_evaluation as algorithm_eval
import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness
import linearity_analysis.ardupilot_a2_target_scout as target_scout
from linearity_analysis.ardupilot_a2_readiness import _build_aligned_samples
from linearity_analysis.family_method_contract import (
    ROLE_EXECUTION_FAMILY,
    STAGE_STATUS_DOCUMENTED,
    STAGE_STATUS_FAILED,
    STAGE_STATUS_NOT_RUN,
    STAGE_STATUS_PASSED,
    attach_family_method_contract,
    claim_scope,
    stage_result,
)

STUDY_NAME = "ardupilot_a2_pair_target_live_evaluation"
CAPTURE_TEMPLATE_PATH = CONFIG_ROOT / "ardupilot_diagnostic_guided_nogps_throttle_capture.yaml"
SMOKE_CONFIG_PATH = CONFIG_ROOT / "ardupilot_real_nominal_guided_nogps_capture.yaml"
SMOKE_REPEAT = 3
DEFAULT_ACCEPTED_TARGET = pair_readiness.ACCEPTED_TARGET
DEFAULT_MAX_ATTEMPTS_PER_CONFIG = 10
DEFAULT_ANALYSIS_VARIANT = algorithm_eval.STRATEGY_NAME
PENULTIMATE_WINDOW_ANALYSIS_VARIANT = "reference_pulse_train_penultimate_window_v1"
SUPPORTED_ANALYSIS_VARIANTS = (
    DEFAULT_ANALYSIS_VARIANT,
    PENULTIMATE_WINDOW_ANALYSIS_VARIANT,
)

SCENARIO_MATRIX_FIELDNAMES = [
    "scenario",
    "reference_tier",
    "accepted_count",
    "attempt_count",
    "accepted_reference_tier_count",
    "live_ready",
    "dominant_direction",
    "median_active_pair_rate",
    "median_baseline_pair_rate",
    "median_pair_specificity",
    "median_pair_sign_consistency",
    "median_pair_to_collective_ratio",
    "pair_tier_range_specificity",
    "phase_spillover_run_count",
    "phase_spillover_run_fraction",
    "median_pulse_active_pair_split_count",
    "median_pulse_gap_pair_split_count",
    "hard_regression",
    "soft_regression",
    "blocking_reasons",
]

PHASE_DIAGNOSTIC_FIELDNAMES = [
    "run_id",
    "scenario",
    "reference_tier_match",
    "selected_scenario",
    "accepted",
    "direction_match",
    "pair_split_direction",
    "pulse_active_sample_count",
    "pulse_active_pair_split_count",
    "pulse_active_pair_split_rate",
    "pulse_gap_sample_count",
    "pulse_gap_pair_split_count",
    "pulse_gap_pair_split_rate",
    "active_plus_gap_sample_count",
    "active_plus_gap_pair_split_count",
    "active_plus_gap_pair_split_rate",
    "phase_spillover_detected",
    "artifact_dir",
]


def _pulse_train_duration_s(*, pulse_count: int, pulse_width_s: float, pulse_gap_s: float) -> float:
    return max(0.0, float(pulse_count) * float(pulse_width_s) + max(0, int(pulse_count) - 1) * float(pulse_gap_s))


def _output_paths(output_root: Path | None) -> dict[str, Path]:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S_%f}_{STUDY_NAME}"
    paths = ensure_study_directories(study_id, root=output_root)
    tables_dir = paths["base_dir"] / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "manifest_path": paths["base_dir"] / "manifest.yaml",
        "report_path": paths["reports_dir"] / "a2_pair_target_live_evaluation.md",
        "summary_path": paths["summary_dir"] / "a2_pair_target_live_evaluation.json",
        "scenario_matrix_path": tables_dir / "scenario_live_matrix.csv",
        "run_level_metrics_path": tables_dir / "run_level_live_metrics.csv",
        "phase_diagnostics_path": tables_dir / "phase_pair_split_diagnostics.csv",
        "generated_schedule_path": tables_dir / "generated_schedule.csv",
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact_dir(value: Path | str | None) -> Path | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return Path(text).expanduser().resolve()


def _stringify_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _write_guided_smoke_artifacts(matrix_dir: Path, payload: dict[str, Any]) -> None:
    reports_dir = matrix_dir / "reports"
    summary_dir = matrix_dir / "summary"
    reports_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "guided_nogps_smoke.md").write_text(render_guided_mode_smoke_markdown(payload), encoding="utf-8")
    write_json(summary_dir / "guided_nogps_smoke.json", payload)


def _run_guided_mode_smoke(*, vehicle: str, frame: str, skip_sitl: bool, enable_visualization: bool) -> dict[str, Any]:
    matrix_dir, rows = run_matrix(
        [SMOKE_CONFIG_PATH],
        vehicle=vehicle,
        frame=frame,
        skip_sitl=skip_sitl,
        repeat=SMOKE_REPEAT,
        enable_visualization=enable_visualization,
    )
    run_dirs = [Path(row["artifact_dir"]).expanduser().resolve() for row in rows if row.get("artifact_dir")]
    payload = build_guided_mode_smoke_payload(
        run_dirs,
        target_mode=algorithm_eval.TARGET_MODE,
        target_consecutive_runs=SMOKE_REPEAT,
    )
    _write_guided_smoke_artifacts(matrix_dir, payload)
    return {
        "matrix_dir": matrix_dir,
        "payload": payload,
    }


def _attach_live_family_contract(
    payload: dict[str, Any],
    *,
    a2_target_scout_dir: Path | str | None,
    a2_pair_target_dir: Path | str | None,
    a2_algorithm_eval_dir: Path | str | None,
    live_artifact_dir: Path,
    live_summary_path: Path,
    live_report_path: Path,
) -> dict[str, Any]:
    target_scout_dir = _artifact_dir(a2_target_scout_dir)
    pair_target_dir = _artifact_dir(a2_pair_target_dir)
    algorithm_eval_dir = _artifact_dir(a2_algorithm_eval_dir)
    overall_decision = dict(payload.get("overall_decision", {}) or {})
    live_pair_target_success_v1 = bool(overall_decision.get("live_pair_target_success_v1"))
    recommended_next_step = str(overall_decision.get("recommended_next_step", ""))
    blocking_reasons = sorted(set(payload.get("blocking_reasons", []) or []))
    return attach_family_method_contract(
        payload,
        family_id="A2",
        backend="ardupilot",
        combo_signature="commands_only | actuator_response | ridge_affine | pooled",
        mechanism_family="direct_control",
        role=ROLE_EXECUTION_FAMILY,
        stage_results={
            "scout": stage_result(
                status=STAGE_STATUS_PASSED,
                artifact_dir=str(target_scout_dir) if target_scout_dir is not None else "",
                summary_path=""
                if target_scout_dir is None
                else pair_readiness._relative_workspace_path(target_scout_dir / "summary" / "a2_target_scout.json"),
                report_path=""
                if target_scout_dir is None
                else pair_readiness._relative_workspace_path(target_scout_dir / "reports" / "a2_target_scout.md"),
                recommended_next_step=algorithm_eval.TARGET_READY_STEP,
            ),
            "readiness": stage_result(
                status=STAGE_STATUS_PASSED,
                artifact_dir=str(pair_target_dir) if pair_target_dir is not None else "",
                summary_path=""
                if pair_target_dir is None
                else pair_readiness._relative_workspace_path(pair_target_dir / "summary" / "a2_pair_target_readiness.json"),
                report_path=""
                if pair_target_dir is None
                else pair_readiness._relative_workspace_path(pair_target_dir / "reports" / "a2_pair_target_readiness.md"),
                recommended_next_step=algorithm_eval.PAIR_READY_PATH,
            ),
            "algorithm_evaluation": stage_result(
                status=STAGE_STATUS_PASSED,
                artifact_dir=str(algorithm_eval_dir) if algorithm_eval_dir is not None else "",
                summary_path=""
                if algorithm_eval_dir is None
                else pair_readiness._relative_workspace_path(
                    algorithm_eval_dir / "summary" / "a2_pair_target_algorithm_evaluation.json"
                ),
                report_path=""
                if algorithm_eval_dir is None
                else pair_readiness._relative_workspace_path(
                    algorithm_eval_dir / "reports" / "a2_pair_target_algorithm_evaluation.md"
                ),
                recommended_next_step="hold_for_live_eval",
            ),
            "live_evaluation": stage_result(
                status=STAGE_STATUS_PASSED if live_pair_target_success_v1 else STAGE_STATUS_FAILED,
                artifact_dir=str(live_artifact_dir),
                summary_path=pair_readiness._relative_workspace_path(live_summary_path),
                report_path=pair_readiness._relative_workspace_path(live_report_path),
                recommended_next_step=recommended_next_step,
                blocking_reasons=blocking_reasons,
            ),
            "final_review": stage_result(
                status=STAGE_STATUS_DOCUMENTED,
                report_path="README.md",
                recommended_next_step="use_repository_readme_as_canonical_evaluation_boundary",
                notes="Repository-level A2 evaluation boundary is summarized in README.md; the evidentiary source remains the retained bounded-repeatability and live-evaluation artifacts.",
            ),
        },
        terminal_outcome="live_backed_execution_family" if live_pair_target_success_v1 else "execution_family_not_yet_live_backed",
        recommended_next_step=recommended_next_step,
        blocking_reasons=blocking_reasons,
        claim_scope_payload=claim_scope(
            summary="A2 live evaluation only licenses a bounded canonical live-backed claim and explicitly preserves the widened-pulse boundary.",
            allowed_claims=[
                "A2 may be reported as live-backed only inside the canonical reviewed scope when live thresholds pass.",
            ],
            blocked_claims=[
                "A2 is live-backed for arbitrary widened pulse families.",
                "A2 no longer needs boundary review.",
            ],
        ),
        residuals=[
            "Widened pulse families remain outside the canonical live-backed claim until separately reviewed.",
        ],
    )


def _validate_algorithm_evaluation_summary(summary: dict[str, Any], expected_direction: str) -> list[str]:
    overall = dict(summary.get("overall_decision", {}) or {})
    algorithm_spec = dict(summary.get("algorithm_spec", {}) or {})
    scenario_scope = tuple(str(item) for item in algorithm_spec.get("scenario_scope", []) if str(item))
    reasons: list[str] = []
    if bool(overall.get("offline_ready_for_live_eval_v1")) is not True:
        reasons.append("algorithm_evaluation_not_live_ready")
    if bool(overall.get("live_eval_required")) is not True:
        reasons.append("algorithm_evaluation_live_eval_not_required")
    if bool(overall.get("hard_regression_detected")) is True:
        reasons.append("algorithm_evaluation_hard_regression_detected")
    if bool(overall.get("soft_regression_detected")) is True:
        reasons.append("algorithm_evaluation_soft_regression_detected")
    if overall.get("recommended_next_step") != "hold_for_live_eval":
        reasons.append("algorithm_evaluation_recommended_next_step_mismatch")
    if algorithm_spec.get("strategy") != algorithm_eval.STRATEGY_NAME:
        reasons.append("algorithm_evaluation_strategy_mismatch")
    if algorithm_spec.get("mode") != algorithm_eval.EVALUATION_MODE:
        reasons.append("algorithm_evaluation_mode_mismatch")
    if algorithm_spec.get("flight_mode") != algorithm_eval.TARGET_MODE:
        reasons.append("algorithm_evaluation_flight_mode_mismatch")
    if algorithm_spec.get("target_signal") != algorithm_eval.TARGET_SIGNAL:
        reasons.append("algorithm_evaluation_target_signal_mismatch")
    if algorithm_spec.get("direction") != expected_direction:
        reasons.append("algorithm_evaluation_direction_mismatch")
    if not scenario_scope or any(item not in algorithm_eval.TARGET_SCENARIOS for item in scenario_scope):
        reasons.append("algorithm_evaluation_scenario_scope_invalid")
    if str(algorithm_spec.get("reference_tier", "")) not in algorithm_eval.REFERENCE_TIERS:
        reasons.append("algorithm_evaluation_reference_tier_invalid")
    return reasons


def _copy_or_write_table(
    *,
    source_path: Path | None,
    destination_path: Path,
    fallback_rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> None:
    if source_path is not None and source_path.exists():
        shutil.copy2(source_path, destination_path)
        return
    write_rows_csv(destination_path, fallback_rows, fieldnames=fieldnames)


def run_ardupilot_a2_pair_target_live_evaluation_contract_refresh(
    *,
    legacy_live_eval_dir: Path,
    output_root: Path | None = None,
    a2_target_scout_dir: Path | None = None,
    a2_pair_target_dir: Path | None = None,
    a2_algorithm_eval_dir: Path | None = None,
) -> dict[str, Any]:
    legacy_live_eval_dir = legacy_live_eval_dir.expanduser().resolve()
    legacy_summary = _read_json(legacy_live_eval_dir / "summary" / "a2_pair_target_live_evaluation.json")
    legacy_manifest_path = legacy_live_eval_dir / "manifest.yaml"
    legacy_manifest = read_yaml(legacy_manifest_path) if legacy_manifest_path.exists() else {}
    legacy_sources = dict(legacy_summary.get("source_artifacts", {}) or legacy_manifest.get("source_artifacts", {}) or {})

    target_scout_dir = _artifact_dir(a2_target_scout_dir or legacy_sources.get("a2_target_scout_dir"))
    pair_target_dir = _artifact_dir(a2_pair_target_dir or legacy_sources.get("a2_pair_target_dir"))
    algorithm_eval_dir = _artifact_dir(a2_algorithm_eval_dir or legacy_sources.get("a2_algorithm_eval_dir"))
    if target_scout_dir is None:
        raise FileNotFoundError("missing A2 target scout directory for contract refresh")
    if pair_target_dir is None:
        raise FileNotFoundError("missing A2 pair-target readiness directory for contract refresh")
    algorithm_eval_dir_text = str(algorithm_eval_dir) if algorithm_eval_dir is not None else str(
        legacy_sources.get("a2_algorithm_eval_dir", "")
    )

    target_scout_dir, _target_manifest, _target_summary = algorithm_eval._load_artifact_bundle(
        target_scout_dir, "a2_target_scout.json"
    )
    pair_target_dir, _pair_manifest, _pair_summary = algorithm_eval._load_artifact_bundle(
        pair_target_dir, "a2_pair_target_readiness.json"
    )

    paths = _output_paths(output_root.expanduser().resolve() if output_root else None)
    payload = dict(legacy_summary)
    payload["source_artifacts"] = {
        **legacy_sources,
        "a2_target_scout_dir": str(target_scout_dir),
        "a2_pair_target_dir": str(pair_target_dir),
        "a2_algorithm_eval_dir": algorithm_eval_dir_text,
        "legacy_live_eval_dir": str(legacy_live_eval_dir),
    }
    payload = _attach_live_family_contract(
        payload,
        a2_target_scout_dir=target_scout_dir,
        a2_pair_target_dir=pair_target_dir,
        a2_algorithm_eval_dir=algorithm_eval_dir_text,
        live_artifact_dir=paths["base_dir"],
        live_summary_path=paths["summary_path"],
        live_report_path=paths["report_path"],
    )

    legacy_tables_dir = legacy_live_eval_dir / "tables"
    _copy_or_write_table(
        source_path=legacy_tables_dir / "scenario_live_matrix.csv",
        destination_path=paths["scenario_matrix_path"],
        fallback_rows=[_flatten_live_scenario_result(result) for result in list(payload.get("scenario_results", []) or [])],
        fieldnames=SCENARIO_MATRIX_FIELDNAMES,
    )
    _copy_or_write_table(
        source_path=legacy_tables_dir / "run_level_live_metrics.csv",
        destination_path=paths["run_level_metrics_path"],
        fallback_rows=[],
        fieldnames=algorithm_eval.RUN_LEVEL_FIELDNAMES,
    )
    _copy_or_write_table(
        source_path=legacy_tables_dir / "phase_pair_split_diagnostics.csv",
        destination_path=paths["phase_diagnostics_path"],
        fallback_rows=[],
        fieldnames=PHASE_DIAGNOSTIC_FIELDNAMES,
    )
    algorithm_spec = dict(payload.get("algorithm_spec", {}) or {})
    selected_scenarios = tuple(str(item) for item in algorithm_spec.get("scenario_scope", []) if str(item))
    reference_tier = str(algorithm_spec.get("reference_tier", ""))
    generated_schedule_rows = (
        algorithm_eval._generated_schedule_rows(
            selected_scenarios=selected_scenarios,
            algorithm_spec=algorithm_spec,
            reference_tier=reference_tier,
        )
        if selected_scenarios and reference_tier
        else []
    )
    _copy_or_write_table(
        source_path=legacy_tables_dir / "generated_schedule.csv",
        destination_path=paths["generated_schedule_path"],
        fallback_rows=generated_schedule_rows,
        fieldnames=algorithm_eval.GENERATED_SCHEDULE_FIELDNAMES,
    )

    paths["report_path"].write_text(render_ardupilot_a2_pair_target_live_evaluation_markdown(payload), encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "source_artifacts": payload["source_artifacts"],
            "output_files": {
                "report": pair_readiness._relative_workspace_path(paths["report_path"]),
                "summary": pair_readiness._relative_workspace_path(paths["summary_path"]),
                "scenario_live_matrix": pair_readiness._relative_workspace_path(paths["scenario_matrix_path"]),
                "run_level_live_metrics": pair_readiness._relative_workspace_path(paths["run_level_metrics_path"]),
                "phase_pair_split_diagnostics": pair_readiness._relative_workspace_path(paths["phase_diagnostics_path"]),
                "generated_schedule": pair_readiness._relative_workspace_path(paths["generated_schedule_path"]),
            },
            "summary": payload,
        },
    )
    overall_decision = dict(payload.get("overall_decision", {}) or {})
    return {
        "smoke_passed": None,
        "smoke_matrix_dir": None,
        "matrix_dir": payload["source_artifacts"].get("matrix_dir", ""),
        "live_evaluation_dir": paths["base_dir"],
        "live_pair_target_success_v1": bool(overall_decision.get("live_pair_target_success_v1")),
    }


def _generate_live_capture_configs(
    temp_dir: Path,
    *,
    algorithm_summary: dict[str, Any],
    algorithm_eval_dir: Path,
) -> list[Path]:
    payload = read_yaml(CAPTURE_TEMPLATE_PATH)
    base_seed = int(payload.get("seed", 0) or 0)
    algorithm_spec = dict(algorithm_summary.get("algorithm_spec", {}) or {})
    selected_scenarios = tuple(str(item) for item in algorithm_spec.get("scenario_scope", []) if str(item))
    reference_tier = str(algorithm_spec.get("reference_tier", ""))
    bias_by_scenario = dict(algorithm_spec.get("bias_by_scenario", {}) or {})
    config_paths: list[Path] = []
    for index, scenario in enumerate(selected_scenarios):
        item = copy.deepcopy(payload)
        study_name = f"{STUDY_NAME}_{scenario}_{reference_tier}"
        pulse_count = int(algorithm_spec["pulse_count"])
        pulse_width_s = float(algorithm_spec["pulse_width_s"])
        pulse_gap_s = float(algorithm_spec["pulse_gap_s"])
        train_duration_s = _pulse_train_duration_s(
            pulse_count=pulse_count,
            pulse_width_s=pulse_width_s,
            pulse_gap_s=pulse_gap_s,
        )
        item["study_name"] = study_name
        item["scenario"] = scenario
        item["flight_mode"] = algorithm_eval.TARGET_MODE
        item["config_profile"] = study_name
        item["seed"] = base_seed + index
        item["axis"] = "throttle"
        item["profile_type"] = "pulse_train"
        item["amplitude"] = float(algorithm_spec["pulse_amplitude"])
        item["bias"] = float(bias_by_scenario[scenario])
        item["duration_s"] = max(float(item.get("duration_s", 0.0) or 0.0), train_duration_s)
        item["perturbation_strategy"] = "a2_pair_target_live_evaluation_v1"
        item.setdefault("extras", {})
        item["extras"]["amplitude_tier"] = reference_tier
        item["extras"]["readiness_scenario"] = scenario
        item["extras"]["profile_family"] = "pulse_train"
        item["extras"]["pulse_count"] = pulse_count
        item["extras"]["pulse_width_s"] = pulse_width_s
        item["extras"]["pulse_gap_s"] = pulse_gap_s
        item["extras"]["train_duration_s"] = train_duration_s
        item["extras"]["live_protocol_version"] = "v1"
        item["extras"]["live_stage"] = "pair_target_live_evaluation"
        item["extras"]["expected_direction"] = str(algorithm_spec["direction"])
        item["extras"]["algorithm_strategy"] = str(algorithm_spec["strategy"])
        item["extras"]["algorithm_eval_study_dir"] = str(algorithm_eval_dir)
        output_path = temp_dir / f"{study_name}.yaml"
        write_yaml(output_path, item)
        config_paths.append(output_path)
    return config_paths


def _flatten_live_scenario_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "scenario": result["scenario"],
        "reference_tier": result["reference_tier"],
        "accepted_count": result["accepted_count"],
        "attempt_count": result["attempt_count"],
        "accepted_reference_tier_count": result["accepted_reference_tier_count"],
        "live_ready": result["live_ready"],
        "dominant_direction": result["dominant_direction"],
        "median_active_pair_rate": result["median_active_pair_rate"],
        "median_baseline_pair_rate": result["median_baseline_pair_rate"],
        "median_pair_specificity": result["median_pair_specificity"],
        "median_pair_sign_consistency": result["median_pair_sign_consistency"],
        "median_pair_to_collective_ratio": result["median_pair_to_collective_ratio"],
        "pair_tier_range_specificity": result["pair_tier_range_specificity"],
        "phase_spillover_run_count": result["phase_spillover_run_count"],
        "phase_spillover_run_fraction": result["phase_spillover_run_fraction"],
        "median_pulse_active_pair_split_count": result["median_pulse_active_pair_split_count"],
        "median_pulse_gap_pair_split_count": result["median_pulse_gap_pair_split_count"],
        "hard_regression": result["hard_regression"],
        "soft_regression": result["soft_regression"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
    }


def _validate_analysis_variant(analysis_variant: str) -> str:
    normalized = str(analysis_variant or DEFAULT_ANALYSIS_VARIANT)
    if normalized not in SUPPORTED_ANALYSIS_VARIANTS:
        raise ValueError(f"unsupported analysis_variant: {normalized}")
    return normalized


def _pulse_phase_segments(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    current_phase = ""
    current_pulse_index = 0
    current_rows: list[dict[str, Any]] = []
    pulse_index = 0
    for sample in samples:
        phase = str(sample.get("phase", ""))
        if phase not in {"pulse_active", "pulse_gap"}:
            if current_rows:
                segments.append(
                    {
                        "phase": current_phase,
                        "pulse_index": current_pulse_index,
                        "rows": list(current_rows),
                    }
                )
                current_rows = []
                current_phase = ""
                current_pulse_index = 0
            continue
        if phase == "pulse_active" and current_phase != "pulse_active":
            if current_rows:
                segments.append(
                    {
                        "phase": current_phase,
                        "pulse_index": current_pulse_index,
                        "rows": list(current_rows),
                    }
                )
                current_rows = []
            pulse_index += 1
            current_phase = phase
            current_pulse_index = pulse_index
            current_rows.append(sample)
            continue
        if phase == "pulse_gap" and current_phase != "pulse_gap":
            if current_rows:
                segments.append(
                    {
                        "phase": current_phase,
                        "pulse_index": current_pulse_index,
                        "rows": list(current_rows),
                    }
                )
                current_rows = []
            current_phase = phase
            current_pulse_index = pulse_index
            current_rows.append(sample)
            continue
        current_rows.append(sample)
    if current_rows:
        segments.append(
            {
                "phase": current_phase,
                "pulse_index": current_pulse_index,
                "rows": list(current_rows),
            }
        )
    return segments


def _variant_metrics_from_samples(
    samples: list[dict[str, Any]],
    *,
    analysis_variant: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if analysis_variant == DEFAULT_ANALYSIS_VARIANT:
        return target_scout._compute_run_target_metrics([dict(sample) for sample in samples]), {
            "analysis_variant": analysis_variant,
            "pulse_count_detected": max(
                (int(segment.get("pulse_index", 0) or 0) for segment in _pulse_phase_segments(samples)),
                default=0,
            ),
            "window_pulse_index": "",
            "window_label": "full_pulse_train",
        }

    segments = _pulse_phase_segments(samples)
    pulse_indices = [int(segment.get("pulse_index", 0) or 0) for segment in segments if segment.get("phase") == "pulse_active"]
    if not pulse_indices:
        return {
            "analysis_status": "active_unavailable",
            "baseline_sample_count": 0,
            "active_sample_count": 0,
        }, {
            "analysis_variant": analysis_variant,
            "pulse_count_detected": 0,
            "window_pulse_index": "",
            "window_label": "penultimate_active_plus_gap",
        }
    pulse_count_detected = max(pulse_indices)
    window_pulse_index = pulse_count_detected - 1 if pulse_count_detected >= 2 else pulse_count_detected
    selected_rows = {
        id(row)
        for segment in segments
        if int(segment.get("pulse_index", 0) or 0) == window_pulse_index
        and str(segment.get("phase", "")) in {"pulse_active", "pulse_gap"}
        for row in list(segment.get("rows", []) or [])
    }
    relabeled_samples: list[dict[str, Any]] = []
    for sample in samples:
        original_phase = str(sample.get("phase", ""))
        effective_phase = original_phase
        if id(sample) in selected_rows:
            effective_phase = "pulse_active"
        elif original_phase == "pulse_active":
            effective_phase = "ignored"
        relabeled_samples.append({**sample, "phase": effective_phase})
    metrics = target_scout._compute_run_target_metrics(relabeled_samples)
    return metrics, {
        "analysis_variant": analysis_variant,
        "pulse_count_detected": pulse_count_detected,
        "window_pulse_index": window_pulse_index,
        "window_label": "penultimate_active_plus_gap",
    }


def _analyze_live_attempt_for_variant(
    row: dict[str, Any],
    *,
    analysis_variant: str,
) -> dict[str, Any]:
    analysis_variant = _validate_analysis_variant(analysis_variant)
    attempt = target_scout._analyze_attempt(row)
    if analysis_variant == DEFAULT_ANALYSIS_VARIANT:
        return {
            **attempt,
            "analysis_variant": analysis_variant,
            "analysis_window_pulse_index": "",
            "analysis_window_label": "full_pulse_train",
        }
    artifact_value = str(row.get("artifact_dir", "")).strip()
    artifact_dir = Path(artifact_value).expanduser().resolve() if artifact_value else None
    if artifact_dir is None or not artifact_dir.exists():
        return {
            **attempt,
            "analysis_variant": analysis_variant,
            "analysis_window_pulse_index": "",
            "analysis_window_label": "penultimate_active_plus_gap",
        }
    manifest = read_yaml(artifact_dir / "manifest.yaml")
    samples = _build_aligned_samples(artifact_dir, manifest)
    metrics, diagnostics = _variant_metrics_from_samples(samples, analysis_variant=analysis_variant)
    return {
        **attempt,
        **metrics,
        "analysis_variant": diagnostics["analysis_variant"],
        "analysis_window_pulse_index": diagnostics["window_pulse_index"],
        "analysis_window_label": diagnostics["window_label"],
    }


def _phase_pair_split_diagnostic(row: dict[str, Any]) -> dict[str, Any]:
    artifact_dir = Path(str(row.get("artifact_dir", ""))).expanduser().resolve()
    manifest = read_yaml(artifact_dir / "manifest.yaml")
    samples = _build_aligned_samples(artifact_dir, manifest)
    pulse_active_sample_count = 0
    pulse_active_pair_split_count = 0
    pulse_gap_sample_count = 0
    pulse_gap_pair_split_count = 0
    for sample in samples:
        phase = str(sample.get("phase", ""))
        if phase not in {"pulse_active", "pulse_gap"}:
            continue
        actuator_values = [float(sample.get(f"actuator_{index}", float("nan"))) for index in range(1, 5)]
        if not all(math.isfinite(value) for value in actuator_values):
            continue
        pair_imbalance = ((actuator_values[0] + actuator_values[1]) / 2.0) - ((actuator_values[2] + actuator_values[3]) / 2.0)
        collective_floor = all(value <= target_scout.FLOOR_THRESHOLD for value in actuator_values)
        pair_split = abs(pair_imbalance) >= target_scout.PAIR_SPLIT_THRESHOLD and not collective_floor
        if phase == "pulse_active":
            pulse_active_sample_count += 1
            pulse_active_pair_split_count += int(pair_split)
        else:
            pulse_gap_sample_count += 1
            pulse_gap_pair_split_count += int(pair_split)
    active_plus_gap_sample_count = pulse_active_sample_count + pulse_gap_sample_count
    active_plus_gap_pair_split_count = pulse_active_pair_split_count + pulse_gap_pair_split_count
    phase_spillover_detected = (
        bool(row.get("accepted"))
        and bool(row.get("direction_match"))
        and pulse_gap_pair_split_count > pulse_active_pair_split_count
        and pulse_gap_pair_split_count > 0
    )
    return {
        "run_id": row.get("run_id", ""),
        "scenario": row.get("scenario", ""),
        "reference_tier_match": bool(row.get("reference_tier_match")),
        "selected_scenario": bool(row.get("selected_scenario")),
        "accepted": bool(row.get("accepted")),
        "direction_match": bool(row.get("direction_match")),
        "pair_split_direction": row.get("pair_split_direction", ""),
        "pulse_active_sample_count": pulse_active_sample_count,
        "pulse_active_pair_split_count": pulse_active_pair_split_count,
        "pulse_active_pair_split_rate": (
            pulse_active_pair_split_count / pulse_active_sample_count if pulse_active_sample_count else 0.0
        ),
        "pulse_gap_sample_count": pulse_gap_sample_count,
        "pulse_gap_pair_split_count": pulse_gap_pair_split_count,
        "pulse_gap_pair_split_rate": pulse_gap_pair_split_count / pulse_gap_sample_count if pulse_gap_sample_count else 0.0,
        "active_plus_gap_sample_count": active_plus_gap_sample_count,
        "active_plus_gap_pair_split_count": active_plus_gap_pair_split_count,
        "active_plus_gap_pair_split_rate": (
            active_plus_gap_pair_split_count / active_plus_gap_sample_count if active_plus_gap_sample_count else 0.0
        ),
        "phase_spillover_detected": phase_spillover_detected,
        "artifact_dir": str(artifact_dir),
    }


def _phase_pair_split_review(
    diagnostics: list[dict[str, Any]],
    *,
    scenario: str,
    reference_tier: str,
) -> dict[str, Any]:
    relevant_rows = [
        row
        for row in diagnostics
        if str(row.get("scenario", "")) == scenario
        and bool(row.get("accepted"))
        and bool(row.get("reference_tier_match"))
        and bool(row.get("selected_scenario"))
    ]
    spillover_run_count = sum(1 for row in relevant_rows if bool(row.get("phase_spillover_detected")))
    sample_count = len(relevant_rows)
    pulse_active_pair_counts = [int(row.get("pulse_active_pair_split_count", 0) or 0) for row in relevant_rows]
    pulse_gap_pair_counts = [int(row.get("pulse_gap_pair_split_count", 0) or 0) for row in relevant_rows]
    return {
        "scenario": scenario,
        "reference_tier": reference_tier,
        "spillover_run_count": spillover_run_count,
        "spillover_run_fraction": (spillover_run_count / sample_count) if sample_count else 0.0,
        "median_pulse_active_pair_split_count": statistics.median(pulse_active_pair_counts) if pulse_active_pair_counts else 0.0,
        "median_pulse_gap_pair_split_count": statistics.median(pulse_gap_pair_counts) if pulse_gap_pair_counts else 0.0,
    }


def render_ardupilot_a2_pair_target_live_evaluation_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    algorithm_spec = payload["algorithm_spec"]
    analysis_variant = str(payload.get("study_scope", {}).get("analysis_variant", DEFAULT_ANALYSIS_VARIANT))
    phase_reviews = {
        str(item.get("scenario", "")): item for item in list(payload.get("phase_pair_split_review", []) or []) if str(item.get("scenario", ""))
    }
    lines = [
        "# ArduPilot A2 Pair-Target Live Evaluation",
        "",
        f"- live_pair_target_success_v1: {'yes' if overall['live_pair_target_success_v1'] else 'no'}",
        f"- hard_regression_detected: {'yes' if overall['hard_regression_detected'] else 'no'}",
        f"- soft_regression_detected: {'yes' if overall['soft_regression_detected'] else 'no'}",
        f"- phase_spillover_detected: {'yes' if overall['phase_spillover_detected'] else 'no'}",
        f"- analysis_variant: {analysis_variant}",
        f"- dominant_direction: {overall['dominant_direction']}",
        f"- recommended_next_step: {overall['recommended_next_step']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Executed Algorithm Spec",
        "",
        f"- strategy: {algorithm_spec['strategy']}",
        f"- flight_mode: {algorithm_spec['flight_mode']}",
        f"- target_signal: {algorithm_spec['target_signal']}",
        f"- scenario_scope: {', '.join(algorithm_spec['scenario_scope'])}",
        f"- reference_tier: {algorithm_spec['reference_tier']}",
        f"- direction: {algorithm_spec['direction']}",
        f"- pulse parameters: amplitude={algorithm_eval._format_metric(algorithm_spec['pulse_amplitude'])}, "
        f"pulse_count={algorithm_spec['pulse_count']}, pulse_width_s={algorithm_eval._format_metric(algorithm_spec['pulse_width_s'])}, "
        f"pulse_gap_s={algorithm_eval._format_metric(algorithm_spec['pulse_gap_s'])}",
        "",
        "## Scenario Matrix",
        "",
        "| scenario | live_ready | hard_regression | soft_regression | active_pair_rate | specificity | ratio | direction |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in payload["scenario_results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    result["scenario"],
                    algorithm_eval._format_metric(result["live_ready"]),
                    algorithm_eval._format_metric(result["hard_regression"]),
                    algorithm_eval._format_metric(result["soft_regression"]),
                    algorithm_eval._format_metric(result["median_active_pair_rate"]),
                    algorithm_eval._format_metric(result["median_pair_specificity"]),
                    algorithm_eval._format_metric(result["median_pair_to_collective_ratio"]),
                    result["dominant_direction"],
                ]
            )
            + " |"
        )
    lines.append("")
    for result in payload["scenario_results"]:
        reference = payload["reference_thresholds"]["canonical_reference_metrics"].get(result["scenario"], {})
        lines.append(f"## {result['scenario']}")
        lines.append("")
        lines.append(f"- live_ready: {'yes' if result['live_ready'] else 'no'}")
        lines.append(
            f"- observed metrics: active_rate={algorithm_eval._format_metric(result['median_active_pair_rate'])}, "
            f"baseline_rate={algorithm_eval._format_metric(result['median_baseline_pair_rate'])}, "
            f"specificity={algorithm_eval._format_metric(result['median_pair_specificity'])}, "
            f"sign_consistency={algorithm_eval._format_metric(result['median_pair_sign_consistency'])}, "
            f"pair_to_collective_ratio={algorithm_eval._format_metric(result['median_pair_to_collective_ratio'])}, "
            f"tier_range={algorithm_eval._format_metric(result['pair_tier_range_specificity'])}, "
            f"direction={result['dominant_direction']}"
        )
        lines.append(
            f"- reference metrics: active_rate={algorithm_eval._format_metric(reference.get('median_active_pair_rate'))}, "
            f"specificity={algorithm_eval._format_metric(reference.get('median_pair_specificity'))}, "
            f"ratio={algorithm_eval._format_metric(reference.get('median_pair_to_collective_ratio'))}, "
            f"tier_range={algorithm_eval._format_metric(reference.get('pair_tier_range_specificity'))}, "
            f"direction={reference.get('dominant_direction', 'n/a')}"
        )
        phase_review = phase_reviews.get(result["scenario"], {})
        lines.append(
            f"- phase diagnostics: spillover_runs={phase_review.get('spillover_run_count', 0)}/{result['accepted_count']}, "
            f"spillover_fraction={algorithm_eval._format_metric(phase_review.get('spillover_run_fraction'))}, "
            f"median_active_pair_splits={algorithm_eval._format_metric(phase_review.get('median_pulse_active_pair_split_count'))}, "
            f"median_gap_pair_splits={algorithm_eval._format_metric(phase_review.get('median_pulse_gap_pair_split_count'))}"
        )
        lines.append(
            f"- blocking_reasons: {', '.join(result['blocking_reasons']) if result['blocking_reasons'] else 'none'}"
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_pair_target_live_evaluation(
    *,
    a2_target_scout_dir: Path,
    a2_pair_target_dir: Path,
    a2_algorithm_eval_dir: Path,
    vehicle: str = "ArduCopter",
    frame: str = "quad",
    skip_sitl: bool = False,
    skip_smoke: bool = False,
    skip_capture: bool = False,
    matrix_dir: Path | None = None,
    output_root: Path | None = None,
    accepted_target: int = DEFAULT_ACCEPTED_TARGET,
    max_attempts_per_config: int = DEFAULT_MAX_ATTEMPTS_PER_CONFIG,
    analysis_variant: str = DEFAULT_ANALYSIS_VARIANT,
    enable_visualization: bool = False,
) -> dict[str, Any]:
    analysis_variant = _validate_analysis_variant(analysis_variant)
    output_root = output_root.expanduser().resolve() if output_root is not None else None
    if matrix_dir is not None and not skip_capture:
        raise ValueError("--matrix-dir is only allowed together with --skip-capture")
    if skip_capture and matrix_dir is None:
        raise ValueError("--matrix-dir is required when --skip-capture is set")

    target_scout_dir, _target_manifest, target_scout_summary = algorithm_eval._load_artifact_bundle(
        a2_target_scout_dir, "a2_target_scout.json"
    )
    pair_target_dir, _pair_manifest, pair_target_summary = algorithm_eval._load_artifact_bundle(
        a2_pair_target_dir, "a2_pair_target_readiness.json"
    )
    algorithm_eval_dir, _algorithm_manifest, algorithm_eval_summary = algorithm_eval._load_artifact_bundle(
        a2_algorithm_eval_dir, "a2_pair_target_algorithm_evaluation.json"
    )

    expected_direction = str(pair_target_summary.get("overall_decision", {}).get("dominant_direction", ""))
    selected_scenarios = tuple(
        str(item)
        for item in dict(algorithm_eval_summary.get("algorithm_spec", {}) or {}).get("scenario_scope", [])
        if str(item)
    )
    preflight_reasons: list[str] = []
    preflight_reasons.extend(algorithm_eval._validate_target_scout_summary(target_scout_summary, selected_scenarios))
    preflight_reasons.extend(algorithm_eval._validate_pair_readiness_summary(pair_target_summary, selected_scenarios, expected_direction))
    preflight_reasons.extend(_validate_algorithm_evaluation_summary(algorithm_eval_summary, expected_direction))
    if preflight_reasons:
        raise RuntimeError(f"A2 live evaluation preflight failed: {', '.join(sorted(set(preflight_reasons)))}")

    smoke_matrix_dir: Path | None = None
    smoke_passed: bool | None = None
    if not skip_smoke:
        smoke_result = _run_guided_mode_smoke(
            vehicle=vehicle,
            frame=frame,
            skip_sitl=skip_sitl,
            enable_visualization=enable_visualization,
        )
        smoke_matrix_dir = Path(smoke_result["matrix_dir"]).expanduser().resolve()
        smoke_passed = bool(smoke_result["payload"].get("passed"))
        if smoke_passed is not True:
            raise RuntimeError(f"GUIDED_NOGPS smoke gate failed: {smoke_result['payload'].get('conclusion', '')}")

    if skip_capture:
        resolved_matrix_dir = matrix_dir.expanduser().resolve() if matrix_dir is not None else None
        if resolved_matrix_dir is None:
            raise ValueError("matrix_dir is required when skip_capture is set")
        runs_manifest = resolved_matrix_dir / "runs.csv"
        if not runs_manifest.exists():
            raise FileNotFoundError(runs_manifest)
    else:
        with tempfile.TemporaryDirectory(prefix=f"{STUDY_NAME}_") as temp_dir_name:
            config_paths = _generate_live_capture_configs(
                Path(temp_dir_name),
                algorithm_summary=algorithm_eval_summary,
                algorithm_eval_dir=algorithm_eval_dir,
            )
            resolved_matrix_dir, _rows = run_matrix(
                config_paths,
                vehicle=vehicle,
                frame=frame,
                skip_sitl=skip_sitl,
                repeat=1,
                accepted_target=accepted_target,
                max_attempts_per_config=max_attempts_per_config,
                enable_visualization=enable_visualization,
            )
        runs_manifest = resolved_matrix_dir / "runs.csv"

    attempts = [
        _analyze_live_attempt_for_variant(row, analysis_variant=analysis_variant)
        for row in read_rows_csv(runs_manifest)
    ]
    relevant_attempts = [
        row
        for row in attempts
        if str(row.get("flight_mode", "")).upper() == algorithm_eval.TARGET_MODE and str(row.get("scenario", "")) in selected_scenarios
    ]
    algorithm_spec = dict(algorithm_eval_summary.get("algorithm_spec", {}) or {})
    reference_tier = str(algorithm_spec.get("reference_tier", ""))
    direction = str(algorithm_spec.get("direction", ""))
    run_level_rows = [
        algorithm_eval._flatten_run_alignment_row(
            row,
            selected_scenarios=selected_scenarios,
            reference_tier=reference_tier,
            direction=direction,
        )
        for row in relevant_attempts
    ]
    phase_diagnostic_rows = [_phase_pair_split_diagnostic(row) for row in run_level_rows]

    reference_thresholds = dict(algorithm_eval_summary.get("reference_thresholds", {}) or {})
    canonical_reference_metrics = dict(reference_thresholds.get("canonical_reference_metrics", {}) or {})
    blocking_reasons: list[str] = []
    scenario_results: list[dict[str, Any]] = []
    phase_pair_split_review: list[dict[str, Any]] = []
    for scenario_name in selected_scenarios:
        scenario_rows = [row for row in relevant_attempts if str(row.get("scenario", "")) == scenario_name]
        accepted_reference_tier_count = sum(
            1
            for row in scenario_rows
            if bool(row.get("accepted")) and str(row.get("amplitude_tier", "")) == reference_tier
        )
        scenario_result = pair_readiness.summarize_pair_target_scenario(
            scenario_name,
            scenario_rows,
            accepted_target=accepted_target,
        )
        scenario_blocking_reasons = list(scenario_result["blocking_reasons"])
        if accepted_reference_tier_count < accepted_target:
            scenario_blocking_reasons.append("reference_tier_coverage_missing")
        if scenario_result["dominant_direction"] != direction:
            scenario_blocking_reasons.append("scenario_direction_mismatch")
        soft_reasons = algorithm_eval._soft_regression_reasons(
            scenario=scenario_name,
            observed=scenario_result,
            reference=canonical_reference_metrics.get(scenario_name, {}),
        )
        phase_review = _phase_pair_split_review(
            phase_diagnostic_rows,
            scenario=scenario_name,
            reference_tier=reference_tier,
        )
        hard_regression = bool(scenario_blocking_reasons)
        soft_regression = bool(soft_reasons)
        live_ready = scenario_result["ready"] and not soft_regression and scenario_result["dominant_direction"] == direction
        blocking_reasons.extend(f"{reason}:{scenario_name}" if ":" not in reason else reason for reason in scenario_blocking_reasons)
        blocking_reasons.extend(soft_reasons)
        phase_pair_split_review.append(phase_review)
        scenario_results.append(
            {
                **scenario_result,
                "reference_tier": reference_tier,
                "accepted_reference_tier_count": accepted_reference_tier_count,
                "live_ready": live_ready,
                "phase_spillover_run_count": phase_review["spillover_run_count"],
                "phase_spillover_run_fraction": phase_review["spillover_run_fraction"],
                "median_pulse_active_pair_split_count": phase_review["median_pulse_active_pair_split_count"],
                "median_pulse_gap_pair_split_count": phase_review["median_pulse_gap_pair_split_count"],
                "hard_regression": hard_regression,
                "soft_regression": soft_regression,
                "blocking_reasons": sorted(set(scenario_blocking_reasons + soft_reasons)),
            }
        )

    hard_regression_detected = any(
        not reason.startswith("soft_regression_")
        for reason in blocking_reasons
    )
    soft_regression_detected = any(reason.startswith("soft_regression_") for reason in blocking_reasons)
    scenario_status = {result["scenario"]: result["live_ready"] for result in scenario_results}
    directions = {result["dominant_direction"] for result in scenario_results if result["dominant_direction"] != "none"}
    dominant_direction = next(iter(directions)) if len(directions) == 1 else "mixed"
    phase_spillover_detected = any(bool(item.get("spillover_run_count")) for item in phase_pair_split_review)
    live_pair_target_success_v1 = (
        bool(scenario_results)
        and all(result["live_ready"] for result in scenario_results)
        and not hard_regression_detected
        and not soft_regression_detected
        and dominant_direction == direction
    )
    if hard_regression_detected and any("scenario_direction_mismatch" in reason for reason in blocking_reasons):
        recommended_next_step = "fix_live_protocol_or_capture"
    elif hard_regression_detected and phase_spillover_detected:
        recommended_next_step = "diagnose_phase_spillover"
    elif hard_regression_detected:
        recommended_next_step = "fix_live_protocol_or_capture"
    elif live_pair_target_success_v1:
        recommended_next_step = "promote_live_artifact_for_review"
    else:
        recommended_next_step = "tighten_algorithm_spec"

    generated_schedule_rows = algorithm_eval._generated_schedule_rows(
        selected_scenarios=selected_scenarios,
        algorithm_spec=algorithm_spec,
        reference_tier=reference_tier,
    )
    payload = {
        "study_scope": {
            "backend": "ardupilot",
            "stage": "live_evaluation",
            "flight_mode": algorithm_eval.TARGET_MODE,
            "target_signal": algorithm_eval.TARGET_SIGNAL,
            "scenario_scope": list(selected_scenarios),
            "reference_tier": reference_tier,
            "accepted_target": accepted_target,
            "analysis_variant": analysis_variant,
        },
        "source_artifacts": {
            "a2_target_scout_dir": str(target_scout_dir),
            "a2_pair_target_dir": str(pair_target_dir),
            "a2_algorithm_eval_dir": str(algorithm_eval_dir),
            "matrix_dir": str(resolved_matrix_dir),
            "runs_manifest": str(runs_manifest),
            "smoke_matrix_dir": str(smoke_matrix_dir) if smoke_matrix_dir is not None else "",
        },
        "algorithm_spec": algorithm_spec,
        "reference_thresholds": reference_thresholds,
        "scenario_results": scenario_results,
        "phase_pair_split_review": phase_pair_split_review,
        "overall_decision": {
            "live_pair_target_success_v1": live_pair_target_success_v1,
            "hard_regression_detected": hard_regression_detected,
            "soft_regression_detected": soft_regression_detected,
            "phase_spillover_detected": phase_spillover_detected,
            "dominant_direction": dominant_direction,
            "recommended_next_step": recommended_next_step,
            "scenario_status": scenario_status,
        },
        "blocking_reasons": sorted(set(blocking_reasons)),
    }

    paths = _output_paths(output_root)
    payload = _attach_live_family_contract(
        payload,
        a2_target_scout_dir=target_scout_dir,
        a2_pair_target_dir=pair_target_dir,
        a2_algorithm_eval_dir=algorithm_eval_dir,
        live_artifact_dir=paths["base_dir"],
        live_summary_path=paths["summary_path"],
        live_report_path=paths["report_path"],
    )
    paths["report_path"].write_text(render_ardupilot_a2_pair_target_live_evaluation_markdown(payload), encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(
        paths["scenario_matrix_path"],
        [_flatten_live_scenario_result(result) for result in scenario_results],
        fieldnames=SCENARIO_MATRIX_FIELDNAMES,
    )
    write_rows_csv(paths["run_level_metrics_path"], run_level_rows, fieldnames=algorithm_eval.RUN_LEVEL_FIELDNAMES)
    write_rows_csv(paths["phase_diagnostics_path"], phase_diagnostic_rows, fieldnames=PHASE_DIAGNOSTIC_FIELDNAMES)
    write_rows_csv(paths["generated_schedule_path"], generated_schedule_rows, fieldnames=algorithm_eval.GENERATED_SCHEDULE_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "source_artifacts": payload["source_artifacts"],
            "output_files": {
                "report": pair_readiness._relative_workspace_path(paths["report_path"]),
                "summary": pair_readiness._relative_workspace_path(paths["summary_path"]),
                "scenario_live_matrix": pair_readiness._relative_workspace_path(paths["scenario_matrix_path"]),
                "run_level_live_metrics": pair_readiness._relative_workspace_path(paths["run_level_metrics_path"]),
                "phase_pair_split_diagnostics": pair_readiness._relative_workspace_path(paths["phase_diagnostics_path"]),
                "generated_schedule": pair_readiness._relative_workspace_path(paths["generated_schedule_path"]),
            },
            "summary": payload,
        },
    )
    return {
        "smoke_matrix_dir": smoke_matrix_dir,
        "smoke_passed": smoke_passed,
        "matrix_dir": resolved_matrix_dir,
        "live_evaluation_dir": paths["base_dir"],
        "live_pair_target_success_v1": live_pair_target_success_v1,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run minimal live A2 pair-target evaluation from canonical A2 artifacts.")
    parser.add_argument("--a2-target-scout-dir", type=Path, default=None)
    parser.add_argument("--a2-pair-target-dir", type=Path, default=None)
    parser.add_argument("--a2-algorithm-eval-dir", type=Path, default=None)
    parser.add_argument("--legacy-live-eval-dir", type=Path, default=None)
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--skip-capture", action="store_true")
    parser.add_argument("--matrix-dir", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--accepted-target", type=int, default=DEFAULT_ACCEPTED_TARGET)
    parser.add_argument("--max-attempts-per-config", type=int, default=DEFAULT_MAX_ATTEMPTS_PER_CONFIG)
    parser.add_argument("--analysis-variant", choices=SUPPORTED_ANALYSIS_VARIANTS, default=DEFAULT_ANALYSIS_VARIANT)
    parser.add_argument("--enable-visualization", action="store_true")
    args = parser.parse_args(argv)

    if args.legacy_live_eval_dir is not None:
        result = run_ardupilot_a2_pair_target_live_evaluation_contract_refresh(
            legacy_live_eval_dir=args.legacy_live_eval_dir,
            output_root=args.output_root,
            a2_target_scout_dir=args.a2_target_scout_dir,
            a2_pair_target_dir=args.a2_pair_target_dir,
            a2_algorithm_eval_dir=args.a2_algorithm_eval_dir,
        )
    else:
        missing = [
            flag
            for flag, value in (
                ("--a2-target-scout-dir", args.a2_target_scout_dir),
                ("--a2-pair-target-dir", args.a2_pair_target_dir),
                ("--a2-algorithm-eval-dir", args.a2_algorithm_eval_dir),
            )
            if value is None
        ]
        if missing:
            parser.error(f"missing required arguments for live evaluation: {', '.join(missing)}")
        result = run_ardupilot_a2_pair_target_live_evaluation(
            a2_target_scout_dir=args.a2_target_scout_dir,
            a2_pair_target_dir=args.a2_pair_target_dir,
            a2_algorithm_eval_dir=args.a2_algorithm_eval_dir,
            vehicle=args.vehicle,
            frame=args.frame,
            skip_sitl=args.skip_sitl,
            skip_smoke=args.skip_smoke,
            skip_capture=args.skip_capture,
            matrix_dir=args.matrix_dir,
            output_root=args.output_root,
            accepted_target=args.accepted_target,
            max_attempts_per_config=args.max_attempts_per_config,
            analysis_variant=args.analysis_variant,
            enable_visualization=args.enable_visualization,
        )
    smoke_passed = result["smoke_passed"]
    print(f"guided_nogps_smoke_passed={'skipped' if smoke_passed is None else _stringify_output(smoke_passed)}")
    print(f"smoke_matrix_dir={_stringify_output(result['smoke_matrix_dir'])}")
    print(f"matrix_dir={_stringify_output(result['matrix_dir'])}")
    print(f"live_evaluation_dir={_stringify_output(result['live_evaluation_dir'])}")
    print(f"live_pair_target_success_v1={_stringify_output(result['live_pair_target_success_v1'])}")


if __name__ == "__main__":
    main()
