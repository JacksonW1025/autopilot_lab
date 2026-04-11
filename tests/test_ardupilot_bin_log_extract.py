from __future__ import annotations

from pathlib import Path

import pytest

from ardupilot_mavlink_backend.bin_log_extract import extract_bin_log
from linearity_core.io import read_rows_csv
from tests.support import fixture_path


REAL_BIN_FIXTURE = fixture_path("raw", "ardupilot", "bin_fallback_fixture", "ardupilot.BIN")


@pytest.mark.skipif(not REAL_BIN_FIXTURE.exists(), reason="real ArduPilot BIN fixture unavailable")
def test_extract_bin_log_writes_extended_message_csvs(tmp_path: Path) -> None:
    summary = extract_bin_log(REAL_BIN_FIXTURE, tmp_path)

    assert summary["message_counts"]["ATT"] > 0
    assert summary["message_counts"]["RATE"] > 0
    assert summary["message_counts"]["POS"] > 0
    assert summary["message_counts"]["AHR2"] > 0
    assert summary["message_counts"]["BAT"] > 0
    assert summary["message_counts"]["MODE"] > 0
    assert summary["message_counts"]["ORGN"] > 0

    for filename in (
        "bin_att.csv",
        "bin_rate.csv",
        "bin_pos.csv",
        "bin_ahr2.csv",
        "bin_bat.csv",
        "bin_mode.csv",
        "bin_orgn.csv",
    ):
        assert read_rows_csv(tmp_path / filename)
