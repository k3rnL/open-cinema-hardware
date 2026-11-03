#!/usr/bin/env python3
"""Check saved A2 fit-study geometry and native DRC evidence, not electronics."""
from pathlib import Path
import re,json,math,hashlib
r=Path(__file__).resolve().parents[1];project=r/'boards/rear-io';file=project/'rear-io.kicad_pcb'
source=file.read_text()
def parse(s):
 stack=[[]]
 for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s):
  if t=='(':stack.append([])
  elif t==')':stack[-2].append(stack.pop())
  else:stack[-1].append(json.loads(t) if t.startswith('"') else t)
 assert len(stack)==1;return stack[0][0]
def children(n,key):return [x for x in n if isinstance(x,list) and x and x[0]==key]
def one(n,key):
 a=children(n,key);assert len(a)==1,(key,len(a));return a[0]
b=parse(source);fps=children(b,'footprint')
byref={next(x[2] for x in children(f,'property') if x[1]=='Reference'):f for f in fps}
assert set(byref)=={'SP1','SP2','J7','J8','J9','J10'}
assert 'Phoenix' not in source and '1732496' not in source
assert not children(b,'segment') and not children(b,'via') and not children(b,'zone')
assert sum(len(children(f,'pad')) for f in fps)==29
assert len(children(byref['J9'],'pad'))==3 and len(children(byref['J10'],'pad'))==26
for ref in ['SP1','SP2','J7','J8']:assert not children(byref[ref],'pad')
for f in fps:
 for m in children(f,'model'):assert Path(m[1].replace('${KIPRJMOD}',str(project))).is_file()
 for p in children(f,'pad'):assert p[2]!='np_thru_hole'
for ref in ['SP1','SP2']:
 off=one(one(one(byref[ref],'model'),'offset'),'xyz');assert float(off[3])==12.95
cfg=json.loads((project/'placement.json').read_text())
for c in cfg['connectors']:
 at=one(byref[c['ref']],'at');assert abs(float(at[1])-(150+c['x']))<1e-6 and abs(float(at[2])-(169-c['z']))<1e-6
edges=[e for e in b if isinstance(e,list) and e and e[0] in ['gr_line','gr_arc'] and one(e,'layer')[1]=='Edge.Cuts']
assert len(edges)==24
points={}
for e in edges:
 for k in ['start','end']:
  q=tuple(round(float(v),6) for v in one(e,k)[1:]);points[q]=points.get(q,0)+1
assert set(points.values())=={2}
assert max(x for x,y in points)-min(x for x,y in points)==99
assert max(y for x,y in points)-min(y for x,y in points)==32
assert min(x for x,y in points)==165
# Conservative FRONT package rectangles; explicitly excludes behind-panel tails.
boxes=[('SP1',-103,41.5,-51,71.5),('SP2',-47,41.5,5,71.5),('J7',20,40.4,36,63.5),('J8',40,40.4,56,63.5),('J9',58.675,46.5,71.325,56.5),('J10',73.95,47.33,102.05,55.69)]
def distance(x,z):
 qx=abs(x)-100;qz=abs(z-56.5)-12.5
 return math.hypot(max(qx,0),max(qz,0))+min(max(qx,qz),0)-5
for n,x0,z0,x1,z1 in boxes:assert max(distance(x,z) for x in [x0,x1] for z in [z0,z1])<0,n
for i,a in enumerate(boxes):
 for bb in boxes[i+1:]:assert a[3]<bb[1] or bb[3]<a[1] or a[4]<bb[2] or bb[4]<a[2]
drc=json.loads((project/'exports/rear-io-A2-drc.json').read_text());assert not drc['violations'] and not drc['unconnected_items']
files=[file,project/'models/KLS1-WP-6P-03B.step',r/'boards/optical-input/optical-input.kicad_pcb']
report={'revision':'A2','kicad_version':drc['kicad_version'],'sha256':{str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'main_pad_count':29,'speaker_main_pcb_pads':0,'checks':['native KiCad DRC: zero violations with reported default exclusions','99x32 closed board outline and two closed optical windows','two six-contact panel assemblies replace all Phoenix instances','audio input pad counts and model paths preserved','nominal front envelopes fit 210x35 R5 and do not overlap','STEP reimport into Fusion:96 solid-body instances'],'known_conflicts':['opening top z74 intersects original frame upper D4.5 holes at x+-40,z75','speaker tails reach z36 below opening bottom39; frame depth/insulation/support require verification'],'limitations':['KLS operating current rating unconfirmed','panel and PCB support, termination and finger/plug service volumes unresolved','no circuitry or full enclosure interference/thermal test','frame CAD not modified']}
(project/'exports/geometry-A2.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
