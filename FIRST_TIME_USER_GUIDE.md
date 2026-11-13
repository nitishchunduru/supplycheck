# SupplyCheck — First-time user guide

SupplyCheck is a local-first Python command-line tool for checking supplier, product, material, and procurement CSV data. It is an early-stage project; it does not connect to SAP or post data into business systems.

## 1. Requirements

- Python 3.10 or newer
- Git (if cloning the repository)
- Windows PowerShell, macOS, or Linux terminal

## 2. Get the project

```bash
git clone https://github.com/nitishchunduru/supplycheck.git
cd supplycheck
```

## 3. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install locally

```bash
python -m pip install -e .
```

## 5. Try the sample validations

From the repository root:

```bash
python -m supplycheck validate suppliers examples/suppliers.csv
python -m supplycheck validate products examples/products.csv
python -m supplycheck validate materials examples/materials.csv
```

For procurement cross-file validation, the command requires supplier and material master CSV paths:

```bash
python -m supplycheck validate procurement examples/info_records.csv --suppliers examples/suppliers.csv --materials examples/materials.csv
```

If your installed CLI reports different usage, run:

```bash
python -m supplycheck --help
python -m supplycheck validate --help
```

## 6. Understand the result

SupplyCheck prints a validation summary and writes JSON and Markdown reports. Read the reported row number, field, issue code, and message; correct the source CSV and run the command again.

A normal validation run can report invalid records while returning exit code 0. Use `--strict` when your automation should return exit code 1 if validation issues are found. A missing input file or invalid command usage returns an error exit code.

## 7. Use safe test data

Start with the repository's fictional examples. Never upload or commit real supplier, customer, employee, financial, or confidential procurement data. If you report a problem, include a small fictional or properly anonymized reproduction.

## 8. Report feedback

- Bug: https://github.com/nitishchunduru/supplycheck/issues/new?template=bug_report.yml
- Feature idea: https://github.com/nitishchunduru/supplycheck/issues/new?template=feature_request.yml

Include your Python version, operating system, command used, expected result, actual result, and a minimal sample with fictional data.

## Scope limits

SupplyCheck performs transparent CSV checks. It is not an SAP connector, does not validate live SAP configuration, and does not establish that a purchasing record is approved or ready for posting.
