import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "pst_signal_trace.py"
SPEC = importlib.util.spec_from_file_location("pst_signal_trace", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PstSignalTraceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pst = self.root / "board" / "allegro"
        self.pst.mkdir(parents=True)
        (self.root / "board" / "board.dsn").write_bytes(b"dsn")
        (self.root / "board" / "board.pdf").write_bytes(b"pdf")
        (self.pst / "pstxnet.dat").write_text(
            "FILE_TYPE = EXPANDEDNETLIST;\n{ Using PSTWRITER 17.4 test }\n"
            "NET_NAME\n'CTRL_A'\n '@ROOT:CTRL_A':\n"
            "NODE_NAME\tD1 A1\n '@ROOT:D1':\n 'IO':;\n"
            "NODE_NAME\tR1 1\n '@ROOT:R1':\n '1':;\n"
            "NET_NAME\n'CTRL_B'\n '@ROOT:CTRL_B':\n"
            "NODE_NAME\tR1 2\n '@ROOT:R1':\n '2':;\n"
            "NODE_NAME\tU1 3\n '@ROOT:U1':\n 'EN':;\n",
            encoding="utf-8",
        )
        (self.pst / "pstxprt.dat").write_text(
            "PART_NAME\n R1 'RES_TSD':;\n C_PATH='@R1';\n"
            "PART_NAME\n U1 'CHIP_REAL':;\n C_PATH='@U1';\n",
            encoding="utf-8",
        )
        (self.pst / "pstchip.dat").write_text(
            "primitive 'RES_TSD';\n VALUE='TSD*';\n"
            "primitive 'CHIP_REAL';\n VALUE='CONTROL';\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_exact_net_and_tsd(self):
        result = MODULE.query_evidence(self.pst, "board", "ctrl_a", None, False)
        self.assertEqual(result[0]["network"], "CTRL_A")
        resistor = next(node for node in result[0]["nodes"] if node["refdes"] == "R1")
        self.assertEqual(resistor["assembly_markers"], ["TSD"])
        self.assertEqual(resistor["fitted_state"], "unknown")
        self.assertNotIn("未焊", resistor["assembly_status"])
        self.assertEqual(MODULE.flatten_results(result)[1]["fitted_state"], "unknown")

    def test_dnp_and_unmarked_do_not_prove_population(self):
        self.assertEqual(MODULE.assembly_markers(None, {"value":"DNP"}), ["DNP"])
        self.assertIn("未核实", MODULE.assembly_status(None, {"value":"10k"}))

    def test_node_returns_two_separate_nets(self):
        result = MODULE.query_evidence(self.pst, "board", None, "R1", False)
        self.assertEqual({item["network"] for item in result}, {"CTRL_A", "CTRL_B"})

    def test_exact_is_not_fuzzy(self):
        with self.assertRaises(LookupError):
            MODULE.query_evidence(self.pst, "board", "CTRL", None, False)
        result = MODULE.query_evidence(self.pst, "board", "CTRL_.*", None, True)
        self.assertEqual(len(result), 2)

    def test_inventory_complete(self):
        rows = MODULE.inventory(self.root)
        self.assertEqual(rows[0]["status"], "完整证据集")
        self.assertTrue(rows[0]["pst_sets"][0]["complete"])


if __name__ == "__main__":
    unittest.main()
