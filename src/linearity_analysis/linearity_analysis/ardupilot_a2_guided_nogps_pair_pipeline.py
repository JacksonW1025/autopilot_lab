from __future__ import annotations

import argparse
import copy
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ardupilot_mavlink_backend.matrix_runner import run_matrix
from linearity_core.io import read_yaml, write_json, write_yaml
from linearity_core.paths import CONFIG_ROOT
from linearity_core.study_artifacts import build_guided_mode_smoke_payload, render_guided_mode_smoke_markdown

from .ardupilot_a2_pair_target_readiness import run_ardupilot_a2_pair_target_readiness
from .ardupilot_a2_target_scout import run_ardupilot_a2_target_scout
from .next_phase_decision_layer import (
    STUDY_NAME as DECISION_LAYER_STUDY_NAME,
    run_formal_v2_next_phase_decision_layer,
)
from .stage_checks import latest_study_dir_by_name

PIPELINE_NAME = "ardupilot_a2_guided_nogps_pair_pipeline"
SMOKE_CONFIG_PATH = CONFIG_ROOT / "ardupilot_real_nominal_guided_nogps_capture.yaml"
CAPTURE_TEMPLATE_PATH = CONFIG_ROOT / "ardupilot_diagnostic_guided_nogps_throttle_capture.yaml"
TARGET_SIGNAL = "pair_imbalance_12_vs_34"
TARGET_READY_STEP = "guided_nogps_pair_target_readiness"
PAIR_READY_PATH = "start_guided_nogps_pair_attack_v1"
PAIR_DOMINANT_DIRECTION = "12_gt_34"
TARGET_MODE = "GUIDED_NOGPS"
SMOKE_REPEAT = 3
DEFAULT_ACCEPTED_TARGET = 5
DEFAULT_MAX_ATTEMPTS_PER_CONFIG = 10
CAPTURE_SPECS = (
    ("nominal", "micro", 0.02, 0.0),
    ("nominal", "probe", 0.05, 0.0),
    ("nominal", "confirm", 0.10, 0.0),
    ("throttle_biased", "micro", 0.02, 0.04),
    ("throttle_biased", "probe", 0.05, 0.04),
    ("throttle_biased", "confirm", 0.10, 0.04),
)
DECISION_SOURCE_NAMES = {
    "anchor_deep_dive_dir": "formal_v2_anchor_deep_dive",
    "in_depth_analysis_dir": "formal_v2_in_depth_analysis",
    "a1_targeted_reproduction_dir": "px4_a1_roll_pitch_targeted_reproduction",
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


def _study_output_dir(output_root: Path | None, study_name: str) -> Path | None:
    if output_root is None:
        return None
    output_root = output_root.expanduser().resolve()
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S_%f}_{study_name}"
    return output_root / study_id


def _resolve_decision_sources() -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for key, study_name in DECISION_SOURCE_NAMES.items():
        study_dir = latest_study_dir_by_name(study_name)
        if study_dir is None:
            raise FileNotFoundError(f"missing required study: {study_name}")
        sources[key] = study_dir.expanduser().resolve()
    return sources


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
    payload = build_guided_mode_smoke_payload(run_dirs, target_mode=TARGET_MODE, target_consecutive_runs=SMOKE_REPEAT)
    _write_guided_smoke_artifacts(matrix_dir, payload)
    return {
        "matrix_dir": matrix_dir,
        "payload": payload,
    }


def _generate_capture_configs(temp_dir: Path) -> list[Path]:
    payload = read_yaml(CAPTURE_TEMPLATE_PATH)
    base_seed = int(payload.get("seed", 0) or 0)
    config_paths: list[Path] = []
    for index, (scenario, tier, amplitude, bias) in enumerate(CAPTURE_SPECS):
        item = copy.deepcopy(payload)
        study_name = f"{PIPELINE_NAME}_{scenario}_{tier}"
        item["study_name"] = study_name
        item["scenario"] = scenario
        item["flight_mode"] = TARGET_MODE
        item["config_profile"] = study_name
        item["seed"] = base_seed + index
        item["axis"] = "throttle"
        item["profile_type"] = "pulse_train"
        item["amplitude"] = amplitude
        item["bias"] = bias
        item["perturbation_strategy"] = "a2_guided_nogps_pair_pipeline_v1"
        item.setdefault("extras", {})
        item["extras"]["amplitude_tier"] = tier
        item["extras"]["readiness_scenario"] = scenario
        item["extras"]["profile_family"] = "pulse_train"
        item["extras"]["pulse_count"] = 5
        item["extras"]["pulse_width_s"] = 0.35
        item["extras"]["pulse_gap_s"] = 0.95
        item["extras"]["pipeline_family"] = PIPELINE_NAME
        item["extras"]["pipeline_protocol_version"] = "v1"
        item["extras"]["pipeline_target_signal"] = TARGET_SIGNAL
        item["extras"]["pipeline_stage"] = "main_capture"
        output_path = temp_dir / f"{study_name}.yaml"
        write_yaml(output_path, item)
        config_paths.append(output_path)
    return config_paths


def _validate_target_scout(summary: dict[str, Any]) -> None:
    overall = dict(summary.get("overall_decision", {}) or {})
    scenario_results = list(summary.get("scenario_results", []) or [])
    scenario_targets = {
        str(result.get("scenario", "")): str(result.get("recommended_target", ""))
        for result in scenario_results
        if str(result.get("flight_mode", "")).upper() == TARGET_MODE
    }
    if overall.get("recommended_mode") != TARGET_MODE:
        raise RuntimeError(f"A2 target scout gate failed: recommended_mode={overall.get('recommended_mode')}")
    if overall.get("recommended_next_target") != TARGET_SIGNAL:
        raise RuntimeError(f"A2 target scout gate failed: recommended_next_target={overall.get('recommended_next_target')}")
    if overall.get("recommended_next_step") != TARGET_READY_STEP:
        raise RuntimeError(f"A2 target scout gate failed: recommended_next_step={overall.get('recommended_next_step')}")
    if scenario_targets != {"nominal": TARGET_SIGNAL, "throttle_biased": TARGET_SIGNAL}:
        raise RuntimeError(f"A2 target scout gate failed: scenario_targets={scenario_targets}")


def _validate_pair_target_readiness(summary: dict[str, Any]) -> None:
    overall = dict(summary.get("overall_decision", {}) or {})
    scenario_status = dict(overall.get("scenario_status", {}) or {})
    if bool(overall.get("ready_for_pair_attack_v1")) is not True:
        raise RuntimeError(
            f"A2 pair readiness gate failed: ready_for_pair_attack_v1={overall.get('ready_for_pair_attack_v1')}"
        )
    if overall.get("recommended_path") != PAIR_READY_PATH:
        raise RuntimeError(f"A2 pair readiness gate failed: recommended_path={overall.get('recommended_path')}")
    if overall.get("dominant_direction") != PAIR_DOMINANT_DIRECTION:
        raise RuntimeError(f"A2 pair readiness gate failed: dominant_direction={overall.get('dominant_direction')}")
    if scenario_status.get("nominal") is not True or scenario_status.get("throttle_biased") is not True:
        raise RuntimeError(f"A2 pair readiness gate failed: scenario_status={scenario_status}")


def _validate_decision_layer(summary: dict[str, Any]) -> None:
    overall = dict(summary.get("overall_recommendation", {}) or {})
    if overall.get("default_entry") != "A2":
        raise RuntimeError(f"A2 decision layer gate failed: default_entry={overall.get('default_entry')}")


def run_ardupilot_a2_guided_nogps_pair_pipeline(
    *,
    vehicle: str = "ArduCopter",
    frame: str = "quad",
    skip_sitl: bool = False,
    skip_smoke: bool = False,
    skip_capture: bool = False,
    matrix_dir: Path | None = None,
    output_root: Path | None = None,
    accepted_target: int = DEFAULT_ACCEPTED_TARGET,
    max_attempts_per_config: int = DEFAULT_MAX_ATTEMPTS_PER_CONFIG,
    skip_decision_layer: bool = False,
    enable_visualization: bool = False,
) -> dict[str, Any]:
    output_root = output_root.expanduser().resolve() if output_root is not None else None
    if matrix_dir is not None and not skip_capture:
        raise ValueError("--matrix-dir is only allowed together with --skip-capture")
    if skip_capture and matrix_dir is None:
        raise ValueError("--matrix-dir is required when --skip-capture is set")

    decision_sources = None if skip_decision_layer else _resolve_decision_sources()

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
        with tempfile.TemporaryDirectory(prefix=f"{PIPELINE_NAME}_") as temp_dir_name:
            config_paths = _generate_capture_configs(Path(temp_dir_name))
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

    a2_target_scout_dir = run_ardupilot_a2_target_scout(runs_manifest=runs_manifest, output_root=output_root)
    target_scout_summary = _read_json(a2_target_scout_dir / "summary" / "a2_target_scout.json")
    _validate_target_scout(target_scout_summary)

    a2_pair_target_dir = run_ardupilot_a2_pair_target_readiness(runs_manifest=runs_manifest, output_root=output_root)
    pair_target_summary = _read_json(a2_pair_target_dir / "summary" / "a2_pair_target_readiness.json")
    _validate_pair_target_readiness(pair_target_summary)

    decision_layer_dir: Path | None = None
    if not skip_decision_layer:
        if decision_sources is None:
            raise RuntimeError("decision sources are required when decision layer is enabled")
        decision_layer_dir = run_formal_v2_next_phase_decision_layer(
            anchor_deep_dive_dir=decision_sources["anchor_deep_dive_dir"],
            in_depth_analysis_dir=decision_sources["in_depth_analysis_dir"],
            a2_pair_target_dir=a2_pair_target_dir,
            a1_targeted_reproduction_dir=decision_sources["a1_targeted_reproduction_dir"],
            output_dir=_study_output_dir(output_root, DECISION_LAYER_STUDY_NAME),
        )
        decision_summary = _read_json(decision_layer_dir / "summary" / "next_phase_decision_layer.json")
        _validate_decision_layer(decision_summary)

    return {
        "guided_nogps_smoke_passed": smoke_passed,
        "smoke_matrix_dir": smoke_matrix_dir,
        "matrix_dir": resolved_matrix_dir,
        "a2_target_scout_dir": a2_target_scout_dir,
        "a2_pair_target_dir": a2_pair_target_dir,
        "decision_layer_dir": decision_layer_dir,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the A2 GUIDED_NOGPS pair pipeline from smoke through decision refresh.")
    parser.add_argument("--vehicle", default="ArduCopter")
    parser.add_argument("--frame", default="quad")
    parser.add_argument("--skip-sitl", action="store_true")
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--skip-capture", action="store_true")
    parser.add_argument("--matrix-dir", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--accepted-target", type=int, default=DEFAULT_ACCEPTED_TARGET)
    parser.add_argument("--max-attempts-per-config", type=int, default=DEFAULT_MAX_ATTEMPTS_PER_CONFIG)
    parser.add_argument("--skip-decision-layer", action="store_true")
    parser.add_argument("--enable-visualization", action="store_true")
    args = parser.parse_args(argv)

    result = run_ardupilot_a2_guided_nogps_pair_pipeline(
        vehicle=args.vehicle,
        frame=args.frame,
        skip_sitl=args.skip_sitl,
        skip_smoke=args.skip_smoke,
        skip_capture=args.skip_capture,
        matrix_dir=args.matrix_dir,
        output_root=args.output_root,
        accepted_target=args.accepted_target,
        max_attempts_per_config=args.max_attempts_per_config,
        skip_decision_layer=args.skip_decision_layer,
        enable_visualization=args.enable_visualization,
    )
    smoke_value = "skipped" if result["guided_nogps_smoke_passed"] is None else _stringify_output(result["guided_nogps_smoke_passed"])
    print(f"guided_nogps_smoke_passed={smoke_value}")
    print(f"smoke_matrix_dir={_stringify_output(result['smoke_matrix_dir'])}")
    print(f"matrix_dir={_stringify_output(result['matrix_dir'])}")
    print(f"a2_target_scout_dir={_stringify_output(result['a2_target_scout_dir'])}")
    print(f"a2_pair_target_dir={_stringify_output(result['a2_pair_target_dir'])}")
    print(f"decision_layer_dir={_stringify_output(result['decision_layer_dir'])}")


if __name__ == "__main__":
    main()
