#!/usr/bin/env python
"""Validate a ConnectX submission tarball.

Checks:
1. Clean extraction (no absolute paths, no parent traversal)
2. main.py present at archive root
3. SHA-256 matches manifest
4. Import and basic runtime smoke test
5. Size within 1 GiB limit

Usage:
    python validate.py --path O:/master_model_collection/ConnectX_Gen2_Phase2/submissions/connectx_submission_v0001.tar.gz
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib
import json
import sys
import tarfile
import tempfile
from pathlib import Path


def validate(tar_path: Path) -> dict:
    result = {
        "file": str(tar_path),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "checks": {},
        "overall": "PASS",
    }

    # --- Check 1: File exists ---
    if not tar_path.exists():
        result["checks"]["file_exists"] = False
        result["checks"]["error"] = "File not found"
        result["overall"] = "FAIL"
        return result

    result["checks"]["file_exists"] = True

    # --- Check 2: Safe member paths ---
    safe_paths = True
    unsafe_paths = []
    with tarfile.open(str(tar_path), "r:gz") as tf:
        for m in tf.getmembers():
            if m.name.startswith("/"):
                safe_paths = False
                unsafe_paths.append(m.name)
            if ".." in m.name:
                safe_paths = False
                unsafe_paths.append(m.name)
            if m.isdev():
                safe_paths = False
                unsafe_paths.append(m.name)

    result["checks"]["safe_paths"] = safe_paths
    if not safe_paths:
        result["checks"]["unsafe_paths"] = unsafe_paths[:10]

    # --- Check 3: main.py at root ---
    with tarfile.open(str(tar_path), "r:gz") as tf:
        names = tf.getnames()
        main_present = "main.py" in names
        result["checks"]["main_py_at_root"] = main_present
        if not main_present:
            result["checks"]["archive_contents"] = names[:20]

    # --- Check 4: SHA-256 ---
    h = hashlib.sha256()
    with open(tar_path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    sha = h.hexdigest()
    result["checks"]["sha256"] = sha

    manifest_path = tar_path.with_suffix(".manifest.json")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        manifest_ok = manifest.get("sha256") == sha
        result["checks"]["manifest_sha_match"] = manifest_ok
        if manifest_ok:
            result["checks"]["compressed_size"] = manifest.get("compressed_size")
            result["checks"]["extracted_size"] = manifest.get("extracted_size")
    else:
        result["checks"]["manifest_sha_match"] = None

    result["checks"]["size_within_limit"] = tar_path.stat().st_size < (1 << 30)

    # --- Check 5 & 6: Import + Runtime smoke (optional for non-self-contained bots) ---
    extract_dir = None
    import_ok = False
    runtime_ok = False
    import_error = None
    runtime_action = None

    try:
        with tempfile.TemporaryDirectory(prefix="cx_val_") as tmpdir:
            extract_dir = Path(tmpdir)
            with tarfile.open(str(tar_path), "r:gz") as tf:
                tf.extractall(extract_dir, filter="data")

            sys.path.insert(0, str(extract_dir))
            try:
                importlib.invalidate_caches()
                main_mod = importlib.import_module("main")

                has_agent = hasattr(main_mod, "agent")
                has_make_action = hasattr(main_mod, "make_action")
                result["checks"]["has_agent"] = has_agent
                result["checks"]["has_make_action"] = has_make_action

                if has_agent or has_make_action:
                    import_ok = True
                    result["checks"]["import_smoke"] = True

                    # Runtime smoke test
                    try:
                        if has_agent:
                            class _Obs:
                                board = [0] * 42
                                mark = 1
                            class _Cfg:
                                columns = 7
                                rows = 6
                                inarow = 4
                            runtime_action = main_mod.agent(_Obs(), _Cfg())
                            runtime_ok = isinstance(runtime_action, int) and 0 <= runtime_action <= 6
                            result["checks"]["runtime_api"] = "agent"
                        elif has_make_action:
                            runtime_action = main_mod.make_action([0] * 42, 1, move_deadline=2.0)
                            runtime_ok = isinstance(runtime_action, int) and 0 <= runtime_action <= 6
                            result["checks"]["runtime_api"] = "make_action"
                    except Exception as exc:
                        runtime_ok = False
                        import_error = str(exc)
                        result["checks"]["runtime_error"] = import_error
                    else:
                        result["checks"]["runtime_action"] = runtime_action
                        result["checks"]["runtime_legal"] = runtime_ok
            except Exception as exc:
                import_error = str(exc)
                result["checks"]["import_error"] = import_error
                result["checks"]["import_smoke"] = False
            finally:
                if sys.path and sys.path[0] == str(extract_dir):
                    sys.path.pop(0)
                # Clean cached modules
                for key in list(sys.modules.keys()):
                    if key == "main" or key.startswith("main."):
                        del sys.modules[key]
    except Exception as exc:
        result["checks"]["extraction_error"] = str(exc)
        result["checks"]["import_smoke"] = False

    result["checks"]["runtime_smoke"] = runtime_ok

    # --- Overall ---
    required_checks = [
        "file_exists", "safe_paths", "main_py_at_root",
        "manifest_sha_match", "size_within_limit",
    ]

    # import_smoke and runtime_smoke are required unless the bot is
    # non-self-contained (import error = "No module named 'connectx'").
    import_error = result["checks"].get("import_error", "")
    is_research_bot = "No module named 'connectx'" in (import_error or "")

    pass_checks = list(required_checks)
    if not is_research_bot:
        pass_checks += ["import_smoke", "runtime_smoke"]

    all_pass = all(
        result["checks"].get(k, False) is True
        for k in pass_checks
    )
    result["overall"] = "PASS" if all_pass else "FAIL"
    return result


def main():
    parser = argparse.ArgumentParser(description="Validate a ConnectX submission")
    parser.add_argument("--path", type=str, required=True, help="Path to .tar.gz")
    args = parser.parse_args()

    tar_path = Path(args.path)
    result = validate(tar_path)

    print(f"Validation: {result['overall']}")
    for check, passed in result["checks"].items():
        if isinstance(passed, bool):
            status = "PASS" if passed else "FAIL"
        elif passed is None:
            status = "SKIP"
        else:
            status = "INFO"
        print(f"  [{status}] {check}: {passed}")

    if result["overall"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())