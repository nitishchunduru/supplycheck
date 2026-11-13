import csv
import tempfile
import unittest
from pathlib import Path
from supplycheck.procurement import validate_procurement

class ProcurementValidationTests(unittest.TestCase):
    def write_csv(self, headers, rows):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", newline="", encoding="utf-8", delete=False)
        with f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        p = Path(f.name)
        self.addCleanup(lambda: p.unlink(missing_ok=True))
        return p

    def masters(self):
        suppliers = self.write_csv(["supplier_id","supplier_name","email","country"],
            [{"supplier_id":"SUP-1","supplier_name":"Example Supplier","email":"supplier@example.com","country":"IN"}])
        materials = self.write_csv(["material_id","material_description","material_type","base_unit"],
            [{"material_id":"MAT-1","material_description":"Steel Bolt","material_type":"ROH","base_unit":"EA"}])
        return suppliers, materials

    def info(self, rows, headers=None):
        return self.write_csv(headers or ["supplier_id","material_id","plant","unit_price","currency"], rows)

    def test_valid_cross_file_reference(self):
        s,m = self.masters()
        i = self.info([{"supplier_id":"SUP-1","material_id":"MAT-1","plant":"1000","unit_price":"12.50","currency":"INR"}])
        r = validate_procurement(s,m,i)
        self.assertTrue(r.is_valid)
        self.assertEqual((r.total_records,r.valid_records,r.invalid_records),(1,1,0))

    def test_unknown_supplier(self):
        s,m = self.masters()
        i = self.info([{"supplier_id":"SUP-X","material_id":"MAT-1","plant":"1000","unit_price":"12","currency":"INR"}])
        self.assertIn("unknown_supplier",[x.code for x in validate_procurement(s,m,i).issues])

    def test_unknown_material(self):
        s,m = self.masters()
        i = self.info([{"supplier_id":"SUP-1","material_id":"MAT-X","plant":"1000","unit_price":"12","currency":"INR"}])
        self.assertIn("unknown_material",[x.code for x in validate_procurement(s,m,i).issues])

    def test_duplicate_combination_case_insensitive(self):
        s,m = self.masters()
        rows = [{"supplier_id":"SUP-1","material_id":"MAT-1","plant":"1000","unit_price":"12","currency":"INR"},
                {"supplier_id":"sup-1","material_id":"mat-1","plant":"1000","unit_price":"13","currency":"INR"}]
        r = validate_procurement(s,m,self.info(rows))
        self.assertIn("duplicate_info_record",[x.code for x in r.issues])
        self.assertEqual(r.invalid_records,1)

    def test_invalid_price_and_currency(self):
        s,m = self.masters()
        i = self.info([{"supplier_id":"SUP-1","material_id":"MAT-1","plant":"1000","unit_price":"-2","currency":"IN"}])
        codes = [x.code for x in validate_procurement(s,m,i).issues]
        self.assertIn("invalid_price",codes)
        self.assertIn("invalid_currency",codes)

    def test_missing_header(self):
        s,m = self.masters()
        i = self.info([{"supplier_id":"SUP-1","material_id":"MAT-1","plant":"1000","unit_price":"12"}],
                      ["supplier_id","material_id","plant","unit_price"])
        r = validate_procurement(s,m,i)
        self.assertIn("currency",r.missing_columns)
        self.assertEqual(r.invalid_records,1)

if __name__ == "__main__":
    unittest.main()
