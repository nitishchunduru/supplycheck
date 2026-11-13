import tempfile
import unittest
from pathlib import Path

from supplycheck.procurement import validate_procurement


class ProcurementEdgeCaseTests(unittest.TestCase):
    def test_extra_values_in_info_record_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            suppliers = root / "suppliers.csv"
            suppliers.write_text(
                "supplier_id,supplier_name,email,country\n"
                "SUP-1,Example Supplier,supplier@example.com,IN\n",
                encoding="utf-8",
            )

            materials = root / "materials.csv"
            materials.write_text(
                "material_id,material_description,material_type,base_unit\n"
                "MAT-1,Steel Bolt,ROH,EA\n",
                encoding="utf-8",
            )

            info_records = root / "info_records.csv"
            info_records.write_text(
                "supplier_id,material_id,plant,unit_price,currency\n"
                "SUP-1,MAT-1,1000,12.50,INR,UNEXPECTED\n",
                encoding="utf-8",
            )

            result = validate_procurement(suppliers, materials, info_records)

        self.assertIn("extra_columns", [issue.code for issue in result.issues])
        self.assertEqual(result.invalid_records, 1)


if __name__ == "__main__":
    unittest.main()
