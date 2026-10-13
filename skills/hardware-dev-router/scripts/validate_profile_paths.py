"""Read-only validation of task-selected Laser profile dependencies."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ENV_KEYS = {
    "matlab_code_root": "LASER_TEST_CODE_ROOT",
    "test_data_root": "LASER_TEST_DATA_ROOT",
    "report_root": "LASER_TEST_REPORT_ROOT",
    "cw513_analysis_root": "LASER_TEST_513_CODE_ROOT",
    "cw513_test_data_root": "LASER_TEST_513_DATA_ROOT",
    "requirement_root": "LASER_TEST_REQUIREMENT_ROOT",
}


def validate(keys, overrides, profile_file, environ=None):
    env = os.environ if environ is None else environ
    profile = {}
    profile_error = None
    needs_profile = any(not overrides.get(k) and not env.get(ENV_KEYS.get(k, ""), "").strip() for k in keys)
    if needs_profile:
        try:
            profile = json.loads(Path(profile_file).read_text(encoding="utf-8-sig"))
            if not isinstance(profile, dict):
                raise ValueError("profile must be an object")
        except (OSError, ValueError) as exc:
            profile_error = str(exc)
            profile = {}
    rows = []
    for key in keys:
        env_name = ENV_KEYS.get(key)
        if key in overrides:
            value, origin = overrides[key], "explicit"
        elif env_name and env.get(env_name, "").strip():
            value, origin = env[env_name], env_name
        else:
            value, origin = profile.get(key), str(profile_file)
        row = {"key": key, "source": origin, "path": value, "valid": False}
        if not isinstance(value, str) or not value.strip():
            row["error"] = profile_error if origin == str(profile_file) and profile_error else "missing or invalid path value"
        else:
            path = Path(value).expanduser()
            row["path"] = str(path)
            try:
                valid = path.is_file() if key.endswith("_executable") else path.is_dir() if key.endswith("_root") else path.exists()
                row["valid"] = valid
                if not valid:
                    row["error"] = "required path missing or wrong file/directory type"
            except (OSError, ValueError) as exc:
                row["error"] = str(exc)
        rows.append(row)
    return {"valid": all(row["valid"] for row in rows), "paths": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    parser.add_argument("--profile", type=Path, default=home / "laser-fpga-profile.json")
    parser.add_argument("--key", action="append", required=True)
    parser.add_argument("--override", action="append", default=[], metavar="KEY=PATH")
    args = parser.parse_args()
    overrides = {}
    for item in args.override:
        key, sep, value = item.partition("=")
        if not sep or key not in args.key or not value.strip() or key in overrides:
            parser.error("each override must uniquely name a selected key with a nonempty path")
        overrides[key] = value
    result = validate(list(dict.fromkeys(args.key)), overrides, args.profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
