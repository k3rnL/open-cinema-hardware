"""Import a KiCad STEP and flatten it to one Fusion component for enclosure joints.
Run in Fusion with SOURCE_STEP, OUTPUT_PREFIX. Original STEP and user document stay unchanged.
"""
import adsk.core,adsk.fusion,pathlib,json

def build_rigid_integration():
 app=adsk.core.Application.get();original=app.activeDocument;doc=None
 try:
  doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(SOURCE_STEP))
  design=adsk.fusion.Design.cast(app.activeProduct);design.designType=adsk.fusion.DesignTypes.DirectDesignType
  root=design.rootComponent
  entries=[]
  for occ in root.allOccurrences:
   for body in occ.bRepBodies:entries.append((occ.fullPathName,body))
  original_count=len(entries)+root.bRepBodies.count
  # Copy occurrence proxies to root; the API preserves their assembly-space locations.
  copies=[]
  for name,body in entries:
   oldbb=body.boundingBox;copied=body.copyToComponent(root);assert copied
   copied.name=name.replace(':','_').replace('+',' / ')+' / '+body.name
   newbb=copied.boundingBox
   assert oldbb.minPoint.distanceTo(newbb.minPoint)<.0001 and oldbb.maxPoint.distanceTo(newbb.maxPoint)<.0001
   copies.append(copied)
  for occ in list(root.occurrences):assert occ.deleteMe()
  assert root.occurrences.count==0 and root.bRepBodies.count==original_count
  assert all(body.isSolid for body in root.bRepBodies)
  prefix=pathlib.Path(OUTPUT_PREFIX);prefix.parent.mkdir(parents=True,exist_ok=True)
  assert design.exportManager.execute(design.exportManager.createSTEPExportOptions(str(prefix)+'.step',root))
  assert design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(str(prefix)+'.f3d'))
  report={'source':pathlib.Path(SOURCE_STEP).name,'body_count':original_count,'root_bodies':root.bRepBodies.count,'child_occurrences':0,'all_solid':True,'copy_bounding_boxes_preserved':True,'purpose':'single rigid component for enclosure alignment; mechanical geometry unchanged'}
  pathlib.Path(str(prefix)+'-verification.json').write_text(json.dumps(report,indent=2)+'\n')
  return report
 finally:
  if doc:doc.close(False)
  if original:original.activate()
build_rigid_integration()
