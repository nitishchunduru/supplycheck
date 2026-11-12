import csv
import tempfile
import unittest
from pathlib import Path

from supplycheck.validator import validate_csv


class SupplierValidationTests(unittest.TestCase):
    def make_csv(self, headers, rows):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", newline="",
                                           encoding="utf-8", delete=False)
        with temp:
            writer = csv.DictWriter(temp, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))
        return temp.name

    def test_valid_supplier_rows(self):
        path = self.make_csv(
            ["supplier_id", "supplier_name", "email", "country"],
            [{"supplier_id": "S001", "supplier_name": "Acme", "email": "a@acme.com", "country": "India"}],
        )
        result = validate_csv(path, "suppliers")
        self.assertEqual(result.valid_records, 1)
        self.assertEqual(result.invalid_records, 0)
        self.assertEqual(result.issues, [])

    def test_duplicate_supplier_id_is_detected_case_insensitively(self):
        path = self.make_csv(
            ["supplier_id", "supplier_name", "email", "country"],
            [
                {"supplier_id": "S001", "supplier_name": "Acme", "email": "a@acme.com", "country": "India"},
                {"supplier_id": "s001", "supplier_name": "Acme Two", "email": "b@acme.com", "country": "India"},
            ],
        )
        result = validate_csv(path, "suppliers")
        self.assertEqual(result.invalid_records, 1)
        self.assertIn("duplicate", [issue.code for issue in result.issues])

    def test_invalid_email_and_missing_name(self):
        path = self.make_csv(
            ["supplier_id", "supplier_name", "email", "country"],
            [{"supplier_id": "S001", "supplier_name": "", "email": "not-an-email", "country": "India"}],
        )
        result = validate_csv(path, "suppliers")
        codes = {issue.code for issue in result.issues}
        self.assertIn("required", codes)
        self.assertIn("invalid_email", codes)

    def test_missing_required_column_is_reported(self):
        path = self.make_csv(
            ["supplier_id", "supplier_name", "email"],
            [{"supplier_id": "S001", "supplier_name": "Acme", "email": "a@acme.com"}],
        )
        result = validate_csv(path, "suppliers")
        self.assertIn("country", result.missing_columns)
        self.assertGreater(result.invalid_records, 0)


class ProductValidationTests(unittest.TestCase):
    def make_csv(self, headers, rows):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", newline="",
                                           encoding="utf-8", delete=False)
        with temp:
            writer = csv.DictWriter(temp, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))
        return temp.name

    def test_negative_price_and_bad_currency(self):
        path = self.make_csv(
            ["product_id", "product_name", "unit_of_measure", "price", "currency"],
            [{"product_id": "P001", "product_name": "Bolt", "unit_of_measure": "EA",
              "price": "-2.5", "currency": "IN"}],
        )
        result = validate_csv(path, "products")
        codes = {issue.code for issue in result.issues}
        self.assertIn("invalid_price", codes)
        self.assertIn("invalid_currency", codes)

    def test_valid_product(self):
        path = self.make_csv(
            ["product_id", "product_name", "unit_of_measure", "price", "currency"],
            [{"product_id": "P001", "product_name": "Bolt", "unit_of_measure": "EA",
              "price": "12.50", "currency": "INR"}],
        )
        result = validate_csv(path, "products")
        self.assertEqual(result.valid_records, 1)
        self.assertTrue(result.is_valid)


if __name__ == "__main__":
    unittest.main()
