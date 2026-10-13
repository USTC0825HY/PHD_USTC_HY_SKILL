"""Offline regression tests for path gating; no instruments or source-data writes."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

from validate_profile_paths import ENV_KEYS, validate

inventory_dir = Path(__file__).resolve().parents[2] / "laser-electrical-data-analysis" / "scripts"
sys.path.insert(0, str(inventory_dir))
spec = importlib.util.spec_from_file_location("skill_inventory_under_test", inventory_dir / "inventory_workspace.py")
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class ProfilePathsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-path-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = self.root / "profile.json"
        self.profile.write_text(json.dumps({"test_data_root": str(self.root / "missing")}), encoding="utf-8")

    def test_missing_input_reports_key_path_and_does_not_create(self):
        result = validate(["test_data_root"], {}, self.profile, {})
        self.assertFalse(result["valid"])
        self.assertEqual(result["paths"][0]["key"], "test_data_root")
        self.assertEqual(result["paths"][0]["path"], str(self.root / "missing"))
        self.assertFalse((self.root / "missing").exists())

    def test_explicit_override_precedes_environment_and_profile(self):
        result = validate(["test_data_root"], {"test_data_root": str(self.root)}, self.profile,
                          {ENV_KEYS["test_data_root"]: str(self.root / "bad-env")})
        self.assertTrue(result["valid"])
        self.assertEqual(result["paths"][0]["source"], "explicit")

    def test_environment_override_precedes_profile(self):
        result = validate(["test_data_root"], {}, self.profile,
                          {ENV_KEYS["test_data_root"]: str(self.root)})
        self.assertTrue(result["valid"])

    def test_unrelated_missing_key_does_not_block_selected_root(self):
        result = validate(["report_root"], {"report_root": str(self.root)}, self.profile, {})
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["paths"]), 1)

    def test_malformed_profile_fails_when_needed(self):
        self.profile.write_text("{", encoding="utf-8")
        self.assertFalse(validate(["test_data_root"], {}, self.profile, {})["valid"])

    def test_explicit_override_works_without_valid_profile(self):
        self.profile.write_text("{", encoding="utf-8")
        self.assertTrue(validate(["test_data_root"], {"test_data_root": str(self.root)}, self.profile, {})["valid"])

    def test_file_is_not_an_input_directory(self):
        self.assertFalse(validate(["test_data_root"], {"test_data_root": str(self.profile)}, self.profile, {})["valid"])

    def test_executable_must_be_file(self):
        self.assertFalse(validate(["vivado_executable"], {"vivado_executable": str(self.root)}, self.profile, {})["valid"])
        self.assertTrue(validate(["vivado_executable"], {"vivado_executable": str(self.profile)}, self.profile, {})["valid"])

    def isolated_config(self):
        return {key: (field, env, self.root / ("absent-" + key))
                for key, (field, env, _) in inventory.ROOT_CONFIG.items()}

    def test_inventory_missing_required_root_fails_before_output(self):
        output = self.root / "must-not-exist" / "inventory.json"
        with mock.patch.object(inventory, "ROOT_CONFIG", self.isolated_config()), \
                mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(sys, "argv", ["inventory", "--output", str(output)]), \
                contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(inventory.main(), 2)
        self.assertFalse(output.parent.exists())
        self.assertIn("test_data_root", stdout.getvalue())

    def test_inventory_explicit_task_root_preserves_optional_missing_status(self):
        with mock.patch.object(inventory, "ROOT_CONFIG", self.isolated_config()), \
                mock.patch.dict(os.environ, {}, clear=True):
            result = inventory.build_inventory(False, {"data": self.root}, ["data"])
        self.assertEqual(result["status"], "partial_inventory")
        self.assertTrue(result["unavailable_roots"])
        self.assertFalse(any(row["required"] for row in result["unavailable_roots"]))

    def test_inventory_cli_override_precedes_environment(self):
        with mock.patch.object(inventory, "ROOT_CONFIG", self.isolated_config()), \
                mock.patch.dict(os.environ, {"LASER_TEST_DATA_ROOT": str(self.root / "bad-env")}, clear=True):
            roots, missing = inventory.resolve_roots({"data": self.root}, ["data"])
        self.assertEqual(roots["data"], self.root)
        self.assertFalse(any(row["required"] for row in missing))


if __name__ == "__main__":
    unittest.main(verbosity=2)
