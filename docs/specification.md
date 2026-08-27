# Data model v0.1

ToolCommons uses three independently addressable records.

## Capability

A capability describes a resource and one or more claims. It records origin,
licence, interfaces, runtime requirements, and declared permissions. A capability
does not assert that a claim has been verified.

## Task

A task describes an input, an expected output, constraints, and assertions. A task
must be usable without knowing which capability will execute it.
It may include a page index and bounding box when the benchmark evaluates extraction
from a known region. Automatic table localisation is evaluated as a separate claim.
The optional `tableStyle` hint selects an algorithm family such as ruled-line or
borderless extraction without encoding settings for a particular tool.

## Receipt

A receipt is an immutable report of one capability attempting one task. It records
the exact capability revision, environment, status, measurements, artefacts, and
content hashes. A receipt may report failure; failures are useful evidence.

## Identity

Records use stable, lower-case identifiers with a reverse-domain-inspired prefix.
Version 0.1 stores records in Git, while content hashes identify executed inputs
and outputs independently of Git history.

## Trust model

Version 0.1 stores outputs and receipts under content-derived SHA-256 names. A new
execution creates a new receipt and never replaces previous evidence. It verifies
internal structure and fixture hashes. Cryptographic signing,
runner identity, reproducibility quorum, and revocation are intentionally deferred
until the execution model has been exercised with real tools.

## Adapter policy

An adapter may use a documented fallback strategy when a tool's default detector
returns no result. Each receipt records the adapter policy in its notes. Earlier
failed or error receipts remain immutable so the effect of policy changes can be
audited rather than silently replacing history.

## Transformations

A transformation has its own stable identifier and version. When used, a receipt
records the raw extractor output as an intermediate artefact and the transformed
result as its output. Comparisons group receipts by both capability and pipeline,
so post-processing can improve a result without concealing raw behaviour.
