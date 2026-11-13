import csv
import tempfile
import unittest
from pathlib import Path

from supplycheck.validator import validate_csv


class MaterialValidationTests(unittest.TestCase):
    def make_csv(self, headers, rows):
        temp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", newline="", encoding="utf-8", delete=False
        )
        with temp:
            writer = csv.DictWriter(temp, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))
        return temp.name

    def test_valid_material_without_plant_data(self):
        path = self.make_csv(
            ["material_id", "material_description", "material_type", "base_unit"],
            [{"material_id": "MAT-1001", "material_description": "Steel Bolt",
              "material_type": "ROH", "base_unit": "EA"}],
        )
        result = validate_csv(path, "materials")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.valid_records, 1)

    def test_custom_material_type_is_allowed(self):
        path = self.make_csv(
            ["material_id", "material_description", "material_type", "base_unit"],
            [{"material_id": "MAT-1002", "material_description": "API Ingredient",
              "material_type": "ZAPI", "base_unit": "KG"}],
        )
        result = validate_csv(path, "materials")
        self.assertTrue(result.is_valid)

    def test_duplicate_material_id_is_case_insensitive(self):
        path = self.make_csv(
            ["material_id", "material_description", "material_type", "base_unit"],
            [
                {"material_id": "MAT-1", "material_description": "Bolt",
                 "material_type": "ROH", "base_unit": "EA"},
                {"material_id": "mat-1", "material_description": "Nut",
                 "material_type": "ROH", "base_unit": "EA"},
            ],
        )
        result = validate_csv(path, "materials")
        self.assertEqual(result.invalid_records, 1)
        self.assertIn("duplicate", [issue.code for issue in result.issues])

    def test_storage_location_requires_plant(self):
        path = self.make_csv(
            ["material_id", "material_description", "material_type", "base_unit",
             "plant", "storage_location"],
            [{"material_id": "MAT-2", "material_description": "Washer",
              "material_type": "ROH", "base_unit": "EA",
              "plant": "", "storage_location": "0001"}],
        )
        result = validate_csv(path, "materials")
        self.assertIn("plant_required", [issue.code for issue in result.issues])

    def test_missing_material_description_is_reported(self):
        path = self.make_csv(
            ["material_id", "material_description", "material_type", "base_unit"],
            [{"material_id": "MAT-3", "material_description": "",
              "material_type": "HALB", "base_unit": "KG"}],
        )
        result = validate_csv(path, "materials")
        self.assertIn("required", [issue.code for issue in result.issues])
        self.assertEqual(result.invalid_records, 1)

    def test_missing_required_material_column_is_reported(self):
        path = self.make_csv(
            ["material_id", "material_description", "base_unit"],
            [{"material_id": "MAT-4", "material_description": "Finished item",
              "base_unit": "EA"}],
        )
        result = validate_csv(path, "materials")
        self.assertIn("material_type", result.missing_columns)
        self.assertEqual(result.invalid_records, 1)


if __name__ == "__main__":
    unittest.main()
