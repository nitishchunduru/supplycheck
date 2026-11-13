# SupplyCheck — 60-second demo

## Goal
Show a new user how SupplyCheck checks fictional procurement CSV data locally and reports a data-quality issue.

## Before recording
From the repository root, activate your virtual environment and install the project if needed:

```powershell
python -m pip install -e .
```

Use only the fictional CSV files in `demo-data/`. Close any files containing real supplier or company data.

## Recording script (about 60 seconds)

**0–8 sec — The problem**  
“Procurement data often arrives as CSV files. A wrong supplier ID, material ID, price, or currency can create problems before the data is imported into a business system.”

**8–18 sec — Introduce SupplyCheck**  
“SupplyCheck is a local-first Python tool that validates supplier, product, material, and procurement CSV data. It runs on your machine; it does not need an API key or database.”

**18–35 sec — Run the procurement check**  
Show the terminal and run the command below. The sample includes one valid info record and one deliberately invalid record that references an unknown supplier.

```powershell
python -m supplycheck validate procurement demo-data/info_records.csv --suppliers demo-data/suppliers.csv --materials demo-data/materials.csv
```

**35–48 sec — Show the report**  
Open the generated report in `reports/` (or the output location printed by the CLI). Point out the unknown supplier reference and the row number. Do not claim that this check replaces SAP validation.

**48–60 sec — Invite users**  
“Try SupplyCheck with fictional or properly anonymized CSV data. If you find a bug or have an improvement idea, open an issue on GitHub. Contributions and clear reproduction steps are welcome.”

## Recording checklist
- [ ] Run the exact command successfully before recording.
- [ ] Confirm the CLI output and report path on your machine.
- [ ] Show only fictional sample data.
- [ ] Keep the terminal font large enough to read.
- [ ] Do not show credentials, personal data, customer data, or confidential procurement files.
- [ ] Add captions and link the repository in the video description.

Repository: https://github.com/nitishchunduru/supplycheck
