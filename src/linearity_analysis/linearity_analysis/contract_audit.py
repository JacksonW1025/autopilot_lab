from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from linearity_core.config import StudyConfig
from linearity_core.dataset import build_prepared_sample_table, prepared_sample_table_fieldnames
from linearity_core.io import ensure_study_directories, read_yaml, write_json, write_rows_csv, write_yaml
from linearity_core.study_artifacts import build_contract_audit_payload, render_contract_audit_markdown


def run_contract_audit(
    px4_run_dir: Path,
    ardupilot_run_dir: Path,
    *,
    output_root: Path | None = None,
) -> Path:
    px4_manifest = read_yaml(px4_run_dir / "manifest.yaml")
    config = StudyConfig.from_dict(px4_manifest.get("study_config", {}) or {})
    study_id = f"{datetime.now(timezone.utc).astimezone():%Y%m%d_%H%M%S}_cross_backend_contract_audit"
    paths = ensure_study_directories(study_id, root=output_root)

    table, inventory = build_prepared_sample_table([px4_run_dir, ardupilot_run_dir], config)
    write_rows_csv(paths["sample_table_path"], table.to_csv_rows(), fieldnames=prepared_sample_table_fieldnames(table.rows))
    write_yaml(paths["schema_inventory_path"], inventory)

    payload = build_contract_audit_payload(px4_run_dir, ardupilot_run_dir)
    paths["contract_audit_report_path"].write_text(render_contract_audit_markdown(payload), encoding="utf-8")
    write_json(paths["contract_audit_json_path"], payload)
    write_yaml(
        paths["manifest_path"],
        {
            "study_name": "cross_backend_contract_audit",
            "study_id": study_id,
            "px4_run_dir": str(px4_run_dir),
            "ardupilot_run_dir": str(ardupilot_run_dir),
            "summary": payload,
        },
    )
    return paths["base_dir"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Compare one accepted PX4 raw run and one accepted ArduPilot raw run against the frozen contract.")
    parser.add_argument("--px4-run", type=Path, required=True, help="accepted PX4 raw run directory")
    parser.add_argument("--ardupilot-run", type=Path, required=True, help="accepted ArduPilot raw run directory")
    parser.add_argument("--output-root", type=Path, default=None, help="optional study artifact root override")
    args = parser.parse_args(argv)

    study_dir = run_contract_audit(
        args.px4_run.expanduser().resolve(),
        args.ardupilot_run.expanduser().resolve(),
        output_root=args.output_root.expanduser().resolve() if args.output_root else None,
    )
    print(f"study_dir={study_dir}")


if __name__ == "__main__":
    main()
