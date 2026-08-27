from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "fixtures" / "pdf-borderless-multiline" / "input.pdf"


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    cell = ParagraphStyle("Cell", parent=styles["BodyText"], fontSize=9.5, leading=12, textColor=colors.HexColor("#263746"))
    header = ParagraphStyle("Header", parent=cell, fontName="Helvetica-Bold", textColor=colors.HexColor("#17324D"))
    note = ParagraphStyle("Note", parent=styles["BodyText"], fontSize=8.5, leading=11, textColor=colors.HexColor("#5B6975"))
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=22 * mm, leftMargin=22 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title="Quarterly Account Activity", author="ToolCommons community fixture",
    )
    story = [
        Paragraph("Quarterly Account Activity", styles["Title"]),
        Spacer(1, 3 * mm),
        Paragraph("January to March 2025 - verified account totals", styles["BodyText"]),
        Spacer(1, 9 * mm),
    ]
    raw_rows = [
        ["Account", "Segment", "Jan", "Feb", "Mar", "Quarter"],
        ["Aurora Labs", "Enterprise", "42", "47", "51", "140"],
        ["Blue Harbor", "Small\nbusiness", "28", "31", "35", "94"],
        ["Casa Verde", "Nonprofit", "19", "22", "24", "65"],
        ["Delta Works", "Public\nsector", "36", "39", "44", "119"],
    ]
    rows = [[paragraph(value, header if index == 0 else cell) for value in row] for index, row in enumerate(raw_rows)]
    table = Table(rows, colWidths=[39 * mm, 37 * mm, 18 * mm, 18 * mm, 18 * mm, 24 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, colors.HexColor("#17324D")),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([
        table,
        Spacer(1, 7 * mm),
        Paragraph("Note: Quarter values are the sum of January, February, and March. Segment labels may wrap onto two lines.", note),
        Spacer(1, 2 * mm),
        Paragraph("Synthetic benchmark fixture. No customer or commercial data is represented.", note),
    ])
    document.build(story)


if __name__ == "__main__":
    main()
