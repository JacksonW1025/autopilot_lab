from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

from .paths import RAW_ARTIFACT_ROOT, STUDY_ARTIFACT_ROOT, raw_root_for_backend


def read_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False), encoding="utf-8")


def read_rows_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_single_row_csv(path: Path, row: dict[str, Any], fieldnames: list[str] | None = None) -> None:
    write_rows_csv(path, [row], fieldnames=fieldnames or list(row.keys()))


def capture_host_snapshot() -> dict[str, str]:
    uptime = subprocess.run(["uptime"], check=True, capture_output=True, text=True).stdout.strip()
    loadavg = Path("/proc/loadavg").read_text(encoding="utf-8").strip()
    return {"uptime": uptime, "loadavg": loadavg}


def ensure_raw_run_directories(backend: str, run_id: str, root: Path | None = None) -> dict[str, Path]:
    base_root = root or raw_root_for_backend(backend)
    base_dir = base_root / run_id
    telemetry_dir = base_dir / "telemetry"
    logs_dir = base_dir / "logs"
    metadata_dir = base_dir / "metadata"
    analysis_inputs_dir = base_dir / "analysis_inputs"
    for path in (base_dir, telemetry_dir, logs_dir, metadata_dir, analysis_inputs_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "base_dir": base_dir,
        "telemetry_dir": telemetry_dir,
        "logs_dir": logs_dir,
        "metadata_dir": metadata_dir,
        "analysis_inputs_dir": analysis_inputs_dir,
        "manifest_path": base_dir / "manifest.yaml",
        "notes_path": base_dir / "notes.md",
        "input_trace_path": telemetry_dir / "input_trace.csv",
        "canonical_samples_path": analysis_inputs_dir / "canonical_samples.csv",
    }


def ensure_study_directories(study_id: str, root: Path | None = None) -> dict[str, Path]:
    base_root = root or STUDY_ARTIFACT_ROOT
    base_dir = base_root / study_id
    prepared_dir = base_dir / "prepared"
    fits_dir = base_dir / "fits"
    reports_dir = base_dir / "reports"
    summary_dir = base_dir / "summary"
    for path in (base_dir, prepared_dir, fits_dir, reports_dir, summary_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "base_dir": base_dir,
        "prepared_dir": prepared_dir,
        "fits_dir": fits_dir,
        "reports_dir": reports_dir,
        "summary_dir": summary_dir,
        "manifest_path": base_dir / "manifest.yaml",
        "sample_table_path": prepared_dir / "sample_table.csv",
        "schema_inventory_path": prepared_dir / "schema_inventory.yaml",
        "summary_report_path": reports_dir / "summary.md",
        "comparison_report_path": reports_dir / "schema_comparison.md",
        "baseline_stability_report_path": reports_dir / "baseline_stability.md",
        "diagnostic_gate_report_path": reports_dir / "diagnostic_gate.md",
        "matrix_gallery_report_path": reports_dir / "matrix_gallery.md",
        "state_evolution_audit_report_path": reports_dir / "state_evolution_audit.md",
        "scenario_generalization_report_path": reports_dir / "scenario_generalization.md",
        "contract_audit_report_path": reports_dir / "contract_audit.md",
        "backend_compare_report_path": reports_dir / "backend_compare.md",
        "summary_json_path": summary_dir / "study_summary.json",
        "baseline_stability_json_path": summary_dir / "baseline_stability.json",
        "diagnostic_gate_json_path": summary_dir / "diagnostic_gate.json",
        "matrix_gallery_json_path": summary_dir / "matrix_gallery.json",
        "state_evolution_audit_json_path": summary_dir / "state_evolution_audit.json",
        "scenario_generalization_json_path": summary_dir / "scenario_generalization.json",
        "contract_audit_json_path": summary_dir / "contract_audit.json",
        "backend_compare_json_path": summary_dir / "backend_compare.json",
    }
