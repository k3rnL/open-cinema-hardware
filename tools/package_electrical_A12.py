#!/usr/bin/env python3
"""Export review BOM/CPL from the saved A12 board and manifest. Not an ordering action."""
import argparse,csv,json,hashlib,zipfile
from pathlib import Path
import pcbnew as p
a=argparse.ArgumentParser();a.add_argument('--board-dir',required=True);o=a.parse_args();d=Path(o.board_dir);out=d/'manufacturing-review';out.mkdir(exist_ok=True);b=p.LoadBoard(str(d/'rear-io-A12.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};m=json.loads((d/'design-manifest.json').read_text());parts=[q for q in m['parts'] if q['ref'] in fs and not q['ref'].startswith('#')]
known={'U7':'C179459','U1':'C17403532','U4':'C2860140','U6':'C2861750','U8':'C2868686','U9':'C55266','U10':'C138714','U11':'C138714','L1':'C503307','L2':'C503307','L3':'C503307','FB1':'C19330','J9':'C4992678','J10':'C428493'}
with (d/'bom-draft.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['ref','value','mpn','fp','dnp','source'])
 for q in parts:w.writerow([q.get(k,'') for k in ['ref','value','mpn','fp','dnp','source']])
with (out/'bom-all-review.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['Designator','Value','Manufacturer Part Number','Footprint','Populate','Assembly','Catalogue reference (not stock confirmation)','Source'])
 for q in parts:
  fp=fs[q['ref']];wire=q['ref'] in ['J31','J32'];smd=bool(fp.GetAttributes()&p.FP_SMD)
  w.writerow([q['ref'],q['value'],q['mpn'],q['fp'],'NO' if q.get('dnp') or wire else 'YES','wire solder termination' if wire else 'SMT' if smd else 'through-hole / manual',known.get(q['ref'],''),q.get('source','')])
with (out/'bom-smt-review.csv').open('w',newline='') as f, (out/'cpl-smt-review.csv').open('w',newline='') as c:
 w=csv.writer(f,lineterminator="\n");w.writerow(['Comment','Designator','Footprint','LCSC Part #','Manufacturer Part Number']);cw=csv.writer(c,lineterminator="\n");cw.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for q in parts:
  fp=fs[q['ref']]
  if not fp.GetAttributes()&p.FP_SMD or q.get('dnp'):continue
  w.writerow([q['value'],q['ref'],q['fp'],known.get(q['ref'],''),q['mpn']]);pos=fp.GetPosition();cw.writerow([q['ref'],f'{p.ToMM(pos.x)-150:.6f}mm',f'{100-p.ToMM(pos.y):.6f}mm','Top',f'{fp.GetOrientationDegrees()%360:.3f}'])
# A review archive includes the hold notice and layer data; never imply this places an order.
with zipfile.ZipFile(out/'rear-io-A12-gerbers-REVIEW-ONLY.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted((out/'gerbers').iterdir()):z.write(f,'gerbers/'+f.name)
 for n in ['README.md','stackup.md']:
  if (out/n).exists():z.write(out/n,n)
# Canonical source and exported-file hashes allow stale package detection.
files=list(d.glob('*.kicad_*'))+[f for f in (d/'exports').iterdir() if f.suffix in ['.step','.f3d','.pdf']]+[f for f in out.rglob('*') if f.is_file() and f.name!='SHA256SUMS']
files=[f for f in files if f.suffix!='.kicad_prl'];(out/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(d)}\n' for f in sorted(files)))
print(json.dumps({'physical_parts_including_wire_terminations':len(parts),'board_sha256':hashlib.sha256((d/'rear-io-A12.kicad_pcb').read_bytes()).hexdigest(),'release':'HOLD / REVIEW ONLY'}))
