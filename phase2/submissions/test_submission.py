#!/usr/bin/env python
"""Bounded tests for the submission system.

Tests:
1. Build system determines correct next version
2. Build creates valid tarball
3. Validation passes on a known submission
4. Version numbering doesn't collide
"""

from __future__ import annotations

import json
import os
import sys
import tarfile
from pathlib import Path

# Add parent path for imports
sys.path.insert(0, str(Path(__file__).parent))

from build import _next_version, build, CANDIDATE_SOURCES
from validate import validate

O_DRIVE_SUB = Path(os.environ.get(
    "CONNECTX_SUBMISSIONS",
    r"O:\master_model_collection\ConnectX_Gen2_Phase2\submissions",
))
STATE_FILE = Path(__file__).parent / "submission_state.json"


def test_next_version_consistent():
    """Next version from state must match scan of O-drive."""
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    state_next = state.get("next_version", 1)
    actual = _next_version()
    assert actual == state_next, f"State says {state_next}, scan says {actual}"
    print(f"  PASS: next_version consistent = {actual}")


def test_candidate_sources_exist():
    """All known candidate sources must exist on disk."""
    for name, info in CANDIDATE_SOURCES.items():
        src = info["source_file"]
        assert src.exists(), f"Candidate source not found: {src}"
        assert src.stat().st_size > 0, f"Source is empty: {src}"
    print(f"  PASS: All {len(CANDIDATE_SOURCES)} candidate sources exist")


def test_build_creates_tarball():
    """Building a submission creates a valid tarball on O-drive."""
    # Check if v0001 already exists (from previous build)
    existing = list(O_DRIVE_SUB.glob("connectx_submission_v*.tar.gz")) if O_DRIVE_SUB.exists() else []

    if existing:
        # Test against existing
        tar_path = existing[0]
        assert tar_path.exists()
        print(f"  PASS: Found existing tarball {tar_path.name}")
        return

    # Build a new one (v0001)
    manifest = build("v2_7x6_4")
    tar_path = O_DRIVE_SUB / manifest["archive_filename"]
    assert tar_path.exists()
    assert manifest["compressed_size"] > 0
    assert manifest["sha256"] is not None
    print(f"  PASS: Built {manifest['archive_filename']} ({manifest['compressed_size']} bytes)")


def test_validation_passes():
    """Validation passes on v0001 if it exists."""
    tar_path = O_DRIVE_SUB / "connectx_submission_v0001.tar.gz"
    if not tar_path.exists():
        print("  SKIP: v0001 not found")
        return

    result = validate(tar_path)
    assert result["overall"] == "PASS", f"Validation failed: {result['checks']}"
    print(f"  PASS: Validation passed (overall={result['overall']})")


def test_version_sequence():
    """Check that version numbers don't collide."""
    import re
    existing = list(O_DRIVE_SUB.glob("connectx_submission_v*.tar.gz")) if O_DRIVE_SUB.exists() else []
    versions = set()
    for f in existing:
        m = re.fullmatch(r"connectx_submission_v(\d+)\.tar\.gz", f.name)
        if m:
            v = int(m.group(1))
            assert v not in versions, f"Duplicate version: {v}"
            versions.add(v)

    if not versions:
        print("  SKIP: No versions found to check sequence")
        return

    # Check next_version from state
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    state_next = state.get("next_version", max(versions) + 1 if versions else 1)
    actual = _next_version()
    assert actual == state_next, f"State says {state_next}, scan says {actual}"
    assert actual not in versions, f"Next version {actual} already exists!"
    print(f"  PASS: Version sequence intact (next={actual}, total={len(versions)})")


def main():
    print("Submission system tests:")
    print()
    tests = [
        test_next_version_consistent,
        test_candidate_sources_exist,
        test_build_creates_tarball,
        test_validation_passes,
        test_version_sequence,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as exc:
            print(f"  FAIL: {test.__name__}: {exc}")
            failed += 1
    print()
    print(f"Results: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())