# Contributing to ToolCommons

ToolCommons welcomes evidence, including evidence that a tool fails. A useful
contribution is reproducible, explicit about its constraints, and careful about
provenance.

## Ways to contribute

You can contribute without adding application code:

- describe a software capability;
- add a public benchmark task and expected result;
- reproduce an existing task in another environment;
- integrate a new extractor through an adapter;
- add a declared transformation;
- investigate or explain conflicting receipts;
- improve documentation, accessibility, or translations.

## Development setup

ToolCommons requires Python 3.11 or later. From a clone of the repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[benchmark]"
.\.venv\Scripts\python.exe -m toolcommons validate .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On Linux or macOS, replace `.\.venv\Scripts\python.exe` with
`.venv/bin/python`.

## Contribution paths

### Add a capability

1. Add a JSON record under `capabilities/`.
2. Use the upstream repository as `source.repository`.
3. Pin or bound the tested revision honestly.
4. Declare the licence, interfaces, platforms, network requirement, and claims.
5. Do not describe a claim as verified merely because the upstream project makes
   it. Verification belongs in receipts.

### Add a task

1. Place public-safe inputs and expected outputs in a new folder under `fixtures/`.
2. Declare the fixture licence and creator.
3. Add their SHA-256 hashes to a task record under `tasks/`.
4. State measurable assertions and resource constraints.
5. Distinguish table localisation from extraction. If a page or bounding box is
   supplied, say so in the task objective.

Fixtures must not contain secrets, personal data, confidential information, or
material that cannot legally be redistributed.

### Add an adapter

1. Implement the common adapter contract in `src/toolcommons/adapters.py`.
2. Keep imports lazy so validation does not require benchmark dependencies.
3. Document default settings and fallbacks in the generated receipt.
4. Return raw rows. Do not hide post-processing inside an extractor.
5. Add the dependency only to the `benchmark` optional dependency group.

### Add a transformation

1. Give the transformation a stable name and version.
2. Implement it in `src/toolcommons/transforms.py`.
3. Add focused unit tests showing both what it changes and what it preserves.
4. Keep raw extractor output as an intermediate artefact.
5. Never overwrite or relabel a raw failure as a raw success.

### Add a receipt

Run the task through the ToolCommons command rather than writing a receipt by
hand. For example:

```powershell
toolcommons run community.pdf.borderless-multiline-table.v1 --with pdfplumber
toolcommons run community.pdf.borderless-multiline-table.v1 --with pdfplumber --transform collapse-multiline
```

A failed or error receipt is welcome when it reflects what genuinely happened.
Remove secrets and private paths from logs before contributing. Do not edit an
existing content-addressed receipt; create a new execution instead.

## Evidence policy

- Claims and results remain separate records.
- Inputs, expected outputs, generated outputs, and versions must be identifiable.
- Raw and transformed results must remain distinguishable.
- Contradictory receipts are retained until their cause is understood.
- Performance figures must describe their measurement method and should not be
  presented as universal rankings after a single run.
- ToolCommons receipts are reproducibility evidence, not security attestations.

## Pull request checklist

Before opening a pull request, confirm that:

- [ ] `python -m toolcommons validate .` succeeds;
- [ ] all contract tests pass;
- [ ] new behaviour has focused tests;
- [ ] fixture licences and provenance are declared;
- [ ] no secret, personal, or confidential data is included;
- [ ] generated receipts and artefacts are content-addressed;
- [ ] documentation explains material assumptions and limitations.

GitHub runs the same validation on Linux and Windows with Python 3.11 and 3.12.
A pull request should not be merged while one of these checks is failing without a
documented reason.

Before writing code, use the repository's structured issue forms to propose a
capability or benchmark, report a reproduction difference, or describe a bug. The
pull request template then carries the same provenance and evidence questions into
review.

## Licence

By contributing, you agree that your contribution is provided under the
Apache-2.0 licence. Fixtures may use another compatible licence when that licence
is explicitly declared in the task provenance.
