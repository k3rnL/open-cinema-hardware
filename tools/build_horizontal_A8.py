#!/usr/bin/env python3
"""Explicit horizontal A8 fit-study rebuild. Requires KiCad Python; --apply required.
KiCad F.Cu is the connector side; installed assembly turns that side downward.
"""
import sys,ast,json,csv,shutil
from pathlib import Path
if '--apply' not in sys.argv:raise SystemExit('Use --apply only in a clean/staged checkout.')
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'boards/rear-io';LIB=D/'OpenCinema_Connectors.pretty'
tree=ast.parse((ROOT/'tools/generate_mechanical.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['v','shape','rounded','text']],type_ignores=[]),'<helpers>','exec'))
plugin=p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP)
def fp(name,desc):
 f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('OpenCinema_Connectors',name));f.SetReference('REF**');f.SetValue(name);f.Reference().SetVisible(False);f.Value().SetVisible(False);f.SetLibDescription(desc);f.SetAttributes(p.FP_THROUGH_HOLE);return f
def pad(f,n,x,y,diam,drill,np=False):
 a=p.PAD(f);a.SetNumber(str(n));a.SetPosition(v(x,y));a.SetSize(v(diam,diam));a.SetDrillSize(v(drill,drill));a.SetAttribute(p.PAD_ATTRIB_NPTH if np else p.PAD_ATTRIB_PTH);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
def rect(f,x,y,w,h,layer=p.F_Fab):shape(f,(x,y),(x+w,y+h),layer,.1,kind=p.SHAPE_T_RECT)
def model(f,name):
 f.Models().clear();m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/models/'+name+'.step';f.Add3DModel(m)
def save(f):plugin.FootprintSave(str(LIB),f)
f=fp('KLS1_WP_6P_03B_Horizontal_A8','KLS V1 2025-09-19: 13mm column pitch, row depths3.8/8.8 behind flange front, six D2.2 holes. CURRENT RATING UNVERIFIED. Numbering is project-defined.')
for col,x in enumerate([-13,0,13]):
 for row,y in enumerate([3.8,8.8]):pad(f,col*2+row+1,x,y,3.4,2.2)
rect(f,-26,-11.4,52,20.9);rect(f,-26.5,-11.9,53,22.4,p.F_CrtYd)
model(f,'KLS1-WP-6P-03B_horizontal_A8');save(f)
f=fp('SameSky_RCJ_011_Horizontal_A8','Same Sky RCJ-01 drawing 2026-08-12 p2: D1.7 signal, three D2.6 shell holes, 10mm shell pitch and4.5mm offset. Body shoulder Y-4; mating face Y-12.')
pad(f,1,0,0,2.7,1.7)
for x,y in [(-5,0),(5,0),(0,-4.5)]:pad(f,2,x,y,3.6,2.6)
rect(f,-5.5,-4,11,6.5);rect(f,-4.15,-12,8.3,8);rect(f,-7,-12.5,14,15.5,p.F_CrtYd)
model(f,'RCJ-011_A8');save(f)
f=p.FootprintLoad(str(LIB),'Cliff_FCR684205R');model(f,'FCR684205R');save(f)
native=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')
hdmi='HDMI_A_Amphenol_10029449-x01xLF_Horizontal'
shutil.copy2(native/'3dmodels/Connector_Video.3dshapes'/(hdmi+'.step'),D/'models'/(hdmi+'.step'))
f=p.FootprintLoad(str(native/'footprints/Connector_Video.pretty'),hdmi)
f.SetFPID(p.LIB_ID('OpenCinema_Connectors',hdmi));f.Reference().SetVisible(False);f.Value().SetVisible(False);model(f,hdmi);save(f)
f=fp('MountingHole_D3_Reference_A8','D3 reference PCB mounting hole. Hardware not finalized.');pad(f,'',0,0,3,3,True);save(f)
b=p.BOARD();b.SetFileName(str(D/'rear-io.kicad_pcb'));b.GetDesignSettings().SetBoardThickness(p.FromMM(1.6));b.GetDesignSettings().SetAuxOrigin(v(150,100))
pos=lambda x,depth:(150-x,100+depth)
# Front lip is narrow enough to clear the rounded opening; wider rear allows support holes.
outline=[(-104,0.2),(104,0.2),(104,4),(114,4),(114,40),(-114,40),(-114,4),(-104,4)]
for a,c in zip(outline,outline[1:]+outline[:1]):shape(b,pos(*a),pos(*c),p.Edge_Cuts)
placements=[]
def put(ref,label,name,x,depth,mpn,angle=0):
 f=p.FootprintLoad(str(LIB),name);f.SetReference(ref);f.SetValue(mpn);f.SetOrientationDegrees(angle);f.SetPosition(v(*pos(x,depth)));b.Add(f)
 placements.append(dict(ref=ref,label=label,footprint=name,rear_x=x,depth=depth,angle=angle,mpn=mpn))
for ref,x in [('SP1',-75),('SP2',-18)]:put(ref,'3 speaker pairs - candidate','KLS1_WP_6P_03B_Horizontal_A8',x,0,'L-KLS1-WP-6P-03B-B/R')
for ref,x in [('J7',25),('J8',44)]:put(ref,'Optical','Cliff_FCR684205R',x,9,'FCR684205R')
put('J9','Coax','SameSky_RCJ_011_Horizontal_A8',64,7,'RCJ-011')
# The KiCad library HDMI mouth faces +Y on the footprint, so rotate 180 degrees.
put('J10','HDMI','HDMI_A_Amphenol_10029449-x01xLF_Horizontal',89,2.7,'10029449-001RLF',180)
for i,(x,dep) in enumerate([(-110,12),(-110,30),(110,12),(110,30)],1):put('H'+str(i),'PCB mounting reference','MountingHole_D3_Reference_A8',x,dep,'D3 reference')
text(b,'OPEN CINEMA A8 / HORIZONTAL FIT STUDY',150,126,1.2)
text(b,'CONNECTORS FACE DOWN WHEN INSTALLED',150,129,1.0)
text(b,'SPEAKER CURRENT RATING UNVERIFIED / UNROUTED',150,133,1.0)
text(b,'PLATE INNER FACE: DEPTH 0 / PCB FRONT EDGE 0.2 mm',150,93,1.1,p.Dwgs_User)
text(b,'ENCLOSURE: CONNECTOR SEATING z67; PCB ABOVE; solder tails point upward',150,145,1.1,p.Dwgs_User)
p.SaveBoard(str(D/'rear-io.kicad_pcb'),b)
(D/'rear-io.kicad_pro').write_text(json.dumps({'meta':{'filename':'rear-io.kicad_pro','version':1},'text_variables':{'REVISION':'A8-horizontal-fit-CANDIDATE'}},indent=2)+'\n')
config={'revision':'A8-horizontal-fit','status':'mechanical experiment; speaker current rating and exact purchasing route unverified','units':'mm','board':{'width':228,'depth':39.8,'front_edge_setback':0.2,'thickness':1.6,'connector_seating_height':67,'orientation':'horizontal, connector side downward'},'datum':{'inner_connection_plate_y':0,'assumed_plate_thickness':1.5,'frame_outer_plane_in_enclosure_y':102,'native_step_transform':'X=-Xraw,Y=Yraw,Z=68.595-Zraw; maps F.Cu seating surface to z67'},'opening':{'width':220,'height':35,'radius':5,'bottom_z':34,'top_z':69},'psu_top_z':35,'alignment_holes':{'diameter':3,'positions_xz':[[-115,44],[-115,59],[115,44],[115,59]],'location':'two provisional support brackets; retained vertical axes'},'connectors':placements,'circuit_status':'no nets, tracks, or decoding; eight spare contacts not needed: six speaker pairs total'}
(D/'placement.json').write_text(json.dumps(config,indent=2)+'\n')
with (D/'connector-placement.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=placements[0].keys());w.writeheader();w.writerows(placements)
print('A8 horizontal board written; six pairs, all directly soldered; no daughterboards')
