# ToolCommons

ToolCommons is an open evidence layer for choosing software capabilities.
It helps humans and agents answer a practical question:

> Which tool can complete this task, under these constraints, and what evidence supports that choice?

The project is deliberately not another marketplace. Its core objects are
machine-readable capability claims, reproducible tasks, and execution receipts.

## First vertical slice

The initial experiment compares open-source tools that extract tables from PDF
documents into structured data. The first fixture is a synthetic quarterly sales
table with a known CSV answer.

## Repository layout

```text
schemas/       JSON Schemas for capabilities, tasks, and receipts
capabilities/  Claims made by tool maintainers or community contributors
tasks/         Reproducible problems and expected results
receipts/      Evidence produced by executions
fixtures/      Public test inputs and expected outputs
src/           The ToolCommons command-line interface
tests/         Contract tests for the initial data model
docs/          Vision, principles, and specification notes
```

## Quick start

Requires Python 3.11 or later.

```powershell
python -m toolcommons validate .
python -m toolcommons summary .
```

Without installed dependencies, validation still checks record identity, required
top-level fields, fixture presence, and content hashes. Installing the project
enables complete JSON Schema validation.

For development:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[benchmark]"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Run the first benchmark

From the repository root:

```powershell
.\.venv\Scripts\toolcommons.exe run community.pdf.digital-table.quarterly-sales.v1 --with pdfplumber --with pymupdf --with camelot
.\.venv\Scripts\toolcommons.exe compare community.pdf.digital-table.quarterly-sales.v1 --output comparisons\quarterly-sales.md
.\.venv\Scripts\python.exe -m toolcommons validate .
.\.venv\Scripts\python.exe -m toolcommons summary .
```

The benchmark exits with code `0` when all assertions pass. Outputs are stored by
their SHA-256 content hash under `receipts/artifacts/`; receipts are immutable and
stored as `receipts/sha256-<hash>.json`.

## Run the borderless multiline benchmark

```powershell
.\.venv\Scripts\toolcommons.exe run community.pdf.borderless-multiline-table.v1 --with pdfplumber --with pymupdf --with camelot
.\.venv\Scripts\toolcommons.exe run community.pdf.borderless-multiline-table.v1 --with pdfplumber --with pymupdf --with camelot --transform collapse-multiline
.\.venv\Scripts\toolcommons.exe compare community.pdf.borderless-multiline-table.v1 --output comparisons\borderless-multiline.md
```

This task intentionally separates table localisation from extraction by supplying
a page index and bounding box. It tests whether wrapped visual lines are rebuilt
as logical table cells. A non-zero exit code means the evidence was recorded but
one or more task assertions failed.

The current timing is a single cold process measurement and peak memory uses
Python allocation tracing. Results are useful evidence for this environment, not
a statistically rigorous performance ranking.

## Status

This is a pre-alpha experiment. The schemas will evolve based on real execution
evidence. Do not use the current receipts as security attestations.

## Contributing

Contributions of capabilities, tasks, adapters, transformations, and reproducible
failure receipts are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the
evidence policy, fixture rules, development setup, and pull request checklist.

## Licence

Apache-2.0. Test fixtures and community submissions must declare their own
licensing and provenance.
