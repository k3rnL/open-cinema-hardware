"""Verify A8 installed STEP against read-only copies of current Home Cinema frame/PSU.
Also verify every body moves with one reference-hole joint. ROOT required.
"""
import adsk.core,adsk.fusion,pathlib,json
def verify():
 app=adsk.core.Application.get();original=app.activeDocument;doc=None
 out=pathlib.Path(ROOT)/'boards/rear-io/exports';mgr=adsk.fusion.TemporaryBRepManager.get()
 try:
  home=next(doc for doc in app.documents if doc.dataFile and doc.dataFile.name=='Home Cinema')
  hr=adsk.fusion.Design.cast(home.products.itemByProductType('DesignProductType')).rootComponent
  context=[];mat=adsk.core.Matrix3D.create();mat.translation=adsk.core.Vector3D.create(0,-10.2,0)
  for occ in hr.allOccurrences:
   if occ.component.name.startswith('Mean Well UHP-500') or (occ.component.name.startswith('Rear Panel v5') and 'rear-io' not in occ.fullPathName):
    for b in occ.bRepBodies:
     cp=mgr.copy(b);mgr.transform(cp,mat);context.append((occ.fullPathName,cp))
  assert len(context)==2,[n for n,b in context]
  doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(str(out/'rear-io-A8-rigid.step')))
  d=adsk.fusion.Design.cast(app.activeProduct);d.designType=adsk.fusion.DesignTypes.DirectDesignType;r=d.rootComponent;bodies=list(r.bRepBodies)
  assert r.allOccurrences.count==0 and len(bodies)==70
  for b in bodies:
   bb=b.boundingBox;w=(bb.maxPoint.x-bb.minPoint.x)*10;dep=(bb.maxPoint.y-bb.minPoint.y)*10
   if abs(w-238)<.05 and abs(dep-1.5)<.05:b.name='A8 PROVISIONAL connection plate'
   if abs(w-12)<.05 and abs(dep-32)<.05:b.name='A8 PROVISIONAL bracket'
  ctx=[]
  for name,cp in context:
   b=r.bRepBodies.add(cp);b.name='CONTEXT '+name;ctx.append(b)
  collection=adsk.core.ObjectCollection.create()
  for b in bodies+ctx:collection.add(b)
  inp=d.createInterferenceInput(collection);inp.areCoincidentFacesIncluded=False
  hits=d.analyzeInterference(inp);clashes=[]
  for i in range(hits.count):
   q=hits.item(i);a,b=q.entityOne,q.entityTwo
   # Within-connector cosmetic overlaps are expected for reconstructed multi-body models.
   if any('CONTEXT ' in x.name or 'PROVISIONAL' in x.name for x in [a,b]):
    if q.interferenceBody.volume*1000>1e-5:clashes.append({'a':a.name,'b':b.name,'volume_mm3':q.interferenceBody.volume*1000})
  psu=next(b for b in ctx if 'Mean Well' in b.name)
  distances=[]
  for b in bodies:
   result=app.measureManager.measureMinimumDistance(psu,b)
   distances.append((result.value*10,b.name))
  psbb=psu.boundingBox
  report={'revision':'A8','root_bodies':70,'child_occurrences':0,'all_solid':all(b.isSolid for b in bodies),'context':'read-only copies from '+home.name+'; no enclosure changes','psu_bbox_mm':{'min':[psbb.minPoint.x*10,psbb.minPoint.y*10,psbb.minPoint.z*10],'max':[psbb.maxPoint.x*10,psbb.maxPoint.y*10,psbb.maxPoint.z*10]},'support_plate_frame_psu_interferences':clashes,'minimum_psu_clearance_mm':min(distances)[0],'nearest_body':min(distances)[1],'lid_height_assumption_mm':80,'max_assembly_z_mm':max(b.boundingBox.maxPoint.z*10 for b in bodies),'limitations':['Nominal reconstructed bodies, not tolerance/thermal qualification','External cable mating bodies not modeled','KLS speaker current rating unverified']}
  (out/'fusion-integration-A8.json').write_text(json.dumps(report,indent=2)+'\n')
  assert not clashes,clashes
  # Context preview only, not part of integration assembly.
  cam=app.activeViewport.camera;cam.isPerspective=False;cam.eye=adsk.core.Point3D.create(24,30,18);cam.target=adsk.core.Point3D.create(0,-3,4);cam.upVector=adsk.core.Vector3D.create(0,0,1);cam.isFitView=True;app.activeViewport.camera=cam;app.activeViewport.fit();adsk.doEvents();app.activeViewport.saveAsImageFile(str(out/'rear-io-A8-context.png'),2200,1200)
  for b in ctx:b.deleteMe()
  d.designType=adsk.fusion.DesignTypes.DirectDesignType
  assy=r.occurrences.addNewComponent(adsk.core.Matrix3D.create());assy.component.name='A8 whole assembly'
  for b in bodies:assert b.copyToComponent(assy)
  for b in bodies:b.deleteMe()
  plate=next(b for b in assy.bRepBodies if 'connection plate' in b.name)
  holes={}
  for e in plate.edges:
   c=adsk.core.Circle3D.cast(e.geometry)
   if c and abs(c.radius-.15)<1e-6:
    x,z=c.center.x*10,c.center.z*10
    if abs(abs(x)-115)<.01 and any(abs(z-h)<.01 for h in [44,59]):holes[(round(x),round(z))]=e
  assert set(holes)=={(-115,44),(-115,59),(115,44),(115,59)}
  fixture=r.occurrences.addNewComponent(adsk.core.Matrix3D.create());fixture.component.name='Temporary alignment target'
  a=adsk.core.Point3D.create(-10.5,.5,4.9);b=adsk.core.Point3D.create(-10.5,.7,4.9)
  ring=mgr.createCylinderOrCone(a,.5,b,.5);bore=mgr.createCylinderOrCone(a,.15,b,.15);assert mgr.booleanOperation(ring,bore,adsk.fusion.BooleanTypes.DifferenceBooleanType)
  fixture.component.bRepBodies.add(ring);fixture.isGrounded=True
  target=next(e for e in fixture.bRepBodies.item(0).edges if adsk.core.Circle3D.cast(e.geometry) and abs(adsk.core.Circle3D.cast(e.geometry).radius-.15)<1e-6)
  before=[b.vertices.item(0).geometry.copy() for b in assy.bRepBodies]
  g1=adsk.fusion.JointGeometry.createByCurve(holes[(-115,44)],adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
  g2=adsk.fusion.JointGeometry.createByCurve(target,adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
  assy.isGroundToParent=False;assy.isGrounded=False;ji=r.joints.createInput(g1,g2);ji.setAsRigidJointMotion();assert r.joints.add(ji)
  d.computeAll();adsk.doEvents()
  after=[b.vertices.item(0).geometry for b in assy.bRepBodies]
  changed=sum(a.distanceTo(b)>1e-6 for a,b in zip(before,after));assert changed==70
  for a,b in zip(before,after):
   expected=a.copy();expected.transformBy(assy.transform2);assert expected.distanceTo(b)<1e-5
  report['alignment_holes_xz']=sorted([list(x) for x in holes]);report['rigid_joint_all_bodies_moved']=changed
  (out/'fusion-integration-A8.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report))
 finally:
  if doc:doc.close(False)
  original.activate()
verify()
