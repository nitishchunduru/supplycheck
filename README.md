# SupplyCheck

**A local-first CSV data quality toolkit for supplier, product, material and procurement data.**

SupplyCheck helps procurement, operations and engineering teams catch common data-quality problems before importing CSV files into business systems.

- Validate supplier, product and material master CSV files.
- Validate purchasing info records against supplier and material master identifiers.
- Detect missing fields, duplicate IDs, unknown supplier/material references, duplicate supplier-material-plant combinations, malformed email addresses, invalid prices and currency-format problems.
- Generate JSON and Markdown reports.
- Run locally with Python's standard library. No API key, database server or paid service required.

> **Project status:** MVP / beta. SupplyCheck provides transparent CSV checks, not a complete SAP integration or a replacement for enterprise master-data governance.

## Quick start

Requires Python 3.10 or newer.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m supplycheck validate suppliers examples/suppliers.csv
python -m supplycheck validate products examples/products.csv
python -m supplycheck validate materials examples/materials.csv
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m supplycheck validate suppliers examples/suppliers.csv
python -m supplycheck validate products examples/products.csv
python -m supplycheck validate materials examples/materials.csv
```

## Procurement cross-file validation (1.3)

```bash
python -m supplycheck validate procurement examples/info_records.csv --suppliers examples/suppliers.csv --materials examples/materials.csv
```

Required info-record columns: `supplier_id`, `material_id`, `plant`, `unit_price`, `currency`.

The procurement validator checks that supplier and material IDs referenced by each info record exist in their respective master CSVs, that supplier + material + plant combinations are unique (case-insensitive), that required values are present, that unit prices are non-negative decimal numbers, and that currency values contain three alphabetic characters.

**Scope boundary:** this command checks references to supplier and material IDs; it does not run the complete supplier/material validators against those master files. It does not establish that a supplier is approved for a plant or verify purchasing organisation, info-record validity dates, source lists, contracts, tax, pricing conditions, SAP customizing, or live SAP data. Treat this as an early CSV quality screen, not proof that a purchasing record is ready for production posting.

All sample data is fictional. Never commit real supplier personal data or confidential procurement records.

## CSV formats

- Suppliers: `supplier_id`, `supplier_name`, `email`, `country`.
- Products: `product_id`, `product_name`, `unit_of_measure`, `price`, `currency`.
- Materials: `material_id`, `material_description`, `material_type`, `base_unit`; optional `plant`, `storage_location`.
- Procurement info records: `supplier_id`, `material_id`, `plant`, `unit_price`, `currency`.

Custom material types such as `ZAPI` are accepted. Material checks only verify that a plant is supplied when a storage location is populated; they do not verify SAP plant or storage-location codes.

## Reports and exit codes

Reports are written to `reports/` by default. Use `--report-dir output` to choose another directory and `--strict` to return exit code `1` when validation finds issues.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Install as a local CLI

```bash
python -m pip install -e .
supplycheck --help
```

## Limitations

- Email validation checks syntax only; it does not verify a mailbox.
- Currency validation checks three alphabetic characters only; it does not verify a live currency registry.
- Country values are checked for presence only.
- Material and procurement checks are basic CSV checks, not SAP integration or configuration validation.
- Procurement cross-file validation does not recursively validate every supplier/material master field; it checks identifier references and info-record rules.
- Excel workbooks, database imports, SAP APIs and vendor onboarding workflows are not currently supported.
- Adapt validation rules to your organisation's policy before production use.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Include tests for new rules and keep sample data fictional.

## Security

See [SECURITY.md](SECURITY.md). Do not submit real supplier personal data, credentials or confidential procurement records in public issues.

## License

MIT. See [LICENSE](LICENSE).
