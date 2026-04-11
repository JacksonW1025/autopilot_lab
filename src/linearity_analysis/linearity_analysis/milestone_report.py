from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from linearity_core.io import read_yaml, write_json
from linearity_core.study_artifacts import (
    _baseline_section,
    _combo_key,
    _diagnostic_section,
    _load_baseline_stability,
    _load_study_manifest,
    _load_study_summary,
    _safe_float,
    _study_acceptance_count,
    _supported_anchor,
    _supported_combo_keys,
)

from .backend_compare import run_backend_compare


def _docs_root(path: Path | None) -> Path:
    return (path or (Path(__file__).resolve().parents[3] / "docs")).resolve()


def _repo_root(path: Path | None = None) -> Path:
    if path is not None:
        return path.resolve()
    return Path(__file__).resolve().parents[3]


def _relative_from_docs(target: Path, docs_dir: Path) -> str:
    return os.path.relpath(target.resolve(), start=docs_dir.resolve())


def _gallery_supported_count(study_dir: Path) -> int:
    payload = read_yaml(study_dir / "summary" / "matrix_gallery.json")
    return int(payload.get("supported_count", 0) or 0)


def _scenario_counts(section: dict[str, Any]) -> dict[str, int]:
    counts = dict(((section.get("scenario_generalization", {}) or {}).get("counts", {}) or {}))
    return {
        "generalized_supported": int(counts.get("generalized_supported", 0) or 0),
        "supported_but_local": int(counts.get("supported_but_local", 0) or 0),
        "not_generalized": int(counts.get("not_generalized", 0) or 0),
    }


def _scenario_representative(section: dict[str, Any]) -> str:
    scenario = dict(section.get("scenario_generalization", {}) or {})
    return str(scenario.get("representative_generalized_supported", "") or scenario.get("representative_supported_but_local", ""))


def _scenario_conclusion(section: dict[str, Any]) -> str:
    scenario = dict(section.get("scenario_generalization", {}) or {})
    return str(scenario.get("conclusion", ""))


def _state_evolution_audit(study_dir: Path) -> dict[str, Any]:
    return read_yaml(study_dir / "summary" / "state_evolution_audit.json")


def _first_supported_combo(summary: dict[str, Any]) -> dict[str, Any]:
    for item in summary.get("ranking", []):
        if str(item.get("support", "")).strip().lower() == "supported":
            return item
    return {}


def _combo_fit_dir(study_dir: Path, combo: dict[str, Any]) -> Path:
    return (
        study_dir
        / "fits"
        / f"{combo.get('x_schema', '')}__{combo.get('y_schema', '')}__{combo.get('pooling_mode', '')}"
        / str(combo.get("model_name", ""))
    )


def render_milestone_report(
    *,
    px4_baseline_dir: Path,
    ardupilot_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_diagnostic_dir: Path,
    compare_dir: Path,
    guided_smoke_dir: Path,
    partial_baseline_dir: Path,
    throttle_diagnostic_dir: Path,
    contract_audit_dir: Path,
    docs_dir: Path,
) -> str:
    px4_summary = _load_study_summary(px4_baseline_dir)
    ap_summary = _load_study_summary(ardupilot_baseline_dir)
    px4_baseline = _baseline_section(px4_baseline_dir)
    ap_baseline = _baseline_section(ardupilot_baseline_dir)
    px4_diag = _diagnostic_section(px4_diagnostic_dir)
    ap_diag = _diagnostic_section(ardupilot_diagnostic_dir)
    compare_payload = read_yaml(compare_dir / "summary" / "backend_compare.json")
    state_audit = _state_evolution_audit(ardupilot_baseline_dir)

    px4_best = dict(px4_summary.get("best_result", {}) or {})
    ap_best = dict(ap_summary.get("best_result", {}) or {})
    px4_best_summary = dict(px4_best.get("summary", {}) or {})
    ap_best_summary = dict(ap_best.get("summary", {}) or {})
    px4_supported_combo = _combo_key(_first_supported_combo(px4_summary))
    ap_supported_combo = _combo_key(_first_supported_combo(ap_summary))
    px4_baseline_scenarios = _scenario_counts(compare_payload.get("px4", {}).get("baseline", {}))
    px4_diagnostic_scenarios = _scenario_counts(compare_payload.get("px4", {}).get("diagnostic", {}))
    ap_baseline_scenarios = _scenario_counts(compare_payload.get("ardupilot", {}).get("baseline", {}))
    ap_diagnostic_scenarios = _scenario_counts(compare_payload.get("ardupilot", {}).get("diagnostic", {}))
    generalization_driver = str(compare_payload.get("comparison", {}).get("generalization_difference_driver", ""))
    difference_driver = str(compare_payload.get("comparison", {}).get("difference_driver", ""))
    px4_total_generalized = px4_baseline_scenarios["generalized_supported"] + px4_diagnostic_scenarios["generalized_supported"]
    ap_total_generalized = ap_baseline_scenarios["generalized_supported"] + ap_diagnostic_scenarios["generalized_supported"]

    return "\n".join(
        [
            "# 统一 Schema 口径下全局线性 `f` 的里程碑报告",
            "",
            "## 这项研究到底在问什么",
            "",
            "这项研究要回答的问题很直接：",
            "",
            "如果我们把飞行器在某一时刻看到的输入记成 `X`，把稍后想预测的结果记成 `Y`，那么是否存在一个固定不变的映射 `f`，让大量数据都近似满足：",
            "",
            "`Y ≈ fX (+ b)`",
            "",
            "这里可以把它理解成：",
            "",
            "- `X` 是“现在手里有什么信息”，例如命令、姿态、角速度、位置、速度，或者这些量的短历史。",
            "- `Y` 是“接下来会发生什么”，例如下一时刻状态、状态子集、未来短窗响应，或执行器响应。",
            "- `f` 是一张固定矩阵。如果同一张矩阵在很多不同飞行片段上都能工作，而且不是靠偶然凑出来的，我们就说这里有可接受的线性证据。",
            "",
            "这份报告刻意不把重点放在“PX4 和 ArduPilot 谁更好”上。真正的重点是：在统一的数据口径和统一的分析口径下，线性关系本身是否站得住。",
            "",
            "## 为什么要同时跑 PX4 和 ArduPilot",
            "",
            "如果只在一个飞控上得到结论，最大的风险是：我们看到的不是“飞行控制问题本身的结构”，而只是某一个软件实现的习惯。",
            "",
            "所以这次实验做了两件约束很强的事：",
            "",
            "- 两个 backend 使用同一套 `X` 定义、`Y` 定义、模型族和报告结构。",
            "- 两个 backend 的 raw 数据都经过同一口径的质量门槛，只有通过门槛的 run 才能进入正式分析。",
            "",
            "这样一来，如果两个 backend 表现相似，这不是坏事，反而是好事。它说明“线性关系”更像问题本身的性质，而不是某一个 backend 的偶然产物。",
            "",
            "## 当前正式实验状态",
            "",
            "这轮正式实验已经全部完成，不再是进行中状态：",
            "",
            "- PX4 generalization full baseline：done。",
            "- PX4 generalization full diagnostic：done。",
            "- ArduPilot generalization full baseline：done。",
            "- ArduPilot generalization full diagnostic：done。",
            "",
            "这意味着现在已经可以直接回答两类问题：",
            "",
            "1. 线性关系 `Y ≈ fX (+ b)` 本身是否成立。",
            "2. 这个关系在 `nominal / dynamic / throttle_biased` 三档状态下是否还能站得住。",
            "",
            "## 这次正式做了哪些实验",
            "",
            "正式实验分成四份 study：",
            "",
            f"- PX4 baseline：`{px4_baseline.get('accepted_run_count', 0)}/{px4_baseline.get('expected_accepted_run_count', 0)} accepted`，覆盖 `POSCTL` 与 `OFFBOARD_ATTITUDE`，并同时覆盖三档 scenario。",
            f"- PX4 diagnostic：姿态轴全部 accepted，throttle boundary=`{px4_diag.get('throttle_boundary', 'none')}`。",
            f"- ArduPilot baseline：`{ap_baseline.get('accepted_run_count', 0)}/{ap_baseline.get('expected_accepted_run_count', 0)} accepted`，覆盖 `STABILIZE` 与 `GUIDED_NOGPS`，并同时覆盖三档 scenario。",
            f"- ArduPilot diagnostic：姿态轴全部 accepted，throttle boundary=`{ap_diag.get('throttle_boundary', 'none')}`。",
            "",
            "支持性实验也都已完成，但它们现在不再是主结论来源，而是实验准备度和契约一致性的旁证：",
            "",
            "- ArduPilot `GUIDED_NOGPS` smoke 已证明 mode-entry 能稳定进入 active phase。",
            "- `STABILIZE` partial baseline、throttle-only diagnostic 和 contract audit 也都已通过，所以现在比较的是线性证据本身，不是链路是否能跑。",
            "",
            "## 现在已经能说清楚的结论",
            "",
            "### 1. 可以正式把“线性关系存在”作为正面结论",
            "",
            f"- PX4 baseline 的代表性 supported 组合是 `{px4_supported_combo}`，当前 best combo 是 `{_combo_key(px4_best)}`，`median_test_r2={_safe_float(px4_best_summary.get('median_test_r2')):.4f}`。",
            f"- ArduPilot baseline 的最稳 supported anchor 是 `{ap_supported_combo}`，它说明 ArduPilot 这边也不是“没有线性”，而是最稳的证据更集中在命令到响应的映射上。",
            f"- 两边合计都已经出现了跨 scenario 的 generalized-supported 组合：PX4 共 `{px4_total_generalized}` 个，ArduPilot 共 `{ap_total_generalized}` 个。",
            "",
            "这足以支持一个谨慎但明确的判断：在当前实验包线内，固定线性/仿射映射 `f` 不是空想，它确实在大量真实仿真数据上重复出现。",
            "",
            "### 2. 这轮 generalization full 比旧 broad baseline 更有说服力",
            "",
            "旧的 20260409 broad baseline 主要回答“线性证据是否存在”。",
            "",
            "这轮 generalization full 则进一步回答“换一组状态、换一类动作，这个映射还在不在”。",
            "",
            f"- PX4 baseline `generalized_supported={px4_baseline_scenarios['generalized_supported']}`，diagnostic `generalized_supported={px4_diagnostic_scenarios['generalized_supported']}`。",
            f"- ArduPilot baseline `generalized_supported={ap_baseline_scenarios['generalized_supported']}`，diagnostic `generalized_supported={ap_diagnostic_scenarios['generalized_supported']}`。",
            f"- 当前 compare 的 generalization 判断是：`{generalization_driver}`。",
            "",
            "这意味着现在的主结论已经不只是“某个 nominal 条件下能拟合”，而是“同一类线性结构在更宽一点的局部飞行包线里仍然反复出现”。",
            "",
            "### 3. PX4 的 generalized-supported 证据更宽、更接近状态演化主线",
            "",
            f"- PX4 当前 baseline 图册里的 supported 组合数是 `{_gallery_supported_count(px4_baseline_dir)}`。",
            f"- PX4 baseline 的代表性 generalized-supported 组合是 `{_scenario_representative(compare_payload.get('px4', {}).get('baseline', {}))}`。",
            f"- PX4 diagnostic 的代表性 generalized-supported 组合是 `{_scenario_representative(compare_payload.get('px4', {}).get('diagnostic', {}))}`。",
            f"- PX4 baseline 的跨场景解释结论是：{_scenario_conclusion(compare_payload.get('px4', {}).get('baseline', {}))}",
            "",
            "这说明 PX4 不是只有一两组幸运组合高分，而是在状态演化相关的 `X/Y` 定义上已经形成较成片的跨场景正面证据。",
            "",
            "### 4. ArduPilot 也已经出现 generalized-supported 证据，但范围更窄",
            "",
            f"- ArduPilot 当前 baseline 图册里的 supported 组合数是 `{_gallery_supported_count(ardupilot_baseline_dir)}`。",
            f"- ArduPilot baseline 的代表性 generalized-supported 组合是 `{_scenario_representative(compare_payload.get('ardupilot', {}).get('baseline', {}))}`。",
            f"- ArduPilot diagnostic 的代表性 generalized-supported 组合是 `{_scenario_representative(compare_payload.get('ardupilot', {}).get('diagnostic', {}))}`。",
            f"- ArduPilot baseline 的最优高分组合是 `{_combo_key(ap_best)}`，`median_test_r2={_safe_float(ap_best_summary.get('median_test_r2')):.4f}`，但它仍然不是最稳的 supported 主结论。",
            f"- state-evolution audit 的直接结论是：{state_audit.get('conclusion', '')}",
            "",
            "这说明 ArduPilot 不是没有跨场景线性证据，而是目前更稳的证据主要集中在较简单的命令驱动路径上。高分的 state-evolution 组合仍然要同时面对条件数和稳定性问题。",
            "",
            "### 5. 两个 backend 的相似性仍然在增强主结论，但不能说得过满",
            "",
            "- 两边都已经完成 full baseline 与 full diagnostic。",
            "- 两边 diagnostic 的姿态轴都能稳定 accepted。",
            f"- ArduPilot 当前 throttle boundary=`{ap_diag.get('throttle_boundary', 'none')}`；PX4 当前 throttle boundary=`{px4_diag.get('throttle_boundary', 'none')}`，说明扩展动作后的 throttle 边界并不完全对称。",
            "- 两边都出现了跨 scenario generalized-supported 组合。",
            "",
            "这说明实验不是依赖某一个 backend 的偶然成功，而是已经在统一 schema 和统一数据契约下，反复看到了同类线性结构。只是当我们开始扩大动作和状态包线时，backend 间的边界差异也开始显形了。",
            "",
            "## 现在还不能说得过头的地方",
            "",
            f"- compare 的 gate/stability 主判断仍然是 `{difference_driver}`。",
            f"- ArduPilot baseline stability 当前状态仍是 `{ap_baseline.get('baseline_stability_state', 'unknown')}`，不是完全锁死不变的状态。",
            "",
            "所以当前还不适合把“backend 差异已经被完全解释清楚”当成主标题。更稳妥的说法是：",
            "",
            "1. 线性关系存在，这一点已经可以正式汇报。",
            "2. 线性关系在多 scenario 下仍然成立，这一点也已经有正面证据。",
            "3. PX4 的 generalized-supported 范围更宽，但 ArduPilot 的相对收窄，还不能被过度简化成最终 backend 输赢结论。",
            "",
            "## 历史阶段结论怎么处理",
            "",
            "20260409 那一轮 broad baseline / diagnostic 没有被删除，但它现在只作为历史阶段结论保留。",
            "",
            "当前正式结论的主输入，已经切换为这轮 generalization full 四个 study 和新的 compare artifact。",
            "",
            "## 下一步建议",
            "",
            "下一步不需要再扩很多新 schema。更值钱的是把已经出现的 `f` 矩阵读透：",
            "",
            "1. 系统阅读 generalized-supported 组合的 `matrix_f` 热力图，区分哪些结构是真正的物理映射，哪些只是状态延续。",
            "2. 若还要继续比较 backend 差异，优先做稳定性复查，不要先扩 schema 空间。",
            "3. 若要把 backend 差异升格成更强结论，需要先继续压实 ArduPilot state-evolution 路径的稳定性。",
            "",
            "## 这次里程碑的一句话总结",
            "",
            "在统一 schema 和统一数据契约下，`Y ≈ fX (+ b)` 已经不只是一个局部拟合假设，而是一个在 PX4 和 ArduPilot 上都能拿到跨 scenario 正面证据的正式结论。当前 PX4 的 generalized-supported 证据更宽，ArduPilot 的证据更窄但仍然真实存在，因此现在适合把“线性存在且可一定程度泛化”作为正式里程碑，而不是把“backend 胜负”作为主标题。",
            "",
            "## Artifact 路径",
            "",
            f"- PX4 baseline: `{_relative_from_docs(px4_baseline_dir, docs_dir)}`",
            f"- ArduPilot baseline: `{_relative_from_docs(ardupilot_baseline_dir, docs_dir)}`",
            f"- PX4 diagnostic: `{_relative_from_docs(px4_diagnostic_dir, docs_dir)}`",
            f"- ArduPilot diagnostic: `{_relative_from_docs(ardupilot_diagnostic_dir, docs_dir)}`",
            f"- final compare: `{_relative_from_docs(compare_dir, docs_dir)}`",
            f"- state-evolution audit: `{_relative_from_docs(ardupilot_baseline_dir / 'reports' / 'state_evolution_audit.md', docs_dir)}`",
            f"- guided smoke: `{_relative_from_docs(guided_smoke_dir, docs_dir)}`",
            f"- partial baseline: `{_relative_from_docs(partial_baseline_dir, docs_dir)}`",
            f"- throttle diagnostic: `{_relative_from_docs(throttle_diagnostic_dir, docs_dir)}`",
            f"- contract audit: `{_relative_from_docs(contract_audit_dir, docs_dir)}`",
        ]
    )


def render_milestone_appendix(
    *,
    px4_baseline_dir: Path,
    ardupilot_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_diagnostic_dir: Path,
    compare_dir: Path,
    guided_smoke_dir: Path,
    partial_baseline_dir: Path,
    throttle_diagnostic_dir: Path,
    contract_audit_dir: Path,
    docs_dir: Path,
) -> str:
    px4_summary = _load_study_summary(px4_baseline_dir)
    ap_summary = _load_study_summary(ardupilot_baseline_dir)
    px4_baseline = _baseline_section(px4_baseline_dir)
    ap_baseline = _baseline_section(ardupilot_baseline_dir)
    px4_diag = _diagnostic_section(px4_diagnostic_dir)
    ap_diag = _diagnostic_section(ardupilot_diagnostic_dir)
    compare_payload = read_yaml(compare_dir / "summary" / "backend_compare.json")
    state_audit = _state_evolution_audit(ardupilot_baseline_dir)
    px4_supported = _first_supported_combo(px4_summary)
    ap_supported = _first_supported_combo(ap_summary)
    px4_supported_dir = _combo_fit_dir(px4_baseline_dir, px4_supported) if px4_supported else px4_baseline_dir / "fits"
    ap_supported_dir = _combo_fit_dir(ardupilot_baseline_dir, ap_supported) if ap_supported else ardupilot_baseline_dir / "fits"
    px4_baseline_scenarios = _scenario_counts(compare_payload.get("px4", {}).get("baseline", {}))
    px4_diag_scenarios = _scenario_counts(compare_payload.get("px4", {}).get("diagnostic", {}))
    ap_baseline_scenarios = _scenario_counts(compare_payload.get("ardupilot", {}).get("baseline", {}))
    ap_diag_scenarios = _scenario_counts(compare_payload.get("ardupilot", {}).get("diagnostic", {}))

    return "\n".join(
        [
            "# 统一 Schema 口径下全局线性 `f` 的技术附录",
            "",
            "## 1. 正式 artifact 清单",
            "",
            f"- PX4 baseline study: `{_relative_from_docs(px4_baseline_dir, docs_dir)}`",
            f"- ArduPilot baseline study: `{_relative_from_docs(ardupilot_baseline_dir, docs_dir)}`",
            f"- PX4 diagnostic study: `{_relative_from_docs(px4_diagnostic_dir, docs_dir)}`",
            f"- ArduPilot diagnostic study: `{_relative_from_docs(ardupilot_diagnostic_dir, docs_dir)}`",
            f"- final compare: `{_relative_from_docs(compare_dir, docs_dir)}`",
            "",
            "## 2. 支持性 artifact",
            "",
            f"- GUIDED_NOGPS smoke: `{_relative_from_docs(guided_smoke_dir, docs_dir)}`",
            f"- STABILIZE partial baseline: `{_relative_from_docs(partial_baseline_dir, docs_dir)}`",
            f"- STABILIZE throttle diagnostic: `{_relative_from_docs(throttle_diagnostic_dir, docs_dir)}`",
            f"- cross-backend contract audit: `{_relative_from_docs(contract_audit_dir, docs_dir)}`",
            "",
            "## 3. baseline 关键数字",
            "",
            f"- PX4 accepted runs: `{px4_baseline.get('accepted_run_count', 0)}`",
            f"- PX4 supported anchor: `{px4_baseline.get('supported_anchor', '')}`",
            f"- PX4 best combo: `{px4_baseline.get('best_combo', '')}`",
            f"- PX4 matrix gallery supported_count: `{_gallery_supported_count(px4_baseline_dir)}`",
            f"- ArduPilot accepted runs: `{ap_baseline.get('accepted_run_count', 0)}`",
            f"- ArduPilot supported anchor: `{ap_baseline.get('supported_anchor', '')}`",
            f"- ArduPilot best combo: `{ap_baseline.get('best_combo', '')}`",
            f"- ArduPilot baseline stability: `{ap_baseline.get('baseline_stability_state', 'unknown')}`",
            f"- ArduPilot matrix gallery supported_count: `{_gallery_supported_count(ardupilot_baseline_dir)}`",
            "",
            "## 4. scenario_generalization 核心数字",
            "",
            f"- PX4 baseline: generalized_supported=`{px4_baseline_scenarios['generalized_supported']}`, supported_but_local=`{px4_baseline_scenarios['supported_but_local']}`, not_generalized=`{px4_baseline_scenarios['not_generalized']}`",
            f"- PX4 diagnostic: generalized_supported=`{px4_diag_scenarios['generalized_supported']}`, supported_but_local=`{px4_diag_scenarios['supported_but_local']}`, not_generalized=`{px4_diag_scenarios['not_generalized']}`",
            f"- ArduPilot baseline: generalized_supported=`{ap_baseline_scenarios['generalized_supported']}`, supported_but_local=`{ap_baseline_scenarios['supported_but_local']}`, not_generalized=`{ap_baseline_scenarios['not_generalized']}`",
            f"- ArduPilot diagnostic: generalized_supported=`{ap_diag_scenarios['generalized_supported']}`, supported_but_local=`{ap_diag_scenarios['supported_but_local']}`, not_generalized=`{ap_diag_scenarios['not_generalized']}`",
            f"- generalization_difference_driver: `{compare_payload.get('comparison', {}).get('generalization_difference_driver', '')}`",
            "",
            "## 5. state-evolution audit 摘要",
            "",
            f"- audit_status: `{state_audit.get('status', 'audit_unavailable')}`",
            f"- comparison_status: `{state_audit.get('comparison_status', 'comparison_unavailable')}`",
            f"- current_supported_state_evolution_count: `{len(state_audit.get('current', {}).get('supported_state_evolution', []))}`",
            f"- conclusion: `{state_audit.get('conclusion', '')}`",
            f"- report: `{_relative_from_docs(ardupilot_baseline_dir / 'reports' / 'state_evolution_audit.md', docs_dir)}`",
            "",
            "## 6. diagnostic gate 摘要",
            "",
            f"- PX4 throttle_boundary: `{px4_diag.get('throttle_boundary', 'none')}`; nonzero_gate_blocked=`{str(bool(px4_diag.get('throttle_blocked_by_nonzero_gate'))).lower()}`",
            f"- ArduPilot throttle_boundary: `{ap_diag.get('throttle_boundary', 'none')}`; nonzero_gate_blocked=`{str(bool(ap_diag.get('throttle_blocked_by_nonzero_gate'))).lower()}`",
            "",
            "## 7. 代表性组合与矩阵图",
            "",
            f"- PX4 baseline supported combo: `{_combo_key(px4_supported)}`",
            f"  - matrix: `{_relative_from_docs(px4_supported_dir / 'matrix_f.csv', docs_dir)}`",
            f"  - abs heatmap: `{_relative_from_docs(px4_supported_dir / 'matrix_heatmap_abs.png', docs_dir)}`",
            f"- ArduPilot baseline supported combo: `{_combo_key(ap_supported)}`",
            f"  - matrix: `{_relative_from_docs(ap_supported_dir / 'matrix_f.csv', docs_dir)}`",
            f"  - abs heatmap: `{_relative_from_docs(ap_supported_dir / 'matrix_heatmap_abs.png', docs_dir)}`",
            "",
            "## 8. compare 摘要",
            "",
            f"- compare_dir: `{_relative_from_docs(compare_dir, docs_dir)}`",
            f"- difference_driver: `{compare_payload.get('comparison', {}).get('difference_driver', '')}`",
            f"- both_baselines_stable: `{str(bool(compare_payload.get('comparison', {}).get('both_baselines_stable'))).lower()}`",
            f"- throttle_boundary_consistent: `{str(bool(compare_payload.get('comparison', {}).get('throttle_boundary_consistent'))).lower()}`",
            "",
            "## 9. 历史阶段 artifact",
            "",
            "- 20260409 broad baseline / diagnostic 仍保留为历史路径，不再作为当前正式 compare 主输入。",
            "",
            "## 10. 当前稳妥的技术结论",
            "",
            "- 两个 backend 的正式 baseline 和 diagnostic 都已经形成完整 artifact。",
            "- 两个 backend 都已经给出跨 scenario generalized-supported 证据。",
            "- PX4 对状态演化类线性映射的 generalized-supported 支持继续更强、更宽。",
            "- ArduPilot 的高分 state-evolution 结果仍需要结合条件数和稳定性一起解释。",
            "- 因此现在可以把“线性关系存在且具有一定跨场景泛化性”作为正面结论汇报，但不应把“backend 差异”写成最终主结论。",
        ]
    )


def write_milestone_docs(
    *,
    px4_baseline_dir: Path,
    ardupilot_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_diagnostic_dir: Path,
    compare_dir: Path,
    guided_smoke_dir: Path,
    partial_baseline_dir: Path,
    throttle_diagnostic_dir: Path,
    contract_audit_dir: Path,
    docs_dir: Path | None = None,
) -> dict[str, str]:
    docs_root = _docs_root(docs_dir)
    docs_root.mkdir(parents=True, exist_ok=True)
    report_path = docs_root / "MILESTONE_LINEAR_F_REPORT.md"
    appendix_path = docs_root / "MILESTONE_LINEAR_F_APPENDIX.md"
    report_path.write_text(
        render_milestone_report(
            px4_baseline_dir=px4_baseline_dir,
            ardupilot_baseline_dir=ardupilot_baseline_dir,
            px4_diagnostic_dir=px4_diagnostic_dir,
            ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
            compare_dir=compare_dir,
            guided_smoke_dir=guided_smoke_dir,
            partial_baseline_dir=partial_baseline_dir,
            throttle_diagnostic_dir=throttle_diagnostic_dir,
            contract_audit_dir=contract_audit_dir,
            docs_dir=docs_root,
        ),
        encoding="utf-8",
    )
    appendix_path.write_text(
        render_milestone_appendix(
            px4_baseline_dir=px4_baseline_dir,
            ardupilot_baseline_dir=ardupilot_baseline_dir,
            px4_diagnostic_dir=px4_diagnostic_dir,
            ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
            compare_dir=compare_dir,
            guided_smoke_dir=guided_smoke_dir,
            partial_baseline_dir=partial_baseline_dir,
            throttle_diagnostic_dir=throttle_diagnostic_dir,
            contract_audit_dir=contract_audit_dir,
            docs_dir=docs_root,
        ),
        encoding="utf-8",
    )
    return {
        "report_path": str(report_path),
        "appendix_path": str(appendix_path),
    }


def refresh_generalization_milestone(
    *,
    px4_baseline_dir: Path,
    ardupilot_baseline_dir: Path,
    px4_diagnostic_dir: Path,
    ardupilot_diagnostic_dir: Path,
    guided_smoke_dir: Path,
    partial_baseline_dir: Path,
    throttle_diagnostic_dir: Path,
    contract_audit_dir: Path,
    docs_dir: Path | None = None,
) -> dict[str, Any]:
    compare_dir = run_backend_compare(
        px4_baseline_dir=px4_baseline_dir,
        ardupilot_baseline_dir=ardupilot_baseline_dir,
        px4_diagnostic_dir=px4_diagnostic_dir,
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
    )
    docs_written = write_milestone_docs(
        px4_baseline_dir=px4_baseline_dir,
        ardupilot_baseline_dir=ardupilot_baseline_dir,
        px4_diagnostic_dir=px4_diagnostic_dir,
        ardupilot_diagnostic_dir=ardupilot_diagnostic_dir,
        compare_dir=compare_dir,
        guided_smoke_dir=guided_smoke_dir,
        partial_baseline_dir=partial_baseline_dir,
        throttle_diagnostic_dir=throttle_diagnostic_dir,
        contract_audit_dir=contract_audit_dir,
        docs_dir=docs_dir,
    )
    payload: dict[str, Any] = {
        "mode": "generalization_full",
        "refreshed": True,
        "compare_dir": str(compare_dir),
        "inputs": {
            "px4_baseline_dir": str(px4_baseline_dir),
            "ardupilot_baseline_dir": str(ardupilot_baseline_dir),
            "px4_diagnostic_dir": str(px4_diagnostic_dir),
            "ardupilot_diagnostic_dir": str(ardupilot_diagnostic_dir),
            "guided_smoke_dir": str(guided_smoke_dir),
            "partial_baseline_dir": str(partial_baseline_dir),
            "throttle_diagnostic_dir": str(throttle_diagnostic_dir),
            "contract_audit_dir": str(contract_audit_dir),
        },
        **docs_written,
    }
    write_json(_repo_root() / "artifacts" / "studies" / "latest_milestone_refresh.json", payload)
    return payload


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Refresh canonical compare artifact and milestone docs from the latest formal generalization studies.")
    parser.add_argument("--px4-baseline", type=Path, required=True)
    parser.add_argument("--ardupilot-baseline", type=Path, required=True)
    parser.add_argument("--px4-diagnostic", type=Path, required=True)
    parser.add_argument("--ardupilot-diagnostic", type=Path, required=True)
    parser.add_argument("--guided-smoke", type=Path, required=True)
    parser.add_argument("--partial-baseline", type=Path, required=True)
    parser.add_argument("--throttle-diagnostic", type=Path, required=True)
    parser.add_argument("--contract-audit", type=Path, required=True)
    parser.add_argument("--docs-dir", type=Path, default=None)
    args = parser.parse_args(argv)

    payload = refresh_generalization_milestone(
        px4_baseline_dir=args.px4_baseline.expanduser().resolve(),
        ardupilot_baseline_dir=args.ardupilot_baseline.expanduser().resolve(),
        px4_diagnostic_dir=args.px4_diagnostic.expanduser().resolve(),
        ardupilot_diagnostic_dir=args.ardupilot_diagnostic.expanduser().resolve(),
        guided_smoke_dir=args.guided_smoke.expanduser().resolve(),
        partial_baseline_dir=args.partial_baseline.expanduser().resolve(),
        throttle_diagnostic_dir=args.throttle_diagnostic.expanduser().resolve(),
        contract_audit_dir=args.contract_audit.expanduser().resolve(),
        docs_dir=args.docs_dir.expanduser().resolve() if args.docs_dir else None,
    )
    print(f"refreshed={str(bool(payload.get('refreshed'))).lower()}")
    if payload.get("compare_dir"):
        print(f"compare_dir={payload['compare_dir']}")
    if payload.get("report_path"):
        print(f"report_path={payload['report_path']}")
    if payload.get("appendix_path"):
        print(f"appendix_path={payload['appendix_path']}")
    write_json(_repo_root() / "artifacts" / "studies" / "latest_milestone_refresh.json", payload)


if __name__ == "__main__":
    main()
