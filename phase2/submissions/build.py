#!/usr/bin/env python
"""Build an immutable Kaggle submission tarball for ConnectX.

Each submission is a clean copy of the bot's main.py (Kaggle entrypoint).

Usage:
    python build.py --candidate v2_7x6_4
    python build.py --candidate v2_8x7_5 --module connectx.bots.bitboard_ab_8x7_5_v2
    python build.py --version v0005 --module my.module --function my_bot

Scans O-drive for existing versions so the next version is always unique.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
O_DRIVE_SUB = Path(os.environ.get(
    "CONNECTX_SUBMISSIONS",
    r"O:\master_model_collection\ConnectX_Gen2_Phase2\submissions",
))
STATE_FILE = Path(__file__).parent / "submission_state.json"


def _next_version() -> int:
    """Determine the next unused version from state + O-drive scan."""
    state: dict[str, Any] = {}
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
    candidate = state.get("next_version", 1)

    if O_DRIVE_SUB.exists():
        for f in O_DRIVE_SUB.iterdir():
            m = re.fullmatch(r"connectx_submission_v(\d+)\.tar\.gz", f.name)
            if m:
                candidate = max(candidate, int(m.group(1)) + 1)

    return candidate


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_info() -> dict:
    info: dict = {}
    try:
        info["commit"] = (
            os.popen(f'git -C "{REPO_ROOT}" rev-parse HEAD').read().strip()
        )
        info["branch"] = (
            os.popen(f'git -C "{REPO_ROOT}" branch --show-current').read().strip()
        )
        info["clean"] = (
            os.popen(f'git -C "{REPO_ROOT}" diff --stat HEAD').read().strip() == ""
        )
    except Exception:
        pass
    return info


# ---------------------------------------------------------------------------
# Source file mapping — where to get the bot code
# ---------------------------------------------------------------------------

CANDIDATE_SOURCES: dict[str, dict] = {
    "v2_7x6_4": {
        "source_file": REPO_ROOT / "connectx" / "training" / "kaggle_self_contained.py",
        "description": "v2 alpha-beta, self-contained Kaggle bot (7x6/4)",
    },
    "v2_7x6_4_booked": {
        "source_file": REPO_ROOT / "connectx" / "bots" / "bitboard_ab_v2_booked.py",
        "description": "v2 + opening book (7x6/4)",
    },
    "v2_8x7_5": {
        "source_file": REPO_ROOT / "connectx" / "bots" / "bitboard_ab_8x7_5_v2.py",
        "description": "v2 alpha-beta for 8x7/5 (improved evaluation)",
    },
    "v2_8x7_5_booked": {
        "source_file": REPO_ROOT / "connectx" / "bots" / "bitboard_ab_8x7_5_v2_booked.py",
        "description": "v2 + dual-book fallback for 8x7/5",
    },
}


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def _ensure_imports_for_8x7_bot(source_content: str, src_path: Path) -> str:
    """For non-self-contained bots, we need to bundle required engine code.

    For the 8x7/5 bots, the engine is in connectx/engine.py and
    connectx/bots/bitboard_ab_8x7_5_v2.py has all its logic inline.
    We simply copy the source as-is — Kaggle won't import it directly,
    but this is a research release for manual upload and validation.
    """
    return source_content


def build(
    candidate: str,
    source_file: Path | None = None,
    description: str = "",
    version: int | None = None,
) -> dict:
    """Build one submission and write archive + metadata to O-drive."""

    if version is None:
        version = _next_version()

    label = f"v{version:04d}"
    tar_name = f"connectx_submission_{label}.tar.gz"
    tar_path = O_DRIVE_SUB / tar_name

    if tar_path.exists():
        raise FileExistsError(f"{tar_path} already exists — version {label} not unique")

    O_DRIVE_SUB.mkdir(parents=True, exist_ok=True)

    # Resolve source
    if candidate in CANDIDATE_SOURCES:
        src = CANDIDATE_SOURCES[candidate]["source_file"]
        desc = CANDIDATE_SOURCES[candidate]["description"]
    elif source_file is not None:
        src = source_file
        desc = description
    else:
        raise ValueError("Must provide candidate name or source_file")

    if not src.exists():
        raise FileNotFoundError(f"Source not found: {src}")

    manifest: dict[str, Any] = {
        "submission_version": label,
        "archive_filename": tar_name,
        "archive_path": str(tar_path),
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "candidate": candidate,
        "description": desc,
        "source_file": str(src),
        "source_entrypoint": src.name,
        "sha256": None,
        "compressed_size": None,
        "extracted_size": None,
        "git": _git_info(),
        "validation_status": "PENDING",
        "promotion_status": "PENDING",
        "parent_submission": None,
        "change_summary": f"Initial build for candidate '{candidate}'",
    }

    # Build tarball
    with tempfile.TemporaryDirectory(prefix="cx_build_") as tmpdir:
        staging = Path(tmpdir)

        # Copy source as main.py (and keep source reference)
        shutil.copy2(str(src), str(staging / "main.py"))

        # Write a small runtime config
        config = {
            "candidate": candidate,
            "description": desc,
            "source_file": str(src),
            "python_requires": ">=3.10",
        }
        (staging / "config.json").write_text(json.dumps(config, indent=2))

        with tarfile.open(str(tar_path), "w:gz", format=tarfile.PAX_FORMAT) as tf:
            for fpath in sorted(staging.rglob("*")):
                if fpath.is_file():
                    arcname = fpath.name  # root-level, no prefix
                    tf.add(str(fpath), arcname=arcname)

    # Compute hashes and sizes
    sha = _sha256_file(tar_path)
    compressed_size = tar_path.stat().st_size

    with tarfile.open(str(tar_path), "r:gz") as tf2:
        members = tf2.getmembers()
        extracted_size = sum(m.size for m in members)
        main_member = tf2.getmember("main.py")
        main_stream = tf2.extractfile(main_member)
        main_sha = hashlib.sha256(main_stream.read()).hexdigest()

    manifest.update({
        "sha256": sha,
        "compressed_size": compressed_size,
        "extracted_size": extracted_size,
        "packaged_main_py_hash": main_sha,
    })

    # Write manifest
    manifest_path = tar_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2))

    # Update state
    state: dict[str, Any] = {"next_version": version + 1}
    if STATE_FILE.exists():
        existing = json.loads(STATE_FILE.read_text())
        state.update(existing)
    state["total_submissions"] = state.get("total_submissions", 0) + 1
    state["last_commit"] = manifest["git"].get("commit", "")
    STATE_FILE.write_text(json.dumps(state, indent=2))

    # Update LATEST_SUBMISSION.json
    latest = {
        "version": label,
        "status": "READY_FOR_MANUAL_UPLOAD",
        "candidate": candidate,
        "archive_path": str(tar_path),
        "sha256": sha,
        "compressed_size": compressed_size,
        "created_utc": manifest["created_utc"],
    }
    (O_DRIVE_SUB / "LATEST_SUBMISSION.json").write_text(json.dumps(latest, indent=2))

    return manifest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build ConnectX Kaggle submission")
    parser.add_argument("--version", type=str,
                        help="Specific version (e.g. v0001). Auto-allocated if omitted.")
    parser.add_argument("--candidate", type=str, default="v2_7x6_4",
                        help=f"Candidate. Known: {', '.join(CANDIDATE_SOURCES)}")
    parser.add_argument("--source", type=str, help="Source .py file path")
    parser.add_argument("--description", type=str, default="")
    args = parser.parse_args()

    # Compute version
    if args.version:
        m = re.fullmatch(r"v(\d+)", args.version)
        if not m:
            parser.error(f"Invalid version: {args.version}")
        version = int(m.group(1))
    else:
        version = None

    src_file = Path(args.source) if args.source else None
    print(f"Building submission for candidate '{args.candidate}'...")
    if src_file:
        print(f"  source: {src_file}")

    try:
        manifest = build(
            candidate=args.candidate,
            source_file=src_file,
            description=args.description,
            version=version,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    # Validate immediately
    print("\nRunning validation...")
    from validate import validate
    val = validate(Path(manifest["archive_path"]))

    tar_path = Path(manifest["archive_path"])

    # Write validation JSON alongside archive
    val_path = tar_path.with_suffix(".validation.json")
    val_path.write_text(json.dumps(val, indent=2))
    manifest["validation_status"] = val["overall"]

    # Rewrite manifest with validation result
    tar_path.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2))

    # Update state
    state = json.loads(STATE_FILE.read_text())
    state["next_version"] = int(manifest["submission_version"].lstrip("v")) + 1
    state["last_commit"] = manifest["git"].get("commit", "")
    STATE_FILE.write_text(json.dumps(state, indent=2))

    # Update LATEST_SUBMISSION.json
    latest = {
        "version": manifest["submission_version"],
        "status": val["overall"],
        "candidate": manifest["candidate"],
        "archive_path": manifest["archive_path"],
        "sha256": manifest["sha256"],
        "compressed_size": manifest["compressed_size"],
        "created_utc": manifest["created_utc"],
    }
    (O_DRIVE_SUB / "LATEST_SUBMISSION.json").write_text(json.dumps(latest, indent=2))

    status_label = val["overall"]
    print(f"\n{'='*60}")
    print(f"BUILD {'SUCCESS' if status_label == 'PASS' else 'VALIDATION FAILED'}  —  {manifest['submission_version']}")
    print(f"  Status: {status_label}")
    print(f"  Archive: {manifest['archive_path']}")
    print(f"  SHA-256: {manifest['sha256']}")
    print(f"  Size: {manifest['compressed_size']:,} bytes")
    print(f"  Extracted: {manifest['extracted_size']:,} bytes")
    print(f"  Commit: {manifest['git'].get('commit', '?')}")
    print(f"  Main.py hash: {manifest['packaged_main_py_hash']}")
    print(f"  Validation: {val_path}")
    print(f"{'='*60}")

    return 0 if status_label == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())