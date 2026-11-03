#!/usr/bin/env python3
"""Add the owner-requested right alignment pair to A4, without moving connectors."""
from pathlib import Path
import json,re,sys,tempfile,uuid
import pcbnew as p
if '--apply' not in sys.argv:raise SystemExit('Use --apply to update a reviewed A4 board.')
root=Path(__file__).resolve().parents[1];project=root/'boards/rear-io';path=project/'rear-io.kicad_pcb';s=path.read_text()
assert '"HREF1"' in s and '"HREF2"' in s and '"HREF3"' not in s,'Expected A4 with only the left alignment pair.'
removed=[]
def remove_right(m):
 block=m.group(0)
 if '(layer "Edge.Cuts")' not in block:return block
 points={tuple(map(float,q)) for q in re.findall(r'\((?:start|end) ([-\d.]+) ([-\d.]+)\)',block)}
 if points=={(264,102),(264,130)}:removed.append(block);return ''
 return block
s=re.sub(r'(?ms)^\t\(gr_line\n.*?^\t\)\n',remove_right,s);assert len(removed)==1
items=[]
def add(a,b,mid=None):
 geom=f'(start {a[0]} {a[1]}) '+(f'(mid {mid[0]} {mid[1]}) ' if mid else '')+f'(end {b[0]} {b[1]})'
 items.append(f'\n\t({"gr_arc" if mid else "gr_line"} {geom} (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))\n')
for a,b in [((264,102),(264,106)),((264,106),(265,106)),((265,114),(264,114)),((264,114),(264,121)),((264,121),(265,121)),((265,129),(264,129)),((264,129),(264,130))]:add(a,b)
add((265,106),(265,114),(269,110));add((265,121),(265,129),(269,125))
s=s.rstrip();s=s[:-1]+''.join(items)+')\n'
s=s.replace('OPEN CINEMA A4 / ALIGNMENT HOLES','OPEN CINEMA A5 / ALIGNMENT HOLES BOTH SIDES').replace('ALIGNMENT HOLES x-115,z44/59 D3 / PROVISIONAL','4 ALIGNMENT HOLES x+/-115,z44/59 D3 / PROVISIONAL').replace('OPEN CINEMA / A4','OPEN CINEMA / A5')
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb') as t:
 t.write(s);t.flush();board=p.LoadBoard(t.name)
board.SetFileName(str(path))
for i,z in [(3,44),(4,59)]:
 f=p.FootprintLoad(str(project/'OpenCinema_Connectors.pretty'),'AlignmentHole_D3_Reference');assert f
 f.SetReference('HREF'+str(i));f.SetPosition(p.VECTOR2I(p.FromMM(265),p.FromMM(169-z)));board.Add(f)
p.SaveBoard(str(path),board)
cfg=json.loads((project/'placement.json').read_text());cfg['revision']='A5-both-side-alignment'
cfg['board'].update(overall_width_including_alignment_tabs=238,alignment_tab_right_x=119,outline_note='228x32 body plus four R4 tabs, centres x+/-115,z44/59; overall238x32')
f=cfg['reference_fixing_points'];f.update(source='Owner Sketch3 left pair plus explicit owner request to mirror on both sides',positions_xz=[[-115,44],[-115,59],[115,44],[115,59]],status='four actual D3 NPTH alignment holes, two per side; provisional mounting',references=['HREF1','HREF2','HREF3','HREF4']);f['alignment_tabs']['rightmost_x']=119
(project/'placement.json').write_text(json.dumps(cfg,indent=2)+'\n')
pj=json.loads((project/'rear-io.kicad_pro').read_text());pj['text_variables']['REVISION']='A5-both-side-alignment';(project/'rear-io.kicad_pro').write_text(json.dumps(pj,indent=2)+'\n')
print('Added HREF3/HREF4 at x+115,z44/59, mirroring the existing left pair.')
