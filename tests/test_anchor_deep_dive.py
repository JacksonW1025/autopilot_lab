from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from linearity_analysis.anchor_deep_dive import DEFAULT_CANONICAL_STUDIES, run_formal_v2_anchor_deep_dive


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_run_anchor_deep_dive_real_artifacts(tmp_path: Path) -> None:
    if not all(path.exists() for path in DEFAULT_CANONICAL_STUDIES.values()):
        pytest.skip("canonical formal-v2 anchor artifact inputs are not available")

    study_dir = run_formal_v2_anchor_deep_dive(output_dir=tmp_path / "anchor_deep_dive")

    manifest_path = study_dir / "manifest.yaml"
    summary_path = study_dir / "summary" / "anchor_deep_dive.json"
    px4_table_path = study_dir / "tables" / "px4_a1_b1_matrix_comparison.csv"
    ardupilot_table_path = study_dir / "tables" / "ardupilot_a2_c1_d1_d2_boundary.csv"

    assert manifest_path.exists()
    assert summary_path.exists()
    assert px4_table_path.exists()
    assert ardupilot_table_path.exists()

    px4_rows = _read_csv_rows(px4_table_path)
    ardupilot_rows = _read_csv_rows(ardupilot_table_path)
    assert len(px4_rows) == 4
    assert len(ardupilot_rows) == 8

    px4_lookup = {row["anchor_id"]: row for row in px4_rows}
    ardupilot_lookup = {row["anchor_id"]: row for row in ardupilot_rows}

    assert float(px4_lookup["A1_baseline"]["median_test_r2"]) == pytest.approx(0.9995277520082995)
    assert float(ardupilot_lookup["A2_baseline"]["x_effective_condition_number"]) == pytest.approx(1.51018879444059)
    assert float(ardupilot_lookup["C1_baseline"]["x_effective_condition_number"]) > 1e9
    assert ardupilot_lookup["D1_baseline"]["generalization_status"] == "generalized_supported"
    assert ardupilot_lookup["D1_diagnostic"]["generalization_status"] == "not_generalized"
    assert ardupilot_lookup["D2_baseline"]["mask_empty_flag"] == "True"

    assert float(ardupilot_lookup["A2_baseline"]["pair_mask_jaccard"]) == pytest.approx(1.0)
    assert float(ardupilot_lookup["C1_baseline"]["pair_raw_top4_jaccard"]) == pytest.approx(1.0)
    assert float(ardupilot_lookup["D1_baseline"]["pair_raw_top4_jaccard"]) == pytest.approx(0.0)

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["px4_line"]["a1_generalization_status"] == "generalized_supported"
    assert "D2" in summary["ardupilot_line"]["mask_empty_families"]
    assert "C1" in summary["ardupilot_line"]["raw_stable_but_formally_blocked_families"]
