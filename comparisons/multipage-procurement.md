# ToolCommons comparison

Task: `community.pdf.multipage-repeated-header.v1`

| Capability | Pipeline | Status | Accuracy | Time (s) | Peak memory (MiB) | Licence | Version |
|---|---|---|---:|---:|---:|---|---|
| github.camelot-dev.camelot | raw | failed | 0.0% | 8.8268 | 119.641 | MIT | 2.0.0 |
| github.camelot-dev.camelot | drop-repeated-headers.v1 | failed | 0.0% | 2.5456 | 119.640 | MIT | 2.0.0 |
| github.pdfplumber.pdfplumber | raw | failed | 33.3% | 1.7477 | 8.893 | MIT | 0.11.10 |
| github.pdfplumber.pdfplumber | drop-repeated-headers.v1 | passed | 100.0% | 0.5505 | 8.893 | MIT | 0.11.10 |
| github.pymupdf.pymupdf | raw | failed | 33.3% | 3.9493 | 14.223 | AGPL-3.0-or-later OR commercial | 1.26.7 |
| github.pymupdf.pymupdf | drop-repeated-headers.v1 | passed | 100.0% | 1.7243 | 14.221 | AGPL-3.0-or-later OR commercial | 1.26.7 |
