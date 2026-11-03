#!/usr/bin/env python3
"""Apply the owner's two provisional alignment holes to a saved A3 PCB.
Requires --apply. Connector footprints and positions are preserved.
"""
from pathlib import Path
import json,math,re,sys,tempfile,uuid
import pcbnew as p
if '--apply' not in sys.argv: raise SystemExit('Use --apply after reviewing manual changes.')
root=Path(__file__).resolve().parents[1];project=root/'boards/rear-io';path=project/'rear-io.kicad_pcb'
s=path.read_text()
if '"HREF1"' in s: raise SystemExit('Alignment holes already present; no changes made.')
removed=[]
def remove_outer(m):
 block=m.group(0)
 if '(layer "Edge.Cuts")' not in block:return block
 points=[tuple(map(float,q)) for q in re.findall(r'\((?:start|end) ([-\d.]+) ([-\d.]+)\)',block)]
 if any(x in (36,264) or y in (100,132) for x,y in points):removed.append(block);return ''
 return block
s=re.sub(r'(?ms)^\t\((?:gr_line|gr_arc)\n.*?^\t\)\n',remove_outer,s)
assert len(removed)==8,'Expected the A3 outer outline; stop rather than alter an unknown design.'
def drawing(a,b,mid=None):
 kind='gr_arc' if mid else 'gr_line'
 geom=f'(start {a[0]} {a[1]}) '+(f'(mid {mid[0]} {mid[1]}) ' if mid else '')+f'(end {b[0]} {b[1]})'
 return f'\n\t({kind} {geom} (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))\n'
q=2/math.sqrt(2);edges=[]
for a,b in [((38,100),(262,100)),((264,102),(264,130)),((262,132),(38,132)),((36,130),(36,129)),((36,129),(35,129)),((35,121),(36,121)),((36,121),(36,114)),((36,114),(35,114)),((35,106),(36,106)),((36,106),(36,102))]:edges.append(drawing(a,b))
for a,m,b in [((262,100),(262+q,102-q),(264,102)),((264,130),(262+q,130+q),(262,132)),((38,132),(38-q,130+q),(36,130)),((36,102),(38-q,102-q),(38,100)),((35,129),(31,125),(35,121)),((35,114),(31,110),(35,106))]:edges.append(drawing(a,b,m))
s=s.rstrip();assert s.endswith(')');s=s[:-1]+''.join(edges)+')\n'
s=s.replace('OPEN CINEMA A3 / STRAIGHT REAR-TAIL SPEAKER CLIPS','OPEN CINEMA A4 / ALIGNMENT HOLES')
s=s.replace('REFERENCE FIXINGS x-115,z44/59 D3 / NO FRAME DRILLS','ALIGNMENT HOLES x-115,z44/59 D3 / PROVISIONAL')
s=s.replace('OPEN CINEMA / A3','OPEN CINEMA / A4')
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb') as tmp:
 tmp.write(s);tmp.flush();board=p.LoadBoard(tmp.name)
board.SetFileName(str(path))
v=lambda x,y:p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for i,z in enumerate([44,59],1):
 f=p.FOOTPRINT(board);f.SetFPID(p.LIB_ID('OpenCinema_Connectors','AlignmentHole_D3_Reference'))
 f.SetReference('REF**');f.SetValue('D3 ALIGNMENT ONLY');f.Reference().SetVisible(False);f.Value().SetVisible(False)
 f.SetLibDescription('D3 non-plated alignment reference hole; provisional mounting, no fastener selected.')
 f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES|p.FP_EXCLUDE_FROM_BOM)
 pad=p.PAD(f);pad.SetNumber('');pad.SetPosition(v(0,0));pad.SetSize(v(3,3));pad.SetDrillSize(v(3,3));pad.SetShape(p.PAD_SHAPE_CIRCLE);pad.SetAttribute(p.PAD_ATTRIB_NPTH);pad.SetLayerSet(p.PAD.PTHMask());f.Add(pad)
 if i==1:p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(project/'OpenCinema_Connectors.pretty'),f)
 f.SetReference('HREF'+str(i));f.SetPosition(v(35,169-z));board.Add(f)
p.SaveBoard(str(path),board)
cfg=json.loads((project/'placement.json').read_text());cfg['revision']='A4-alignment-holes'
cfg['board']['overall_width_including_alignment_tabs']=233
cfg['board']['alignment_tab_left_x']=-119
cfg['board']['outline_note']='228x32 body plus two left D-shaped R4 alignment tabs, centre x-115,z44/59; overall233x32'
cfg['reference_fixing_points']['status']='two actual D3 NPTH alignment holes; provisional mounting, no fastener chosen'
cfg['reference_fixing_points']['references']=['HREF1','HREF2']
cfg['reference_fixing_points']['alignment_tabs']={'radius':4,'leftmost_x':-119,'nominal_radial_material_around_hole':2.5}
(project/'placement.json').write_text(json.dumps(cfg,indent=2)+'\n')
pj=json.loads((project/'rear-io.kicad_pro').read_text());pj['text_variables']['REVISION']='A4-alignment-holes';(project/'rear-io.kicad_pro').write_text(json.dumps(pj,indent=2)+'\n')
print('Added two D3 alignment holes at x-115,z44/59, with R4 left tabs; connector geometry preserved.')
