#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
for pkg_src in (
    ROOT_DIR / "src" / "linearity_core",
    ROOT_DIR / "src" / "linearity_analysis",
):
    pkg_text = str(pkg_src)
    if pkg_text not in sys.path:
        sys.path.insert(0, pkg_text)

from linearity_analysis.matrix_gallery import generate_matrix_heatmaps_for_paths
from linearity_core.io import read_yaml


def _combo_parts(combo_text: str) -> tuple[str, str, str, str]:
    parts = [item.strip() for item in combo_text.split("|")]
    if len(parts) != 4:
        raise ValueError(f"invalid combo text: {combo_text}")
    return parts[0], parts[1], parts[2], parts[3]


def _fit_dir(study_dir: Path, combo_text: str) -> Path:
    x_schema, y_schema, model_name, pooling_mode = _combo_parts(combo_text)
    return study_dir / "fits" / f"{x_schema}__{y_schema}__{pooling_mode}" / model_name


def _scenario_combo(study_dir: Path, preferred_statuses: list[str]) -> str:
    payload = read_yaml(study_dir / "summary" / "scenario_generalization.json")
    for preferred in preferred_statuses:
        for entry in payload.get("entries", []) or []:
            if str(entry.get("generalization_status", "")).strip() == preferred:
                return " | ".join(
                    [
                        str(entry.get("x_schema", "")),
                        str(entry.get("y_schema", "")),
                        str(entry.get("model_name", "")),
                        str(entry.get("pooling_mode", "")),
                    ]
                )
    summary = read_yaml(study_dir / "summary" / "study_summary.json")
    for entry in summary.get("ranking", []) or []:
        if str(entry.get("support", "")).strip().lower() == "supported":
            return " | ".join(
                [
                    str(entry.get("x_schema", "")),
                    str(entry.get("y_schema", "")),
                    str(entry.get("model_name", "")),
                    str(entry.get("pooling_mode", "")),
                ]
            )
    raise ValueError(f"no supported combo found in {study_dir}")


def _targeted_combo(validation_dir: Path, mode_key: str) -> tuple[Path, str, str]:
    payload = read_yaml(validation_dir / "summary" / "state_evolution_validation.json")
    section = dict(payload.get("modes", {}).get(mode_key, {}) or {})
    combo_text = str(section.get("positive_combo", "") or section.get("representative_combo", ""))
    if not combo_text:
        raise ValueError(f"no targeted combo available for {mode_key}")
    baseline_dir = Path(str(section.get("baseline_dir", ""))).expanduser().resolve()
    return baseline_dir, combo_text, str(section.get("status", "unknown"))


def _ensure_heatmaps(fit_dir: Path) -> tuple[Path, Path]:
    matrix_csv = fit_dir / "matrix_f.csv"
    abs_png = fit_dir / "matrix_heatmap_abs.png"
    signed_png = fit_dir / "matrix_heatmap_signed.png"
    if not abs_png.exists() or not signed_png.exists():
        generate_matrix_heatmaps_for_paths([matrix_csv])
    return abs_png, signed_png


def _copy_pair(src_abs: Path, src_signed: Path, dst_abs: Path, dst_signed: Path) -> None:
    dst_abs.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_abs, dst_abs)
    shutil.copy2(src_signed, dst_signed)


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if len(argv) != 5:
        raise SystemExit(
            "usage: refresh_formal_v2_heatmaps.py <px4_baseline_dir> <px4_diagnostic_dir> <ardupilot_baseline_dir> <ardupilot_diagnostic_dir> <validation_dir>"
        )

    px4_baseline_dir = Path(argv[0]).expanduser().resolve()
    px4_diagnostic_dir = Path(argv[1]).expanduser().resolve()
    ardupilot_baseline_dir = Path(argv[2]).expanduser().resolve()
    _ = Path(argv[3]).expanduser().resolve()
    validation_dir = Path(argv[4]).expanduser().resolve()

    docs_dir = ROOT_DIR / "docs" / "figures" / "heatmaps"
    docs_dir.mkdir(parents=True, exist_ok=True)

    px4_baseline_combo = _scenario_combo(px4_baseline_dir, ["generalized_supported", "supported_but_local"])
    px4_diagnostic_combo = _scenario_combo(px4_diagnostic_dir, ["generalized_supported", "supported_but_local"])
    ardupilot_baseline_combo = _scenario_combo(ardupilot_baseline_dir, ["generalized_supported", "supported_but_local"])
    stabilize_dir, stabilize_combo, stabilize_status = _targeted_combo(validation_dir, "stabilize")
    guided_dir, guided_combo, guided_status = _targeted_combo(validation_dir, "guided_nogps")

    px4_baseline_abs, px4_baseline_signed = _ensure_heatmaps(_fit_dir(px4_baseline_dir, px4_baseline_combo))
    px4_diagnostic_abs, px4_diagnostic_signed = _ensure_heatmaps(_fit_dir(px4_diagnostic_dir, px4_diagnostic_combo))
    ap_baseline_abs, ap_baseline_signed = _ensure_heatmaps(_fit_dir(ardupilot_baseline_dir, ardupilot_baseline_combo))
    stabilize_abs, stabilize_signed = _ensure_heatmaps(_fit_dir(stabilize_dir, stabilize_combo))
    guided_abs, guided_signed = _ensure_heatmaps(_fit_dir(guided_dir, guided_combo))

    copies = [
        (
            px4_baseline_abs,
            px4_baseline_signed,
            docs_dir / "px4_baseline_generalized_main_abs.png",
            docs_dir / "px4_baseline_generalized_main_signed.png",
        ),
        (
            px4_diagnostic_abs,
            px4_diagnostic_signed,
            docs_dir / "px4_diagnostic_generalized_main_abs.png",
            docs_dir / "px4_diagnostic_generalized_main_signed.png",
        ),
        (
            ap_baseline_abs,
            ap_baseline_signed,
            docs_dir / "ardupilot_full_baseline_main_abs.png",
            docs_dir / "ardupilot_full_baseline_main_signed.png",
        ),
        (
            stabilize_abs,
            stabilize_signed,
            docs_dir / "ardupilot_targeted_stabilize_abs.png",
            docs_dir / "ardupilot_targeted_stabilize_signed.png",
        ),
        (
            guided_abs,
            guided_signed,
            docs_dir / "ardupilot_targeted_guided_nogps_abs.png",
            docs_dir / "ardupilot_targeted_guided_nogps_signed.png",
        ),
    ]
    for src_abs, src_signed, dst_abs, dst_signed in copies:
        _copy_pair(src_abs, src_signed, dst_abs, dst_signed)

    readme_lines = [
        "# Curated Heatmaps",
        "",
        "当前目录放的是 `Formal V2` 最值得直接看的几张热力图拷贝。",
        "",
        "## 1. PX4 generalization full baseline 主图",
        f"- 组合：`{px4_baseline_combo}`",
        f"- 来源矩阵目录：`../../../{_fit_dir(px4_baseline_dir, px4_baseline_combo).relative_to(ROOT_DIR)}/`",
        "- 图片：",
        "  - `px4_baseline_generalized_main_abs.png`",
        "  - `px4_baseline_generalized_main_signed.png`",
        "",
        "## 2. PX4 generalization full diagnostic 主图",
        f"- 组合：`{px4_diagnostic_combo}`",
        f"- 来源矩阵目录：`../../../{_fit_dir(px4_diagnostic_dir, px4_diagnostic_combo).relative_to(ROOT_DIR)}/`",
        "- 图片：",
        "  - `px4_diagnostic_generalized_main_abs.png`",
        "  - `px4_diagnostic_generalized_main_signed.png`",
        "",
        "## 3. ArduPilot generalization full baseline 主图",
        f"- 组合：`{ardupilot_baseline_combo}`",
        f"- 来源矩阵目录：`../../../{_fit_dir(ardupilot_baseline_dir, ardupilot_baseline_combo).relative_to(ROOT_DIR)}/`",
        "- 图片：",
        "  - `ardupilot_full_baseline_main_abs.png`",
        "  - `ardupilot_full_baseline_main_signed.png`",
        "",
        "## 4. ArduPilot targeted STABILIZE 代表图",
        f"- validation_status：`{stabilize_status}`",
        f"- 组合：`{stabilize_combo}`",
        f"- 来源矩阵目录：`../../../{_fit_dir(stabilize_dir, stabilize_combo).relative_to(ROOT_DIR)}/`",
        "- 图片：",
        "  - `ardupilot_targeted_stabilize_abs.png`",
        "  - `ardupilot_targeted_stabilize_signed.png`",
        "",
        "## 5. ArduPilot targeted GUIDED_NOGPS 代表图",
        f"- validation_status：`{guided_status}`",
        f"- 组合：`{guided_combo}`",
        f"- 来源矩阵目录：`../../../{_fit_dir(guided_dir, guided_combo).relative_to(ROOT_DIR)}/`",
        "- 图片：",
        "  - `ardupilot_targeted_guided_nogps_abs.png`",
        "  - `ardupilot_targeted_guided_nogps_signed.png`",
    ]
    (docs_dir / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
