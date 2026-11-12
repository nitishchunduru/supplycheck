# Contributing to SupplyCheck

Thanks for considering a contribution!

## Development setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m unittest discover -s tests -v
```

The core project uses only the Python standard library.

## Contribution guidelines

1. Open an issue to describe a bug or proposed change before large changes.
2. Keep changes focused and explain the user problem they solve.
3. Add or update unit tests for every validation rule or behavior change.
4. Use fictional sample data only.
5. Update the README when commands, CSV schemas or limitations change.
6. Do not add network calls, telemetry or paid-service dependencies without discussion.

## Pull requests

Include:
- A concise problem statement.
- Summary of the implementation.
- Test command and result.
- Example input/output when behavior changes.

Be respectful and constructive in review discussions.
