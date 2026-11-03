#!/usr/bin/env python3
"""Check A7 nominal geometry, source-relative models and recorded native evidence."""
from pathlib import Path
import ast,re,json,hashlib,math
R=Path(__file__).resolve().parents[1];P=R/'boards/rear-io'
t=ast.parse((R/'tools/check_connectors_A5.py').read_text())
exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ['parse','children','one']],type_ignores=[]),'<parser>','exec'))
def refs(b):return {next(x[2] for x in children(f,'property') if x[1]=='Reference'):f for f in children(b,'footprint')}
b=parse((P/'rear-io.kicad_pcb').read_text());fs=refs(b)
assert set(fs)=={'SP1','SP2','J7','J8','J9','J10','HREF1','HREF2','HREF3','HREF4','HOPT1','HOPT2','HOPT3','HOPT4','CRADLE1'}
assert not any(children(b,k) for k in ['segment','via','zone'])
def at(f):return list(map(float,one(f,'at')[1:3]))
for ref,x,z,dia in [('HREF1',-115,44,3),('HREF2',-115,59,3),('HREF3',115,44,3),('HREF4',115,59,3),('HOPT1',20,42,2.2),('HOPT2',20,62,2.2),('HOPT3',64,42,2.2),('HOPT4',64,62,2.2)]:
 f=fs[ref];assert at(f)==[150+x,169-z]
 a=one(f,'pad');assert a[2]=='np_thru_hole' and float(one(a,'drill')[1])==dia
for ref,x,z in [('SP1',-77,52),('SP2',-11,52),('J7',32,50.5),('J8',52,50.5),('J9',69,51.5),('J10',91,51.5)]:assert at(fs[ref])==[150+x,169-z]
for ref in ['SP1','SP2']:
 f=fs[ref];assert f[1]=='OpenCinema_Connectors:Cliff_FE6930_Straight'
 pads=children(f,'pad');assert len(pads)==10
 for row,y in enumerate([-9.3,9.3]):
  for col,x in enumerate([-19.5,-6.5,6.5,19.5]):
   pad=next(a for a in pads if a[1]==str(row*4+col+1))
   assert at(pad)==[x,y] and pad[2]=='thru_hole'
   assert one(pad,'drill')[1:]==['oval','2.2','3.2']
 assert sorted(at(a) for a in pads if a[2]=='np_thru_hole')==[[-29,0],[29,0]]
for ref in ['J7','J8']:assert not children(fs[ref],'pad')
assert sum(len(children(f,'pad')) for f in fs.values())==57
for f in fs.values():
 for m in children(f,'model'):assert Path(m[1].replace('${KIPRJMOD}',str(P))).is_file()
child=R/'boards/optical-input/optical-input.kicad_pcb'
old=json.loads((P/'exports/geometry-A6.json').read_text())
assert hashlib.sha256(child.read_bytes()).hexdigest()==old['sha256']['boards/optical-input/optical-input.kicad_pcb']
for f in [P/'exports/rear-io-A7-drc.json',R/'boards/optical-input/optical-input-A7-drc.json']:
 d=json.loads(f.read_text());assert not d['violations'] and not d['unconnected_items']
fusion=json.loads((P/'exports/fusion-integration-A7.json').read_text())
packing=json.loads((P/'exports/packing-A7.json').read_text())
assert fusion['joint_test']['all_bodies_moved']==135 and not fusion['cradle_interferences']
assert not packing['outside_opening'] and not packing['speaker_neighbor_interferences']
assert packing['f3d_reimport']['root_bodies']==135
assert fusion['alignment_holes_xz_mm']==[[-115,44],[-115,59],[115,44],[115,59]]
files=[P/'rear-io.kicad_pcb',P/'rear-io.kicad_pro',P/'placement.json',P/'OpenCinema_Connectors.pretty/Cliff_FE6930_Straight.kicad_mod',child,P/'models/Cliff_FE6930.step',P/'models/optical-cradle-with-fasteners-A6.step',P/'models/optical-daughterboard-supported-A6.step',P/'exports/rear-io-A7-assembly.step',P/'exports/rear-io-A7-rigid.step',P/'exports/rear-io-A7-rigid.f3d']
report={'revision':'A7','sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'main_pads':57,'main_electrical_pads':45,'main_npth':12,'all_four_alignment_holes_retained':True,'optical_child_source_unchanged_from_A6':True,'native_drc_main_and_child':'zero violations; no circuit','fusion':fusion,'packing':packing,'limitations':['0.5mm nominal left-ear margin and approximately0.4mm RCA/cradle gap require tolerance review','sample/slot/attachment qualification pending','no complete enclosure, load, thermal or electrical validation']}
(P/'exports/geometry-A7.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
