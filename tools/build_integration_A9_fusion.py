"""A9 PCB-and-connectors export; owner designs the plate and brackets.
Run in Fusion with ROOT set to this repository. Uses the unchanged A8 KiCad
assembly export, flattens it and applies the same installed orientation.
"""
import adsk.core, adsk.fusion, pathlib, json, hashlib

def build():
 app=adsk.core.Application.get(); original=app.activeDocument; doc=None
 root=pathlib.Path(ROOT); out=root/'boards/rear-io/exports'
 def signature(r):
  return sorted([round(b.volume,8),*[round(v,6) for v in (b.boundingBox.minPoint.x,b.boundingBox.minPoint.y,b.boundingBox.minPoint.z,b.boundingBox.maxPoint.x,b.boundingBox.maxPoint.y,b.boundingBox.maxPoint.z)]] for b in r.bRepBodies)
 try:
  doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(str(out/'rear-io-A8-assembly.step')))
  d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'));d.designType=adsk.fusion.DesignTypes.DirectDesignType;r=d.rootComponent
  mgr=adsk.fusion.TemporaryBRepManager.get();matrix=adsk.core.Matrix3D.create()
  matrix.setWithArray([-1,0,0,0,0,1,0,0,0,0,-1,6.8595,0,0,0,1])
  entries=[(occ.fullPathName,b) for occ in r.allOccurrences for b in occ.bRepBodies]
  for name,b in entries:
   cp=mgr.copy(b);mgr.transform(cp,matrix);ob=r.bRepBodies.add(cp);ob.name=name+' / '+b.name;ob.appearance=b.appearance
  for occ in list(r.occurrences):occ.deleteMe()
  assert r.bRepBodies.count==67 and r.occurrences.count==0
  assert all(b.isSolid for b in r.bRepBodies)
  expected=signature(r)
  assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/'rear-io-A9-rigid.step'),r))
  assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(out/'rear-io-A9-rigid.f3d')))
  for name,eye in [('installed-front',(0,40,5.4)),('installed-oblique',(24,25,24))]:
   cam=app.activeViewport.camera;cam.isPerspective=False;cam.eye=adsk.core.Point3D.create(*eye);cam.target=adsk.core.Point3D.create(0,-1.3,5.4);cam.upVector=adsk.core.Vector3D.create(0,0,1);cam.isFitView=True
   app.activeViewport.camera=cam;app.activeViewport.fit();adsk.doEvents()
   assert app.activeViewport.saveAsImageFile(str(out/('rear-io-A9-'+name+'.png')),1800,800)
  report={'revision':'A9 integration export; PCB remains A8','root_bodies':67,'child_occurrences':0,'all_solid':True,'backplate_bodies':0,'bracket_bodies':0,'pcb_holes_mm':{'diameter':3,'x':[-110,110],'inward_depth':[12,30]},'reimports':[],'pcb_sha256':hashlib.sha256((root/'boards/rear-io/rear-io.kicad_pcb').read_bytes()).hexdigest()}
  for filename in ['rear-io-A8-board-rigid.step','rear-io-A9-rigid.step','rear-io-A9-rigid.f3d']:
   opts=app.importManager.createFusionArchiveImportOptions(str(out/filename)) if filename.endswith('.f3d') else app.importManager.createSTEPImportOptions(str(out/filename))
   tmp=app.importManager.importToNewDocument(opts);td=adsk.fusion.Design.cast(tmp.products.itemByProductType('DesignProductType'));rr=td.rootComponent
   assert rr.bRepBodies.count==67 and rr.occurrences.count==0 and all(b.isSolid for b in rr.bRepBodies)
   assert signature(rr)==expected,filename
   report['reimports'].append({'file':filename,'bodies':67,'children':0,'geometry_matches':True})
   tmp.close(False)
  (out/'geometry-check-A9.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report))
 finally:
  if doc:doc.close(False)
  original.activate()
build()
