#!/usr/bin/env python3
"""One-time A6 -> A7 migration. Preserves outline/alignment holes, replaces speakers.
Run with KiCad pcbnew Python and --apply in a reviewed checkout. No circuitry.
"""
import ast,csv,json,math,sys
from pathlib import Path
import pcbnew as p
if '--apply' not in sys.argv:raise SystemExit('Use --apply after reviewing manual changes.')
R=Path(__file__).resolve().parents[1];P=R/'boards/rear-io';L=P/'OpenCinema_Connectors.pretty'
cfg=json.loads((P/'placement.json').read_text());assert cfg['revision']=='A6-supported-optics'
tree=ast.parse((R/'tools/generate_mechanical.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['v','shape','rounded','text']],type_ignores=[]),'<helpers>','exec'))
b=p.LoadBoard(str(P/'rear-io.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
pos=lambda x,z:v(150+x,169-z)
f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('OpenCinema_Connectors','Cliff_FE6930_Straight'))
f.SetReference('REF**');f.SetValue('FE6930');f.Reference().SetVisible(False);f.Value().SetVisible(False);f.SetAttributes(p.FP_THROUGH_HOLE)
f.SetLibDescription('Cliff FE6930 issue2. 13mm columns;18.6+/-1mm rows. Project-derived plated slots2.2x3.2; fixing D3.2/pitch58. NOT vendor land pattern, physical sample qualification required.')
for row,y in enumerate([-9.3,9.3]):
 for col,x in enumerate([-19.5,-6.5,6.5,19.5]):
  a=p.PAD(f);a.SetNumber(str(row*4+col+1));a.SetPosition(v(x,y));a.SetSize(v(3.6,4.6));a.SetDrillSize(v(2.2,3.2));a.SetDrillShape(p.PAD_DRILL_SHAPE_OBLONG);a.SetShape(p.PAD_SHAPE_OVAL);a.SetAttribute(p.PAD_ATTRIB_PTH);a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
for x in [-29,29]:
 a=p.PAD(f);a.SetPosition(v(x,0));a.SetNumber('');a.SetSize(v(3.2,3.2));a.SetDrillSize(v(3.2,3.2));a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetAttribute(p.PAD_ATTRIB_NPTH);a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
shape(f,(-29,-15),(29,15),p.F_Fab,kind=p.SHAPE_T_RECT)
for x in [-29,29]:shape(f,(x,0),(x+3.5,0),p.F_Fab,kind=p.SHAPE_T_CIRCLE)
# Follow the flange plus its central ears rather than an oversized65x30 rectangle.
outline=[(-29.5,-15.5),(29.5,-15.5),(29.5,-4),(33,-4),(33,4),(29.5,4),(29.5,15.5),(-29.5,15.5),(-29.5,4),(-33,4),(-33,-4),(-29.5,-4)]
for a,bb in zip(outline,outline[1:]+outline[:1]):shape(f,a,bb,p.F_CrtYd,.05)
for x in [-19.5,-6.5,6.5,19.5]:
 for y in [-10,10]:shape(f,(x-3.5,y-3.5),(x+3.5,y+3.5),p.F_Fab,kind=p.SHAPE_T_RECT)
m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/models/Cliff_FE6930.step';f.Add3DModel(m)
p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(L),f)
for ref,x in [('SP1',-77),('SP2',-11)]:
 b.Remove(fs[ref]);nf=p.FootprintLoad(str(L),'Cliff_FE6930_Straight');nf.SetFPID(p.LIB_ID('OpenCinema_Connectors','Cliff_FE6930_Straight'));nf.SetReference(ref);nf.SetPosition(pos(x,52));b.Add(nf)
# Shift existing inputs/support as complete footprints; library pad geometry unchanged.
for ref,dx in [('J7',4),('J8',4),('J9',4),('J10',3),('CRADLE1',4),('HOPT1',4),('HOPT2',4),('HOPT3',4),('HOPT4',4)]:fs[ref].Move(v(dx,0))
for sh in list(b.GetDrawings()):
 if sh.GetLayer()==p.Edge_Cuts:
  # Only the two internal optical windows occupy this narrow x range.
  bb=sh.GetBoundingBox();x=p.ToMM(bb.GetCenter().x)
  if 168<x<208:sh.Move(v(4,0))
 elif isinstance(sh,p.PCB_TEXT):b.Remove(sh)
text(b,'OPEN CINEMA A7 / CLIFF FE6930 / 6 SPEAKER PAIRS + 2 SPARES',150,91,1.15,p.Dwgs_User)
text(b,'220 x 35 R5 / z34..69 / FOUR D3 ALIGNMENT HOLES RETAINED',150,95,1,p.Dwgs_User)
text(b,'MECHANICAL FIT STUDY / SAMPLE AND FOOTPRINT QUALIFICATION REQUIRED',150,145,1,p.Dwgs_User)
text(b,'OPEN CINEMA / A7',85,102.2,1)
text(b,'UNROUTED / NO CIRCUIT',235,102.2,1)
newxs={'SP1':-77,'SP2':-11,'J7':32,'J8':52,'J9':69,'J10':91}
for c in cfg['connectors']:
 c['x']=c['origin_x']=newxs[c['ref']]
 if c['ref'].startswith('SP'):
  c.update(footprint='Cliff_FE6930_Straight',mpn='Cliff FE6930',label='SPK 1-4' if c['ref']=='SP1' else 'SPK 5-6 + SPARES')
 else:text(b,c['label'],150+c['x'],130.5,.95)
for x,label in [(-90,'1 / 3'),(-64,'2 / 4'),(-24,'5 / SPARE1'),(2,'6 / SPARE2')]:text(b,label,150+x,129.8,.85)
p.SaveBoard(str(P/'rear-io.kicad_pcb'),b)
cfg['revision']='A7-Cliff-FE6930-eight-pairs'
cfg['optical_clearance_windows']['centres_x']=[32,52]
cfg['speakers']={'status':'owner accepted FE6930; nominal fit model; production qualification pending','quantity':2,'contacts_per_block':8,'working_pairs':6,'spare_pairs':2,'mount':'straight rear solder tags through vertical PCB; four component fixing holes reserved','main_pcb_signal_pads':16,'main_pcb_component_mounting_holes':4,'overall_width_per_block':65,'flange_width':58,'body_front_height':30,'tail_direction':'normal to rear face; no downward extension','tail_projection_behind_pcb_seating_plane':3.5,'hole_pattern':'13mm column pitch,18.6+/-1mm row spacing; numbering follows front-view drawing','drills':'provisional plated slots2.2x3.2; pads3.6x4.6; component fixing D3.2, pitch58','current_rating':'manufacturer7 A at60 V AC','colour_mapping':'R B B R in each row; pair contacts1+/2-,4+/3-,5+/6-,8+/7-','pair_assignment':{'SP1':['1/2 = channel1','4/3 = channel2','5/6 = channel3','8/7 = channel4'],'SP2':['1/2 = channel5','4/3 = channel6','5/6 = spare1','8/7 = spare2']},'electrical_status':'no nets; all16 contacts independent; spare assignment provisional'}
for k in ['main_holes_xz','receiver_lug_centres_xz']:
 for pair in cfg['optical_support'][k]:pair[0]+=4
cfg['optical_support']['translation_from_A6_mm']=[4,0,0]
(P/'placement.json').write_text(json.dumps(cfg,indent=2)+'\n')
with (P/'connector-placement.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=cfg['connectors'][0].keys(),lineterminator='\n');w.writeheader();w.writerows(cfg['connectors'])
pj=json.loads((P/'rear-io.kicad_pro').read_text());pj['text_variables']['REVISION']=cfg['revision'];(P/'rear-io.kicad_pro').write_text(json.dumps(pj,indent=2)+'\n')
print('A7 saved: FE6930x2,16 contacts; windows/optics/cradle/RCA +4mm, HDMI +3mm; owner holes preserved')
