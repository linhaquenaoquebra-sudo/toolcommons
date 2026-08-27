# Vision

Software discovery currently optimises for popularity, descriptions, and search
ranking. Those signals do not establish whether a tool can solve a particular
problem safely and reproducibly.

ToolCommons provides an open evidence layer shared by humans and software agents.
It connects three questions:

1. What does a resource claim it can do?
2. What concrete task tests that claim?
3. What happened when someone executed that task?

## Principles

- **Evidence before popularity.** Stars and reviews may provide context, but do
  not substitute for reproducible results.
- **Claims are not results.** Capability manifests and execution receipts remain
  separate objects.
- **Constraints are part of the task.** Privacy, network access, platform,
  memory, time, and licensing can change which tool is appropriate.
- **Humans and agents are peers at the interface.** Every important operation
  must have both a readable representation and a stable machine contract.
- **Provenance is preserved.** Inputs, outputs, versions, environments, and
  measurement methods are identified explicitly.
- **Federation over ownership.** The formats should remain useful without a
  central ToolCommons service.
- **Disagreement is data.** Conflicting receipts are retained and investigated,
  not averaged into a false certainty.

## Initial boundary

The first vertical slice covers extracting a table from a digital PDF into CSV.
It does not initially cover OCR, scanned documents, security certification,
distributed execution, or a public reputation score.

## What success looks like

A person or agent supplies a task and constraints. ToolCommons returns candidate
capabilities together with comparable receipts and enough provenance to reproduce
or contest the recommendation.
