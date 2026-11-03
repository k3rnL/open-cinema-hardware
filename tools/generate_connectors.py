#!/usr/bin/env python3
"""Explicit A1 mechanical rebuild. Requires KiCad 10 pcbnew. Never run over unmerged edits.
Real pads; no circuit/net assignments. Optical receivers live on daughterboards.
"""
import sys
if '--rebuild-historical-a1' not in sys.argv:raise SystemExit('Historical A1 tool; use A2 tools. Explicit --rebuild-historical-a1 required.')
import ast, json, math, shutil, csv
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'boards/rear-io'; CHILD=ROOT/'boards/optical-input'
LIB=PROJECT/'OpenCinema_Connectors.pretty'; LIB.mkdir(exist_ok=True)
PLUGIN=p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP)
# Reuse only pure drawing helpers, never execute the obsolete A0 generator.
tree=ast.parse((ROOT/'tools/generate_mechanical.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['v','shape','rounded','text']],type_ignores=[]),'<drawing helpers>','exec'))
def footprint(name,desc):
 f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('OpenCinema_Connectors',name));f.SetReference('REF**');f.SetValue(name);f.SetLibDescription(desc)
 f.Value().SetVisible(False);f.Reference().SetVisible(False);return f

def pad(f,n,x,y,w,h,drill=None):
 a=p.PAD(f);a.SetNumber(str(n));a.SetPosition(v(x,y));a.SetSize(v(w,h))
 a.SetAttribute(p.PAD_ATTRIB_PTH if drill else p.PAD_ATTRIB_SMD)
 a.SetShape(p.PAD_SHAPE_CIRCLE if drill and w==h else p.PAD_SHAPE_RECT)
 if drill:a.SetDrillSize(v(drill,drill));a.SetLayerSet(p.PAD.PTHMask())
 else:a.SetLayerSet(p.PAD.SMDMask());a.SetLocalSolderMaskMargin(p.FromMM(.07))
 f.Add(a);return a

def npth(f,x,y,d):
 a=pad(f,'',x,y,d,d,d);a.SetAttribute(p.PAD_ATTRIB_NPTH);return a

def rect(f,x,y,w,h,layer=p.F_Fab,thick=.1):shape(f,(x,y),(x+w,y+h),layer,thick,kind=p.SHAPE_T_RECT)
def model(f,name,path='models/',off=(0,0,0)):
 m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/'+path+name+'.step';m.m_Offset=p.VECTOR3D(*off);f.Add3DModel(m)
def save(f):PLUGIN.FootprintSave(str(LIB),f)

# Phoenix library geometry with manufacturer-specified 1.2 mm finished drills.
base=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector_Phoenix_SPT.pretty')
f=p.FootprintLoad(str(base),'PhoenixContact_SPT_2.5_2-V-5.0-EX_1x02_P5.0mm_Vertical')
f.SetFPID(p.LIB_ID('OpenCinema_Connectors','Phoenix_1732496'));f.SetValue('1732496');f.Value().SetVisible(False);f.Reference().SetVisible(False)
f.SetLibDescription('Phoenix Contact 1732496 / SPT 2.5/2-V-5.0-EX; KiCad geometry, drill corrected to manufacturer 1.2 mm')
f.Models().clear();model(f,'1732496')
for a in f.Pads():a.SetDrillSize(v(1.2,1.2))
save(f)

f=footprint('SameSky_RCJ-021','RCJ-021 vertical RCA; Same Sky RCJ-02 drawing 2026-06-25 p2; signal=1, shell=2')
f.SetAttributes(p.FP_THROUGH_HOLE)
pad(f,1,0,-1.6,2.8,2.8,1.7)
for x in [-5.15,5.15]:pad(f,2,x,0,3.2,3.2,2)
shape(f,(0,0),(4.15,0),p.F_Fab,kind=p.SHAPE_T_CIRCLE)
rect(f,-6.325,-5,12.65,10);rect(f,-6.9,-5.5,13.8,11,p.F_CrtYd,.05)
model(f,'RCJ-021');save(f)

f=footprint('Amphenol_10078837-001LF','Vertical HDMI A; drawing 10078837 rev H sheets 1-5. 21 solder tails plus 5 shell stakes; no dust cover model.')
f.SetAttributes(p.FP_SMD)
# Top/component view: physical tail order 19,1..18,20,21.
order=[19]+list(range(1,19))+[20,21]
for i,n in enumerate(order):
 x=-5.21+i*.5
 if n==19:x-=.105
 if n==21:x+=.105
 pad(f,n,x,-2.5225,.49 if n in [19,21] else .28,3.325)
for x,y,d,w in [(-13.25,-2.5,1.5,2.7),(13.25,-2.5,1.5,2.7),(-7.25,0,1.3,2.5),(7.25,0,1.3,2.5),(0,3.3,1.3,2.5)]:pad(f,'SH',x,y,w,w,d)
rect(f,-14.05,-2.5,28.1,6.65);rect(f,-14.7,-4.8,29.4,9.8,p.F_CrtYd,.05)
model(f,'10078837-001LF');save(f)

f=footprint('Cliff_FCR684205R','Cliff ORJ5 receiver; drawing version 2.0 2023-06-29 pp3,7. Front/mouth toward -Y. Pin 1 at right in mating-face view.')
f.SetAttributes(p.FP_THROUGH_HOLE)
# Looking into the -Y-facing mouth reverses the PCB top-view X axis.
for n,x in [(1,-2.54),(2,0),(3,2.54)]:pad(f,n,x,0,1.5,1.5,.8)
for x,y in [(-4.6,2.1),(4.6,2.1),(0,-3.9)]:npth(f,x,y,2)
rect(f,-5.75,-8.5,11.5,12);rect(f,-4.75,-10.8,9.5,2.3)
rect(f,-6.25,-11.3,12.5,15.3,p.F_CrtYd,.05)
shape(f,(-3,-9.8),(3,-9.8),p.F_Fab)
model(f,'FCR684205R',path='../rear-io/models/');save(f)

f=footprint('Optical_Daughterboard_Assembly','Mechanical instance of separate optical-input PCB with FCR684205R. No direct solder pads on main board; wiring and support deferred.')
f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES)
rect(f,-8,-13,16,23.1);rect(f,-8.5,-13.5,17,24.1,p.F_CrtYd,.05)
# Model origins are relative to parent F.Cu seating surface.
model(f,'optical-daughterboard-assembly');save(f)

# The main vertical carrier.
board=p.BOARD();board.SetFileName(str(PROJECT/'rear-io.kicad_pcb'))
settings=board.GetDesignSettings();settings.SetBoardThickness(p.FromMM(1.6))
OX,OY,TOP=150,100,69
pos=lambda x,z:(OX+x,OY+TOP-z)
settings.SetAuxOrigin(v(*pos(0,0)));settings.SetGridOrigin(v(*pos(0,51.5)))
rounded(board,36,100,228,32,2,p.Edge_Cuts)
rounded(board,*pos(-105,64),210,25,5,p.Dwgs_User)
# Optical modules cross the main PCB plane. These are clearance windows, not mounting holes.
for x in [28,48]:rounded(board,*pos(x-8.5,64),17,24.1,.5,p.Edge_Cuts)
# User's Sketch3 fixing points: REFERENCE ONLY, deliberately no pads/drills.
for z in [44,59]:
 cx,cy=pos(-110,z);shape(board,(cx,cy),(cx+1.5,cy),p.Dwgs_User,kind=p.SHAPE_T_CIRCLE)
text(board,'2x D3 FRAME FIXING REFERENCES / NO PCB DRILLS',150,94,1.05,p.Dwgs_User)
text(board,'OPEN CINEMA / REAR I-O / A1',110,102.5,1.15)
text(board,'CONNECTOR FIT STUDY - UNROUTED',211,102.5,1.05)
text(board,'EXTERIOR REAR VIEW / 210 x 25 R5 OPENING',150,137,1.2,p.Dwgs_User)
text(board,'OPTICAL BOARDS PASS THROUGH TWO CLEARANCE WINDOWS',150,140,1.05,p.Dwgs_User)
placements=[]
def put(ref,label,name,x,z,mpn,foot_offset=(0,0)):
 f=p.FootprintLoad(str(LIB),name);f.SetReference(ref);f.SetValue(mpn);f.Value().SetVisible(False);f.Reference().SetVisible(False)
 f.SetPosition(v(*pos(x+foot_offset[0],z+foot_offset[1])));board.Add(f)
 text(board,label,*pos(x,38.5),.95)
 placements.append(dict(ref=ref,label=label,footprint=name,x=x,z=z,mpn=mpn,origin_x=x+foot_offset[0],origin_z=z+foot_offset[1]))
for i,x in enumerate([-88,-70,-52,-34,-16,2],1):put('J'+str(i),'SPK '+str(i),'Phoenix_1732496',x,51.5,'1732496',(-3.4,4))
for i,x in [(7,28),(8,48)]:put('J'+str(i),'OPT '+str(i-6),'Optical_Daughterboard_Assembly',x,50.5,'OC-OPTICAL-A1 / FCR684205R')
put('J9','COAX','SameSky_RCJ-021',65,51.5,'RCJ-021')
put('J10','HDMI','Amphenol_10078837-001LF',88,51.5,'10078837-001LF')
p.SaveBoard(str(PROJECT/'rear-io.kicad_pcb'),board)

child=p.BOARD();child.SetFileName(str(CHILD/'optical-input.kicad_pcb'));child.GetDesignSettings().SetBoardThickness(p.FromMM(1.6))
child.GetDesignSettings().SetAuxOrigin(v(100,100));rounded(child,92,91.5,16,24,.5,p.Edge_Cuts)
f=p.FootprintLoad(str(LIB),'Cliff_FCR684205R');f.SetReference('J1');f.SetValue('FCR684205R');f.SetPosition(v(100,100));child.Add(f)
text(child,'OPTICAL A1',100,108,.9);text(child,'UNROUTED',100,111,.8)
text(child,'1 OUT / 2 GND / 3 VCC',100,118,.8,p.Dwgs_User)
p.SaveBoard(str(CHILD/'optical-input.kicad_pcb'),child)
for folder,name in [(PROJECT,'rear-io'),(CHILD,'optical-input')]:
 (folder/(name+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':name+'.kicad_pro','version':1},'text_variables':{'REVISION':'A1-connector-fit'}},indent=2)+'\n')
 uri='${KIPRJMOD}/'+('' if folder==PROJECT else '../rear-io/')+'OpenCinema_Connectors.pretty'
 (folder/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "OpenCinema_Connectors")(type "KiCad")(uri "'+uri+'")(options "")(descr "A1 real connector footprints and optical assembly")))\n')
config={'revision':'A1-connector-fit','units':'mm','board':{'width':228,'height':32,'thickness':1.6,'top_z':69,'bottom_z':37,'orientation':'vertical; F.Cu exterior'},'opening':{'width':210,'height':25,'radius':5,'centre_z':51.5},'reference_fixing_points':{'source':'Rear Panel v4 Sketch3','diameter':3,'positions_xz':[[-110,44],[-110,59]],'status':'reference only, no drill'},'optical_clearance_windows':{'centres_x':[28,48],'bottom_z':39.9,'top_z':64,'width':17,'radius':.5},'daughterboard':{'width':16,'depth':24,'thickness':1.6,'pcb_top_z':44.5,'mounting':'undecided; physically supported independently of main PCB','connection':'deferred; no interboard header selected'},'connectors':placements,'circuit_status':'no nets or tracks, logic/LVDS/power deferred'}
(PROJECT/'placement.json').write_text(json.dumps(config,indent=2)+'\n')
with (PROJECT/'connector-placement.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=placements[0].keys());w.writeheader();w.writerows(placements)
print('Generated A1 main PCB and optical daughterboard')
