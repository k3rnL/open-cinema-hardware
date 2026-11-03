#!/usr/bin/env python3
"""Explicit A2 fit revision. Keep manual changes safe: run only with --rebuild.
Preserves saved input footprints/child boards; rebuilds the carrier and drawings.
Speaker blocks are panel-mounted mechanical instances, not main-board pads.
"""
import ast,json,math,csv,sys
from pathlib import Path
import pcbnew as p
if '--rebuild' not in sys.argv:raise SystemExit('Explicit regeneration requires --rebuild; review manual edits first.')
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT/'boards/rear-io';LIB=PROJECT/'OpenCinema_Connectors.pretty'
tree=ast.parse((ROOT/'tools/generate_mechanical.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['v','shape','rounded','text']],type_ignores=[]),'<drawing helpers>','exec'))
source=p.LoadBoard(str(PROJECT/'rear-io.kicad_pcb'))
board=p.BOARD();board.SetFileName(str(PROJECT/'rear-io.kicad_pcb'))
board.GetDesignSettings().SetBoardThickness(p.FromMM(1.6))
board.GetDesignSettings().SetAuxOrigin(v(150,169))
board.GetDesignSettings().SetGridOrigin(v(150,112.5))
for original in source.GetFootprints():
 if original.GetReference() in ['J7','J8','J9','J10']:board.Add(original.Duplicate(False))
assert {f.GetReference() for f in board.GetFootprints()}=={'J7','J8','J9','J10'}
pos=lambda x,z:(150+x,169-z)
rounded(board,*pos(15,69),99,32,2,p.Edge_Cuts)
for x in [28,48]:rounded(board,*pos(x-8.5,64),17,24.1,.5,p.Edge_Cuts)
rounded(board,*pos(-105,74),210,35,5,p.Dwgs_User)
for z in [44,59]:
 cx,cy=pos(-110,z);shape(board,(cx,cy),(cx+1.5,cy),p.Dwgs_User,kind=p.SHAPE_T_CIRCLE)
text(board,'OPEN CINEMA A2 / MECHANICAL CANDIDATE',150,88,1.2,p.Dwgs_User)
text(board,'210 x 35 R5 / GROWN UPWARDS BY OWNER AGREEMENT',150,92,1.1,p.Dwgs_User)
text(board,'PANEL-MOUNT SPEAKER CLIPS / WIRES TO AMPLIFIER',100,139,1.1,p.Dwgs_User)
text(board,'NO MAIN-PCB SPEAKER PADS / CURRENT RATING UNCONFIRMED',100,142,1,p.Dwgs_User)
text(board,'2x D3 OWNER FIXING REFERENCES ONLY',150,146,1,p.Dwgs_User)
text(board,'A2 INPUT PCB / UNROUTED',217,102.5,1.05)
f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('OpenCinema_Connectors','KLS_WP_6P_03B_Panel_Assembly'))
f.SetValue('L-KLS1-WP-6P-03B-B/R');f.SetReference('REF**')
f.SetLibDescription('Panel-supported six-contact red/black clip block. Drawing V1 2025-09-19. Mechanical candidate; no main-PCB pads. Right-angle tails handwired provisionally; current rating unconfirmed.')
f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES)
f.Value().SetVisible(False);f.Reference().SetVisible(False)
shape(f,(-22.5,-15),(22.5,15),p.F_Fab,kind=p.SHAPE_T_RECT)
for x in [-22.5,22.5]:
 shape(f,(x,0),(x+3.5,0),p.F_Fab,kind=p.SHAPE_T_CIRCLE)
 shape(f,(x,0),(x+1.25,0),p.F_Fab,kind=p.SHAPE_T_CIRCLE)
shape(f,(-26.5,-15.5),(26.5,21),p.F_CrtYd,.05,kind=p.SHAPE_T_RECT)
for x in [-13,0,13]:
 for y in [-11,11]:shape(f,(x-4,y-4),(x+4,y+4),p.F_Fab,kind=p.SHAPE_T_RECT)
# Flange FRONT at 12.95 beyond PCB component seating plane. Provisional support plane.
m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/models/KLS1-WP-6P-03B.step';m.m_Offset=p.VECTOR3D(0,0,12.95);f.Add3DModel(m)
p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(LIB),f)
config=json.loads((PROJECT/'placement.json').read_text())
placements=[c for c in config['connectors'] if c['ref'] in ['J7','J8','J9','J10']]
for i,x in [(1,-77),(2,-21)]:
 f=p.FootprintLoad(str(LIB),'KLS_WP_6P_03B_Panel_Assembly');f.SetReference('SP'+str(i));f.SetPosition(v(*pos(x,56.5)));board.Add(f)
 text(board,'SPK '+('1 / 2 / 3' if i==1 else '4 / 5 / 6'),*pos(x,33.5),1,p.Dwgs_User)
 placements.insert(i-1,dict(ref='SP'+str(i),label='SPK '+('1–3' if i==1 else '4–6'),footprint='KLS_WP_6P_03B_Panel_Assembly',x=x,z=56.5,mpn='L-KLS1-WP-6P-03B-B/R',origin_x=x,origin_z=56.5))
for c in placements:
 if c['ref'].startswith('J'):text(board,c['label'],*pos(c['x'],38.5),.95)
p.SaveBoard(str(PROJECT/'rear-io.kicad_pcb'),board)
config.update(revision='A2-speaker-clip-fit',board={'width':99,'height':32,'thickness':1.6,'left_x':15,'right_x':114,'top_z':69,'bottom_z':37,'orientation':'vertical; F.Cu exterior; audio inputs only'},opening={'width':210,'height':35,'radius':5,'centre_z':56.5,'bottom_z':39,'top_z':74,'status':'owner permits taller opening; frame CAD not edited'},connectors=placements,speakers={'status':'mechanical candidate, not electrically qualified','mount':'connection plate, no attachment to input PCB','termination':'insulated handwired tails to amplifier proposed; retention and strain relief unresolved','flange_front_from_pcb_mm':12.95,'flange_back_from_pcb_mm':10.45,'main_pcb_pads':0,'current_rating':'not published in inspected drawing','colour_mapping':'illustrative black upper/red lower; confirm exact ordering'},circuit_status='no nets or tracks; input logic/LVDS/power deferred')
(PROJECT/'placement.json').write_text(json.dumps(config,indent=2)+'\n')
with (PROJECT/'connector-placement.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=placements[0].keys(),lineterminator='\n');w.writeheader();w.writerows(placements)
pj=json.loads((PROJECT/'rear-io.kicad_pro').read_text());pj['text_variables']['REVISION']='A2-speaker-clip-fit';(PROJECT/'rear-io.kicad_pro').write_text(json.dumps(pj,indent=2)+'\n')
print('A2: two 6-contact clips; 99x32 vertical input board; 210x35 opening')
