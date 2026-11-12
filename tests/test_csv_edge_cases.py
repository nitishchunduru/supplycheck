import tempfile
import unittest
from pathlib import Path
from supplycheck.validator import validate_csv

class CsvInputEdgeCaseTests(unittest.TestCase):
    def write_csv(self, content):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", encoding="utf-8",
                                         newline="", delete=False) as f:
            f.write(content)
            name = f.name
        self.addCleanup(lambda: Path(name).unlink(missing_ok=True))
        return name

    def test_utf8_bom_is_supported(self):
        p = self.write_csv("\ufeffsupplier_id,supplier_name,email,country\nS1,Acme,a@acme.com,India\n")
        result = validate_csv(p, "suppliers")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.valid_records, 1)

    def test_duplicate_headers_rejected_after_normalization(self):
        p = self.write_csv("supplier_id,SUPPLIER_ID,supplier_name,email,country\nS1,S2,Acme,a@acme.com,India\n")
        with self.assertRaisesRegex(ValueError, "duplicate column"):
            validate_csv(p, "suppliers")

    def test_extra_values_reported_without_crashing(self):
        p = self.write_csv("supplier_id,supplier_name,email,country\nS1,Acme,a@acme.com,India,unexpected\n")
        result = validate_csv(p, "suppliers")
        self.assertEqual(result.invalid_records, 1)
        self.assertIn("extra_columns", [x.code for x in result.issues])

    def test_blank_lines_ignored(self):
        p = self.write_csv("supplier_id,supplier_name,email,country\n\nS1,Acme,a@acme.com,India\n\n")
        result = validate_csv(p, "suppliers")
        self.assertEqual(result.total_records, 1)
        self.assertTrue(result.is_valid)

    def test_malformed_quoted_csv_has_clear_error(self):
        p = self.write_csv('supplier_id,supplier_name,email,country\nS1,"Acme,a@acme.com,India\n')
        with self.assertRaisesRegex(ValueError, "Malformed CSV"):
            validate_csv(p, "suppliers")

if __name__ == "__main__":
    unittest.main()
