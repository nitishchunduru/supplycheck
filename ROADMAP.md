# SupplyCheck Roadmap

SupplyCheck is evolving into a practical, local-first data quality toolkit for supplier, material, product, and procurement CSV files.

This roadmap describes planned directions. Features are not considered complete until implemented, tested, and documented.

## Current Release

### v1.3.0 — Procurement Cross-File Validation

- Supplier and product CSV validation
- Material master validation
- Procurement info-record cross-file validation
- JSON and Markdown reports
- CLI strict-mode exit codes
- Automated tests and Python 3.10–3.14 CI

## Next Release

### v1.4.0 — Practical SAP MM Data Quality

**1. Stronger validation**

- Review validation rules against realistic SAP MM data scenarios.
- Improve edge-case handling and error messages.
- Evaluate additional purchasing info-record checks.

**2. Better examples**

- Add realistic, fictional supplier, material, and procurement datasets.
- Include examples of valid and invalid records.
- Document complete end-to-end validation workflows.

**3. Better reports**

- Improve report readability.
- Make issue details easier to understand and resolve.
- Add tests for report content and edge cases.

**4. Quality and compatibility**

- Expand automated tests.
- Maintain Python 3.10–3.14 compatibility.
- Keep runtime dependencies minimal.
- Verify all CLI commands and examples before release.

## Future Directions

### v1.5.0 — Extended Data Quality

- Evaluate additional configurable validation rules.
- Explore reusable validation profiles.
- Improve handling of larger CSV datasets.

### Future — Integration Readiness

- Evaluate Excel import and export.
- Explore structured validation configuration.
- Assess integration options for enterprise workflows.

## Out of Scope for Current Releases

- Direct SAP system connectivity.
- Automatic SAP data posting or modification.
- Replacement of SAP standard validation and governance.
- Database-backed enterprise workflows.

## Development Principles

- Local-first and privacy-conscious.
- No unnecessary runtime dependencies.
- Backward compatibility where practical.
- Every new validation rule needs automated tests.
- Sample data must be fictional.
- Documentation must accurately describe implemented behavior.

## Release Policy

A roadmap item is a proposal, not a feature commitment.

Each release must pass the complete test suite, CI workflow, CLI smoke tests, and documentation review before publication.

