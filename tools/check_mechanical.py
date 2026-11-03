#!/usr/bin/env python3
"""Check A0 geometry against the design parameters, not electrical function."""
import hashlib
import json
import math
from pathlib import Path
import pcbnew as p

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'boards/rear-io'
cfg=json.loads((PROJECT/'placement.json').read_text())
path=PROJECT/'rear-io.kicad_pcb'
b=p.LoadBoard(str(path))
fp={f.GetReference():f for f in b.GetFootprints()}
assert set(fp)=={'H1','H2','H3','H4'}|{f'J{i}' for i in range(1,11)}
assert len(list(b.GetTracks()))==0 and len(list(b.Zones()))==0
assert sum(len(list(f.Pads())) for f in fp.values())==4
assert abs(p.ToMM(b.GetDesignSettings().GetBoardThickness())-1.6)<1e-6
edges=[d for d in b.GetDrawings() if d.GetLayer()==p.Edge_Cuts]
assert len(edges)==8
ends={}
for e in edges:
    for q in (e.GetStart(),e.GetEnd()): ends[(q.x,q.y)]=ends.get((q.x,q.y),0)+1
assert len(ends)==8 and set(ends.values())=={2},'Outline must be one closed rounded rectangle'
xs=[xy[0] for xy in ends]; ys=[xy[1] for xy in ends]
assert abs(p.ToMM(max(xs)-min(xs))-228)<1e-6
assert abs(p.ToMM(max(ys)-min(ys))-32)<1e-6
ox,oy,top=150,100,69
def expected(x,z): return (ox+x,oy+top-z)
def match(f,xy):
    q=f.GetPosition()
    assert max(abs(p.ToMM(q.x)-xy[0]),abs(p.ToMM(q.y)-xy[1]))<1e-6

for i,(x,z) in enumerate(cfg['mounting_holes']['positions_xz'],1):
    f=fp[f'H{i}']; match(f,expected(x,z))
    pad=list(f.Pads())[0]
    assert pad.GetAttribute()==p.PAD_ATTRIB_NPTH
    assert abs(p.ToMM(pad.GetDrillSize().x)-3.2)<1e-6

def inside_opening(x,z):
    # Exact signed distance to rounded rectangle, margin checked at all corners.
    qx=abs(x)-(105-5)
    qy=abs(z-51.5)-(12.5-5)
    return math.hypot(max(qx,0),max(qy,0))+min(max(qx,qy),0)-5 < -0.01

boxes=[]
for c in cfg['connectors']:
    f=fp[c['ref']]; match(f,expected(c['x'],c['z']))
    assert not list(f.Pads())
    assert len(list(f.Models()))==1
    env=cfg['connector_envelopes'][c['type']]
    w,h=env['width'],env['height']
    for dx in (-w/2,w/2):
        for dz in (-h/2,h/2): assert inside_opening(c['x']+dx,c['z']+dz),c['ref']
    boxes.append((c['x']-w/2,c['z']-h/2,c['x']+w/2,c['z']+h/2))
for i,a in enumerate(boxes):
    for bb in boxes[i+1:]: assert a[2]<=bb[0] or bb[2]<=a[0] or a[3]<=bb[1] or bb[3]<=a[1]

report={'revision':cfg['revision'],'kicad_version':p.GetBuildVersion(),'pcb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':['228 x 32 mm closed outline','1.6 mm nominal thickness','10 padless connector envelopes at specified positions','6 speaker pairs and 4 audio inputs','all envelope face corners inside 210 x 25 R5 opening','no overlapping connector bodies in projection','4 proposed NPTH mounting holes, diameter 3.2 mm','no tracks or copper zones'],'limitations':'Connector dimensions, depth, mating access and complete enclosure fit are unverified. No electrical checks.'}
(PROJECT/'exports/geometry-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
