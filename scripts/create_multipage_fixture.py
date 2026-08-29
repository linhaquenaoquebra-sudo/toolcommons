from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "fixtures" / "pdf-multipage-procurement" / "input.pdf"

ROWS = [
    ["PO-2025-001", "2025-01-08", "Civic IT", "Laptop docks", "12", "1,428.00"],
    ["PO-2025-002", "2025-01-15", "North Paper", "Recycled paper", "80", "376.00"],
    ["PO-2025-003", "2025-01-27", "SafeWork", "Protective gloves", "150", "592.50"],
    ["PO-2025-004", "2025-02-04", "Metro Signs", "Wayfinding signs", "18", "1,116.00"],
    ["PO-2025-005", "2025-02-11", "Green Office", "LED desk lamps", "25", "875.00"],
    ["PO-2025-006", "2025-02-20", "WaterLab", "Sampling bottles", "60", "438.00"],
    ["PO-2025-007", "2025-03-03", "Civic IT", "Network switches", "4", "2,760.00"],
    ["PO-2025-008", "2025-03-12", "Urban Tools", "Survey tripods", "6", "1,170.00"],
    ["PO-2025-009", "2025-03-24", "North Paper", "Archive folders", "120", "330.00"],
    ["PO-2025-010", "2025-04-02", "SafeWork", "Safety helmets", "30", "645.00"],
    ["PO-2025-011", "2025-04-14", "Green Office", "Meeting chairs", "16", "2,080.00"],
    ["PO-2025-012", "2025-04-29", "WaterLab", "Field test kits", "10", "1,950.00"],
]


def footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#657483"))
    canvas.drawString(20 * mm, 13 * mm, "Synthetic public benchmark - CC0-1.0")
    canvas.drawRightString(A4[0] - 20 * mm, 13 * mm, f"Page {document.page}")
    canvas.restoreState()


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("ReportTitle", parent=styles["Title"], fontSize=18, leading=22, textColor=colors.HexColor("#16324F"), spaceAfter=4)
    context = ParagraphStyle("Context", parent=styles["BodyText"], fontSize=9, leading=12, textColor=colors.HexColor("#4D6072"))
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=17 * mm, bottomMargin=22 * mm,
        title="Public Procurement Register 2025", author="ToolCommons community fixture",
    )
    header = ["Order", "Date", "Supplier", "Description", "Qty", "Amount EUR"]
    story = []
    for page_index in range(3):
        story.extend([
            Paragraph("Public Procurement Register", title),
            Paragraph(f"Reporting period: January-April 2025 | Section {page_index + 1} of 3", context),
            Spacer(1, 7 * mm),
        ])
        table = Table(
            [header, *ROWS[page_index * 4:(page_index + 1) * 4]],
            colWidths=[29 * mm, 26 * mm, 31 * mm, 45 * mm, 13 * mm, 29 * mm],
            rowHeights=[10 * mm] + [12 * mm] * 4,
            repeatRows=1, hAlign="LEFT",
        )
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16324F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#7890A4")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EDF3F7")]),
            ("ALIGN", (4, 0), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.extend([
            table,
            Spacer(1, 7 * mm),
            Paragraph("Amounts exclude VAT. Supplier names and transactions are fictional and contain no personal or commercial data.", context),
        ])
        if page_index < 2:
            story.append(PageBreak())
    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    main()
