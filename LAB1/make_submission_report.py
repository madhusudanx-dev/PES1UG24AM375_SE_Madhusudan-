from pathlib import Path
import csv
import re
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

ROOT = Path(__file__).parent
rows = list(csv.DictReader(open(ROOT / 'requirements_table.csv', encoding='utf-8')))
SOURCE_DIAGRAM = Path(r'C:\Users\mukul\Downloads\library_usecase_diagram.drawio.pdf')

styles = getSampleStyleSheet()
title = ParagraphStyle('ReportTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=TA_CENTER, textColor=colors.HexColor('#17365D'), spaceAfter=8)
subtitle = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceAfter=18)
h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, leading=17, textColor=colors.HexColor('#17365D'), spaceBefore=8, spaceAfter=8)
body = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=9, leading=12, spaceAfter=6)
small = ParagraphStyle('Small', parent=styles['BodyText'], fontSize=7.1, leading=8.5)
caption = ParagraphStyle('Caption', parent=styles['BodyText'], fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceBefore=5, spaceAfter=8)

def P(text, style=body):
    # Preserve intentional ReportLab markup while escaping only bare ampersands.
    text = re.sub(r'&(?!#?\w+;)', '&amp;', text)
    return Paragraph(text, style)

def build():
    out = ROOT / 'Lab1_Submission_Report.pdf'
    doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=24, leftMargin=24, topMargin=28, bottomMargin=28, title='Digital Campus Library Reservation Gateway - Lab 1 Submission')
    story = [P('Digital Campus Library Reservation Gateway', title), P('Software Engineering Lab 1 | Requirements Engineering &amp; UML Use-Case Modelling | Problem Statement #08', subtitle)]
    story += [P('Submission Overview', h1), P('This report consolidates the complete Lab 1 submission for the Campus &amp; Academic Operations scenario. It includes the required seven-row requirements specification, the supplied draw.io UML use-case diagram preserved as vector PDF content, and the one-page UC-02 use-case flow.', body), Spacer(1, 4)]
    story += [P('1. Complete Requirements Table', h1)]
    keys = ['Req ID','Type','Description','Priority','Acceptance Criteria','Rationale']
    data = [[P(f'<b>{k}</b>', small) for k in keys]]
    for row in rows: data.append([P(row[k], small) for k in keys])
    table = Table(data, colWidths=[34,52,120,40,180,115], repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17365D')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#9EADBA')),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F2F6FA')]),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story += [table, PageBreak(), P('2. UML Use-Case Diagram', h1), P('The supplied draw.io UML export is preserved as the authoritative diagram deliverable in the repository and is included as the next report page.', body), PageBreak()]
    story += [P('3. Use-Case Flow Specification - UC-02 Place Hold on Loaned Book', h1), P('<b>Primary actor:</b> Student Member &nbsp;&nbsp; <b>Supporting actor:</b> Head Librarian / Notification Service &nbsp;&nbsp; <b>Goal:</b> Join the FIFO queue for a currently loaned book.', body), P('Preconditions', h1)]
    for x in ['Student is authenticated with an active library account.','The ISBN exists in the catalog and all copies are currently loaned.','The student is below the active-hold limit and has no duplicate active hold.']: story.append(P('• ' + x, body))
    story += [P('Postconditions', h1)]
    for x in ['A WAITING hold record stores member, ISBN, FIFO position, and timestamp.','The member sees the assigned position and the librarian queue is updated.','No existing checkout is changed.']: story.append(P('• ' + x, body))
    story += [P('Main Success Scenario', h1)]
    for x in ['1. Student searches by title, author, or ISBN.','2. System validates the query and shows the loaned title.','3. Student selects the title and chooses Place hold.','4. System validates authentication, account standing, hold limit, and duplicates.','5. System locks the queue, assigns the next FIFO position, and creates the hold.','6. System releases the lock and schedules an availability notification.','7. System displays confirmation with queue position and notification conditions.','8. Use case ends successfully.']: story.append(P(x, body))
    story += [P('Alternate Flow - Member Not Eligible (4a)', h1), P('4a1. If the limit, duplicate, or blocked-account rule fails, no hold is created.<br/>4a2. The system shows the specific reason and required corrective action.<br/>4a3. The student may return to search; the queue is unchanged.', body), P('Relationships', h1), P('Place Hold <b>&lt;&lt;include&gt;&gt;</b> Validate Member Eligibility.<br/>Send Availability Notification <b>&lt;&lt;extend&gt;&gt;</b> Process Book Return when a waiting queue exists.', body)]
    story += [Spacer(1,8), P('Source deliverables: requirements_table.csv/docx/pdf, use_case_diagram.pdf, use_case_flow.md/docx/pdf, and the corresponding README traceability notes.', caption)]
    doc.build(story)
    # Replace the diagram placeholder page with the supplied draw.io PDF page.
    report_reader = PdfReader(str(out))
    merged = PdfWriter()
    merged.add_page(report_reader.pages[0])
    merged.add_page(PdfReader(str(ROOT / 'use_case_diagram.pdf')).pages[0])
    merged.add_page(report_reader.pages[-1])
    with open(out, 'wb') as f:
        merged.write(f)

def clean_diagram_pdf():
    reader = PdfReader(str(SOURCE_DIAGRAM))
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    with open(ROOT / 'use_case_diagram.pdf', 'wb') as f:
        writer.write(f)

if __name__ == '__main__':
    clean_diagram_pdf()
    build()
