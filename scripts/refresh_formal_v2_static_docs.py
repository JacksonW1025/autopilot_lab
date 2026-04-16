#!/usr/bin/env python3
from __future__ import annotations

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

from linearity_core.io import read_yaml


def _relative(target: Path) -> str:
    return f"../{target.resolve().relative_to(ROOT_DIR)}"


def _first_scenario_combo(study_dir: Path, preferred_statuses: list[str]) -> str:
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
    return "n/a"


def _targeted_summary(validation_dir: Path, mode_key: str) -> tuple[str, str]:
    payload = read_yaml(validation_dir / "summary" / "state_evolution_validation.json")
    section = dict(payload.get("modes", {}).get(mode_key, {}) or {})
    combo = str(section.get("positive_combo", "") or section.get("representative_combo", "") or "n/a")
    status = str(section.get("status", "unknown"))
    return status, combo


def _targeted_inputs(validation_dir: Path) -> list[tuple[str, str]]:
    payload = read_yaml(validation_dir / "summary" / "state_evolution_validation.json")
    lines: list[tuple[str, str]] = []
    for mode_key, mode_label in (("stabilize", "STABILIZE"), ("guided_nogps", "GUIDED_NOGPS")):
        section = dict(payload.get("modes", {}).get(mode_key, {}) or {})
        baseline_dir = str(section.get("baseline_dir", "") or "").strip()
        diagnostic_dir = str(section.get("diagnostic_dir", "") or "").strip()
        if baseline_dir:
            lines.append((f"{mode_label} targeted baseline", _relative(Path(baseline_dir))))
        if diagnostic_dir:
            lines.append((f"{mode_label} targeted diagnostic", _relative(Path(diagnostic_dir))))
    return lines


def write_xy_schema_guide(
    *,
    px4_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_baseline_dir: Path,
    ardupilot_diagnostic_dir: Path,
    validation_dir: Path,
) -> None:
    px4_combo = _first_scenario_combo(px4_baseline_dir, ["generalized_supported", "supported_but_local"])
    ardupilot_combo = _first_scenario_combo(ardupilot_baseline_dir, ["generalized_supported", "supported_but_local"])
    stabilize_status, stabilize_combo = _targeted_summary(validation_dir, "stabilize")
    guided_status, guided_combo = _targeted_summary(validation_dir, "guided_nogps")
    targeted_inputs = _targeted_inputs(validation_dir)

    lines = [
        "# X/Y Schema Guide",
        "",
        "## 先怎么读当前 Formal V2 结果",
        "",
        "如果你现在要读最新结果，不要再从 20260409 的 broad baseline 或准备性 artifact 开始。",
        "",
        "当前推荐顺序是：",
        "",
        "1. PX4 generalization full baseline",
        f"   - `{_relative(px4_baseline_dir)}`",
        "2. PX4 generalization full diagnostic",
        f"   - `{_relative(px4_diagnostic_dir)}`",
        "3. ArduPilot generalization full baseline",
        f"   - `{_relative(ardupilot_baseline_dir)}`",
        "4. ArduPilot generalization full diagnostic",
        f"   - `{_relative(ardupilot_diagnostic_dir)}`",
        "5. ArduPilot targeted state-evolution validation",
        f"   - `{_relative(validation_dir)}`",
        "",
        "理由很简单：Formal V2 现在同时回答“线性是否存在、是否跨 scenario 成立、以及 ArduPilot 的 state-evolution 在 mode-isolated 条件下是成熟正结论还是成熟负结论”。",
        "",
        "## 当前最值得先看的代表性组合",
        "",
        "### PX4：状态演化主线",
        "",
        f"- `{px4_combo}`",
        f"- 路径：`{_relative(px4_baseline_dir)}`",
        "",
        "### ArduPilot：当前最稳的跨场景主结构",
        "",
        f"- `{ardupilot_combo}`",
        f"- 路径：`{_relative(ardupilot_baseline_dir)}`",
        "",
        "### ArduPilot targeted：mode-isolated state-evolution",
        "",
        f"- STABILIZE：status=`{stabilize_status}`；combo=`{stabilize_combo}`",
        f"- GUIDED_NOGPS：status=`{guided_status}`；combo=`{guided_combo}`",
        f"- 路径：`{_relative(validation_dir)}`",
        *[f"- {label}：`{path}`" for label, path in targeted_inputs],
        "",
        "## 当前推荐的阅读方法",
        "",
        "1. 先看 generalization full 的 `summary.md` 与 `scenario_generalization.md`。",
        "2. 再看 targeted line 的 `state_evolution_validation.md`。",
        "3. 如果某个 state-evolution 组合高 `R2` 但结论仍谨慎，再一起看：",
        "   - `sparsity_overlap.md`",
        "   - `state_evolution_audit.md`",
        "",
        "## 当前最重要的阅读边界",
        "",
        "- `best_result` 不一定等于“最稳的正式结论”。",
        "- 对 ArduPilot 尤其要注意：高 `R2` 不等于已经得到稳定 state-evolution 结论，必须把 scenario generalization、条件数、稳定性和 sparsity overlap 一起看。",
    ]
    (ROOT_DIR / "docs" / "XY_SCHEMA_GUIDE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_experiment_protocol(
    *,
    px4_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_baseline_dir: Path,
    ardupilot_diagnostic_dir: Path,
    validation_dir: Path,
) -> None:
    targeted_inputs = _targeted_inputs(validation_dir)
    lines = [
        "# Experiment Protocol",
        "",
        "## 当前正式实验线",
        "",
        "当前仓库的正式结论已经切换到 `Formal V2`。",
        "",
        "它由两条同级正式线组成：",
        "",
        "- generalization full：回答“线性关系是否存在，以及它是否能跨 scenario 成立”。",
        "- ArduPilot targeted state-evolution validation：回答“在不混 mode 时，state-evolution 是否形成成熟正结论；否则是否可以成熟地下负结论”。",
        "",
        "## 当前正式顺序",
        "",
        "### PX4",
        "",
        f"1. 复用现有 generalization full baseline：`{_relative(px4_baseline_dir)}`",
        f"2. 复用现有 generalization full diagnostic：`{_relative(px4_diagnostic_dir)}`",
        "",
        "### ArduPilot",
        "",
        f"1. generalization full baseline：`{_relative(ardupilot_baseline_dir)}`",
        f"2. generalization full diagnostic：`{_relative(ardupilot_diagnostic_dir)}`",
        *[f"{index}. {label}：`{path}`" for index, (label, path) in enumerate(targeted_inputs, start=3)],
        f"{3 + len(targeted_inputs)}. targeted validation aggregate：`{_relative(validation_dir)}`",
        "",
        "## 历史完成项",
        "",
        "以下内容已移出 Formal V2 正式文档引用集，不再作为当前正式 compare 主输入：",
        "",
        "- `20260409` 的 broad baseline / diagnostic",
        "- ArduPilot `GUIDED_NOGPS` smoke",
        "- `STABILIZE` partial baseline",
        "- `STABILIZE` throttle-only diagnostic",
        "- cross-backend contract audit",
        "",
        "## 当前正式输出物",
        "",
        "每个 generalization full study 至少要输出：",
        "",
        "- `reports/summary.md`",
        "- `reports/scenario_generalization.md`",
        "- `reports/sparsity_overlap.md`",
        "- `summary/study_summary.json`",
        "- `summary/scenario_generalization.json`",
        "- `summary/sparsity_overlap.json`",
        "",
        "每个 targeted study 额外要输出：",
        "",
        "- `reports/state_evolution_audit.md`",
        "- `summary/state_evolution_audit.json`",
        "",
        "targeted 聚合还要输出：",
        "",
        "- `reports/state_evolution_validation.md`",
        "- `summary/state_evolution_validation.json`",
        "",
        "## 当前结论口径",
        "",
        "- `supported`：当前 study 中已经得到可接受的线性 `f`。",
        "- `generalized_supported`：当前 `supported` 结果在多个 scenario 下仍然稳定成立。",
        "- `mature_positive`：至少一个 strict-raw-linear state-evolution 组合同时在 baseline、diagnostic 和 sparse-edge overlap 上保持稳定。",
        "- `mature_negative`：state-evolution 长期表现为高 `R2` + 高条件数 + stable sparse edges，因此可以成熟地下负结论。",
    ]
    (ROOT_DIR / "docs" / "EXPERIMENT_PROTOCOL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if len(argv) != 5:
        raise SystemExit(
            "usage: refresh_formal_v2_static_docs.py <px4_baseline_dir> <px4_diagnostic_dir> <ardupilot_baseline_dir> <ardupilot_diagnostic_dir> <validation_dir>"
        )
    px4_baseline_dir = Path(argv[0]).expanduser().resolve()
    px4_diagnostic_dir = Path(argv[1]).expanduser().resolve()
    ardupilot_baseline_dir = Path(argv[2]).expanduser().resolve()
    ardupilot_diagnostic_dir = Path(argv[3]).expanduser().resolve()
    validation_dir = Path(argv[4]).expanduser().resolve()
    write_xy_schema_guide(
        px4_baseline_dir=px4_baseline_dir,
        px4_diagnostic_dir=px4_diagnostic_dir,
        ardupilot_baseline_dir=ardupilot_baseline_dir,
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
        validation_dir=validation_dir,
    )
    write_experiment_protocol(
        px4_baseline_dir=px4_baseline_dir,
        px4_diagnostic_dir=px4_diagnostic_dir,
        ardupilot_baseline_dir=ardupilot_baseline_dir,
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
        validation_dir=validation_dir,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
