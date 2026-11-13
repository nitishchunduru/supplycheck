# SupplyCheck

**A local-first CSV data quality toolkit for supplier, product and material master data.**

SupplyCheck helps procurement, operations and engineering teams catch common master-data problems before importing CSV files into business systems.

- Validate supplier, product and material master CSV files.
- Detect duplicate IDs, missing fields, malformed email addresses, invalid prices and currency codes.
- Check basic material master fields and the plant/storage-location dependency.
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

The CLI writes JSON and Markdown reports to `reports/` by default. Use `--report-dir output` to choose another directory. Use `--strict` to return exit code `1` when validation finds issues.

## CSV formats

### Suppliers

Required columns: `supplier_id`, `supplier_name`, `email`, `country`.

### Products

Required columns: `product_id`, `product_name`, `unit_of_measure`, `price`, `currency`.

### Materials

Required columns: `material_id`, `material_description`, `material_type`, `base_unit`.

Optional columns: `plant`, `storage_location`. If `storage_location` is populated, `plant` must also be populated. This is a basic relationship check; SupplyCheck does not verify plant or storage-location codes against an SAP system.

Custom material types such as `ZAPI` are accepted. The tool deliberately does not enforce a fixed SAP material-type catalogue because organisations configure their own types.

Example:

```csv
material_id,material_description,material_type,base_unit,plant,storage_location
MAT-1001,Carbon Steel Bolt,ROH,EA,1000,0001
MAT-1004,API Ingredient,ZAPI,KG,3000,0001
```

All sample data is fictional. Do not upload confidential supplier or material master data to public issues.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Install as a local CLI (optional)

```bash
python -m pip install -e .
supplycheck --help
```

## Limitations

- Email validation checks basic syntax only; it does not verify a mailbox.
- Currency validation checks three alphabetic characters only; it does not verify a live currency registry.
- Country values are checked for presence, not against a country database.
- Material checks validate required fields and the plant/storage-location dependency only. They do not validate SAP configuration, material type customizing, units of measure, plants, storage locations, valuation, or API connectivity.
- CSV validation does not currently handle Excel workbooks, database imports, SAP APIs or vendor onboarding workflows.
- Validation rules are intentionally small and transparent; adapt them to your organisation's policy before production use.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for new validation rules and keep sample data fictional.

## Security

Please see [SECURITY.md](SECURITY.md). Do not submit real supplier personal data, credentials or confidential procurement records in public issues.

## License

MIT. See [LICENSE](LICENSE).
