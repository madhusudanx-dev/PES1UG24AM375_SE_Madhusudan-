from pathlib import Path
import textwrap
ROOT=Path(__file__).parent
def esc(s): return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
def pdf(path,cmds,w,h):
 body='\n'.join(cmds).encode('latin-1','replace'); objs=[b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {w} {h}] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>'.encode(),b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',b'<< /Length %d >>\nstream\n'%len(body)+body+b'\nendstream']; out=b'%PDF-1.4\n'; offs=[]
 for i,o in enumerate(objs,1): offs.append(len(out)); out+=f'{i} 0 obj\n'.encode()+o+b'\nendobj\n'
 x=len(out); out+=f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode()+b''.join(f'{o:010d} 00000 n \n'.encode() for o in offs)+f'trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF'.encode(); path.write_bytes(out)
def tx(c,x,y,s,size=10,col='0 0 0'): c += [f'{col} rg',f'BT /F1 {size} Tf {x} {y} Td ({esc(s)}) Tj ET']
def flow():
 c=[]; tx(c,45,800,'Use-Case Flow: Place Hold on Loaned Book',16,'0.09 0.21 0.36'); tx(c,45,780,'UC-02 | Student Member | Digital Campus Library Reservation Gateway',9,'0.3 0.3 0.3'); y=750
 sections=[('PRECONDITIONS',['Student is authenticated with an active library account.','ISBN exists and all copies are currently loaned.','Student is below the active-hold limit and has no duplicate hold.']),('POSTCONDITIONS',['A WAITING hold record stores member, ISBN, FIFO position, and timestamp.','Member sees the assigned position; librarian queue is updated.','No existing checkout is changed.']),('MAIN SUCCESS SCENARIO',['1. Student searches by title, author, or ISBN.','2. System validates the query and shows the loaned title.','3. Student selects the title and chooses Place hold.','4. System validates authentication, account standing, hold limit, and duplicates.','5. System locks the queue, assigns the next FIFO position, and creates the hold.','6. System releases the lock and schedules an availability notification.','7. System displays confirmation with queue position and notification conditions.','8. Use case ends successfully.']),('ALTERNATE FLOW: MEMBER NOT ELIGIBLE (4a)',['4a1. If the limit, duplicate, or blocked-account rule fails, no hold is created.','4a2. System shows the reason and required corrective action.','4a3. Student may return to search; the queue is unchanged.']),('RELATIONSHIPS',['Place Hold <<include>> Validate Member Eligibility.','Send Availability Notification <<extend>> Process Book Return when a waiting queue exists.'])]
 for head,lines in sections:
  tx(c,45,y,head,11,'0.09 0.21 0.36'); y-=18
  for ln in lines:
   for part in textwrap.wrap(ln,95): tx(c,58,y,part,9); y-=13
  y-=10
 pdf(ROOT/'use_case_flow.pdf',c,595,842)
def diagram():
 c=[]; tx(c,255,490,'Digital Campus Library Reservation Gateway',18,'0.09 0.21 0.36'); c += ['0.09 0.21 0.36 RG 2 w 220 55 520 390 re S']; tx(c,235,425,'Library Reservation Gateway',11,'0.09 0.21 0.36')
 boxes=[(290,385,180,48,'UC-01 Search ISBN Catalog'),(530,385,180,48,'UC-02 Place Hold'),(530,270,180,48,'UC-03 Validate Member Eligibility'),(290,145,180,48,'UC-04 Process Book Return'),(530,145,180,48,'UC-05 Send Availability Notification'),(290,270,180,48,'UC-06 Manage Circulation & Fines')]
 for x,y,bw,bh,label in boxes:
  cx=x+bw/2; cy=y+bh/2; k=.5522848; rx=bw/2; ry=bh/2
  c += [f'0.92 0.95 0.98 rg {cx+rx} {cy} m {cx+rx} {cy+k*ry} {cx+k*rx} {cy+ry} {cx} {cy+ry} c {cx-k*rx} {cy+ry} {cx-rx} {cy+k*ry} {cx-rx} {cy} c {cx-rx} {cy-k*ry} {cx-k*rx} {cy-ry} {cx} {cy-ry} c {cx+k*rx} {cy-ry} {cx+rx} {cy-k*ry} {cx+rx} {cy} c f', '0.18 0.46 0.71 RG 1.2 w', f'{cx+rx} {cy} m {cx+rx} {cy+k*ry} {cx+k*rx} {cy+ry} {cx} {cy+ry} c {cx-k*rx} {cy+ry} {cx-rx} {cy+k*ry} {cx-rx} {cy} c {cx-rx} {cy-k*ry} {cx-k*rx} {cy-ry} {cx} {cy-ry} c {cx+k*rx} {cy-ry} {cx+rx} {cy-k*ry} {cx+rx} {cy} c S']; tx(c,x+10,y+20,label,9)
 for x,y,label in [(90,380,'Student Member'),(90,150,'Head Librarian'),(785,280,'Notification Service')]:
  q=3.866; cy=y+38; c += ['0 0 0 RG 1.5 w',f'{x} {cy+7} m {x+q} {cy+7} {x+7} {cy+q} {x+7} {cy} c {x+7} {cy-q} {x+q} {cy-7} {x} {cy-7} c {x-q} {cy-7} {x-7} {cy-q} {x-7} {cy} c {x-7} {cy+q} {x-q} {cy+7} {x} {cy+7} c S',f'{x} {y+25} m {x} {y-18} l S',f'{x-22} {y+8} m {x+22} {y+8} l S',f'{x} {y-18} m {x-18} {y-48} l S',f'{x} {y-18} m {x+18} {y-48} l S']; tx(c,x-35,y-75,label,10)
 for x1,y1,x2,y2 in [(135,388,290,409),(135,388,290,169),(135,158,290,169),(135,158,290,294),(785,288,710,409),(785,288,710,169),(470,409,530,294),(530,169,470,169)]: c += ['0.3 0.3 0.3 RG 1 w',f'{x1} {y1} m {x2} {y2} l S']
 c += ['0.5 0.38 0 RG 1 w 530 375 m 620 318 l S']; tx(c,548,350,'<<include>>',9,'0.5 0.38 0'); c += ['0.5 0.38 0 RG 1 w 620 193 m 470 169 l S']; tx(c,515,205,'<<extend>>',9,'0.5 0.38 0'); pdf(ROOT/'use_case_diagram.pdf',c,900,520)
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="900" height="520"><rect width="100%" height="100%" fill="white"/><text x="450" y="30" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">Digital Campus Library Reservation Gateway</text><rect x="220" y="55" width="520" height="390" fill="none" stroke="#17365D" stroke-width="2"/>'
 for x,y,bw,bh,label in boxes: svg+=f'<ellipse cx="{x+bw/2}" cy="{520-y-bh/2}" rx="{bw/2}" ry="{bh/2}" fill="#EAF2F8" stroke="#2F75B5"/><text x="{x+bw/2}" y="{520-y-bh/2+4}" text-anchor="middle" font-family="Arial" font-size="12">{label}</text>'
 (ROOT/'use_case_diagram.svg').write_text(svg+'</svg>',encoding='utf-8')
if __name__=='__main__': flow(); diagram()
