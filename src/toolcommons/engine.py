from __future__ import annotations

import csv
import hashlib
import json
import platform
import time
import tracemalloc
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any

from .adapters import Adapter, Rows
from .transforms import Transform


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_task(root: Path, task_id: str) -> dict[str, Any]:
    for path in sorted((root / "tasks").glob("*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        if task.get("id") == task_id:
            return task
    raise ValueError(f"Task not found: {task_id}")


def read_csv(path: Path) -> Rows:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.reader(stream))


def encode_csv(rows: Rows) -> bytes:
    stream = StringIO(newline="")
    csv.writer(stream, lineterminator="\n").writerows(rows)
    return stream.getvalue().encode("utf-8")


def cell_accuracy(actual: Rows, expected: Rows) -> float:
    actual_cells = [cell.strip() for row in actual for cell in row]
    expected_cells = [cell.strip() for row in expected for cell in row]
    matches = sum(left == right for left, right in zip(actual_cells, expected_cells))
    return matches / max(len(actual_cells), len(expected_cells), 1)


def assertions_pass(assertions: list[dict[str, Any]], metrics: dict[str, float]) -> bool:
    for assertion in assertions:
        actual, expected = metrics.get(assertion["metric"]), assertion["value"]
        if actual is None or (assertion["operator"] == "eq" and actual != expected) or (assertion["operator"] == "gte" and actual < expected):
            return False
    return True


def store_artifact(root: Path, content: bytes) -> tuple[Path, str]:
    content_hash = sha256_bytes(content)
    relative = Path("receipts") / "artifacts" / f"sha256-{content_hash}.csv"
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(content)
    return relative, content_hash


def run(root: Path, task_id: str, adapter: Adapter, transforms: list[Transform] | None = None) -> Path:
    transforms = transforms or []
    task = load_task(root, task_id)
    input_path, expected_path = root / task["input"]["path"], root / task["expected"]["path"]
    if sha256_file(input_path) != task["input"]["sha256"]:
        raise ValueError("Input hash does not match the task manifest")
    if sha256_file(expected_path) != task["expected"]["sha256"]:
        raise ValueError("Expected-output hash does not match the task manifest")

    rows: Rows = []
    error: str | None = None
    tracemalloc.start()
    started = time.perf_counter()
    try:
        rows = adapter.extract(input_path, task)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    duration = time.perf_counter() - started
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    raw_output = encode_csv(rows)
    raw_relative, raw_hash = store_artifact(root, raw_output)
    for transform in transforms:
        rows = transform.apply(rows)
    output = encode_csv(rows)
    artifact_relative, output_hash = store_artifact(root, output)

    expected = read_csv(expected_path)
    metrics: dict[str, float] = {
        "cellAccuracy": round(cell_accuracy(rows, expected), 6),
        "rowCount": len(rows),
        "columnCount": max((len(row) for row in rows), default=0),
        "peakMemoryMiB": round(peak_bytes / 1048576, 3),
    }
    within_limits = duration <= task["constraints"]["maxDurationSeconds"] and metrics["peakMemoryMiB"] <= task["constraints"]["maxMemoryMiB"]
    passed = error is None and within_limits and assertions_pass(task["assertions"], metrics)
    receipt: dict[str, Any] = {
        "schemaVersion": "0.1", "id": "pending", "capabilityId": adapter.capability_id,
        "taskId": task["id"], "status": "passed" if passed else ("error" if error else "failed"),
        "pipelineId": "+".join(transform.identifier for transform in transforms) or "raw",
        "transformations": [transform.identifier for transform in transforms],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "environment": {"os": platform.platform(), "architecture": platform.machine(), "python": platform.python_version()},
        "execution": {"toolVersion": adapter.version(), "durationSeconds": round(duration, 6), "networkUsed": False},
        "metrics": metrics,
        "artifacts": [{"role": "input", "path": task["input"]["path"], "sha256": sha256_file(input_path)}],
        "notes": error or f"Executed by the {adapter.name} adapter using default detection with text-alignment fallback."
    }
    if transforms:
        receipt["artifacts"].append({"role": "intermediate", "path": raw_relative.as_posix(), "sha256": raw_hash})
    receipt["artifacts"].append({"role": "output", "path": artifact_relative.as_posix(), "sha256": output_hash})
    identity = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt_hash = sha256_bytes(identity)
    receipt["id"] = f"receipt.{receipt_hash[:24]}"
    receipt_path = root / "receipts" / f"sha256-{receipt_hash}.json"
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    return receipt_path


def latest_receipts(root: Path, task_id: str) -> list[dict[str, Any]]:
    licenses = {}
    for path in (root / "capabilities").glob("*.json"):
        capability = json.loads(path.read_text(encoding="utf-8"))
        licenses[capability["id"]] = capability["license"]
    latest: dict[str, dict[str, Any]] = {}
    for path in (root / "receipts").glob("*.json"):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if receipt.get("taskId") != task_id:
            continue
        capability = receipt["capabilityId"]
        receipt["license"] = licenses.get(capability, "unknown")
        key = f"{capability}|{receipt.get('pipelineId', 'raw')}"
        if key not in latest or receipt["recordedAt"] > latest[key]["recordedAt"]:
            latest[key] = receipt
    return sorted(latest.values(), key=lambda item: item["capabilityId"])


def comparison_markdown(receipts: list[dict[str, Any]]) -> str:
    lines = [
        "# ToolCommons comparison",
        "",
        f"Task: `{receipts[0]['taskId']}`" if receipts else "No receipts.",
        "",
        "| Capability | Pipeline | Status | Accuracy | Time (s) | Peak memory (MiB) | Licence | Version |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for receipt in receipts:
        metrics = receipt["metrics"]
        lines.append(f"| {receipt['capabilityId']} | {receipt.get('pipelineId', 'raw')} | {receipt['status']} | {metrics.get('cellAccuracy', 0):.1%} | {receipt['execution']['durationSeconds']:.4f} | {metrics.get('peakMemoryMiB', 0):.3f} | {receipt['license']} | {receipt['execution']['toolVersion']} |")
    return "\n".join(lines)
