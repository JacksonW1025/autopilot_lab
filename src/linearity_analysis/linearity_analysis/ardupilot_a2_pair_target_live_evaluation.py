from __future__ import annotations

import argparse
import copy
import json
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

STUDY_NAME = "ardupilot_a2_pair_target_live_evaluation"
CAPTURE_TEMPLATE_PATH = CONFIG_ROOT / "ardupilot_diagnostic_guided_nogps_throttle_capture.yaml"
SMOKE_CONFIG_PATH = CONFIG_ROOT / "ardupilot_real_nominal_guided_nogps_capture.yaml"
SMOKE_REPEAT = 3
DEFAULT_ACCEPTED_TARGET = pair_readiness.ACCEPTED_TARGET
DEFAULT_MAX_ATTEMPTS_PER_CONFIG = 10

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
    "hard_regression",
    "soft_regression",
    "blocking_reasons",
]


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
        "generated_schedule_path": tables_dir / "generated_schedule.csv",
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
        item["study_name"] = study_name
        item["scenario"] = scenario
        item["flight_mode"] = algorithm_eval.TARGET_MODE
        item["config_profile"] = study_name
        item["seed"] = base_seed + index
        item["axis"] = "throttle"
        item["profile_type"] = "pulse_train"
        item["amplitude"] = float(algorithm_spec["pulse_amplitude"])
        item["bias"] = float(bias_by_scenario[scenario])
        item["perturbation_strategy"] = "a2_pair_target_live_evaluation_v1"
        item.setdefault("extras", {})
        item["extras"]["amplitude_tier"] = reference_tier
        item["extras"]["readiness_scenario"] = scenario
        item["extras"]["profile_family"] = "pulse_train"
        item["extras"]["pulse_count"] = int(algorithm_spec["pulse_count"])
        item["extras"]["pulse_width_s"] = float(algorithm_spec["pulse_width_s"])
        item["extras"]["pulse_gap_s"] = float(algorithm_spec["pulse_gap_s"])
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
        "hard_regression": result["hard_regression"],
        "soft_regression": result["soft_regression"],
        "blocking_reasons": ",".join(result["blocking_reasons"]),
    }


def render_ardupilot_a2_pair_target_live_evaluation_markdown(payload: dict[str, Any]) -> str:
    overall = payload["overall_decision"]
    algorithm_spec = payload["algorithm_spec"]
    lines = [
        "# ArduPilot A2 Pair-Target Live Evaluation",
        "",
        f"- live_pair_target_success_v1: {'yes' if overall['live_pair_target_success_v1'] else 'no'}",
        f"- hard_regression_detected: {'yes' if overall['hard_regression_detected'] else 'no'}",
        f"- soft_regression_detected: {'yes' if overall['soft_regression_detected'] else 'no'}",
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
    enable_visualization: bool = False,
) -> dict[str, Any]:
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

    attempts = [target_scout._analyze_attempt(row) for row in read_rows_csv(runs_manifest)]
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

    reference_thresholds = dict(algorithm_eval_summary.get("reference_thresholds", {}) or {})
    canonical_reference_metrics = dict(reference_thresholds.get("canonical_reference_metrics", {}) or {})
    blocking_reasons: list[str] = []
    scenario_results: list[dict[str, Any]] = []
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
        hard_regression = bool(scenario_blocking_reasons)
        soft_regression = bool(soft_reasons)
        live_ready = scenario_result["ready"] and not soft_regression and scenario_result["dominant_direction"] == direction
        blocking_reasons.extend(f"{reason}:{scenario_name}" if ":" not in reason else reason for reason in scenario_blocking_reasons)
        blocking_reasons.extend(soft_reasons)
        scenario_results.append(
            {
                **scenario_result,
                "reference_tier": reference_tier,
                "accepted_reference_tier_count": accepted_reference_tier_count,
                "live_ready": live_ready,
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
    live_pair_target_success_v1 = (
        bool(scenario_results)
        and all(result["live_ready"] for result in scenario_results)
        and not hard_regression_detected
        and not soft_regression_detected
        and dominant_direction == direction
    )
    if hard_regression_detected:
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
        "overall_decision": {
            "live_pair_target_success_v1": live_pair_target_success_v1,
            "hard_regression_detected": hard_regression_detected,
            "soft_regression_detected": soft_regression_detected,
            "dominant_direction": dominant_direction,
            "recommended_next_step": recommended_next_step,
            "scenario_status": scenario_status,
        },
        "blocking_reasons": sorted(set(blocking_reasons)),
    }

    paths = _output_paths(output_root)
    paths["report_path"].write_text(render_ardupilot_a2_pair_target_live_evaluation_markdown(payload), encoding="utf-8")
    write_json(paths["summary_path"], payload)
    write_rows_csv(
        paths["scenario_matrix_path"],
        [_flatten_live_scenario_result(result) for result in scenario_results],
        fieldnames=SCENARIO_MATRIX_FIELDNAMES,
    )
    write_rows_csv(paths["run_level_metrics_path"], run_level_rows, fieldnames=algorithm_eval.RUN_LEVEL_FIELDNAMES)
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
    parser.add_argument("--a2-target-scout-dir", type=Path, required=True)
    parser.add_argument("--a2-pair-target-dir", type=Path, required=True)
    parser.add_argument("--a2-algorithm-eval-dir", type=Path, required=True)
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--skip-capture", action="store_true")
    parser.add_argument("--matrix-dir", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--accepted-target", type=int, default=DEFAULT_ACCEPTED_TARGET)
    parser.add_argument("--max-attempts-per-config", type=int, default=DEFAULT_MAX_ATTEMPTS_PER_CONFIG)
    parser.add_argument("--enable-visualization", action="store_true")
    args = parser.parse_args(argv)

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
