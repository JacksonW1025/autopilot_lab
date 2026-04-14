from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Any

from linearity_core.io import read_yaml, write_json
from linearity_core.paths import (
    ARDUPILOT_MATRIX_ROOT,
    ARTIFACT_ROOT,
    DOCS_ROOT,
    PX4_MATRIX_ROOT,
    RAW_ARTIFACT_ROOT,
    STUDY_ARTIFACT_ROOT,
    WORKSPACE_ROOT,
)

REFERENCE_PATTERN = re.compile(r"\.\./artifacts/[A-Za-z0-9_./-]+")
CANONICAL_DOCS = [
    DOCS_ROOT / "MILESTONE_LINEAR_F_REPORT.md",
    DOCS_ROOT / "MILESTONE_LINEAR_F_APPENDIX.md",
]
MANAGED_ROOTS = [STUDY_ARTIFACT_ROOT, PX4_MATRIX_ROOT, ARDUPILOT_MATRIX_ROOT]


def _artifact_top_level(path: Path) -> Path | None:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(ARTIFACT_ROOT.resolve())
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) < 2:
        return None
    if parts[0] in {"studies", "px4_matrix", "ardupilot_matrix"}:
        return ARTIFACT_ROOT / parts[0] / parts[1]
    if parts[0] == "raw" and len(parts) >= 3:
        return ARTIFACT_ROOT / "raw" / parts[1] / parts[2]
    return None


def _localize_source_run_dir(path_value: str) -> Path | None:
    candidate = Path(path_value).expanduser()
    if candidate.exists():
        return candidate.resolve()
    if "artifacts/" not in path_value:
        return None
    relative_text = path_value.split("artifacts/", 1)[1]
    fallback = ARTIFACT_ROOT / relative_text
    if fallback.exists():
        return fallback.resolve()
    return None


def _managed_directories() -> list[Path]:
    managed: list[Path] = []
    for root in MANAGED_ROOTS:
        if not root.exists():
            continue
        managed.extend(sorted(path for path in root.iterdir() if path.is_dir()))
    if RAW_ARTIFACT_ROOT.exists():
        for backend_root in sorted(path for path in RAW_ARTIFACT_ROOT.iterdir() if path.is_dir()):
            managed.extend(sorted(path for path in backend_root.iterdir() if path.is_dir()))
    return managed


def _directory_size_bytes(path: Path) -> int:
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            total += item.stat().st_size
    return total


def _collect_doc_references(doc_paths: list[Path]) -> dict[Path, list[str]]:
    keep_reasons: dict[Path, list[str]] = {}
    for doc_path in doc_paths:
        if not doc_path.exists():
            continue
        text = doc_path.read_text(encoding="utf-8")
        for match in REFERENCE_PATTERN.findall(text):
            resolved = (doc_path.parent / match).resolve()
            artifact_dir = _artifact_top_level(resolved)
            if artifact_dir is None:
                continue
            keep_reasons.setdefault(artifact_dir, []).append(f"doc:{doc_path.name}")
    return keep_reasons


def _extend_keep_with_study_sources(keep_reasons: dict[Path, list[str]]) -> dict[Path, list[str]]:
    expanded = {path.resolve(): list(reasons) for path, reasons in keep_reasons.items()}
    for study_dir, reasons in list(expanded.items()):
        if study_dir.parent.resolve() != STUDY_ARTIFACT_ROOT.resolve():
            continue
        manifest_path = study_dir / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = read_yaml(manifest_path)
        for raw_path_value in manifest.get("source_run_dirs", []) or []:
            localized = _localize_source_run_dir(str(raw_path_value))
            if localized is None:
                continue
            artifact_dir = _artifact_top_level(localized)
            if artifact_dir is None:
                continue
            expanded.setdefault(artifact_dir.resolve(), []).append(f"source_of:{study_dir.name}")
    return expanded


def build_prune_payload(
    *,
    workspace_root: Path = WORKSPACE_ROOT,
    doc_paths: list[Path] | None = None,
    include_source_runs: bool = True,
) -> dict[str, Any]:
    docs = doc_paths or CANONICAL_DOCS
    keep_reasons = _collect_doc_references(docs)
    if include_source_runs:
        keep_reasons = _extend_keep_with_study_sources(keep_reasons)
    keep_dirs = sorted(keep_reasons)
    managed_dirs = [path.resolve() for path in _managed_directories()]
    keep_set = {path.resolve() for path in keep_dirs}
    drop_dirs = [path for path in managed_dirs if path not in keep_set]
    keep_entries = [
        {
            "path": str(path),
            "relative_path": str(path.relative_to(workspace_root.resolve())),
            "size_bytes": _directory_size_bytes(path),
            "reasons": sorted(set(keep_reasons.get(path, []))),
        }
        for path in keep_dirs
    ]
    drop_entries = [
        {
            "path": str(path),
            "relative_path": str(path.relative_to(workspace_root.resolve())),
            "size_bytes": _directory_size_bytes(path),
        }
        for path in drop_dirs
    ]
    return {
        "workspace_root": str(workspace_root.resolve()),
        "docs": [str(path.resolve()) for path in docs if path.exists()],
        "include_source_runs": include_source_runs,
        "keep_count": len(keep_entries),
        "drop_count": len(drop_entries),
        "keep_bytes": sum(item["size_bytes"] for item in keep_entries),
        "drop_bytes": sum(item["size_bytes"] for item in drop_entries),
        "keep": keep_entries,
        "drop": drop_entries,
    }


def apply_prune(payload: dict[str, Any]) -> dict[str, Any]:
    deleted: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for item in payload.get("drop", []):
        path = Path(str(item.get("path", "")))
        if not path.exists():
            continue
        try:
            shutil.rmtree(path)
            deleted.append(
                {
                    "path": str(path),
                    "relative_path": str(item.get("relative_path", "")),
                    "size_bytes": int(item.get("size_bytes", 0) or 0),
                }
            )
        except OSError as exc:
            errors.append({"path": str(path), "error": f"{type(exc).__name__}:{exc}"})
    return {
        "deleted_count": len(deleted),
        "deleted_bytes": sum(item["size_bytes"] for item in deleted),
        "deleted": deleted,
        "errors": errors,
    }


def _human_size(size_bytes: int) -> str:
    value = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f}{unit}"
        value /= 1024.0
    return f"{size_bytes}B"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Prune stale experiment artifacts while preserving canonical milestone dependencies.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=WORKSPACE_ROOT / "metadata" / "artifact_prune",
        help="Directory for keep/drop manifests.",
    )
    parser.add_argument(
        "--exclude-source-runs",
        action="store_true",
        help="Do not keep transitive raw source runs referenced by study manifests.",
    )
    parser.add_argument("--apply", action="store_true", help="Delete drop candidates after writing manifests.")
    args = parser.parse_args(argv)

    payload = build_prune_payload(include_source_runs=not args.exclude_source_runs)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    keep_path = output_dir / "keep_manifest.json"
    drop_path = output_dir / "drop_manifest.json"
    write_json(
        keep_path,
        {
            "workspace_root": payload["workspace_root"],
            "docs": payload["docs"],
            "include_source_runs": payload["include_source_runs"],
            "keep_count": payload["keep_count"],
            "keep_bytes": payload["keep_bytes"],
            "keep": payload["keep"],
        },
    )
    write_json(
        drop_path,
        {
            "workspace_root": payload["workspace_root"],
            "include_source_runs": payload["include_source_runs"],
            "drop_count": payload["drop_count"],
            "drop_bytes": payload["drop_bytes"],
            "drop": payload["drop"],
        },
    )
    print(f"keep_manifest={keep_path}")
    print(f"drop_manifest={drop_path}")
    print(f"keep_count={payload['keep_count']}")
    print(f"drop_count={payload['drop_count']}")
    print(f"drop_bytes={payload['drop_bytes']}")
    print(f"drop_human={_human_size(int(payload['drop_bytes']))}")

    if args.apply:
        result = apply_prune(payload)
        write_json(output_dir / "apply_result.json", result)
        print(f"deleted_count={result['deleted_count']}")
        print(f"deleted_bytes={result['deleted_bytes']}")
        print(f"deleted_human={_human_size(int(result['deleted_bytes']))}")
        print(f"errors={len(result['errors'])}")


if __name__ == "__main__":
    main()
