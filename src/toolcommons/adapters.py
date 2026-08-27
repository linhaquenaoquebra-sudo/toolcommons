from __future__ import annotations

import importlib.metadata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

Rows = list[list[str]]


@dataclass(frozen=True)
class Adapter:
    name: str
    capability_id: str
    distribution: str
    extract: Callable[[Path, dict[str, Any]], Rows]

    def version(self) -> str:
        try:
            return importlib.metadata.version(self.distribution)
        except importlib.metadata.PackageNotFoundError:
            return "unavailable"


def extract_pdfplumber(path: Path, task: dict[str, Any]) -> Rows:
    import pdfplumber
    with pdfplumber.open(path) as document:
        page = document.pages[task["input"].get("pageIndex", 0)]
        if bbox := task["input"].get("bboxPoints"):
            page = page.crop(tuple(bbox))
        table = page.extract_table()
        if not table:
            table = page.extract_table({
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "min_words_vertical": 1,
                "min_words_horizontal": 1,
                "text_tolerance": 3,
            })
    if not table:
        raise RuntimeError("pdfplumber detected no table")
    return [[cell or "" for cell in row] for row in table]


def extract_pymupdf(path: Path, task: dict[str, Any]) -> Rows:
    import pymupdf
    with pymupdf.open(path) as document:
        page = document[task["input"].get("pageIndex", 0)]
        clip = pymupdf.Rect(task["input"]["bboxPoints"]) if task["input"].get("bboxPoints") else None
        finder = page.find_tables(clip=clip)
        if not finder.tables:
            finder = page.find_tables(clip=clip, strategy="text", min_words_vertical=1, min_words_horizontal=1)
        if not finder.tables:
            raise RuntimeError("PyMuPDF detected no table")
        table = finder.tables[0].extract()
    return [[cell or "" for cell in row] for row in table]


def extract_camelot(path: Path, task: dict[str, Any]) -> Rows:
    import camelot
    import pymupdf

    page_index = task["input"].get("pageIndex", 0)
    kwargs: dict[str, Any] = {
        "pages": str(page_index + 1),
        "flavor": "lattice" if task["input"].get("tableStyle") == "ruled" else "stream",
    }
    if bbox := task["input"].get("bboxPoints"):
        with pymupdf.open(path) as document:
            page_height = document[page_index].rect.height
        x0, top, x1, bottom = bbox
        kwargs["table_areas"] = [f"{x0},{page_height - top},{x1},{page_height - bottom}"]
    tables = camelot.read_pdf(str(path), **kwargs)
    if not tables:
        raise RuntimeError("Camelot detected no table")
    return [[str(cell or "") for cell in row] for row in tables[0].df.values.tolist()]


ADAPTERS = {
    "pdfplumber": Adapter("pdfplumber", "github.pdfplumber.pdfplumber", "pdfplumber", extract_pdfplumber),
    "pymupdf": Adapter("pymupdf", "github.pymupdf.pymupdf", "PyMuPDF", extract_pymupdf),
    "camelot": Adapter("camelot", "github.camelot-dev.camelot", "camelot-py", extract_camelot),
}


def get_adapter(name: str) -> Adapter:
    try:
        return ADAPTERS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown adapter {name!r}; choose one of: {', '.join(sorted(ADAPTERS))}") from exc
