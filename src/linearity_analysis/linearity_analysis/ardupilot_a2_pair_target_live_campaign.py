from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from linearity_core.io import ensure_study_directories, read_yaml, write_json, write_rows_csv, write_yaml

import linearity_analysis.ardupilot_a2_pair_target_algorithm_evaluation as algorithm_eval
import linearity_analysis.ardupilot_a2_pair_target_live_evaluation as live_eval
import linearity_analysis.ardupilot_a2_pair_target_readiness as pair_readiness

STUDY_NAME = "ardupilot_a2_pair_target_live_campaign"
EXPECTED_CAMPAIGN_VERSION = "v1"
EXPECTED_DIRECTION = "12_gt_34"
EXPECTED_SCENARIO_SCOPE = "both"
EXPECTED_PULSE_COUNT = 5
EXPECTED_PULSE_WIDTH_S = 0.35
EXPECTED_PULSE_GAP_S = 0.95
EXPECTED_PHASE_IDS = (
    "probe_stability_r1",
    "probe_stability_r2",
    "micro_robustness_r1",
    "confirm_robustness_r1",
)
FAILURE_CATEGORY_PREFLIGHT = "preflight_artifact_mismatch"
FAILURE_CATEGORY_SMOKE = "smoke_gate_failure"
FAILURE_CATEGORY_ALGO_HARD = "algorithm_eval_hard_regression"
FAILURE_CATEGORY_ALGO_SOFT = "algorithm_eval_soft_regression"
FAILURE_CATEGORY_LIVE_CAPTURE = "live_capture_failure"
FAILURE_CATEGORY_LIVE_DIRECTION = "live_direction_mismatch"
FAILURE_CATEGORY_LIVE_THRESHOLD = "live_threshold_regression"
FAILURE_CATEGORY_LIVE_SOFT = "live_soft_regression"

PHASE_BOARD_FIELDNAMES = [
    "phase_id",
    "phase_class",
    "reference_tier",
    "pulse_amplitude",
    "algorithm_eval_dir",
    "live_evaluation_dir",
    "algorithm_eval_ready",
    "live_pair_target_success_v1",
    "dominant_direction",
    "hard_regression_detected",
    "soft_regression_detected",
    "stopped_campaign",
    "stop_reason",
    "failure_categories",
]

SCENARIO_BOARD_FIELDNAMES = [
    "phase_id",
    "phase_class",
    "stage_source",
    "scenario",
    "reference_tier",
    "ready_signal",
    "hard_regression",
    "soft_regression",
    "dominant_direction",
    "median_active_pair_rate",
    "median_baseline_pair_rate",
    "median_pair_specificity",
    "median_pair_sign_consistency",
    "median_pair_to_collective_ratio",
    "pair_tier_range_specificity",
    "blocking_reasons",
]

FAILURE_TAXONOMY_FIELDNAMES = [
    "phase_id",
    "stage",
    "failure_category",
    "failure_reason",
    "stopped_campaign",
    "study_dir",
]


def _output_paths(output_root: Path | None) -> dict[str, Path]:
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S_%f}_{STUDY_NAME}"
    paths = ensure_study_directories(study_id, root=output_root)
    tables_dir = paths["base_dir"] / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    phases_dir = paths["base_dir"] / "phases"
    phases_dir.mkdir(parents=True, exist_ok=True)
    return {
        **paths,
        "tables_dir": tables_dir,
        "phases_dir": phases_dir,
        "manifest_path": paths["base_dir"] / "manifest.yaml",
        "report_path": paths["reports_dir"] / "a2_pair_target_live_campaign.md",
        "summary_path": paths["summary_dir"] / "a2_pair_target_live_campaign.json",
        "phase_board_path": tables_dir / "campaign_phase_board.csv",
        "scenario_board_path": tables_dir / "campaign_scenario_board.csv",
        "failure_taxonomy_path": tables_dir / "failure_taxonomy.csv",
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _stringify_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _resolve_path(value: Any, *, base_dir: Path) -> Path | None:
    if value in ("", None):
        return None
    candidate = Path(str(value)).expanduser()
    if not candidate.is_absolute():
        candidate = (base_dir / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return candidate


def _phase_class(phase_id: str) -> str:
    if phase_id.startswith("probe_stability_"):
        return "probe_stability"
    if phase_id.startswith("micro_robustness_"):
        return "micro_robustness"
    if phase_id.startswith("confirm_robustness_"):
        return "confirm_robustness"
    return "other"


def _validate_phase_spec(phase: dict[str, Any], *, skip_capture: bool, base_dir: Path) -> dict[str, Any]:
    required = {
        "phase_id",
        "reference_tier",
        "scenario_scope",
        "direction",
        "pulse_amplitude",
        "use_canonical_bias_by_scenario",
        "pulse_count",
        "pulse_width_s",
        "pulse_gap_s",
        "accepted_target",
        "max_attempts_per_config",
    }
    missing = sorted(required - set(phase.keys()))
    if missing:
        raise ValueError(f"phase spec missing fields: {', '.join(missing)}")
    phase_id = str(phase["phase_id"])
    reference_tier = str(phase["reference_tier"])
    if reference_tier not in algorithm_eval.REFERENCE_TIERS:
        raise ValueError(f"{phase_id}: unsupported reference_tier={reference_tier}")
    scenario_scope = str(phase["scenario_scope"])
    if scenario_scope != EXPECTED_SCENARIO_SCOPE:
        raise ValueError(f"{phase_id}: scenario_scope must be {EXPECTED_SCENARIO_SCOPE}")
    direction = str(phase["direction"])
    if direction != EXPECTED_DIRECTION:
        raise ValueError(f"{phase_id}: direction must be {EXPECTED_DIRECTION}")
    if bool(phase["use_canonical_bias_by_scenario"]) is not True:
        raise ValueError(f"{phase_id}: use_canonical_bias_by_scenario must be true")
    if int(phase["pulse_count"]) != EXPECTED_PULSE_COUNT:
        raise ValueError(f"{phase_id}: pulse_count must be {EXPECTED_PULSE_COUNT}")
    if float(phase["pulse_width_s"]) != EXPECTED_PULSE_WIDTH_S:
        raise ValueError(f"{phase_id}: pulse_width_s must be {EXPECTED_PULSE_WIDTH_S}")
    if float(phase["pulse_gap_s"]) != EXPECTED_PULSE_GAP_S:
        raise ValueError(f"{phase_id}: pulse_gap_s must be {EXPECTED_PULSE_GAP_S}")
    accepted_target = int(phase["accepted_target"])
    max_attempts = int(phase["max_attempts_per_config"])
    if accepted_target <= 0:
        raise ValueError(f"{phase_id}: accepted_target must be positive")
    if max_attempts < accepted_target:
        raise ValueError(f"{phase_id}: max_attempts_per_config must be >= accepted_target")
    phase_matrix_dir = _resolve_path(phase.get("matrix_dir"), base_dir=base_dir)
    if skip_capture and phase_matrix_dir is None:
        raise ValueError(f"{phase_id}: matrix_dir is required when --skip-capture is set")
    if not skip_capture and phase_matrix_dir is not None:
        raise ValueError(f"{phase_id}: matrix_dir is only allowed with --skip-capture")
    if phase_matrix_dir is not None and not phase_matrix_dir.exists():
        raise FileNotFoundError(f"{phase_id}: matrix_dir not found: {phase_matrix_dir}")
    return {
        "phase_id": phase_id,
        "reference_tier": reference_tier,
        "scenario_scope": scenario_scope,
        "direction": direction,
        "pulse_amplitude": float(phase["pulse_amplitude"]),
        "use_canonical_bias_by_scenario": True,
        "pulse_count": int(phase["pulse_count"]),
        "pulse_width_s": float(phase["pulse_width_s"]),
        "pulse_gap_s": float(phase["pulse_gap_s"]),
        "accepted_target": accepted_target,
        "max_attempts_per_config": max_attempts,
        "matrix_dir": phase_matrix_dir,
        "phase_class": _phase_class(phase_id),
    }


def _load_campaign_spec(spec_path: Path, *, skip_capture: bool) -> dict[str, Any]:
    resolved_path = spec_path.expanduser().resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(resolved_path)
    payload = read_yaml(resolved_path)
    required = {"campaign_name", "campaign_version", "a2_target_scout_dir", "a2_pair_target_dir", "phase_order", "phases"}
    missing = sorted(required - set(payload.keys()))
    if missing:
        raise ValueError(f"campaign spec missing fields: {', '.join(missing)}")
    if str(payload["campaign_version"]) != EXPECTED_CAMPAIGN_VERSION:
        raise ValueError(f"campaign_version must be {EXPECTED_CAMPAIGN_VERSION}")
    phase_order = [str(item) for item in list(payload["phase_order"] or [])]
    if not phase_order:
        raise ValueError("phase_order must not be empty")
    if tuple(phase_order) != EXPECTED_PHASE_IDS:
        raise ValueError(f"phase_order must exactly be {list(EXPECTED_PHASE_IDS)}")
    phases_raw = list(payload["phases"] or [])
    if not phases_raw:
        raise ValueError("phases must not be empty")
    phase_map: dict[str, dict[str, Any]] = {}
    for raw in phases_raw:
        if not isinstance(raw, dict):
            raise ValueError("each phase must be a mapping")
        normalized = _validate_phase_spec(raw, skip_capture=skip_capture, base_dir=resolved_path.parent)
        phase_id = str(normalized["phase_id"])
        if phase_id in phase_map:
            raise ValueError(f"duplicate phase_id: {phase_id}")
        phase_map[phase_id] = normalized
    if set(phase_order) != set(phase_map):
        raise ValueError("phase_order must exactly match phases[].phase_id")
    if tuple(sorted(phase_map)) != tuple(sorted(EXPECTED_PHASE_IDS)):
        raise ValueError(f"phases[].phase_id must exactly be {list(EXPECTED_PHASE_IDS)}")
    a2_target_scout_dir = _resolve_path(payload["a2_target_scout_dir"], base_dir=resolved_path.parent)
    a2_pair_target_dir = _resolve_path(payload["a2_pair_target_dir"], base_dir=resolved_path.parent)
    if a2_target_scout_dir is None or a2_pair_target_dir is None:
        raise ValueError("a2_target_scout_dir and a2_pair_target_dir are required")
    return {
        "spec_path": resolved_path,
        "campaign_name": str(payload["campaign_name"]),
        "campaign_version": str(payload["campaign_version"]),
        "a2_target_scout_dir": a2_target_scout_dir,
        "a2_pair_target_dir": a2_pair_target_dir,
        "phase_order": phase_order,
        "phases": phase_map,
    }


def _failure_row(
    *,
    phase_id: str,
    stage: str,
    category: str,
    reason: str,
    stopped_campaign: bool,
    study_dir: Path | str | None,
) -> dict[str, Any]:
    return {
        "phase_id": phase_id,
        "stage": stage,
        "failure_category": category,
        "failure_reason": reason,
        "stopped_campaign": stopped_campaign,
        "study_dir": "" if study_dir in ("", None) else str(study_dir),
    }


def _phase_output_root(base_dir: Path, phase_id: str, stage_name: str) -> Path:
    return base_dir / "phases" / phase_id / stage_name


def _append_failure_rows(
    rows: list[dict[str, Any]],
    *,
    phase_id: str,
    stage: str,
    categories: list[tuple[str, str]],
    stopped_campaign: bool,
    study_dir: Path | str | None,
) -> None:
    for category, reason in categories:
        rows.append(
            _failure_row(
                phase_id=phase_id,
                stage=stage,
                category=category,
                reason=reason,
                stopped_campaign=stopped_campaign,
                study_dir=study_dir,
            )
        )


def _algorithm_eval_failure_categories(summary: dict[str, Any]) -> list[tuple[str, str]]:
    overall = dict(summary.get("overall_decision", {}) or {})
    blocking_reasons = [str(reason) for reason in list(summary.get("blocking_reasons", []) or [])]
    categories: list[tuple[str, str]] = []
    if bool(overall.get("offline_ready_for_live_eval_v1")) is not True:
        categories.extend(
            (FAILURE_CATEGORY_ALGO_HARD, reason)
            for reason in (blocking_reasons or ["offline_ready_for_live_eval_v1=false"])
        )
    elif bool(overall.get("hard_regression_detected")):
        categories.extend((FAILURE_CATEGORY_ALGO_HARD, reason) for reason in (blocking_reasons or ["hard_regression_detected"]))
    elif bool(overall.get("soft_regression_detected")):
        categories.extend((FAILURE_CATEGORY_ALGO_SOFT, reason) for reason in (blocking_reasons or ["soft_regression_detected"]))
    elif overall.get("recommended_next_step") != "hold_for_live_eval":
        categories.append((FAILURE_CATEGORY_ALGO_HARD, str(overall.get("recommended_next_step"))))
    return categories


def _live_eval_failure_categories(summary: dict[str, Any]) -> list[tuple[str, str]]:
    overall = dict(summary.get("overall_decision", {}) or {})
    blocking_reasons = [str(reason) for reason in list(summary.get("blocking_reasons", []) or [])]
    categories: list[tuple[str, str]] = []
    direction_reasons = [reason for reason in blocking_reasons if "direction_mismatch" in reason]
    threshold_reasons = [reason for reason in blocking_reasons if "direction_mismatch" not in reason]
    if direction_reasons:
        categories.extend((FAILURE_CATEGORY_LIVE_DIRECTION, reason) for reason in direction_reasons)
    if bool(overall.get("hard_regression_detected")) and threshold_reasons:
        categories.extend((FAILURE_CATEGORY_LIVE_THRESHOLD, reason) for reason in threshold_reasons)
    if bool(overall.get("soft_regression_detected")):
        soft_reasons = [reason for reason in blocking_reasons if reason.startswith("soft_regression_")] or ["soft_regression_detected"]
        categories.extend((FAILURE_CATEGORY_LIVE_SOFT, reason) for reason in soft_reasons)
    if not categories and bool(overall.get("hard_regression_detected")):
        categories.append((FAILURE_CATEGORY_LIVE_THRESHOLD, "hard_regression_detected"))
    return categories


def _should_stop_after_phase(phase_class: str, failure_categories: list[tuple[str, str]]) -> tuple[bool, str]:
    if any(category == FAILURE_CATEGORY_LIVE_DIRECTION for category, _reason in failure_categories):
        return True, "direction_mismatch"
    if any(category == FAILURE_CATEGORY_ALGO_HARD for category, _reason in failure_categories):
        if phase_class == "probe_stability":
            return True, "probe_hard_regression"
        if phase_class == "confirm_robustness":
            return True, "confirm_hard_regression"
        return False, ""
    if any(category == FAILURE_CATEGORY_LIVE_THRESHOLD for category, _reason in failure_categories):
        if phase_class == "probe_stability":
            return True, "probe_hard_regression"
        if phase_class == "confirm_robustness":
            return True, "confirm_hard_regression"
        return False, ""
    if any(category == FAILURE_CATEGORY_LIVE_CAPTURE for category, _reason in failure_categories):
        return True, "live_capture_failure"
    return False, ""


def _phase_board_row(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase_id": result["phase_id"],
        "phase_class": result["phase_class"],
        "reference_tier": result["reference_tier"],
        "pulse_amplitude": result["pulse_amplitude"],
        "algorithm_eval_dir": result["algorithm_eval_dir"],
        "live_evaluation_dir": result["live_evaluation_dir"],
        "algorithm_eval_ready": result["algorithm_eval_ready"],
        "live_pair_target_success_v1": result["live_pair_target_success_v1"],
        "dominant_direction": result["dominant_direction"],
        "hard_regression_detected": result["hard_regression_detected"],
        "soft_regression_detected": result["soft_regression_detected"],
        "stopped_campaign": result["stopped_campaign"],
        "stop_reason": result["stop_reason"],
        "failure_categories": ",".join(result["failure_categories"]),
    }


def _scenario_board_rows(phase_result: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in phase_result["scenario_results"]:
        rows.append(
            {
                "phase_id": phase_result["phase_id"],
                "phase_class": phase_result["phase_class"],
                "stage_source": phase_result["stage_source"],
                "scenario": result["scenario"],
                "reference_tier": phase_result["reference_tier"],
                "ready_signal": result["ready_signal"],
                "hard_regression": result["hard_regression"],
                "soft_regression": result["soft_regression"],
                "dominant_direction": result["dominant_direction"],
                "median_active_pair_rate": result["median_active_pair_rate"],
                "median_baseline_pair_rate": result["median_baseline_pair_rate"],
                "median_pair_specificity": result["median_pair_specificity"],
                "median_pair_sign_consistency": result["median_pair_sign_consistency"],
                "median_pair_to_collective_ratio": result["median_pair_to_collective_ratio"],
                "pair_tier_range_specificity": result["pair_tier_range_specificity"],
                "blocking_reasons": ",".join(result["blocking_reasons"]),
            }
        )
    return rows


def render_ardupilot_a2_pair_target_live_campaign_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    lines = [
        "# ArduPilot A2 Pair-Target Live Campaign",
        "",
        f"- campaign_name: {payload['campaign']['campaign_name']}",
        f"- campaign_version: {payload['campaign']['campaign_version']}",
        f"- probe_stability_passed: {'yes' if overall['probe_stability_passed'] else 'no'}",
        f"- tier_robustness_passed: {'yes' if overall['tier_robustness_passed'] else 'no'}",
        f"- dominant_direction_consistent: {'yes' if overall['dominant_direction_consistent'] else 'no'}",
        f"- hard_regression_detected: {'yes' if overall['hard_regression_detected'] else 'no'}",
        f"- soft_regression_detected: {'yes' if overall['soft_regression_detected'] else 'no'}",
        f"- ready_for_live_evidence_review_v1: {'yes' if overall['ready_for_live_evidence_review_v1'] else 'no'}",
        f"- recommended_next_step: {overall['recommended_next_step']}",
        f"- blocking_reasons: {', '.join(payload['blocking_reasons']) if payload['blocking_reasons'] else 'none'}",
        "",
        "## Canonical Probe Stability",
        "",
    ]
    for phase in payload["phase_results"]:
        if phase["phase_class"] != "probe_stability":
            continue
        lines.append(
            f"- {phase['phase_id']}: "
            f"algorithm_eval_ready={algorithm_eval._format_metric(phase['algorithm_eval_ready'])}, "
            f"live_pair_target_success_v1={algorithm_eval._format_metric(phase['live_pair_target_success_v1'])}, "
            f"direction={phase['dominant_direction'] or 'n/a'}, "
            f"failures={', '.join(phase['failure_categories']) if phase['failure_categories'] else 'none'}"
        )
    lines.extend(
        [
            "",
            "## Tier Robustness",
            "",
        ]
    )
    for phase in payload["phase_results"]:
        if phase["phase_class"] not in {"micro_robustness", "confirm_robustness"}:
            continue
        lines.append(
            f"- {phase['phase_id']}: "
            f"algorithm_eval_ready={algorithm_eval._format_metric(phase['algorithm_eval_ready'])}, "
            f"live_pair_target_success_v1={algorithm_eval._format_metric(phase['live_pair_target_success_v1'])}, "
            f"direction={phase['dominant_direction'] or 'n/a'}, "
            f"failures={', '.join(phase['failure_categories']) if phase['failure_categories'] else 'none'}"
        )
    lines.extend(
        [
            "",
            "## Direction Consistency",
            "",
            f"- dominant_direction_consistent: {'yes' if overall['dominant_direction_consistent'] else 'no'}",
        ]
    )
    for phase in payload["phase_results"]:
        lines.append(f"- {phase['phase_id']}: {phase['dominant_direction'] or 'n/a'}")
    lines.extend(
        [
            "",
            "## Failure Taxonomy",
            "",
        ]
    )
    if payload["failure_taxonomy"]:
        for row in payload["failure_taxonomy"]:
            lines.append(
                f"- {row['phase_id'] or 'campaign'} / {row['stage']}: {row['failure_category']} ({row['failure_reason']})"
            )
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Manual Review Recommendation",
            "",
            f"- recommended_next_step: {overall['recommended_next_step']}",
            f"- ready_for_live_evidence_review_v1: {'yes' if overall['ready_for_live_evidence_review_v1'] else 'no'}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_ardupilot_a2_pair_target_live_campaign(
    *,
    campaign_spec: Path,
    vehicle: str = "ArduCopter",
    frame: str = "quad",
    skip_sitl: bool = False,
    skip_smoke: bool = False,
    skip_capture: bool = False,
    output_root: Path | None = None,
    enable_visualization: bool = False,
) -> dict[str, Any]:
    output_root = output_root.expanduser().resolve() if output_root is not None else None
    spec = _load_campaign_spec(campaign_spec, skip_capture=skip_capture)
    paths = _output_paths(output_root)

    failure_taxonomy_rows: list[dict[str, Any]] = []
    phase_results: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []
    smoke_matrix_dir: Path | None = None
    smoke_passed: bool | None = None
    stopped_campaign = False
    stop_reason = ""

    selected_scenarios = algorithm_eval._selected_scenarios(EXPECTED_SCENARIO_SCOPE)
    try:
        _target_dir, _target_manifest, target_summary = algorithm_eval._load_artifact_bundle(
            spec["a2_target_scout_dir"], "a2_target_scout.json"
        )
        _pair_dir, _pair_manifest, pair_summary = algorithm_eval._load_artifact_bundle(
            spec["a2_pair_target_dir"], "a2_pair_target_readiness.json"
        )
        preflight_reasons = []
        preflight_reasons.extend(algorithm_eval._validate_target_scout_summary(target_summary, selected_scenarios))
        preflight_reasons.extend(
            algorithm_eval._validate_pair_readiness_summary(pair_summary, selected_scenarios, EXPECTED_DIRECTION)
        )
        if preflight_reasons:
            stopped_campaign = True
            stop_reason = "preflight_artifact_mismatch"
            blocking_reasons.extend(preflight_reasons)
            _append_failure_rows(
                failure_taxonomy_rows,
                phase_id="",
                stage="preflight",
                categories=[(FAILURE_CATEGORY_PREFLIGHT, reason) for reason in preflight_reasons],
                stopped_campaign=True,
                study_dir="",
            )
    except Exception as exc:
        stopped_campaign = True
        stop_reason = "preflight_artifact_mismatch"
        blocking_reasons.append(str(exc))
        _append_failure_rows(
            failure_taxonomy_rows,
            phase_id="",
            stage="preflight",
            categories=[(FAILURE_CATEGORY_PREFLIGHT, str(exc))],
            stopped_campaign=True,
            study_dir="",
        )

    if not stopped_campaign and not skip_smoke:
        try:
            smoke_result = live_eval._run_guided_mode_smoke(
                vehicle=vehicle,
                frame=frame,
                skip_sitl=skip_sitl,
                enable_visualization=enable_visualization,
            )
            smoke_matrix_dir = Path(smoke_result["matrix_dir"]).expanduser().resolve()
            smoke_passed = bool(smoke_result["payload"].get("passed"))
            if smoke_passed is not True:
                stopped_campaign = True
                stop_reason = "smoke_gate_failure"
                reason = str(smoke_result["payload"].get("conclusion", "smoke_gate_failed"))
                blocking_reasons.append(reason)
                _append_failure_rows(
                    failure_taxonomy_rows,
                    phase_id="",
                    stage="smoke",
                    categories=[(FAILURE_CATEGORY_SMOKE, reason)],
                    stopped_campaign=True,
                    study_dir=smoke_matrix_dir,
                )
        except Exception as exc:
            stopped_campaign = True
            stop_reason = "smoke_gate_failure"
            blocking_reasons.append(str(exc))
            _append_failure_rows(
                failure_taxonomy_rows,
                phase_id="",
                stage="smoke",
                categories=[(FAILURE_CATEGORY_SMOKE, str(exc))],
                stopped_campaign=True,
                study_dir=smoke_matrix_dir,
            )

    for phase_id in spec["phase_order"]:
        phase_spec = dict(spec["phases"][phase_id])
        phase_result = {
            "phase_id": phase_id,
            "phase_class": phase_spec["phase_class"],
            "reference_tier": phase_spec["reference_tier"],
            "pulse_amplitude": phase_spec["pulse_amplitude"],
            "algorithm_eval_dir": "",
            "live_evaluation_dir": "",
            "algorithm_eval_ready": False,
            "live_pair_target_success_v1": False,
            "dominant_direction": "",
            "hard_regression_detected": False,
            "soft_regression_detected": False,
            "stopped_campaign": False,
            "stop_reason": "",
            "failure_categories": [],
            "stage_source": "algorithm_evaluation",
            "scenario_results": [],
        }
        if stopped_campaign:
            phase_results.append(phase_result)
            continue

        algorithm_summary: dict[str, Any] | None = None
        try:
            algorithm_dir = algorithm_eval.run_ardupilot_a2_pair_target_algorithm_evaluation(
                a2_target_scout_dir=spec["a2_target_scout_dir"],
                a2_pair_target_dir=spec["a2_pair_target_dir"],
                output_root=_phase_output_root(paths["base_dir"], phase_id, "algorithm_eval"),
                mode=algorithm_eval.EVALUATION_MODE,
                strategy=algorithm_eval.STRATEGY_NAME,
                scenario=phase_spec["scenario_scope"],
                reference_tier=phase_spec["reference_tier"],
                direction=phase_spec["direction"],
                pulse_amplitude=phase_spec["pulse_amplitude"],
                bias=None,
                pulse_count=phase_spec["pulse_count"],
                pulse_width_s=phase_spec["pulse_width_s"],
                pulse_gap_s=phase_spec["pulse_gap_s"],
            )
            algorithm_summary = _read_json(Path(algorithm_dir) / "summary" / "a2_pair_target_algorithm_evaluation.json")
            phase_result["algorithm_eval_dir"] = str(Path(algorithm_dir).resolve())
            algo_failure_categories = _algorithm_eval_failure_categories(algorithm_summary)
            phase_result["algorithm_eval_ready"] = (
                bool(algorithm_summary.get("overall_decision", {}).get("offline_ready_for_live_eval_v1")) is True
                and bool(algorithm_summary.get("overall_decision", {}).get("live_eval_required")) is True
                and algorithm_summary.get("overall_decision", {}).get("recommended_next_step") == "hold_for_live_eval"
            )
            phase_result["failure_categories"].extend(category for category, _ in algo_failure_categories)
            phase_result["hard_regression_detected"] = bool(
                algorithm_summary.get("overall_decision", {}).get("hard_regression_detected")
            )
            phase_result["soft_regression_detected"] = bool(
                algorithm_summary.get("overall_decision", {}).get("soft_regression_detected")
            )
            phase_result["scenario_results"] = [
                {
                    "scenario": str(result.get("scenario", "")),
                    "ready_signal": bool(result.get("reference_ready")),
                    "hard_regression": bool(result.get("hard_regression")),
                    "soft_regression": bool(result.get("soft_regression")),
                    "dominant_direction": str(result.get("dominant_direction", "")),
                    "median_active_pair_rate": result.get("median_active_pair_rate"),
                    "median_baseline_pair_rate": result.get("median_baseline_pair_rate"),
                    "median_pair_specificity": result.get("median_pair_specificity"),
                    "median_pair_sign_consistency": result.get("median_pair_sign_consistency"),
                    "median_pair_to_collective_ratio": result.get("median_pair_to_collective_ratio"),
                    "pair_tier_range_specificity": result.get("pair_tier_range_specificity"),
                    "blocking_reasons": list(result.get("blocking_reasons", []) or []),
                }
                for result in list(algorithm_summary.get("scenario_results", []) or [])
            ]
            if algo_failure_categories:
                stop_now, stop_code = _should_stop_after_phase(phase_spec["phase_class"], algo_failure_categories)
                blocking_reasons.extend(
                    f"{phase_id}:{reason}" for _category, reason in algo_failure_categories
                )
                _append_failure_rows(
                    failure_taxonomy_rows,
                    phase_id=phase_id,
                    stage="algorithm_evaluation",
                    categories=algo_failure_categories,
                    stopped_campaign=stop_now,
                    study_dir=algorithm_dir,
                )
                if stop_now:
                    stopped_campaign = True
                    stop_reason = stop_code
                    phase_result["stopped_campaign"] = True
                    phase_result["stop_reason"] = stop_code
                phase_results.append(phase_result)
                continue
        except Exception as exc:
            phase_result["failure_categories"].append(FAILURE_CATEGORY_ALGO_HARD)
            phase_result["hard_regression_detected"] = True
            phase_result["scenario_results"] = []
            blocking_reasons.append(f"{phase_id}:{exc}")
            stop_now, stop_code = _should_stop_after_phase(
                phase_spec["phase_class"],
                [(FAILURE_CATEGORY_ALGO_HARD, str(exc))],
            )
            _append_failure_rows(
                failure_taxonomy_rows,
                phase_id=phase_id,
                stage="algorithm_evaluation",
                categories=[(FAILURE_CATEGORY_ALGO_HARD, str(exc))],
                stopped_campaign=stop_now,
                study_dir=phase_result["algorithm_eval_dir"],
            )
            if stop_now:
                stopped_campaign = True
                stop_reason = stop_code
                phase_result["stopped_campaign"] = True
                phase_result["stop_reason"] = stop_code
            phase_results.append(phase_result)
            continue

        try:
            live_result = live_eval.run_ardupilot_a2_pair_target_live_evaluation(
                a2_target_scout_dir=spec["a2_target_scout_dir"],
                a2_pair_target_dir=spec["a2_pair_target_dir"],
                a2_algorithm_eval_dir=Path(phase_result["algorithm_eval_dir"]),
                vehicle=vehicle,
                frame=frame,
                skip_sitl=skip_sitl,
                skip_smoke=True,
                skip_capture=skip_capture,
                matrix_dir=phase_spec["matrix_dir"],
                output_root=_phase_output_root(paths["base_dir"], phase_id, "live_eval"),
                accepted_target=phase_spec["accepted_target"],
                max_attempts_per_config=phase_spec["max_attempts_per_config"],
                enable_visualization=enable_visualization,
            )
            live_summary = _read_json(
                Path(live_result["live_evaluation_dir"]) / "summary" / "a2_pair_target_live_evaluation.json"
            )
            phase_result["stage_source"] = "live_evaluation"
            phase_result["live_evaluation_dir"] = str(Path(live_result["live_evaluation_dir"]).resolve())
            phase_result["live_pair_target_success_v1"] = bool(
                live_summary.get("overall_decision", {}).get("live_pair_target_success_v1")
            )
            phase_result["dominant_direction"] = str(live_summary.get("overall_decision", {}).get("dominant_direction", ""))
            phase_result["hard_regression_detected"] = bool(
                live_summary.get("overall_decision", {}).get("hard_regression_detected")
            )
            phase_result["soft_regression_detected"] = bool(
                live_summary.get("overall_decision", {}).get("soft_regression_detected")
            )
            phase_result["scenario_results"] = [
                {
                    "scenario": str(result.get("scenario", "")),
                    "ready_signal": bool(result.get("live_ready")),
                    "hard_regression": bool(result.get("hard_regression")),
                    "soft_regression": bool(result.get("soft_regression")),
                    "dominant_direction": str(result.get("dominant_direction", "")),
                    "median_active_pair_rate": result.get("median_active_pair_rate"),
                    "median_baseline_pair_rate": result.get("median_baseline_pair_rate"),
                    "median_pair_specificity": result.get("median_pair_specificity"),
                    "median_pair_sign_consistency": result.get("median_pair_sign_consistency"),
                    "median_pair_to_collective_ratio": result.get("median_pair_to_collective_ratio"),
                    "pair_tier_range_specificity": result.get("pair_tier_range_specificity"),
                    "blocking_reasons": list(result.get("blocking_reasons", []) or []),
                }
                for result in list(live_summary.get("scenario_results", []) or [])
            ]
            live_failure_categories = _live_eval_failure_categories(live_summary)
            phase_result["failure_categories"].extend(category for category, _ in live_failure_categories)
            if live_failure_categories:
                stop_now, stop_code = _should_stop_after_phase(phase_spec["phase_class"], live_failure_categories)
                blocking_reasons.extend(f"{phase_id}:{reason}" for _category, reason in live_failure_categories)
                _append_failure_rows(
                    failure_taxonomy_rows,
                    phase_id=phase_id,
                    stage="live_evaluation",
                    categories=live_failure_categories,
                    stopped_campaign=stop_now,
                    study_dir=phase_result["live_evaluation_dir"],
                )
                if stop_now:
                    stopped_campaign = True
                    stop_reason = stop_code
                    phase_result["stopped_campaign"] = True
                    phase_result["stop_reason"] = stop_code
        except Exception as exc:
            phase_result["failure_categories"].append(FAILURE_CATEGORY_LIVE_CAPTURE)
            phase_result["hard_regression_detected"] = True
            blocking_reasons.append(f"{phase_id}:{exc}")
            _append_failure_rows(
                failure_taxonomy_rows,
                phase_id=phase_id,
                stage="live_evaluation",
                categories=[(FAILURE_CATEGORY_LIVE_CAPTURE, str(exc))],
                stopped_campaign=True,
                study_dir=phase_result["live_evaluation_dir"],
            )
            stopped_campaign = True
            stop_reason = "live_capture_failure"
            phase_result["stopped_campaign"] = True
            phase_result["stop_reason"] = stop_reason
        phase_results.append(phase_result)

    probe_results = [phase for phase in phase_results if phase["phase_class"] == "probe_stability"]
    tier_results = [phase for phase in phase_results if phase["phase_class"] in {"micro_robustness", "confirm_robustness"}]
    probe_stability_passed = bool(probe_results) and len(probe_results) == 2 and all(
        phase["live_pair_target_success_v1"] for phase in probe_results
    )
    tier_robustness_passed = bool(tier_results) and len(tier_results) == 2 and all(
        phase["live_pair_target_success_v1"] for phase in tier_results
    )
    direction_values = [phase["dominant_direction"] for phase in phase_results if phase["dominant_direction"]]
    dominant_direction_consistent = (
        len(direction_values) == len(phase_results)
        and all(direction == EXPECTED_DIRECTION for direction in direction_values)
    )
    hard_regression_detected = any(
        row["failure_category"]
        in {
            FAILURE_CATEGORY_PREFLIGHT,
            FAILURE_CATEGORY_SMOKE,
            FAILURE_CATEGORY_ALGO_HARD,
            FAILURE_CATEGORY_LIVE_CAPTURE,
            FAILURE_CATEGORY_LIVE_DIRECTION,
            FAILURE_CATEGORY_LIVE_THRESHOLD,
        }
        for row in failure_taxonomy_rows
    )
    soft_regression_detected = any(
        row["failure_category"] in {FAILURE_CATEGORY_ALGO_SOFT, FAILURE_CATEGORY_LIVE_SOFT}
        for row in failure_taxonomy_rows
    )
    ready_for_live_evidence_review_v1 = (
        probe_stability_passed
        and tier_robustness_passed
        and dominant_direction_consistent
        and not hard_regression_detected
        and not soft_regression_detected
    )
    if any(
        row["failure_category"] in {FAILURE_CATEGORY_PREFLIGHT, FAILURE_CATEGORY_SMOKE, FAILURE_CATEGORY_LIVE_CAPTURE}
        for row in failure_taxonomy_rows
    ):
        recommended_next_step = "fix_runtime_or_protocol"
    elif not probe_stability_passed:
        recommended_next_step = "rerun_probe_stability"
    elif not tier_robustness_passed or soft_regression_detected:
        recommended_next_step = "investigate_tier_regression"
    else:
        recommended_next_step = "publish_live_evidence_review"

    payload = {
        "campaign": {
            "campaign_name": spec["campaign_name"],
            "campaign_version": spec["campaign_version"],
            "phase_order": spec["phase_order"],
            "spec_path": str(spec["spec_path"]),
        },
        "source_artifacts": {
            "a2_target_scout_dir": str(spec["a2_target_scout_dir"]),
            "a2_pair_target_dir": str(spec["a2_pair_target_dir"]),
            "smoke_matrix_dir": str(smoke_matrix_dir) if smoke_matrix_dir is not None else "",
        },
        "phase_results": phase_results,
        "failure_taxonomy": failure_taxonomy_rows,
        "overall_decision": {
            "probe_stability_passed": probe_stability_passed,
            "tier_robustness_passed": tier_robustness_passed,
            "dominant_direction_consistent": dominant_direction_consistent,
            "hard_regression_detected": hard_regression_detected,
            "soft_regression_detected": soft_regression_detected,
            "ready_for_live_evidence_review_v1": ready_for_live_evidence_review_v1,
            "recommended_next_step": recommended_next_step,
            "stopped_early": stopped_campaign,
            "stop_reason": stop_reason,
        },
        "blocking_reasons": sorted(set(blocking_reasons)),
    }

    paths["report_path"].write_text(render_ardupilot_a2_pair_target_live_campaign_markdown(payload), encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(paths["phase_board_path"], [_phase_board_row(result) for result in phase_results], fieldnames=PHASE_BOARD_FIELDNAMES)
    scenario_rows = [row for result in phase_results for row in _scenario_board_rows(result)]
    write_rows_csv(paths["scenario_board_path"], scenario_rows, fieldnames=SCENARIO_BOARD_FIELDNAMES)
    write_rows_csv(paths["failure_taxonomy_path"], failure_taxonomy_rows, fieldnames=FAILURE_TAXONOMY_FIELDNAMES)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": STUDY_NAME,
            "study_id": paths["base_dir"].name,
            "campaign_spec": str(spec["spec_path"]),
            "source_artifacts": payload["source_artifacts"],
            "output_files": {
                "report": pair_readiness._relative_workspace_path(paths["report_path"]),
                "summary": pair_readiness._relative_workspace_path(paths["summary_path"]),
                "campaign_phase_board": pair_readiness._relative_workspace_path(paths["phase_board_path"]),
                "campaign_scenario_board": pair_readiness._relative_workspace_path(paths["scenario_board_path"]),
                "failure_taxonomy": pair_readiness._relative_workspace_path(paths["failure_taxonomy_path"]),
            },
            "summary": payload,
        },
    )
    return {
        "campaign_dir": paths["base_dir"],
        "smoke_matrix_dir": smoke_matrix_dir,
        "smoke_passed": smoke_passed,
        "probe_stability_passed": probe_stability_passed,
        "tier_robustness_passed": tier_robustness_passed,
        "ready_for_live_evidence_review_v1": ready_for_live_evidence_review_v1,
        "recommended_next_step": recommended_next_step,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the A2 pair-target medium live robustness campaign.")
    parser.add_argument("--campaign-spec", type=Path, required=True)
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--skip-capture", action="store_true")
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--enable-visualization", action="store_true")
    args = parser.parse_args(argv)

    result = run_ardupilot_a2_pair_target_live_campaign(
        campaign_spec=args.campaign_spec,
        vehicle=args.vehicle,
        frame=args.frame,
        skip_sitl=args.skip_sitl,
        skip_smoke=args.skip_smoke,
        skip_capture=args.skip_capture,
        output_root=args.output_root,
        enable_visualization=args.enable_visualization,
    )
    smoke_passed = result["smoke_passed"]
    print(f"guided_nogps_smoke_passed={'skipped' if smoke_passed is None else _stringify_output(smoke_passed)}")
    print(f"smoke_matrix_dir={_stringify_output(result['smoke_matrix_dir'])}")
    print(f"campaign_dir={_stringify_output(result['campaign_dir'])}")
    print(f"probe_stability_passed={_stringify_output(result['probe_stability_passed'])}")
    print(f"tier_robustness_passed={_stringify_output(result['tier_robustness_passed'])}")
    print(f"ready_for_live_evidence_review_v1={_stringify_output(result['ready_for_live_evidence_review_v1'])}")
    print(f"recommended_next_step={_stringify_output(result['recommended_next_step'])}")


if __name__ == "__main__":
    main()
