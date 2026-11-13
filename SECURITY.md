# Security Policy

## Supported versions

Security fixes are prioritized for the latest published release and the current default branch. Older releases may not receive fixes; users should upgrade to the latest release where possible.

## Reporting a vulnerability

Please do not disclose exploitable vulnerabilities, credentials, private data or detailed attack instructions in public issues.

Use GitHub's **Private vulnerability reporting** feature for this repository if it is enabled. If that option is unavailable, contact the repository maintainer privately through the contact details on the maintainer's GitHub profile. Include a concise description, affected version or commit, reproduction steps and potential impact. Do not attach real procurement files or personal data.

Please allow reasonable time for investigation and a fix before public disclosure. The project will acknowledge reports and coordinate a response where contact is possible.

## Data handling and project scope

SupplyCheck is designed as a local CSV utility. Its current validation commands process files on the user's machine and do not intentionally upload CSV contents or send them to external services.

- Do not use real confidential supplier, customer, employee, financial or procurement data in public examples, tests or bug reports.
- Use fictional or properly anonymized records.
- Report unexpected network activity, unsafe file handling, path traversal, data disclosure or report-writing issues.
- Do not include passwords, API keys, access tokens or other secrets in issues or pull requests.

This policy describes the current project scope; it is not a guarantee that every future optional integration will have identical data-handling behavior. Any future networked feature must document its data flows before release.
