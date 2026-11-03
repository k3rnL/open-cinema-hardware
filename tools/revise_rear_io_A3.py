#!/usr/bin/env python3
"""Explicit A3 fit rebuild: straight rear-tail speaker blocks on vertical PCB.
Requires --rebuild. No circuitry. Footprint drill/pad choices are provisional.
"""
import ast,json,math,csv,sys
from pathlib import Path
import pcbnew as p
if '--historical-a3' not in sys.argv:raise SystemExit('Historical A3 rebuild would remove alignment holes. Use an isolated checkout with --historical-a3.')
if '--rebuild' not in sys.argv:raise SystemExit('Use --rebuild only after reviewing manual changes.')
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT/'boards/rear-io';LIB=PROJECT/'OpenCinema_Connectors.pretty'
tree=ast.parse((ROOT/'tools/generate_mechanical.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['v','shape','rounded','text']],type_ignores=[]),'<drawing helpers>','exec'))
source=p.LoadBoard(str(PROJECT/'rear-io.kicad_pcb'))
board=p.BOARD();board.SetFileName(str(PROJECT/'rear-io.kicad_pcb'))
board.GetDesignSettings().SetBoardThickness(p.FromMM(1.6))
board.GetDesignSettings().SetAuxOrigin(v(150,169));board.GetDesignSettings().SetGridOrigin(v(150,117))
for original in source.GetFootprints():
 if original.GetReference() in ['J7','J8','J9','J10']:board.Add(original.Duplicate(False))
assert {f.GetReference() for f in board.GetFootprints()}=={'J7','J8','J9','J10'}
pos=lambda x,z:(150+x,169-z)
rounded(board,*pos(-114,69),228,32,2,p.Edge_Cuts)
for x in [28,48]:rounded(board,*pos(x-8.5,64),17,24.1,.5,p.Edge_Cuts)
rounded(board,*pos(-110,69),220,35,5,p.Dwgs_User)
for z in [44,59]:
 cx,cy=pos(-115,z);shape(board,(cx,cy),(cx+1.5,cy),p.Dwgs_User,kind=p.SHAPE_T_CIRCLE)
text(board,'OPEN CINEMA A3 / STRAIGHT REAR-TAIL SPEAKER CLIPS',150,91,1.15,p.Dwgs_User)
text(board,'220 x 35 R5 / z34..69 / OWNER FRAME SNAPSHOT',150,95,1.05,p.Dwgs_User)
text(board,'REFERENCE FIXINGS x-115,z44/59 D3 / NO FRAME DRILLS',150,141,1,p.Dwgs_User)
text(board,'PT-603B: CURRENT AND FOOTPRINT QUALIFICATION PENDING',150,145,1,p.Dwgs_User)
text(board,'OPEN CINEMA / A3',92,102.3,1.1)
text(board,'INPUT PCB / UNROUTED',215,102.3,1)
f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('OpenCinema_Connectors','DragonCity_PT-603B_Straight'))
f.SetReference('REF**');f.SetValue('PT-603B');f.Value().SetVisible(False);f.Reference().SetVisible(False)
f.SetAttributes(p.FP_THROUGH_HOLE)
f.SetLibDescription('Dragon City PT-603B dwpt603b.pdf. Straight rear tails. 13 column/19.5 row spacing; project provisional D2.2 signal drills/D3.2 mounting clearances. Pin numbers project-defined, current unconfirmed. NOT fabrication-qualified.')
for row,y in enumerate([-9.75,9.75]):
 for col,x in enumerate([-13,0,13]):
  a=p.PAD(f);a.SetNumber(str(row*3+col+1));a.SetPosition(v(x,y));a.SetSize(v(3.6,3.6));a.SetDrillSize(v(2.2,2.2));a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetAttribute(p.PAD_ATTRIB_PTH);a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
for x in [-22.5,22.5]:
 a=p.PAD(f);a.SetPosition(v(x,0));a.SetNumber('');a.SetSize(v(3.2,3.2));a.SetDrillSize(v(3.2,3.2));a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetAttribute(p.PAD_ATTRIB_NPTH);a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
shape(f,(-22.5,-15),(22.5,15),p.F_Fab,kind=p.SHAPE_T_RECT)
shape(f,(-26.5,-15.5),(26.5,15.5),p.F_CrtYd,.05,kind=p.SHAPE_T_RECT)
for x in [-22.5,22.5]:shape(f,(x,0),(x+3.5,0),p.F_Fab,kind=p.SHAPE_T_CIRCLE)
for x in [-13,0,13]:
 for y in [-11,11]:shape(f,(x-4,y-4),(x+4,y+4),p.F_Fab,kind=p.SHAPE_T_RECT)
m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/models/DragonCity_PT-603B.step';m.m_Offset=p.VECTOR3D(0,0,0);f.Add3DModel(m)
p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(LIB),f)
config=json.loads((PROJECT/'placement.json').read_text());placements=[c for c in config['connectors'] if c['ref'] in ['J7','J8','J9','J10']]
for i,x in [(1,-77),(2,-21)]:
 f=p.FootprintLoad(str(LIB),'DragonCity_PT-603B_Straight');f.SetReference('SP'+str(i));f.SetPosition(v(*pos(x,52)));board.Add(f)
 placements.insert(i-1,dict(ref='SP'+str(i),label='SPK '+('1–3' if i==1 else '4–6'),footprint='DragonCity_PT-603B_Straight',x=x,z=52,mpn='Dragon City PT-603B',origin_x=x,origin_z=52))
for c in placements:text(board,c['label'],*pos(c['x'],38.5),.95)
p.SaveBoard(str(PROJECT/'rear-io.kicad_pcb'),board)
config.update(revision='A3-straight-speaker-clips',board={'width':228,'height':32,'thickness':1.6,'left_x':-114,'right_x':114,'top_z':69,'bottom_z':37,'orientation':'vertical; F.Cu exterior; straight speaker pins through board'},opening={'width':220,'height':35,'radius':5,'centre_z':51.5,'bottom_z':34,'top_z':69,'status':'measured read-only from updated owner Sketch3'},reference_fixing_points={'source':'2026-11-03 updated Rear Panel v4 Sketch3','diameter':3,'positions_xz':[[-115,44],[-115,59]],'status':'reference only; no frame fixing drills'},connectors=placements,speakers={'status':'mechanical candidate; procurement/current/production footprint unqualified','mount':'vertical PCB with component fixing holes reserved; panel load support not designed','main_pcb_signal_pads':12,'main_pcb_component_mounting_holes':4,'body_front_height':30,'tail_direction':'normal to rear face, into enclosure; no below-body extension','tail_projection_behind_pcb_seating_plane':3.4,'hole_pattern':'13mm column spacing,19.5mm row spacing; numbering project-defined','drills':'signal D2.2 project allowance, component fix D3.2 based on panel drawing; confirm before production','current_rating':'not published in inspected drawing','colour_mapping':'illustrative black upper/red lower; verify supplied variant'},circuit_status='no nets or tracks; input logic/LVDS/power and speaker harness deferred')
(PROJECT/'placement.json').write_text(json.dumps(config,indent=2)+'\n')
with (PROJECT/'connector-placement.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=placements[0].keys(),lineterminator='\n');w.writeheader();w.writerows(placements)
pj=json.loads((PROJECT/'rear-io.kicad_pro').read_text());pj['text_variables']['REVISION']='A3-straight-speaker-clips';(PROJECT/'rear-io.kicad_pro').write_text(json.dumps(pj,indent=2)+'\n')
print('A3:220x35 opening at z34..69; straight rear tails;228x32 vertical board')
