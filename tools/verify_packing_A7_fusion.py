"""A7 nominal opening fit, speaker-to-assembly clashes, and F3D structure.
Run inside Fusion with CHECK_ROOT. No owner document changes.
"""
import adsk.core,adsk.fusion,json
from pathlib import Path
def verify_packing():
 original=app.activeDocument;doc=None
 try:
  out=Path(CHECK_ROOT)/'boards/rear-io/exports'
  doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(str(out/'rear-io-A7-assembly.step')))
  d=adsk.fusion.Design.cast(app.activeProduct);r=d.rootComponent
  groups=[o for o in r.allOccurrences if o.bRepBodies.count]
  mgr=adsk.fusion.TemporaryBRepManager.get()
  def pt(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
  def box(x,y,z,w,h,t):return mgr.createBox(adsk.core.OrientedBoundingBox3D.create(pt(x,y,z),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,h/10,t/10))
  opening=box(0,51.5,5,210,35,70)
  assert mgr.booleanOperation(opening,box(0,51.5,5,220,25,70),adsk.fusion.BooleanTypes.UnionBooleanType)
  for x in [-105,105]:
   for y in [39,64]:
    disk=mgr.createCylinderOrCone(pt(x,y,-30),.5,pt(x,y,40),.5)
    assert mgr.booleanOperation(opening,disk,adsk.fusion.BooleanTypes.UnionBooleanType)
  fitted=[];outside=[];pairs=[];checks=0
  for o in groups:
   if 'PCB' in o.fullPathName or 'cradle' in o.fullPathName:continue
   for b in o.bRepBodies:
    copied=mgr.copy(b)
    assert copied.boundingBox.minPoint.distanceTo(b.boundingBox.minPoint)<.0001
    assert mgr.booleanOperation(copied,opening,adsk.fusion.BooleanTypes.DifferenceBooleanType)
    if copied.volume>1e-7:outside.append({'component':o.fullPathName,'body':b.name,'outside_volume_mm3':copied.volume*1000})
   fitted.append(o.fullPathName)
  for i,o in enumerate(groups):
   for other in groups[i+1:]:
    if 'Cliff_FE6930' not in o.fullPathName and 'Cliff_FE6930' not in other.fullPathName:continue
    if not o.boundingBox.intersects(other.boundingBox):continue
    for a in o.bRepBodies:
     for b in other.bRepBodies:
      if not a.boundingBox.intersects(b.boundingBox):continue
      coll=adsk.core.ObjectCollection.create();coll.add(a);coll.add(b)
      inp=d.createInterferenceInput(coll);inp.areCoincidentFacesIncluded=False
      result=d.analyzeInterference(inp);checks+=1
      for q in result:
       if q.interferenceBody.volume>1e-7:pairs.append({'a':o.fullPathName+'/'+a.name,'b':other.fullPathName+'/'+b.name,'volume_mm3':q.interferenceBody.volume*1000})
  report={'revision':'A7','opening':'220x35 R5, x+/-110,z34..69','opening_projection_components':fitted,'outside_opening':outside,'speaker_neighbor_interferences':pairs,'speaker_bbox_candidate_body_pairs_checked':checks,'minimum_nominal_speaker_ear_to_left_opening_mm':.5,'nominal_inter_speaker_ear_gap_mm':1,'scope':'Nominal solids/projection only; no plate setback, plug travel, manufacturing tolerances or enclosure/PSU fit.'}
  (out/'packing-A7.json').write_text(json.dumps(report,indent=2)+'\n')
  assert not outside and not pairs,report
  doc.close(False);doc=None
  doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(str(out/'rear-io-A7-rigid.f3d')))
  r=adsk.fusion.Design.cast(app.activeProduct).rootComponent
  assert r.bRepBodies.count==135 and r.allOccurrences.count==0 and all(b.isSolid for b in r.bRepBodies)
  report['f3d_reimport']={'root_bodies':r.bRepBodies.count,'child_occurrences':r.allOccurrences.count,'all_solid':True}
  (out/'packing-A7.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
 finally:
  if doc:doc.close(False)
  original.activate()
verify_packing()
