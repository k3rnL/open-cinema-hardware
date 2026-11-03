#!/usr/bin/env python3
"""Inspect saved A1 boards and project-relative models. Does not rebuild or verify electronics."""
import sys
if '--check-historical-a1' not in sys.argv:raise SystemExit('Historical A1 tool; use A2 tools. Explicit --check-historical-a1 required.')
import hashlib,json,math
from pathlib import Path
import pcbnew as p
r=Path(__file__).resolve().parents[1]; project=r/'boards/rear-io'
cfg=json.loads((project/'placement.json').read_text());b=p.LoadBoard(str(project/'rear-io.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
assert set(fps)=={f'J{i}' for i in range(1,11)}
assert len(list(b.GetTracks()))==len(list(b.Zones()))==0
assert abs(p.ToMM(b.GetDesignSettings().GetBoardThickness())-1.6)<1e-6
edges=[d for d in b.GetDrawings() if d.GetLayer()==p.Edge_Cuts];assert len(edges)==24
ends={}
for e in edges:
 for q in (e.GetStart(),e.GetEnd()):ends[(q.x,q.y)]=ends.get((q.x,q.y),0)+1
assert set(ends.values())=={2},'Every outline/window endpoint must join exactly two edges'
assert round(p.ToMM(max(q[0] for q in ends)-min(q[0] for q in ends)),4)==228
assert round(p.ToMM(max(q[1] for q in ends)-min(q[1] for q in ends)),4)==32
# Check manufacturer hole pattern, not merely total footprint count.
for i in range(1,7):
 pads=list(fps[f'J{i}'].Pads());assert len(pads)==4
 assert sorted(a.GetNumber() for a in pads)==['1','1','2','2']
 assert all(abs(p.ToMM(a.GetDrillSize().x)-1.2)<1e-6 for a in pads)
assert len(list(fps['J9'].Pads()))==3
hdmi=list(fps['J10'].Pads());assert len(hdmi)==26
assert {a.GetNumber() for a in hdmi if a.GetNumber()!='SH'}=={str(i) for i in range(1,22)}
assert sum(a.GetNumber()=='SH' for a in hdmi)==5
assert not list(fps['J7'].Pads()) and not list(fps['J8'].Pads())
for c in cfg['connectors']:
 f=fps[c['ref']];q=f.GetPosition()
 assert abs(p.ToMM(q.x)-(150+c['origin_x']))<1e-6 and abs(p.ToMM(q.y)-(169-c['origin_z']))<1e-6
 assert len(list(f.Models()))==1
 for m in f.Models():assert Path(m.m_Filename.replace('${KIPRJMOD}',str(project))).is_file()
 for a in f.Pads():assert a.GetNetCode()==0 and a.GetAttribute()!=p.PAD_ATTRIB_NPTH
# Independent projected bounds from package drawings (conservative clip width for RCA).
boxes=[]
for i,x in enumerate([-88,-70,-52,-34,-16,2],1):boxes.append((f'J{i}',x-5.7,44.75,x+5.7,58.25))
boxes.extend([('J7',20,40.4,36,63.5),('J8',40,40.4,56,63.5),('J9',58.675,46.5,71.325,56.5),('J10',73.95,47.33,102.05,55.69)])
def distance(x,z):
 qx=abs(x)-100;qz=abs(z-51.5)-7.5
 return math.hypot(max(qx,0),max(qz,0))+min(max(qx,qz),0)-5
for name,x0,z0,x1,z1 in boxes:
 assert max(distance(x,z) for x in (x0,x1) for z in (z0,z1))<0,name
for i,a in enumerate(boxes):
 for bb in boxes[i+1:]:assert a[3]<bb[1] or bb[3]<a[1] or a[4]<bb[2] or bb[4]<a[2]
childdir=r/'boards/optical-input';child=p.LoadBoard(str(childdir/'optical-input.kicad_pcb'));cf=list(child.GetFootprints());assert len(cf)==1
pads=list(cf[0].Pads());assert len(pads)==6
assert sorted(a.GetNumber() for a in pads if a.GetAttribute()==p.PAD_ATTRIB_PTH)==['1','2','3']
assert sum(a.GetAttribute()==p.PAD_ATTRIB_NPTH for a in pads)==3
assert len(list(child.GetTracks()))==len(list(child.Zones()))==0
for m in cf[0].Models():assert Path(m.m_Filename.replace('${KIPRJMOD}',str(childdir))).is_file()
for path in [project/'exports/rear-io-A1-drc.json',childdir/'optical-input-A1-drc.json']:
 drc=json.loads(path.read_text());assert not drc['violations'] and not drc['unconnected_items']
report={'revision':'A1','kicad_version':p.GetBuildVersion(),'sha256':{str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [project/'rear-io.kicad_pcb',childdir/'optical-input.kicad_pcb']},'main_pad_count':53,'child_pad_count':6,'checks':['228 x 32 board; closed outer perimeter and two windows','six two-pole terminals, RCA and HDMI have real pads','two separate optical assemblies; receiver pads on child board','project-relative models resolve','no mounting drills added at owner reference points','nominal drawing envelopes fit within rounded opening and do not overlap','native DRC reports zero violations on both saved boards'],'limitations':['No nets/tracks or circuit connectivity validation','Nominal projected fit only; no plug/tool access, tolerance stack or full enclosure interference test','Daughterboard supports/interconnect and plate setback undecided']}
(project/'exports/geometry-A1.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
