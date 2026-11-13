# Contributing to SupplyCheck

Thanks for considering a contribution! SupplyCheck is an early-stage, local-first Python project. Bug reports, documentation improvements, test cases and focused code changes are welcome.

## Before you start

- Search existing issues and pull requests to avoid duplicate work.
- For a substantial change, open an issue first to discuss the problem and proposed approach.
- For a small documentation correction or isolated bug fix, a pull request is welcome.
- Do not share confidential supplier, customer, employee, financial or company data. Use fictional or properly anonymized examples.

## Development setup

Requires Python 3.10 or newer.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests -v
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

The runtime currently uses the Python standard library. The editable install uses the project's build configuration.

## What makes a good contribution?

- A clear user problem and a focused solution.
- A regression test for a bug fix.
- Unit tests for new or changed validation rules.
- Helpful error messages and documented limitations.
- Fictional sample data.
- No unnecessary runtime dependencies, network calls, telemetry or paid-service requirements.

Good first contributions include improving examples, clarifying documentation, adding edge-case tests and reproducing reported CSV parsing issues.

## Pull-request checklist

Please include:

1. What problem does this solve?
2. What changed?
3. How was it tested? Include the exact command and result.
4. Are README, examples or changelog updates needed?
5. Does the change preserve local-first behavior and avoid exposing sensitive data?

Keep pull requests focused and explain any compatibility impact. CI must pass before a change is considered ready to merge.

## Review and conduct

Be respectful, patient and constructive. Ask questions when requirements are unclear, explain review feedback, and focus discussion on the work rather than the person. Harassment, discrimination and abusive behavior are not acceptable.

## Security

For suspected vulnerabilities, follow [SECURITY.md](SECURITY.md). Do not publish exploit details or sensitive data in public issues.

## License

By submitting a contribution, you agree that it may be distributed under the project's MIT license.
