from pathlib import Path
import csv
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ROOT=Path(__file__).parent
rows=list(csv.DictReader(open(ROOT/'requirements_table.csv',encoding='utf-8')))

def build_req_docx():
 d=Document(); sec=d.sections[0]; sec.top_margin=Inches(.55); sec.bottom_margin=Inches(.55); sec.left_margin=Inches(.55); sec.right_margin=Inches(.55)
 p=d.add_paragraph(); p.alignment=1; r=p.add_run('Digital Campus Library Reservation Gateway'); r.bold=True; r.font.size=Pt(16); r.font.color.rgb=RGBColor(23,54,93)
 p=d.add_paragraph(); p.alignment=1; p.add_run('Requirements Table | Problem Statement #08').italic=True
 t=d.add_table(rows=1, cols=6); t.style='Table Grid'; hdr=['Req ID','Type','Description','Priority','Acceptance Criteria','Rationale']
 for i,h in enumerate(hdr): t.rows[0].cells[i].text=h
 for row in rows:
  cells=t.add_row().cells
  for i,k in enumerate(['Req ID','Type','Description','Priority','Acceptance Criteria','Rationale']): cells[i].text=row[k]
 for row in t.rows:
  for cell in row.cells:
   for p in cell.paragraphs:
    for run in p.runs: run.font.size=Pt(7.2)
 d.save(ROOT/'requirements_table.docx')

def build_flow_docx():
 d=Document(); sec=d.sections[0]; sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.8); sec.right_margin=Inches(.8)
 p=d.add_paragraph(); r=p.add_run('Use-Case Flow: Place Hold on Loaned Book'); r.bold=True; r.font.size=Pt(16); r.font.color.rgb=RGBColor(23,54,93)
 d.add_paragraph('UC-02 | Primary actor: Student Member | Digital Campus Library Reservation Gateway')
 sections=[('Preconditions',['Student is authenticated with an active library account.','ISBN exists and all copies are currently loaned.','Student is below the active-hold limit and has no duplicate hold.']),('Postconditions',['A WAITING hold record stores member, ISBN, FIFO position, and timestamp.','Member sees the assigned position; librarian queue is updated.','No existing checkout is changed.']),('Main Success Scenario',['1. Student searches by title, author, or ISBN.','2. System validates the query and shows the loaned title.','3. Student selects the title and chooses Place hold.','4. System validates authentication, account standing, hold limit, and duplicates.','5. System locks the queue, assigns the next FIFO position, and creates the hold.','6. System releases the lock and schedules an availability notification.','7. System displays confirmation with queue position and notification conditions.','8. Use case ends successfully.']),('Alternate Flow: Member Not Eligible (4a)',['4a1. If the limit, duplicate, or blocked-account rule fails, no hold is created.','4a2. System shows the reason and required corrective action.','4a3. Student may return to search; the queue is unchanged.']),('Relationships',['Place Hold <<include>> Validate Member Eligibility.','Send Availability Notification <<extend>> Process Book Return when a waiting queue exists.'])]
 for head,items in sections:
  p=d.add_paragraph(); r=p.add_run(head); r.bold=True; r.font.color.rgb=RGBColor(23,54,93)
  for item in items: d.add_paragraph(item,style='List Bullet')
 d.save(ROOT/'use_case_flow.docx')

def build_req_pdf():
 styles=getSampleStyleSheet(); normal=ParagraphStyle('n',parent=styles['BodyText'],fontSize=6.2,leading=7.2); title=ParagraphStyle('t',parent=styles['Title'],fontSize=16,textColor=colors.HexColor('#17365D'))
 doc=SimpleDocTemplate(str(ROOT/'requirements_table.pdf'),pagesize=A4,rightMargin=20,leftMargin=20,topMargin=24,bottomMargin=20)
 data=[[Paragraph('<b>'+x+'</b>',normal) for x in ['Req ID','Type','Description','Priority','Acceptance Criteria','Rationale']]]
 for r in rows: data.append([Paragraph(r[k],normal) for k in ['Req ID','Type','Description','Priority','Acceptance Criteria','Rationale']])
 table=Table(data,colWidths=[38,55,125,42,170,100],repeatRows=1); table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17365D')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#9EADBA')),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F2F6FA')]),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]))
 doc.build([Paragraph('Digital Campus Library Reservation Gateway',title),Paragraph('Requirements Table | Problem Statement #08',styles['Normal']),Spacer(1,10),table])

if __name__=='__main__': build_req_docx(); build_flow_docx(); build_req_pdf()
