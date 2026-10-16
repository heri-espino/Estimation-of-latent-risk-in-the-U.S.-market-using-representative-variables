"""Small stdlib-only tests for the stage-0 data audit."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "preflight.py"
spec = importlib.util.spec_from_file_location("risk_preflight", MODULE)
preflight = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(preflight)

HEADER = "country,observation_date,available_date,variable,value,source\n"
ONE = "MEX,2020-01-31,2020-02-07,m2,123.4,Banxico\n"


class PreflightTests(unittest.TestCase):
    def check(self, rows: str) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "panel.csv"
            path.write_text(HEADER + rows, encoding="utf-8")
            return preflight.audit_panel(path)

    def test_valid_panel(self):
        result = self.check(ONE + "USA,2020-01-31,2020-01-31,equity_returns,0.01,Market\n")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["valid_rows"], 2)

    def test_duplicate_key_rejected(self):
        result = self.check(ONE + ONE)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("duplicate" in entry["error"] for entry in result["errors"]))

    def test_release_before_observation_rejected(self):
        result = self.check("MEX,2020-02-29,2020-01-29,m2,12,Banxico\n")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("earlier" in entry["error"] for entry in result["errors"]))

    def test_nonfinite_values_rejected(self):
        result = self.check("MEX,2020-01-31,2020-02-07,m2,nan,Banxico\n")
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
