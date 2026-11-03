#!/usr/bin/env python3
"""Verify saved A6 support geometry, unchanged connector pads, and Fusion evidence."""
from pathlib import Path
import re,json,hashlib,ast
R=Path(__file__).resolve().parents[1];P=R/'boards/rear-io'
# Reuse parser helpers without executing historical checks or writing old reports.
t=ast.parse((R/'tools/check_connectors_A5.py').read_text())
exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ['parse','children','one']],type_ignores=[]),'<parser>','exec'))
def refs(board):return {next(x[2] for x in children(f,'property') if x[1]=='Reference'):f for f in children(board,'footprint')}
b=parse((P/'rear-io.kicad_pcb').read_text());fs=refs(b)
assert set(fs)=={'SP1','SP2','J7','J8','J9','J10','HREF1','HREF2','HREF3','HREF4','HOPT1','HOPT2','HOPT3','HOPT4','CRADLE1'}
assert not any(children(b,k) for k in ['segment','via','zone'])
baseline=json.loads((P/'exports/alignment-baseline-A3.json').read_text())
for ref in ['SP1','SP2','J9','J10']:
 assert hashlib.sha256(json.dumps(fs[ref],sort_keys=True).encode()).hexdigest()==baseline['footprint_sha256'][ref]
def checkhole(fs,ref,x,y,diam):
 f=fs[ref];assert list(map(float,one(f,'at')[1:3]))==[x,y]
 pad=one(f,'pad');assert pad[2]=='np_thru_hole' and float(one(pad,'drill')[1])==diam
for ref,x,z in [('HREF1',-115,44),('HREF2',-115,59),('HREF3',115,44),('HREF4',115,59)]:checkhole(fs,ref,150+x,169-z,3)
for ref,x,z in [('HOPT1',16,42),('HOPT2',16,62),('HOPT3',60,42),('HOPT4',60,62)]:checkhole(fs,ref,150+x,169-z,2.2)
for ref,x in [('J7',28),('J8',48)]:
 assert list(map(float,one(fs[ref],'at')[1:3]))==[150+x,118.5]
 assert not children(fs[ref],'pad')
 assert 'supported-A6.step' in one(fs[ref],'model')[1]
assert sum(len(children(f,'pad')) for f in fs.values())==53
for f in fs.values():
 for m in children(f,'model'):assert Path(m[1].replace('${KIPRJMOD}',str(P))).is_file()
child=parse((R/'boards/optical-input/optical-input.kicad_pcb').read_text());cf=refs(child)
assert set(cf)=={'J1','H1','H2'}
for ref,x in [('H1',95),('H2',105)]:checkhole(cf,ref,x,112,2.2)
assert len(children(cf['J1'],'pad'))==6
assert not any(children(child,k) for k in ['segment','via','zone'])
for f in [P/'exports/rear-io-A6-drc.json',R/'boards/optical-input/optical-input-A6-drc.json']:
 d=json.loads(f.read_text());assert not d['violations'] and not d['unconnected_items']
fusion=json.loads((P/'exports/fusion-integration-A6.json').read_text())
assert fusion['joint_test']['all_bodies_moved']==123 and not fusion['cradle_interferences']
assert fusion['alignment_holes_xz_mm']==[[-115,44],[-115,59],[115,44],[115,59]]
files=[P/'rear-io.kicad_pcb',R/'boards/optical-input/optical-input.kicad_pcb',P/'models/optical-cradle-A6.step',P/'models/optical-cradle-with-fasteners-A6.step',P/'models/optical-daughterboard-supported-A6.step',P/'exports/rear-io-A6-rigid.step',P/'exports/rear-io-A6-rigid.f3d']
report={'revision':'A6','sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'main_pads':53,'main_electrical_pads':41,'main_npth':12,'daughterboard_mounting_npth':2,'all_four_alignment_holes_retained':True,'speaker_rca_hdmi_footprints_unchanged_from_A3':True,'native_drc_main_and_child':'zero violations; no nets/circuit','fusion':fusion,'limitations':['prototype support; no load/thermal/tolerance/enclosure qualification','speaker exact supply/rating and footprint unresolved','no circuit, wiring or production release']}
(P/'exports/geometry-A6.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
