"""JSON and Markdown report writers."""
from __future__ import annotations

import json
from pathlib import Path
from .validator import ValidationResult


def write_json(result: ValidationResult, destination: str | Path) -> Path:
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    return target


def write_markdown(result: ValidationResult, destination: str | Path) -> Path:
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    data = result.to_dict()
    lines = [
        f"# SupplyCheck {result.record_type.title()} Validation Report",
        "",
        f"- **Source:** `{result.source}`",
        f"- **Records checked:** {result.total_records}",
        f"- **Valid records:** {result.valid_records}",
        f"- **Invalid records:** {result.invalid_records}",
        f"- **Issues:** {len(result.issues)}",
        "",
        "## Missing columns",
        "",
    ]
    lines.extend([f"- `{column}`" for column in result.missing_columns] or ["- None"])
    lines += ["", "## Issues", ""]
    if result.issues:
        lines += ["| CSV row | Field | Code | Details |", "|---:|---|---|---|"]
        for issue in result.issues:
            message = issue.message.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {issue.row} | `{issue.field}` | `{issue.code}` | {message} |")
    else:
        lines.append("No issues found. All records passed the configured checks.")
    lines += ["", "---", "Generated locally by SupplyCheck.", ""]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target
