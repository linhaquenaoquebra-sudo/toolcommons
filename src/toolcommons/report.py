from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _records(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    return [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in sorted(directory.glob("*.json"))
    ]


def build_manifest(root: Path) -> dict[str, Any]:
    """Build a deterministic, agent-readable view of repository evidence."""
    capabilities = []
    for _, record in _records(root / "capabilities"):
        capabilities.append({
            "id": record["id"],
            "name": record["name"],
            "description": record["description"],
            "repository": record["source"]["repository"],
            "revision": record["source"]["revision"],
            "license": record["license"],
            "interfaces": sorted(record["interfaces"]),
            "platforms": sorted(record["runtime"]["platforms"]),
            "networkRequired": record["runtime"]["networkRequired"],
            "claims": sorted(record["claims"], key=lambda claim: claim["id"]),
        })

    tasks = []
    for _, record in _records(root / "tasks"):
        tasks.append({
            "id": record["id"],
            "title": record["title"],
            "objective": record["objective"],
            "input": record["input"],
            "expected": record["expected"],
            "constraints": record["constraints"],
            "assertions": record["assertions"],
            "provenance": record["provenance"],
        })

    latest: dict[tuple[str, str, str], tuple[Path, dict[str, Any]]] = {}
    for path, receipt in _records(root / "receipts"):
        key = (
            receipt["taskId"],
            receipt["capabilityId"],
            receipt.get("pipelineId", "raw"),
        )
        if key not in latest or receipt["recordedAt"] > latest[key][1]["recordedAt"]:
            latest[key] = (path, receipt)

    results = []
    for key in sorted(latest):
        path, receipt = latest[key]
        results.append({
            "taskId": receipt["taskId"],
            "capabilityId": receipt["capabilityId"],
            "pipelineId": receipt.get("pipelineId", "raw"),
            "status": receipt["status"],
            "recordedAt": receipt["recordedAt"],
            "toolVersion": receipt["execution"]["toolVersion"],
            "environment": receipt["environment"],
            "durationSeconds": receipt["execution"]["durationSeconds"],
            "networkUsed": receipt["execution"]["networkUsed"],
            "metrics": receipt["metrics"],
            "transformations": receipt.get("transformations", []),
            "receiptPath": path.relative_to(root).as_posix(),
            "notes": receipt.get("notes", ""),
        })

    return {
        "schemaVersion": "0.1",
        "kind": "toolcommons.benchmark-manifest",
        "capabilities": sorted(capabilities, key=lambda item: item["id"]),
        "tasks": sorted(tasks, key=lambda item: item["id"]),
        "results": results,
    }


def manifest_json(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _metric(result: dict[str, Any], name: str, suffix: str = "") -> str:
    value = result["metrics"].get(name)
    return "—" if value is None else f"{value}{suffix}"


def manifest_markdown(manifest: dict[str, Any]) -> str:
    capability_names = {item["id"]: item["name"] for item in manifest["capabilities"]}
    lines = [
        "# ToolCommons benchmark manifest",
        "",
        "A deterministic view of declared capabilities, reproducible tasks, and the latest receipt for each task–capability–pipeline combination.",
        "",
        f"- Capabilities: **{len(manifest['capabilities'])}**",
        f"- Tasks: **{len(manifest['tasks'])}**",
        f"- Latest results: **{len(manifest['results'])}**",
        "",
        "## Capabilities",
        "",
    ]
    for capability in manifest["capabilities"]:
        interfaces = ", ".join(capability["interfaces"])
        platforms = ", ".join(capability["platforms"])
        lines.extend([
            f"### {capability['name']}",
            "",
            capability["description"],
            "",
            f"- ID: `{capability['id']}`",
            f"- Source: [{capability['repository']}]({capability['repository']}) at `{capability['revision']}`",
            f"- Licence: `{capability['license']}`",
            f"- Interfaces: {interfaces}",
            f"- Platforms: {platforms}",
            f"- Network required: {'yes' if capability['networkRequired'] else 'no'}",
            "",
        ])

    lines.extend(["## Tasks and evidence", ""])
    results_by_task: dict[str, list[dict[str, Any]]] = {}
    for result in manifest["results"]:
        results_by_task.setdefault(result["taskId"], []).append(result)
    for task in manifest["tasks"]:
        lines.extend([
            f"### {task['title']}",
            "",
            task["objective"],
            "",
            f"Task ID: `{task['id']}` · Fixture licence: `{task['provenance']['license']}`",
            "",
            "| Tool | Pipeline | Status | Cell accuracy | Time (s) | Peak memory (MiB) | Version | Evidence |",
            "|---|---|---|---:|---:|---:|---|---|",
        ])
        for result in results_by_task.get(task["id"], []):
            accuracy = result["metrics"].get("cellAccuracy")
            accuracy_text = "—" if accuracy is None else f"{accuracy:.1%}"
            lines.append(
                f"| {capability_names.get(result['capabilityId'], result['capabilityId'])} "
                f"| `{result['pipelineId']}` | {result['status']} | {accuracy_text} "
                f"| {result['durationSeconds']:.4f} | {_metric(result, 'peakMemoryMiB')} "
                f"| `{result['toolVersion']}` | [receipt](../{result['receiptPath']}) |"
            )
        if not results_by_task.get(task["id"]):
            lines.append("| — | — | no evidence | — | — | — | — | — |")
        lines.extend([
            "",
            "Limits: timings are individual recorded executions, results apply only to the declared fixture and environment, and receipts are not security attestations.",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
