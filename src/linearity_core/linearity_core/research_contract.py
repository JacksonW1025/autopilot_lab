from __future__ import annotations

from typing import Any


SUPPORTED_RESEARCH_TIERS = {
    "authoritative_research",
    "diagnostic_research",
    "demo_only",
}


def normalize_research_tier(value: Any, *, default: str = "authoritative_research") -> str:
    tier = str(value or default).strip().lower()
    if tier not in SUPPORTED_RESEARCH_TIERS:
        raise ValueError(f"不支持的 research_tier: {tier}")
    return tier


def build_acceptance_block(
    *,
    experiment_started: bool | None,
    active_phase_present: bool | None,
    expected_active_samples: int | None,
    active_sample_count: int | None,
    active_nonzero_command_samples: int | None,
    failsafe_during_experiment: bool | None,
    missing_topics_blocking: list[str] | None,
    accepted: bool,
    rejection_reasons: list[str] | None = None,
) -> dict[str, Any]:
    reasons = sorted(dict.fromkeys(str(item) for item in (rejection_reasons or []) if str(item)))
    return {
        "experiment_started": experiment_started,
        "active_phase_present": active_phase_present,
        "expected_active_samples": expected_active_samples,
        "active_sample_count": active_sample_count,
        "active_nonzero_command_samples": active_nonzero_command_samples,
        "failsafe_during_experiment": failsafe_during_experiment,
        "missing_topics_blocking": list(missing_topics_blocking or []),
        "accepted": bool(accepted),
        "rejection_reasons": reasons,
    }


def unavailable_acceptance_block(reason: str = "acceptance_unavailable") -> dict[str, Any]:
    return build_acceptance_block(
        experiment_started=None,
        active_phase_present=None,
        expected_active_samples=None,
        active_sample_count=None,
        active_nonzero_command_samples=None,
        failsafe_during_experiment=None,
        missing_topics_blocking=[],
        accepted=False,
        rejection_reasons=[reason],
    )


def apply_manifest_research_contract(
    manifest: dict[str, Any],
    *,
    research_tier: str,
    acceptance: dict[str, Any],
) -> dict[str, Any]:
    payload = dict(manifest)
    payload["raw_schema_version"] = 2
    payload["research_acceptance"] = "accepted" if bool(acceptance.get("accepted")) else "rejected"
    payload["research_rejection_reasons"] = list(acceptance.get("rejection_reasons", []) or [])
    payload["research_tier"] = normalize_research_tier(research_tier)
    data_quality = dict(payload.get("data_quality", {}) or {})
    data_quality["acceptance"] = acceptance
    payload["data_quality"] = data_quality
    return payload


def manifest_acceptance_state(manifest: dict[str, Any]) -> str:
    raw_schema_version = int(manifest.get("raw_schema_version", 0) or 0)
    state = str(manifest.get("research_acceptance", "")).strip().lower()
    if raw_schema_version < 2 or state not in {"accepted", "rejected"}:
        return "legacy"
    return state
