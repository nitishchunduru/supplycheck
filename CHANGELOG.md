# Changelog

All notable SupplyCheck changes are documented here.

## 1.3.0 — Procurement cross-file validation
- Added purchasing info-record validation against supplier and material master CSV files.
- Added unknown supplier/material reference checks.
- Added duplicate supplier + material + plant combination detection (case-insensitive).
- Added required-field, non-negative unit-price and currency-format checks.
- Added fictional procurement examples and automated tests.
- Extended CI coverage through Python 3.14.

## 1.2.0 — Material master validation
- Added material master CSV validation and required-field checks.
- Added duplicate material ID detection and plant/storage-location dependency checking.
- Added fictional examples and automated tests.

## 1.1.0 — CSV validation reliability
- Added UTF-8 BOM support and duplicate normalized-header detection.
- Added detection of extra CSV values beyond the header.
- Improved blank-line, malformed-quote and UTF-8 decoding error handling.
- Expanded CSV edge-case tests and CI coverage.

## 1.0.0 — Initial MVP
- Supplier and product CSV validation.
- Duplicate ID, required-field, email, price and currency checks.
- JSON and Markdown reports.
- Standard-library tests and example datasets.
