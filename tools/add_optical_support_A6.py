#!/usr/bin/env python3
"""Add A6 support holes/models to A5 saved boards; no electrical changes."""
from pathlib import Path
import json
import pcbnew as p
R=Path(__file__).resolve().parents[1]; main=R/'boards/rear-io'; child=R/'boards/optical-input'
def v(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def hole(board,ref,x,y):
 f=p.FOOTPRINT(board);f.SetReference(ref);f.SetValue('M2 clearance / support');f.SetFPID(p.LIB_ID('','M2_support'))
 f.Reference().SetVisible(False);f.Value().SetVisible(False);f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
 a=p.PAD(f);a.SetAttribute(p.PAD_ATTRIB_NPTH);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetSize(v(2.2,2.2));a.SetDrillSize(v(2.2,2.2));a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
 f.SetPosition(v(x,y));board.Add(f)
b=p.LoadBoard(str(main/'rear-io.kicad_pcb'))
assert not any(f.GetReference()=='CRADLE1' for f in b.GetFootprints()),'A6 already applied'
for i,(x,z) in enumerate([(16,42),(16,62),(60,42),(60,62)],1):hole(b,'HOPT'+str(i),150+x,169-z)
for f in b.GetFootprints():
 if f.GetReference() in ['J7','J8']:
  f.SetValue('OC-OPTICAL-A6 / FCR684205R');f.Models().clear();m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/models/optical-daughterboard-supported-A6.step';f.Add3DModel(m)
f=p.FOOTPRINT(b);f.SetReference('CRADLE1');f.SetValue('OC-OPTICAL-CRADLE-A6');f.Reference().SetVisible(False);f.Value().SetVisible(False)
f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES);f.SetPosition(v(188,117.5))
m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/models/optical-cradle-with-fasteners-A6.step';m.m_Offset=p.VECTOR3D(-38,-51.5,0);f.Add3DModel(m);b.Add(f)
for d in b.GetDrawings():
 if isinstance(d,p.PCB_TEXT) and '/ A5' in d.GetText():d.SetText(d.GetText().replace('/ A5','/ A6'))
p.SaveBoard(str(main/'rear-io.kicad_pcb'),b)
b=p.LoadBoard(str(child/'optical-input.kicad_pcb'))
for ref,x in [('H1',95),('H2',105)]:hole(b,ref,x,112)
for d in b.GetDrawings():
 if isinstance(d,p.PCB_TEXT) and d.GetText()=='OPTICAL A1':d.SetText('OPTICAL A6')
p.SaveBoard(str(child/'optical-input.kicad_pcb'),b)
cfg=json.loads((main/'placement.json').read_text());cfg['revision']='A6-supported-optics'
cfg['daughterboard']['mounting']='two M2 screws per board; shared insulating cradle; receiver mounting lugs also bolted to cradle'
cfg['daughterboard']['mounting_holes_local_xy']=[[-5,12],[5,12]]
cfg['optical_support']={'reference':'OC-OPTICAL-CRADLE-A6','status':'modeled prototype proposal; JLC3DP PA12 quotation and thermal/load tests pending','main_holes_xz':[[16,42],[16,62],[60,42],[60,62]],'main_drills':2.2,'printed_clearance_drills':2.4,'minimum_z':39.0,'maximum_inward_depth_from_main_front':16.85,'receiver_lug_centres_xz':[[28,60.5],[48,60.5]],'sourcing':'custom part separate from JLCPCB PCBA; fasteners separate JLCMC sourcing pending'}
for c in cfg['connectors']:
 if c['ref'] in ['J7','J8']:c['mpn']='OC-OPTICAL-A6 / FCR684205R'
(main/'placement.json').write_text(json.dumps(cfg,indent=2)+'\n')
print('A6 support holes and model references added; connectors retained')
