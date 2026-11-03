#!/usr/bin/env python3
"""Check saved A3 fit-study geometry and native DRC evidence, not electronics."""
from pathlib import Path
import re,json,math,hashlib,sys
if '--historical-a3' not in sys.argv:raise SystemExit('Historical A3 checker. Use check_connectors_A4.py for the current model.')
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
assert sum(len(children(f,'pad')) for f in fps)==45
assert len(children(byref['J9'],'pad'))==3 and len(children(byref['J10'],'pad'))==26
for ref in ['J7','J8']:assert not children(byref[ref],'pad')
for ref in ['SP1','SP2']:
 pads=children(byref[ref],'pad');assert len(pads)==8
 sig=[p for p in pads if p[2]=='thru_hole'];assert len(sig)==6
 assert {(float(one(p,'at')[1]),float(one(p,'at')[2])) for p in sig}=={(x,y) for x in [-13,0,13] for y in [-9.75,9.75]}
 assert all(float(one(p,'drill')[1])==2.2 for p in sig)
 assert sum(p[2]=='np_thru_hole' for p in pads)==2
for f in fps:
 for m in children(f,'model'):assert Path(m[1].replace('${KIPRJMOD}',str(project))).is_file()

for ref in ['SP1','SP2']:
 off=one(one(one(byref[ref],'model'),'offset'),'xyz');assert float(off[3])==0
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
assert max(x for x,y in points)-min(x for x,y in points)==228
assert max(y for x,y in points)-min(y for x,y in points)==32
assert min(x for x,y in points)==36
# Conservative FRONT package rectangles; explicitly excludes behind-panel tails.
boxes=[('SP1',-103,37,-51,67),('SP2',-47,37,5,67),('J7',20,40.4,36,63.5),('J8',40,40.4,56,63.5),('J9',58.675,46.5,71.325,56.5),('J10',73.95,47.33,102.05,55.69)]
def distance(x,z):
 qx=abs(x)-105;qz=abs(z-51.5)-12.5
 return math.hypot(max(qx,0),max(qz,0))+min(max(qx,qz),0)-5
for n,x0,z0,x1,z1 in boxes:assert max(distance(x,z) for x in [x0,x1] for z in [z0,z1])<0,n
for i,a in enumerate(boxes):
 for bb in boxes[i+1:]:assert a[3]<bb[1] or bb[3]<a[1] or a[4]<bb[2] or bb[4]<a[2]
drc=json.loads((project/'exports/rear-io-A3-drc.json').read_text());assert not drc['violations'] and not drc['unconnected_items']
files=[file,project/'models/DragonCity_PT-603B.step',r/'boards/optical-input/optical-input.kicad_pcb']
model=json.loads((project/'models/speaker-model-geometry-A3.json').read_text())
assert model['min_mm'][1]>-15.03 and model['max_mm'][1]<15.03
assert abs(model['min_mm'][2]+3.4)<.03
frame=json.loads((r/'mechanical/reference/rear-panel-220x35-sketch3.json').read_text())
assert {tuple(c['centre'][:2]) for c in frame['circles'] if abs(c['radius']-1.5)<1e-5}=={(-115,44),(-115,59)}
fusion=json.loads((project/'exports/fusion-import-A3.json').read_text());assert fusion['all_solid']
report={'revision':'A3','kicad_version':drc['kicad_version'],'sha256':{str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'electrical_pads':41,'component_mounting_npth':4,'speaker_pads':12,'checks':['native KiCad DRC zero violations under recorded defaults','228x32 closed board and two closed optical windows','two straight-tail six-contact footprints; no A1/A2 speaker instances','13x19.5 speaker pin grid and model positions match','speaker model height30; rear tails3.4; no below-body tail extension','front envelopes fit measured 220x35 R5 opening without overlap','updated owner fixing references x-115,z44/59 preserved','project-relative model paths resolve'],'step_import':fusion,'limitations':['signal drill diameter, pin thickness/numbering, ear envelope and component mounting clearance are project assumptions','manufacturer current rating and small-quantity supply unconfirmed','4mm board-bottom to old PSU-top in projection is not full clearance validation','support, harness, plate stack, electrical and thermal qualification deferred']}
(project/'exports/geometry-A3.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
