# SupplyCheck

**A local-first CSV data quality toolkit for supplier and product master data.**

SupplyCheck helps procurement, operations and engineering teams catch common master-data problems before importing CSV files into business systems.

- Validate supplier and product CSV files.
- Detect duplicate IDs, missing fields, malformed email addresses, invalid prices and currency codes.
- Generate JSON and Markdown reports.
- Run locally with Python's standard library. No API key, database server or paid service required.

> **Project status:** MVP / beta. This release provides basic CSV validation, not a complete SAP integration or a replacement for enterprise master-data governance.

## Quick start

Requires Python 3.10 or newer.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m supplycheck validate suppliers examples/suppliers.csv
python -m supplycheck validate products examples/products.csv
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m supplycheck validate suppliers examples/suppliers.csv
python -m supplycheck validate products examples/products.csv
```

The CLI writes reports to `reports/` by default:

- `suppliers_validation.json`
- `suppliers_validation.md`
- `products_validation.json`
- `products_validation.md`

Use a custom report directory:

```bash
python -m supplycheck validate suppliers path/to/suppliers.csv --report-dir output
```

Use strict mode in scripts or CI. It returns exit code `1` when validation finds issues:

```bash
python -m supplycheck validate suppliers examples/suppliers.csv --strict
```

## CSV formats

### Suppliers

Required columns (header matching is case-insensitive):

| Column | Rule |
|---|---|
| `supplier_id` | Required and unique (case-insensitive) |
| `supplier_name` | Required |
| `email` | Required; basic email format check |
| `country` | Required |

Example:

```csv
supplier_id,supplier_name,email,country
S001,ABC Metals,procurement@example.com,India
```

### Products

| Column | Rule |
|---|---|
| `product_id` | Required and unique (case-insensitive) |
| `product_name` | Required |
| `unit_of_measure` | Required |
| `price` | Required; non-negative decimal |
| `currency` | Required; three-letter alphabetic code |

Example:

```csv
product_id,product_name,unit_of_measure,price,currency
MAT-1001,Stainless Steel Bolt,EA,12.50,INR
```

## Run tests

No third-party test framework is needed:

```bash
python -m unittest discover -s tests -v
```

## Install as a local CLI (optional)

```bash
python -m pip install -e .
supplycheck --help
```

## Design

```text
CSV input
   |
   v
CSV reader + header normalization
   |
   v
Supplier / product validation rules
   |
   +------> Terminal summary
   |
   +------> JSON report
   |
   +------> Markdown report
```

The tool does not modify input files. All processing happens locally.

## Limitations

- The email check is intentionally a basic syntax check; it does not verify that a mailbox exists.
- Currency validation checks for a three-letter alphabetic code; it does not verify the code against a live currency registry.
- Country values are checked for presence, not against a country database.
- CSV validation does not currently handle Excel workbooks, database imports, SAP APIs or vendor onboarding workflows.
- Validation rules are intentionally small and transparent; adapt them to your organisation's policy before production use.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for new validation rules and keep sample data fictional.

## Security

Please see [SECURITY.md](SECURITY.md). Do not submit real supplier personal data, credentials or confidential procurement records in public issues.

## License

MIT. See [LICENSE](LICENSE).
