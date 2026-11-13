
import tempfile
import unittest
from pathlib import Path

from supplycheck.cli import main


class CliTests(unittest.TestCase):
    def test_normal_validation_returns_zero_with_invalid_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = main([
                "validate", "suppliers",
                "examples/suppliers.csv",
                "--report-dir", tmp,
            ])
        self.assertEqual(result, 0)

    def test_strict_validation_returns_one_with_invalid_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = main([
                "validate", "suppliers",
                "examples/suppliers.csv",
                "--strict",
                "--report-dir", tmp,
            ])
        self.assertEqual(result, 1)

    def test_missing_file_returns_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = main([
                "validate", "suppliers",
                str(Path(tmp) / "missing.csv"),
                "--report-dir", tmp,
            ])
        self.assertEqual(result, 2)

    def test_missing_procurement_arguments_exits_with_two(self):
        with self.assertRaises(SystemExit) as context:
            main(["validate", "procurement", "examples/info_records.csv"])
        self.assertEqual(context.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
