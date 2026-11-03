"""Horizontal A8 enclosure integration. Run in Fusion with ROOT.
Output axes: X exterior rear view, Y outward (plate inner face0), Z enclosure height.
Never edits the owner's enclosure. Includes provisional support/connection plate.
"""
import adsk.core,adsk.fusion,pathlib,json,math
def build():
 app=adsk.core.Application.get();original=app.activeDocument;doc=None
 out=pathlib.Path(ROOT)/'boards/rear-io/exports'
 try:
  doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(str(out/'rear-io-A8-assembly.step')))
  d=adsk.fusion.Design.cast(app.activeProduct);d.designType=adsk.fusion.DesignTypes.DirectDesignType;r=d.rootComponent
  mgr=adsk.fusion.TemporaryBRepManager.get()
  matrix=adsk.core.Matrix3D.create();matrix.setWithArray([-1,0,0,0,0,1,0,0,0,0,-1,6.8595,0,0,0,1])
  entries=[]
  for occ in r.allOccurrences:
   for body in occ.bRepBodies:entries.append((occ.fullPathName,body))
  for name,body in entries:
   cp=mgr.copy(body);mgr.transform(cp,matrix);ob=r.bRepBodies.add(cp);ob.name=name+' / '+body.name;ob.appearance=body.appearance
  for occ in list(r.occurrences):occ.deleteMe()
  assert r.occurrences.count==0
  # Export correctly oriented board/connectors before adding supports.
  assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/'rear-io-A8-board-rigid.step'),r))
  def pt(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
  def box(x,y,z,w,dep,h):return mgr.createBox(adsk.core.OrientedBoundingBox3D.create(pt(x,y,z),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,dep/10,h/10))
  def cyl(x,y,z,rad,length,axis):return mgr.createCylinderOrCone(pt(x,y,z),rad/10,pt(x,y+(length if axis=='y' else 0),z+(length if axis=='z' else 0)),rad/10)
  def cut(a,b):assert mgr.booleanOperation(a,b,adsk.fusion.BooleanTypes.DifferenceBooleanType);return a
  def union(a,b):assert mgr.booleanOperation(a,b,adsk.fusion.BooleanTypes.UnionBooleanType);return a
  def add(b,name):ob=r.bRepBodies.add(b);ob.name=name;return ob
  plate=box(0,.75,52.5,238,1.5,39)
  for x in [-115,115]:
   for z in [44,59]:plate=cut(plate,cyl(x,-.1,z,1.5,1.7,'y'))
  for x in [-75,-18]:
   plate=cut(plate,box(x,.75,52,38.5,1.7,30.6))
   for xx in [x-22.5,x+22.5]:plate=cut(plate,cyl(xx,-.1,52,1.25,1.7,'y'))
  for x in [25,44]:plate=cut(plate,box(x,.75,60.1,10,1.7,10.5))
  # RCA is recessed3mm behind inner face; opening must admit the mating plug.
  plate=cut(plate,box(64,.75,60.4,14,1.7,14))
  plate=cut(plate,box(89,.75,63.95,16.5,1.7,7.5))
  pb=add(plate,'A8 PROVISIONAL connection plate 1.5mm - cable-fit test required')
  for x in [-115,115]:
   br=box(x,-3,53.5,8,2,27)
   br=union(br,box((1 if x>0 else -1)*113,-18,66,12,32,2))
   for z in [44,59]:br=cut(br,cyl(x,-4.1,z,1.5,2.2,'y'))
   for dep in [12,30]:br=cut(br,cyl((1 if x>0 else -1)*110,-dep,64.9,1.5,2.2,'z'))
   add(br,'A8 PROVISIONAL bracket '+('left' if x<0 else 'right')+' - D3 reference holes')
  assert all(b.isSolid for b in r.bRepBodies)
  report={'revision':'A8','root_bodies':r.bRepBodies.count,'child_occurrences':0,'all_solid':True,'datums_mm':{'plate_inner_y':0,'plate_outer_y':1.5,'pcb_connector_seating_z':67,'enclosure_translation_y':102},'alignment_holes_xz':[[-115,44],[-115,59],[115,44],[115,59]],'support_status':'provisional geometry, not engineered mounting hardware','parts':[]}
  for b in r.bRepBodies:
   bb=b.boundingBox;report['parts'].append({'name':b.name,'min_mm':[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],'max_mm':[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10]})
  assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/'rear-io-A8-rigid.step'),r))
  assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(out/'rear-io-A8-rigid.f3d')))
  # Export the provisional plate separately for later owner editing.
  tmp=r.occurrences.addNewComponent(adsk.core.Matrix3D.create());pb.copyToComponent(tmp)
  assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/'rear-io-A8-connection-plate.step'),tmp.component));tmp.deleteMe()
  (out/'geometry-A8.json').write_text(json.dumps(report,indent=2)+'\n')
  # Reproducible front and oblique previews in installed orientation.
  for name,eye,up in [('installed-front',(0,40,5.4),(0,0,1)),('installed-oblique',(24,25,24),(0,0,1))]:
   cam=app.activeViewport.camera;cam.isPerspective=False;cam.eye=adsk.core.Point3D.create(*eye);cam.target=adsk.core.Point3D.create(0,-1.3,5.4);cam.upVector=adsk.core.Vector3D.create(*up);cam.isFitView=True;app.activeViewport.camera=cam;app.activeViewport.fit();adsk.doEvents();app.activeViewport.saveAsImageFile(str(out/('rear-io-A8-'+name+'.png')),2200,900)
  print(json.dumps({k:v for k,v in report.items() if k!='parts'}))
 finally:
  if doc:doc.close(False)
  original.activate()
build()
