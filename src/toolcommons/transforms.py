from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .adapters import Rows


@dataclass(frozen=True)
class Transform:
    name: str
    version: str
    apply: Callable[[Rows], Rows]

    @property
    def identifier(self) -> str:
        return f"{self.name}.v{self.version}"


def collapse_sparse_continuations(rows: Rows) -> Rows:
    """Merge sparse visual lines into neighbouring rows with numeric values.

    The first non-empty row is treated as the header. Remaining rows containing a
    value from the third column onward are anchors. Sparse rows are attached to the
    adjacent anchor that has empty cells where the fragment contains text.
    """
    compact = [(index, [cell.strip() for cell in row]) for index, row in enumerate(rows) if any(cell.strip() for cell in row)]
    if len(compact) < 2:
        return [row for _, row in compact]
    header_index, header = compact[0]
    body = compact[1:]
    anchors = [(index, row) for index, row in body if any(cell for cell in row[2:])]
    if not anchors:
        return [header] + [row for _, row in body]

    fragments: dict[int, list[tuple[int, list[str]]]] = {index: [] for index, _ in anchors}
    anchor_indices = [index for index, _ in anchors]
    anchor_rows = {index: row for index, row in anchors}
    for fragment_index, fragment in body:
        if fragment_index in anchor_rows:
            continue
        previous = max((index for index in anchor_indices if index < fragment_index), default=None)
        following = min((index for index in anchor_indices if index > fragment_index), default=None)
        candidates = [index for index in (previous, following) if index is not None]
        if not candidates:
            continue
        populated = [position for position, value in enumerate(fragment) if value]
        target = max(
            candidates,
            key=lambda index: (
                sum(not anchor_rows[index][position] for position in populated if position < len(anchor_rows[index])),
                -abs(index - fragment_index),
                index > fragment_index,
            ),
        )
        fragments[target].append((fragment_index, fragment))

    result: Rows = [header]
    for anchor_index, anchor in anchors:
        pieces = fragments[anchor_index] + [(anchor_index, anchor)]
        width = max(len(row) for _, row in pieces)
        merged = []
        for column in range(width):
            values = [row[column] for _, row in sorted(pieces) if column < len(row) and row[column]]
            merged.append("\n".join(values))
        result.append(merged)
    return result


def drop_repeated_headers(rows: Rows) -> Rows:
    """Keep the first header and remove identical headers from later pages."""
    if not rows:
        return []
    header = rows[0]
    return [header, *(row for row in rows[1:] if row != header)]


TRANSFORMS = {
    "collapse-multiline": Transform("collapse-sparse-continuations", "1", collapse_sparse_continuations),
    "drop-repeated-headers": Transform("drop-repeated-headers", "1", drop_repeated_headers),
}


def get_transform(name: str) -> Transform:
    try:
        return TRANSFORMS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown transform {name!r}; choose one of: {', '.join(sorted(TRANSFORMS))}") from exc
