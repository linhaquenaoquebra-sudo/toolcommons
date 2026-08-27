# Benchmark findings

## Borderless multiline table v1

The first attempt supplied the complete page. Both pdfplumber and PyMuPDF failed
to detect a table with their default strategies. Their text-alignment fallbacks
then interpreted the full page as a 23 by 22 matrix.

The task was refined to state that it evaluates extraction from a known region,
not automatic table localisation. A page index and bounding box were added to the
task contract. The original receipts remain in the repository.

With the region supplied, both adapters found six columns but returned fifteen
physical rows instead of five logical rows. Wrapped segment labels were emitted as
separate rows, with empty spacer rows retained. Both therefore failed the exact
cell, row, and column assertions.

This establishes the next capability boundary: logical row reconstruction should
be modelled as an explicit transformation rather than silently added to the raw
extractor. A future pipeline can compare raw extraction with extraction plus a
declared canonicalisation step.

## Explicit reconstruction pipeline

`collapse-sparse-continuations.v1` removes empty visual spacer rows, identifies
rows with numeric values as anchors, and assigns sparse text fragments to the
adjacent anchor with matching empty cells. Raw and transformed CSV files are both
content-addressed in the receipt.

Applied to the borderless fixture, the declared pipeline raised pdfplumber and
PyMuPDF from 6.7% to 100% cell accuracy. The raw failures remain visible beside
the transformed results.

## Camelot 2.0

Camelot uses its `lattice` parser for the ruled fixture and `stream` for the
borderless fixture, selected through the task's tool-neutral `tableStyle` hint.
It reached 100% on the ruled table without transformation. On the borderless
fixture its raw result reached 22.2%, ahead of the two 6.7% raw results, but still
failed the exact assertions. With the same reconstruction transform it reached
100%.

The recorded duration is one cold execution and includes import and parser setup.
Peak memory is measured with Python's allocation tracer and does not capture every
native allocation. These values should not yet be interpreted as a statistically
rigorous performance ranking.
