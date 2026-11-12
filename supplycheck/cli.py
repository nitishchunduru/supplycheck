"""Command-line interface for SupplyCheck."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from . import __version__
from .reports import write_json, write_markdown
from .validator import validate_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="supplycheck",
        description="Validate supplier and product master-data CSV files locally.",
        epilog="Example: python -m supplycheck validate suppliers examples/suppliers.csv",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="Validate a supplier or product CSV.")
    validate.add_argument("record_type", choices=("suppliers", "products"))
    validate.add_argument("input", type=Path, help="Path to the input CSV file.")
    validate.add_argument("--report-dir", type=Path, default=Path("reports"),
                          help="Directory for JSON and Markdown reports (default: reports).")
    validate.add_argument("--strict", action="store_true",
                          help="Return exit code 1 when validation finds any issue.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = validate_csv(args.input, args.record_type)
        args.report_dir.mkdir(parents=True, exist_ok=True)
        stem = f"{args.record_type}_validation"
        json_path = write_json(result, args.report_dir / f"{stem}.json")
        md_path = write_markdown(result, args.report_dir / f"{stem}.md")

        print(f"\nSupplyCheck {__version__} — {result.record_type.title()} validation")
        print("=" * 55)
        print(f"Records checked : {result.total_records}")
        print(f"Valid records   : {result.valid_records}")
        print(f"Invalid records : {result.invalid_records}")
        print(f"Issues found    : {len(result.issues)}")
        print(f"\nJSON report     : {json_path}")
        print(f"Markdown report : {md_path}")
        if result.issues:
            print("\nIssues:")
            for issue in result.issues:
                print(f"  Row {issue.row} | {issue.field} | {issue.code}: {issue.message}")
        else:
            print("\nAll records passed validation.")
        return 1 if args.strict and not result.is_valid else 0
    except (OSError, ValueError) as exc:
        print(f"SupplyCheck error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
