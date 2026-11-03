"""Check the A8 mechanical PCB, actual pads, local models and matching export hashes."""
from pathlib import Path
import json,hashlib
import pcbnew as p
root=Path(__file__).resolve().parents[1];d=root/'boards/rear-io'
b=p.LoadBoard(str(d/'rear-io.kicad_pcb'));fps={f.GetReference():f for f in b.GetFootprints()}
assert set(fps)=={'SP1','SP2','J7','J8','J9','J10','H1','H2','H3','H4'}
assert len(b.GetTracks())==0 and len(b.Zones())==0
pads=[]
for ref,f in fps.items():
 for a in f.Pads():
  assert a.GetNetCode()==0
  x=150-p.ToMM(a.GetPosition().x);dep=p.ToMM(a.GetPosition().y)-100
  # Every pad center lies on the closed front-lip/rear rectangle footprint.
  assert .2<=dep<=40 and abs(x)<= (104 if dep<4 else 114),(ref,x,dep)
  pads.append({'ref':ref,'number':a.GetNumber(),'x':x,'depth':dep,'drill_mm':p.ToMM(a.GetDrillSize().x),'npth':a.GetAttribute()==p.PAD_ATTRIB_NPTH})
 for m in f.Models():
  path=Path(m.m_Filename.replace('${KIPRJMOD}',str(d)));assert path.is_file(),path
for ref in ['SP1','SP2']:
 a=list(fps[ref].Pads());assert len(a)==6 and all(abs(p.ToMM(q.GetDrillSize().x)-2.2)<1e-6 for q in a)
for ref in ['J7','J8']:assert len(list(fps[ref].Pads()))==6
drc=json.loads((d/'exports/rear-io-A8-drc.json').read_text());assert not drc['violations'] and not drc['unconnected_items']
report={'revision':'A8','footprints':len(fps),'electrical_pads':sum(not x['npth'] for x in pads),'npth':sum(x['npth'] for x in pads),'all_pad_centers_on_board':True,'all_models_resolved':True,'nets_assigned':0,'tracks':0,'drc_violations':0,'pads':pads,'sha256':{}}
for path in [d/'rear-io.kicad_pcb',d/'placement.json']+sorted((d/'exports').glob('*A8*.step')):
 report['sha256'][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()
(d/'exports/geometry-check-A8.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['pads','sha256']}))
