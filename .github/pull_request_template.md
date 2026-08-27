## Purpose

<!-- What problem does this change solve, and for whom or which agent? -->

## Contribution type

- [ ] Capability description
- [ ] Benchmark task or fixture
- [ ] Adapter
- [ ] Transformation
- [ ] Reproducibility receipt
- [ ] Documentation or community tooling
- [ ] Other

## Evidence and provenance

<!-- Link the related issue. Describe sources, versions, fixture creators, licences, constraints, and material assumptions. -->

## Verification

<!-- List the commands you ran and summarize the results. -->

```text
python -m toolcommons validate .
python -m unittest discover -s tests -v
```

## Checklist

- [ ] The change is independent of secrets and private infrastructure.
- [ ] New behaviour has focused tests.
- [ ] Fixture licences and provenance are declared.
- [ ] No secret, personal, confidential, or unlawfully redistributed data is included.
- [ ] Claims remain separate from execution evidence.
- [ ] Raw and transformed results remain distinguishable.
- [ ] New receipts and artefacts are content-addressed and existing receipts were not edited.
- [ ] Documentation explains material assumptions, limitations, and measurement methods.
- [ ] Local validation and contract tests pass.

## Reviewer notes

<!-- Call out anything that deserves special scrutiny or that you intentionally left for a follow-up. -->
