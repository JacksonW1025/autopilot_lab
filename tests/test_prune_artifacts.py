from __future__ import annotations

import json
from pathlib import Path

import linearity_analysis.prune_artifacts as prune_artifacts
from linearity_core.io import write_yaml


def test_build_prune_payload_keeps_canonical_docs_and_transitive_source_runs(tmp_path: Path, monkeypatch) -> None:
    artifacts_root = tmp_path / "artifacts"
    docs_root = tmp_path / "docs"
    studies_root = artifacts_root / "studies"
    px4_matrix_root = artifacts_root / "px4_matrix"
    ardupilot_matrix_root = artifacts_root / "ardupilot_matrix"
    raw_root = artifacts_root / "raw"
    for path in (studies_root, px4_matrix_root, ardupilot_matrix_root, raw_root / "px4", raw_root / "ardupilot", docs_root):
        path.mkdir(parents=True, exist_ok=True)

    keep_study = studies_root / "20260409_060620_px4_real_broad_ablation"
    keep_raw = raw_root / "px4" / "20260409_073245_px4_manual_pulse_train_throttle_r1"
    drop_study = studies_root / "20260408_000000_old_study"
    drop_raw = raw_root / "ardupilot" / "20260408_000000_old_run"
    for path in (keep_study, keep_raw, drop_study, drop_raw):
        (path / "dummy.txt").parent.mkdir(parents=True, exist_ok=True)
        (path / "dummy.txt").write_text("x", encoding="utf-8")

    write_yaml(
        keep_study / "manifest.yaml",
        {
            "study_name": "px4_real_broad_ablation",
            "source_run_dirs": [str(keep_raw)],
        },
    )
    report = docs_root / "MILESTONE_LINEAR_F_REPORT.md"
    appendix = docs_root / "MILESTONE_LINEAR_F_APPENDIX.md"
    report.write_text(f"see ../artifacts/studies/{keep_study.name}/reports/summary.md\n", encoding="utf-8")
    appendix.write_text("", encoding="utf-8")

    monkeypatch.setattr(prune_artifacts, "ARTIFACT_ROOT", artifacts_root)
    monkeypatch.setattr(prune_artifacts, "STUDY_ARTIFACT_ROOT", studies_root)
    monkeypatch.setattr(prune_artifacts, "PX4_MATRIX_ROOT", px4_matrix_root)
    monkeypatch.setattr(prune_artifacts, "ARDUPILOT_MATRIX_ROOT", ardupilot_matrix_root)
    monkeypatch.setattr(prune_artifacts, "RAW_ARTIFACT_ROOT", raw_root)
    monkeypatch.setattr(prune_artifacts, "DOCS_ROOT", docs_root)
    monkeypatch.setattr(prune_artifacts, "WORKSPACE_ROOT", tmp_path)
    monkeypatch.setattr(prune_artifacts, "CANONICAL_DOCS", [report, appendix])
    monkeypatch.setattr(prune_artifacts, "MANAGED_ROOTS", [studies_root, px4_matrix_root, ardupilot_matrix_root])

    payload = prune_artifacts.build_prune_payload(workspace_root=tmp_path, doc_paths=[report, appendix])
    keep_paths = {item["relative_path"] for item in payload["keep"]}
    drop_paths = {item["relative_path"] for item in payload["drop"]}
    assert f"artifacts/studies/{keep_study.name}" in keep_paths
    assert f"artifacts/raw/px4/{keep_raw.name}" in keep_paths
    assert f"artifacts/studies/{drop_study.name}" in drop_paths
    assert f"artifacts/raw/ardupilot/{drop_raw.name}" in drop_paths


def test_apply_prune_deletes_drop_candidates(tmp_path: Path) -> None:
    doomed = tmp_path / "artifacts" / "studies" / "old"
    doomed.mkdir(parents=True)
    (doomed / "dummy.txt").write_text("x", encoding="utf-8")
    payload = {
        "drop": [
            {
                "path": str(doomed),
                "relative_path": "artifacts/studies/old",
                "size_bytes": 1,
            }
        ]
    }
    result = prune_artifacts.apply_prune(payload)
    assert result["deleted_count"] == 1
    assert not doomed.exists()


def test_prune_main_writes_manifests(tmp_path: Path, monkeypatch) -> None:
    payload = {
        "workspace_root": str(tmp_path),
        "docs": [],
        "keep_count": 1,
        "drop_count": 1,
        "keep_bytes": 10,
        "drop_bytes": 20,
        "keep": [{"path": "/keep", "relative_path": "keep", "size_bytes": 10, "reasons": ["doc:report"]}],
        "drop": [{"path": "/drop", "relative_path": "drop", "size_bytes": 20}],
    }
    monkeypatch.setattr(prune_artifacts, "build_prune_payload", lambda **_kwargs: payload)
    output_dir = tmp_path / "metadata" / "artifact_prune"
    prune_artifacts.main(["--output-dir", str(output_dir)])
    keep_manifest = json.loads((output_dir / "keep_manifest.json").read_text(encoding="utf-8"))
    drop_manifest = json.loads((output_dir / "drop_manifest.json").read_text(encoding="utf-8"))
    assert keep_manifest["keep_count"] == 1
    assert drop_manifest["drop_count"] == 1
