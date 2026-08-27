from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .adapters import get_adapter
from .engine import comparison_markdown, latest_receipts, run
from .transforms import get_transform

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # keep the repository inspectable before dependencies are installed
    Draft202012Validator = None
    FormatChecker = None


KINDS = ("capability", "task", "receipt")
DIRECTORIES = {"capability": "capabilities", "task": "tasks", "receipt": "receipts"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    for kind in KINDS:
        schema = load_json(root / "schemas" / f"{kind}.schema.json")
        validator = (
            Draft202012Validator(schema, format_checker=FormatChecker())
            if Draft202012Validator is not None
            else None
        )
        directory = root / DIRECTORIES[kind]
        for path in sorted(directory.glob("*.json")):
            record = load_json(path)
            if validator is not None:
                for error in validator.iter_errors(record):
                    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                    errors.append(f"{path.relative_to(root)}:{location}: {error.message}")
            else:
                missing = set(schema.get("required", [])) - set(record)
                for field in sorted(missing):
                    errors.append(f"{path.relative_to(root)}:{field}: required field is missing")
                if record.get("schemaVersion") != "0.1":
                    errors.append(f"{path.relative_to(root)}:schemaVersion: expected 0.1")
            if kind == "task":
                errors.extend(validate_task_hashes(root, path, record))
    return errors


def validate_task_hashes(root: Path, record_path: Path, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("input", "expected"):
        artifact = record.get(field, {})
        relative = artifact.get("path")
        expected_hash = artifact.get("sha256")
        if not relative:
            continue
        path = root / relative
        if not path.is_file():
            errors.append(f"{record_path.relative_to(root)}:{field}.path: missing {relative}")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected_hash and actual_hash != expected_hash:
            errors.append(f"{record_path.relative_to(root)}:{field}.sha256: expected {actual_hash}")
    return errors


def print_summary(root: Path) -> None:
    counts = {kind: len(list((root / DIRECTORIES[kind]).glob("*.json"))) for kind in KINDS}
    print("ToolCommons repository")
    print(f"Capabilities: {counts['capability']}")
    print(f"Tasks:       {counts['task']}")
    print(f"Receipts:    {counts['receipt']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="toolcommons")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "summary"):
        item = subparsers.add_parser(command)
        item.add_argument("root", nargs="?", default=".", type=Path)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("task_id")
    run_parser.add_argument("--with", dest="adapters", action="append", required=True)
    run_parser.add_argument("--transform", dest="transforms", action="append", default=[])
    run_parser.add_argument("--root", default=".", type=Path)
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("task_id")
    compare_parser.add_argument("--root", default=".", type=Path)
    compare_parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.command == "run":
        exit_code = 0
        transforms = [get_transform(name) for name in args.transforms]
        for name in args.adapters:
            receipt_path = run(root, args.task_id, get_adapter(name), transforms)
            receipt = load_json(receipt_path)
            print(f"{name}: {receipt['status']} -> {receipt_path.relative_to(root)}")
            exit_code = max(exit_code, receipt["status"] != "passed")
        return int(exit_code)
    if args.command == "compare":
        receipts = latest_receipts(root, args.task_id)
        if not receipts:
            print("No receipts found for this task.")
            return 1
        report = comparison_markdown(receipts)
        print(report)
        if args.output:
            output = args.output if args.output.is_absolute() else root / args.output
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(report + "\n", encoding="utf-8")
            print(f"\nSaved to {output.relative_to(root)}")
        return 0
    if args.command == "summary":
        print_summary(root)
        return 0
    errors = validate_repository(root)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("All ToolCommons records are valid.")
    return 0
