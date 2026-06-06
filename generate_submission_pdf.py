"""Generate a simple one-page submission PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle)

OUTPUT = "WikiApp_Submission.pdf"
BLUE  = HexColor("#1e3a8a")
BLUE2 = HexColor("#2563eb")
DARK  = HexColor("#111827")

styles = getSampleStyleSheet()

title_style = ParagraphStyle("T", parent=styles["Title"], fontSize=22, leading=28,
    textColor=BLUE, alignment=TA_CENTER, spaceAfter=8)
sub_style = ParagraphStyle("S", parent=styles["Normal"], fontSize=12, leading=16,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=20)
heading_style = ParagraphStyle("H", parent=styles["Heading2"], fontSize=14, leading=20,
    textColor=BLUE2, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6)
body_style = ParagraphStyle("B", parent=styles["Normal"], fontSize=11, leading=16,
    textColor=DARK, alignment=TA_LEFT, spaceAfter=4)
link_style = ParagraphStyle("L", parent=styles["Normal"], fontSize=14, leading=22,
    textColor=BLUE2, alignment=TA_CENTER, spaceAfter=6)

story = []

story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("WikiApp - Assessment 2 Part A", title_style))
story.append(Paragraph("Movindu Lochana &nbsp;|&nbsp; s1577380 &nbsp;|&nbsp; "
                       "BIT235 Object Oriented Programming", sub_style))

# --- The link ---
story.append(Paragraph("GitHub Repository", heading_style))
link_box = Table([[
    Paragraph(
        '<link href="https://github.com/DustyxT/WikiApp/tree/part-a" color="#2563eb">'
        '<b><u>https://github.com/DustyxT/WikiApp/tree/part-a</u></b></link>',
        link_style)
]], colWidths=[16*cm])
link_box.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), HexColor("#dbeafe")),
    ("BOX", (0,0), (-1,-1), 1, BLUE),
    ("TOPPADDING", (0,0), (-1,-1), 14),
    ("BOTTOMPADDING", (0,0), (-1,-1), 14),
]))
story.append(link_box)

# --- How to run ---
story.append(Paragraph("How to run", heading_style))
story.append(Paragraph("Requires Java 17 or higher. Maven is bundled via the Maven Wrapper.",
                       body_style))
story.append(Spacer(1, 0.2*cm))

steps = [
    [Paragraph("<b>1.</b>", body_style),
     Paragraph("Unzip the project (or clone with "
               "<font face=\"Courier\">git clone -b part-a "
               "https://github.com/DustyxT/WikiApp.git</font>).", body_style)],
    [Paragraph("<b>2.</b>", body_style),
     Paragraph("Open a terminal in the project folder.", body_style)],
    [Paragraph("<b>3.</b>", body_style),
     Paragraph("Run <font face=\"Courier\">.\\mvnw.cmd spring-boot:run</font> "
               "(Windows) or <font face=\"Courier\">./mvnw spring-boot:run</font> "
               "(Mac/Linux).", body_style)],
    [Paragraph("<b>4.</b>", body_style),
     Paragraph("Open <b>http://localhost:8080</b> in a browser.", body_style)],
    [Paragraph("<b>5.</b>", body_style),
     Paragraph("Log in with username <b>movindu</b> and password <b>123</b>.",
               body_style)],
]
steps_table = Table(steps, colWidths=[1*cm, 15*cm], hAlign="LEFT")
steps_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(steps_table)

doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=1.5*cm, bottomMargin=1.5*cm,
                        title="WikiApp - Part A Submission",
                        author="Movindu Lochana (s1577380)")
doc.build(story)
print(f"Wrote: {OUTPUT}")
