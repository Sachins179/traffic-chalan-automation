"""
PDF chalan generator using ReportLab.
Supports multiple violations per chalan.
"""
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.utils.config_loader import config
from src.utils.logger import get_logger

log = get_logger("chalan.pdf")

_HEADER_COLOR = colors.HexColor("#1a237e")
_LABEL_BG = colors.HexColor("#e3f2fd")
_LABEL_FG = colors.HexColor("#0d47a1")
_TOTAL_BG = colors.HexColor("#ffebee")
_TOTAL_FG = colors.HexColor("#b71c1c")


def generate_chalan_pdf(
    *,
    owner_name: str,
    vehicle_number: str,
    violation_names: list[str],
    fine_breakdown: dict,
    total_fine: int,
) -> str:
    """
    Build a chalan PDF and return its absolute path.

    Args:
        owner_name: Vehicle owner's name.
        vehicle_number: Vehicle registration number.
        violation_names: List of violation names.
        fine_breakdown: Dict mapping violation -> fine.
        total_fine: Total fine amount.

    Returns:
        Absolute path to the generated PDF.
    """
    pdfs_dir = config.abs_path("pdfs_dir")
    pdfs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = pdfs_dir / f"chalan_{vehicle_number}_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TCA_Title",
        parent=styles["Title"],
        textColor=_HEADER_COLOR,
        fontSize=20,
        spaceAfter=20,
    )
    normal = styles["Normal"]

    elements = [
        Paragraph("TRAFFIC E-CHALAN", title_style),
        Paragraph(
            f"<b>Chalan Date:</b> "
            f"{datetime.now().strftime('%d-%b-%Y %H:%M')}",
            normal,
        ),
        Spacer(1, 0.8 * cm),
    ]

    # ---------------- Vehicle info table ----------------
    info_rows = [
        ["Owner Name", owner_name],
        ["Vehicle Number", vehicle_number],
    ]
    info_table = Table(info_rows, colWidths=[5 * cm, 10 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), _LABEL_BG),
        ("TEXTCOLOR", (0, 0), (0, -1), _LABEL_FG),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(info_table)

    elements.append(Spacer(1, 0.8 * cm))
    elements.append(Paragraph("<b>Violations Detected:</b>", normal))
    elements.append(Spacer(1, 0.3 * cm))

    # ---------------- Violations table ----------------
    violation_rows = [["Violation", "Fine (Rs.)"]]
    for name, fine in fine_breakdown.items():
        violation_rows.append([name, str(fine)])
    violation_rows.append(["TOTAL", str(total_fine)])

    v_table = Table(violation_rows, colWidths=[10 * cm, 5 * cm])
    v_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), _HEADER_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), _TOTAL_BG),
        ("TEXTCOLOR", (0, -1), (-1, -1), _TOTAL_FG),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(v_table)

    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph(
        "<i>Please pay the total fine within 15 days to avoid "
        "additional penalties.</i>",
        normal,
    ))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph(
        "This is a system-generated chalan and does not require a signature.",
        normal,
    ))

    doc.build(elements)
    log.info("PDF chalan generated: %s", filepath)
    return str(filepath)