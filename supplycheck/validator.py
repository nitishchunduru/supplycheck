"""Validation rules for supplier, product and material master-data CSV files."""
from __future__ import annotations

import csv
import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SUPPLIER_REQUIRED = ("supplier_id", "supplier_name", "email", "country")
PRODUCT_REQUIRED = ("product_id", "product_name", "unit_of_measure", "price", "currency")
MATERIAL_REQUIRED = ("material_id", "material_description", "material_type", "base_unit")
_EXTRA_KEY = "__supplycheck_extra_columns__"


@dataclass(frozen=True)
class Issue:
    row: int
    field: str
    code: str
    message: str
    value: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ValidationResult:
    source: str
    record_type: str
    total_records: int
    valid_records: int
    invalid_records: int
    issues: list[Issue]
    missing_columns: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.issues and not self.missing_columns

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "record_type": self.record_type,
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "issue_count": len(self.issues),
            "missing_columns": self.missing_columns,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _read_csv(path: str | Path) -> tuple[list[dict], list[str]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Input path is not a file: {file_path}")
    try:
        with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, restkey=_EXTRA_KEY, strict=True)
            if not reader.fieldnames:
                raise ValueError("CSV is empty or has no header row.")
            headers = [h.strip().lower() if h else "" for h in reader.fieldnames]
            if _EXTRA_KEY in headers:
                raise ValueError(f"'{_EXTRA_KEY}' is a reserved CSV column name.")
            if len(headers) != len(set(headers)):
                raise ValueError("CSV contains duplicate column names.")
            rows = []
            for row in reader:
                extras = row.pop(_EXTRA_KEY, None)
                normalized = {
                    (key.strip().lower() if key else ""): (value or "").strip()
                    for key, value in row.items()
                }
                if extras:
                    normalized[_EXTRA_KEY] = extras
                rows.append(normalized)
            return rows, headers
    except UnicodeDecodeError as exc:
        raise ValueError("CSV must be encoded as UTF-8 (UTF-8 with BOM is supported).") from exc
    except csv.Error as exc:
        raise ValueError(f"Malformed CSV: {exc}") from exc


def validate_csv(path: str | Path, record_type: str) -> ValidationResult:
    kind = record_type.strip().lower()
    if kind not in {"suppliers", "products", "materials"}:
        raise ValueError("record_type must be 'suppliers', 'products' or 'materials'.")

    rows, headers = _read_csv(path)
    if kind == "suppliers":
        required = SUPPLIER_REQUIRED
        id_field = "supplier_id"
    elif kind == "products":
        required = PRODUCT_REQUIRED
        id_field = "product_id"
    else:
        required = MATERIAL_REQUIRED
        id_field = "material_id"

    missing_columns = [column for column in required if column not in headers]
    issues: list[Issue] = []
    for column in missing_columns:
        issues.append(Issue(
            1, column, "missing_column",
            f"Required column '{column}' is missing from the CSV header."
        ))

    seen: dict[str, int] = {}
    for index, row in enumerate(rows, start=2):
        row_issues: list[Issue] = []
        extras = row.get(_EXTRA_KEY)
        if extras:
            row_issues.append(Issue(
                index, "row", "extra_columns",
                f"Row contains {len(extras)} value(s) beyond the CSV header.",
                ", ".join(extras)
            ))

        record_id = row.get(id_field, "")
        if not record_id:
            row_issues.append(Issue(index, id_field, "required", f"{id_field} is required."))
        elif record_id.casefold() in seen:
            row_issues.append(Issue(
                index, id_field, "duplicate",
                f"Duplicate {id_field} '{record_id}' (first seen on row {seen[record_id.casefold()]}).",
                record_id
            ))
        else:
            seen[record_id.casefold()] = index

        if kind == "suppliers":
            for field in ("supplier_name", "country"):
                if not row.get(field, ""):
                    row_issues.append(Issue(index, field, "required", f"{field} is required."))
            email = row.get("email", "")
            if not email:
                row_issues.append(Issue(index, "email", "required", "email is required."))
            elif not EMAIL_RE.fullmatch(email):
                row_issues.append(Issue(
                    index, "email", "invalid_email",
                    f"'{email}' is not a valid email address.", email
                ))

        elif kind == "products":
            for field in ("product_name", "unit_of_measure", "currency"):
                if not row.get(field, ""):
                    row_issues.append(Issue(index, field, "required", f"{field} is required."))
            price = row.get("price", "")
            if not price:
                row_issues.append(Issue(index, "price", "required", "price is required."))
            else:
                try:
                    amount = Decimal(price)
                    if not amount.is_finite() or amount < 0:
                        raise InvalidOperation
                except (InvalidOperation, ValueError):
                    row_issues.append(Issue(
                        index, "price", "invalid_price",
                        f"'{price}' must be a non-negative number.", price
                    ))
            currency = row.get("currency", "")
            if currency and (len(currency) != 3 or not currency.isalpha()):
                row_issues.append(Issue(
                    index, "currency", "invalid_currency",
                    "currency must be a three-letter code, e.g. USD or INR.", currency
                ))

        else:
            for field in ("material_description", "material_type", "base_unit"):
                if not row.get(field, ""):
                    row_issues.append(Issue(index, field, "required", f"{field} is required."))

            # In SAP-style plant/storage-location data, a storage location belongs to a plant.
            # This checks the relationship only; it does not verify either code against SAP.
            plant = row.get("plant", "")
            storage_location = row.get("storage_location", "")
            if storage_location and not plant:
                row_issues.append(Issue(
                    index, "plant", "plant_required",
                    "plant is required when storage_location is provided.",
                    storage_location
                ))

        issues.extend(row_issues)

    invalid_rows = {issue.row for issue in issues if issue.row > 1}
    if missing_columns and rows:
        invalid_rows.update(range(2, len(rows) + 2))
    invalid_records = len(invalid_rows)
    return ValidationResult(
        str(Path(path)), kind, len(rows),
        max(0, len(rows) - invalid_records), invalid_records,
        issues, missing_columns
    )
