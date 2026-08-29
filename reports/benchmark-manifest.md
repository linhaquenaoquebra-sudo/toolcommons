# ToolCommons benchmark manifest

A deterministic view of declared capabilities, reproducible tasks, and the latest receipt for each task–capability–pipeline combination.

- Capabilities: **3**
- Tasks: **3**
- Latest results: **15**

## Capabilities

### Camelot

Extracts tables from text-based PDF documents using ruled-line and whitespace parsers.

- ID: `github.camelot-dev.camelot`
- Source: [https://github.com/camelot-dev/camelot](https://github.com/camelot-dev/camelot) at `1.x-2.x`
- Licence: `MIT`
- Interfaces: cli, python
- Platforms: linux, macos, windows
- Network required: no

### pdfplumber

Extracts text, tables, and geometry from digital PDF documents.

- ID: `github.pdfplumber.pdfplumber`
- Source: [https://github.com/jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) at `0.11.x`
- Licence: `MIT`
- Interfaces: cli, python
- Platforms: linux, macos, windows
- Network required: no

### PyMuPDF

High-performance Python library for extracting and manipulating PDF content.

- ID: `github.pymupdf.pymupdf`
- Source: [https://github.com/pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) at `1.26.x`
- Licence: `AGPL-3.0-or-later OR commercial`
- Interfaces: python
- Platforms: linux, macos, windows
- Network required: no

## Tasks and evidence

### Extract a borderless table with multiline cells from a digital PDF

Convert the visually aligned table into CSV without absorbing surrounding prose and while preserving wrapped cell values.

Task ID: `community.pdf.borderless-multiline-table.v1` · Fixture licence: `CC0-1.0`

| Tool | Pipeline | Status | Cell accuracy | Time (s) | Peak memory (MiB) | Version | Evidence |
|---|---|---|---:|---:|---:|---|---|
| Camelot | `collapse-sparse-continuations.v1` | passed | 100.0% | 5.5464 | 50.187 | `2.0.0` | [receipt](../receipts/sha256-e432d7cb7a0a4f517b0b793f08bec4b900b665fc803454cfe6f92fc73fb6c457.json) |
| Camelot | `raw` | failed | 22.2% | 5.1014 | 50.186 | `2.0.0` | [receipt](../receipts/sha256-61e7b15e4e2792d452d117f808909dfc5ec8d125af474c59374dce9ea44e800f.json) |
| pdfplumber | `collapse-sparse-continuations.v1` | passed | 100.0% | 2.2815 | 6.514 | `0.11.10` | [receipt](../receipts/sha256-bc2a985f15935249a8c377001fcf7fda230442dbf3f01faacc0060a4d2b93b5d.json) |
| pdfplumber | `raw` | failed | 6.7% | 0.6998 | 6.511 | `0.11.10` | [receipt](../receipts/sha256-827a739faa7dec78f81d73836414ff1c312c760f1c61b5e730996a0a2f66eed0.json) |
| PyMuPDF | `collapse-sparse-continuations.v1` | passed | 100.0% | 4.1916 | 14.01 | `1.26.7` | [receipt](../receipts/sha256-2c7e9ee1d6e898d0a730b2686a782bd8e178e1ea752b7bc877209e0602e42203.json) |
| PyMuPDF | `raw` | failed | 6.7% | 2.9458 | 14.018 | `1.26.7` | [receipt](../receipts/sha256-aae7bc39b870d61ba42d5be93a58dcf2df36e3c5ae5d6b47a5184f8ea42419d7.json) |

Limits: timings are individual recorded executions, results apply only to the declared fixture and environment, and receipts are not security attestations.

### Extract a ruled quarterly sales table from a digital PDF

Convert the table in the supplied digital PDF into CSV while preserving every header and value.

Task ID: `community.pdf.digital-table.quarterly-sales.v1` · Fixture licence: `CC0-1.0`

| Tool | Pipeline | Status | Cell accuracy | Time (s) | Peak memory (MiB) | Version | Evidence |
|---|---|---|---:|---:|---:|---|---|
| Camelot | `raw` | passed | 100.0% | 19.8404 | 117.227 | `2.0.0` | [receipt](../receipts/sha256-3f3251e16504f8614718eed5acf40b91ff6b378ef0218d75ee3c6501ec9d9ab6.json) |
| pdfplumber | `raw` | passed | 100.0% | 1.6755 | 6.047 | `0.11.10` | [receipt](../receipts/sha256-ab24f5f0a40deb97a2cc06b866b7baf0a3f50a4e90ea58da703ab68617f8438a.json) |
| PyMuPDF | `raw` | passed | 100.0% | 3.3060 | 14.092 | `1.26.7` | [receipt](../receipts/sha256-e881a741754a50ee2e7575a589aec88e3e1bbcb0b545130cc9bf8f111922a938.json) |

Limits: timings are individual recorded executions, results apply only to the declared fixture and environment, and receipts are not security attestations.

### Extract a multipage procurement table with repeated headers

Combine a ruled table across three pages into one CSV, preserve row order, exclude surrounding report text, and retain the header exactly once.

Task ID: `community.pdf.multipage-repeated-header.v1` · Fixture licence: `CC0-1.0`

| Tool | Pipeline | Status | Cell accuracy | Time (s) | Peak memory (MiB) | Version | Evidence |
|---|---|---|---:|---:|---:|---|---|
| Camelot | `drop-repeated-headers.v1` | failed | 0.0% | 2.5456 | 119.64 | `2.0.0` | [receipt](../receipts/sha256-03ccbf5f227037db587e0d3c1e12b52809b0a77fdbc95d6c4e7b78733c7b0256.json) |
| Camelot | `raw` | failed | 0.0% | 8.8268 | 119.641 | `2.0.0` | [receipt](../receipts/sha256-7c32da509504c19773df8cab0fef1e8424d626a7cc7bac0a6dec7a1888ff7406.json) |
| pdfplumber | `drop-repeated-headers.v1` | passed | 100.0% | 0.5505 | 8.893 | `0.11.10` | [receipt](../receipts/sha256-da99d2b517755f3d6babec175e9ae0f287853bce197ad08dc65f1d8d27e14631.json) |
| pdfplumber | `raw` | failed | 33.3% | 1.7477 | 8.893 | `0.11.10` | [receipt](../receipts/sha256-14c535a1fa7a8bc6b78e335fbb819b9163da5c3b5feb3aa5e7a6a324a41b382c.json) |
| PyMuPDF | `drop-repeated-headers.v1` | passed | 100.0% | 1.7243 | 14.221 | `1.26.7` | [receipt](../receipts/sha256-c443949e7aa9a340b66d20fbe5eb5a0570d8eba6f080a94e95b541eac551759f.json) |
| PyMuPDF | `raw` | failed | 33.3% | 3.9493 | 14.223 | `1.26.7` | [receipt](../receipts/sha256-476beb48651977314caab005b4d0be5668c6035c258b6cf64b094c108d47a0cb.json) |

Limits: timings are individual recorded executions, results apply only to the declared fixture and environment, and receipts are not security attestations.
