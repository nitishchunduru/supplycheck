import json
import tempfile
import unittest
from pathlib import Path

from supplycheck.reports import write_json, write_markdown
from supplycheck.validator import Issue, ValidationResult


class ReportTests(unittest.TestCase):
    def make_result(self, issues=None, missing_columns=None):
        return ValidationResult(
            source="sample.csv",
            record_type="suppliers",
            total_records=2,
            valid_records=1,
            invalid_records=1 if issues else 0,
            issues=issues or [],
            missing_columns=missing_columns or [],
        )

    def test_json_report_contains_validation_summary(self):
        result = self.make_result([
            Issue(3, "email", "invalid_email", "Invalid email")
        ])
        with tempfile.TemporaryDirectory() as tmp:
            path = write_json(result, Path(tmp) / "nested" / "report.json")
            data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(data["record_type"], "suppliers")
        self.assertEqual(data["total_records"], 2)
        self.assertEqual(data["issue_count"], 1)
        self.assertEqual(data["issues"][0]["code"], "invalid_email")

    def test_markdown_report_escapes_pipes_and_newlines(self):
        result = self.make_result([
            Issue(3, "email", "invalid_email", "Bad | email\naddress")
        ])
        with tempfile.TemporaryDirectory() as tmp:
            path = write_markdown(result, Path(tmp) / "report.md")
            content = path.read_text(encoding="utf-8")

        self.assertIn("| CSV row | Field | Code | Details |", content)
        self.assertIn(r"Bad \| email address", content)

    def test_markdown_report_handles_no_issues_and_missing_columns(self):
        result = self.make_result(missing_columns=["supplier_name"])
        with tempfile.TemporaryDirectory() as tmp:
            path = write_markdown(result, Path(tmp) / "report.md")
            content = path.read_text(encoding="utf-8")

        self.assertIn("supplier_name", content)
        self.assertIn("No issues found.", content)


if __name__ == "__main__":
    unittest.main()
