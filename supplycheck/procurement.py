"""Cross-file procurement checks for supplier, material and purchasing info records."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
from pathlib import Path
from .validator import Issue, ValidationResult, _EXTRA_KEY, _read_csv

INFO_REQUIRED = ("supplier_id", "material_id", "plant", "unit_price", "currency")

def validate_procurement(suppliers_path, materials_path, info_records_path) -> ValidationResult:
    """Check purchasing info records against supplier and material master CSVs."""
    supplier_rows, supplier_headers = _read_csv(suppliers_path)
    material_rows, material_headers = _read_csv(materials_path)
    info_rows, info_headers = _read_csv(info_records_path)
    issues = []
    if "supplier_id" not in supplier_headers:
        issues.append(Issue(1, "supplier_id", "missing_master_column",
                            "Supplier master is missing required column 'supplier_id'."))
    if "material_id" not in material_headers:
        issues.append(Issue(1, "material_id", "missing_master_column",
                            "Material master is missing required column 'material_id'."))
    missing_columns = [f for f in INFO_REQUIRED if f not in info_headers]
    for field in missing_columns:
        issues.append(Issue(1, field, "missing_column",
                            f"Required purchasing info-record column '{field}' is missing."))
    supplier_ids = {r.get("supplier_id", "").casefold() for r in supplier_rows if r.get("supplier_id", "")}
    material_ids = {r.get("material_id", "").casefold() for r in material_rows if r.get("material_id", "")}
    seen = {}
    for row_num, row in enumerate(info_rows, start=2):
        row_issues = []
        extras = row.get(_EXTRA_KEY)
        if extras:
            row_issues.append(Issue(
                row_num, "row", "extra_columns",
                f"Row contains {len(extras)} value(s) beyond the CSV header.",
                ", ".join(extras)
            ))
        supplier_id, material_id, plant = (row.get("supplier_id", ""),
                                             row.get("material_id", ""), row.get("plant", ""))
        for field, value in (("supplier_id", supplier_id), ("material_id", material_id),
                             ("plant", plant), ("unit_price", row.get("unit_price", "")),
                             ("currency", row.get("currency", ""))):
            if not value:
                row_issues.append(Issue(row_num, field, "required", f"{field} is required."))
        if supplier_id and "supplier_id" in supplier_headers and supplier_id.casefold() not in supplier_ids:
            row_issues.append(Issue(row_num, "supplier_id", "unknown_supplier",
                                    f"Supplier '{supplier_id}' was not found in the supplier master.", supplier_id))
        if material_id and "material_id" in material_headers and material_id.casefold() not in material_ids:
            row_issues.append(Issue(row_num, "material_id", "unknown_material",
                                    f"Material '{material_id}' was not found in the material master.", material_id))
        if supplier_id and material_id and plant:
            key = (supplier_id.casefold(), material_id.casefold(), plant.casefold())
            if key in seen:
                row_issues.append(Issue(row_num, "supplier_id/material_id/plant",
                                        "duplicate_info_record",
                                        f"Duplicate supplier-material-plant combination (first seen on row {seen[key]}).",
                                        f"{supplier_id}/{material_id}/{plant}"))
            else:
                seen[key] = row_num
        price = row.get("unit_price", "")
        if price:
            try:
                amount = Decimal(price)
                if not amount.is_finite() or amount < 0: raise InvalidOperation
            except (InvalidOperation, ValueError):
                row_issues.append(Issue(row_num, "unit_price", "invalid_price",
                                        f"'{price}' must be a non-negative number.", price))
        currency = row.get("currency", "")
        if currency and (len(currency) != 3 or not currency.isalpha()):
            row_issues.append(Issue(row_num, "currency", "invalid_currency",
                                    "currency must be a three-letter alphabetic code, e.g. INR or USD.", currency))
        issues.extend(row_issues)
    invalid_rows = {i.row for i in issues if i.row > 1}
    if missing_columns and info_rows: invalid_rows.update(range(2, len(info_rows) + 2))
    invalid = len(invalid_rows)
    return ValidationResult(str(Path(info_records_path)), "procurement", len(info_rows),
                            max(0, len(info_rows)-invalid), invalid, issues, missing_columns)
