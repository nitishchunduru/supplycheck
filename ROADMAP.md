# SupplyCheck Roadmap

SupplyCheck is a local-first Python toolkit for checking supplier, product, material and procurement CSV data. This roadmap prioritizes trustworthy community adoption before expanding the feature set.

A roadmap item is planned work, not a claim that the feature already exists. Only released and documented behavior is considered complete.

## Current status

### Released: v1.3.0 — Procurement Cross-File Validation

- Supplier, product and material CSV validation.
- Procurement info-record checks against supplier and material identifiers.
- JSON and Markdown reports.
- CLI strict-mode exit codes and input/CSV edge-case handling.
- Automated tests and CI across Python 3.10–3.14.
- Local-first operation using the Python standard library at runtime.

The project is an early-stage beta. It does not connect to SAP, validate live SAP configuration, or post data into business systems.

## Community growth plan

### 1.4 — Community Readiness

The repository already includes the initial community foundation:

- Contribution guide and pull-request expectations.
- Bug-report and feature-request issue templates.
- Pull-request template.
- Security policy.
- Fictional example datasets.
- Public roadmap, changelog, MIT license and automated CI.

Ongoing maintenance:
- Keep examples, CLI documentation and supported Python versions synchronized.
- Review incoming issues and pull requests promptly and respectfully.
- Add focused tests for every behavior change.
- Keep release notes and installation instructions accurate.

### Adoption — Feedback before feature expansion

This phase is not complete until real external use is evidenced.

- Invite SAP MM learners, procurement practitioners and Python developers to try the tool with fictional or properly anonymized CSVs.
- Ask users which checks are useful, confusing or missing.
- Record reproducible feedback as GitHub issues.
- Fix genuine defects and clarify limitations before adding broad new features.
- Welcome independent contributors; review and credit substantive contributions.
- Do not manufacture stars, downloads, testimonials, issues, contributors or usage claims.

### 1.5 — Practical improvements informed by users

Potential work, subject to actual feedback:

- More realistic fictional datasets and end-to-end examples.
- Clearer validation diagnostics and report usability.
- Additional SAP MM-inspired CSV checks with explicit scope boundaries.
- Packaging and installation improvements.
- Compatibility and performance tests for larger CSV files.

### Future — Integration readiness

Evaluate only when there is a demonstrated user need:

- Configurable validation profiles.
- Excel import/export.
- Optional integrations with enterprise workflows.

## Out of scope

- Direct SAP system connectivity or automatic SAP data posting.
- Claims of SAP certification or replacement of SAP standard controls.
- Uploading CSV files, telemetry or remote processing by default.
- Database-backed enterprise workflows without a clear use case.

## Development principles

- Local-first and privacy-conscious.
- No unnecessary runtime dependencies.
- Fictional sample data only.
- Every new validation rule needs automated tests.
- Preserve backward compatibility where practical.
- Clearly distinguish implemented behavior from proposals.
- Never represent adoption, downloads, contributors or impact without verifiable evidence.

## Release policy

A release must pass the full test suite, CI workflow, CLI smoke tests and documentation review. Package publication is a separate release action and must not be claimed until a public registry listing and install test are verified.
