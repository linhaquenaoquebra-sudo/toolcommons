from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "fixtures" / "pdf-quarterly-sales" / "input.pdf"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=24 * mm, leftMargin=24 * mm,
        topMargin=22 * mm, bottomMargin=22 * mm,
        title="Quarterly Sales 2025", author="ToolCommons community fixture",
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Quarterly Sales 2025", styles["Title"]),
        Spacer(1, 5 * mm),
        Paragraph(
            "Synthetic benchmark fixture. Values are unit sales and contain no private data.",
            styles["BodyText"],
        ),
        Spacer(1, 8 * mm),
    ]
    rows = [
        ["Region", "Q1", "Q2", "Q3", "Q4", "Total"],
        ["North", "120", "135", "142", "158", "555"],
        ["South", "98", "105", "117", "126", "446"],
        ["East", "143", "151", "149", "162", "605"],
        ["West", "110", "108", "121", "137", "476"],
    ]
    table = Table(rows, colWidths=[42 * mm, 20 * mm, 20 * mm, 20 * mm, 20 * mm, 24 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("ALIGN", (1, 0), (-1, 0), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EDF3F7")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#8095A8")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    document.build(story)


if __name__ == "__main__":
    main()
