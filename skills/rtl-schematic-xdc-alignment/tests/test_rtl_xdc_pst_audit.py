import argparse
import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "rtl_xdc_pst_audit.py"
SPEC = importlib.util.spec_from_file_location("rtl_xdc_pst_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class RtlXdcPstAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.rtl = self.root / "top.v"
        self.xdc = self.root / "top.xdc"
        self.pst = self.root / "pstxnet.dat"
        self.rtl.write_text("module top(input wire busy, output wire [1:0] ctrl); endmodule\n", encoding="utf-8")
        self.pst.write_text(
            "NET_NAME\n'N_A1'\n '@ROOT:N_A1':\nNODE_NAME\tD1 A1\n '@ROOT:D1':\n 'IO':;\n"
            "NET_NAME\n'N_A2'\n '@ROOT:N_A2':\nNODE_NAME\tD1 A2\n '@ROOT:D1':\n 'IO':;\n"
            "NET_NAME\n'N_A3'\n '@ROOT:N_A3':\nNODE_NAME\tD1 A3\n '@ROOT:D1':\n 'IO':;\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def run_audit(self, xdc):
        self.xdc.write_text(xdc, encoding="utf-8")
        return MODULE.audit(argparse.Namespace(rtl=self.rtl, top="top", xdc=self.xdc, pstxnet=self.pst, fpga_refdes="D1"))

    def test_valid_multiline_bus(self):
        result = self.run_audit(
            "set_property PACKAGE_PIN A1 [get_ports {busy}]\n"
            "set_property PACKAGE_PIN A2 [get_ports {ctrl[0]}]\n"
            "set_property PACKAGE_PIN A3 [get_ports {ctrl[1]}]\n"
            "set_property IOSTANDARD LVCMOS18 [get_ports {\n busy ctrl[*]\n}]\n"
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(len(result["rows"]), 3)

    def test_duplicate_pin(self):
        result = self.run_audit(
            "set_property PACKAGE_PIN A1 [get_ports busy]\n"
            "set_property PACKAGE_PIN A1 [get_ports {ctrl[0]}]\n"
            "set_property IOSTANDARD LVCMOS18 [get_ports {busy ctrl[0]}]\n"
        )
        self.assertTrue(any("同时绑定" in error for error in result["errors"]))

    def test_missing_port_iostandard_and_pst_ball(self):
        result = self.run_audit(
            "set_property PACKAGE_PIN Z9 [get_ports absent]\n"
        )
        joined = "\n".join(result["errors"])
        self.assertIn("RTL顶层中不存在", joined)
        self.assertIn("缺少IOSTANDARD", joined)
        self.assertIn("未在PST", joined)


if __name__ == "__main__":
    unittest.main()
