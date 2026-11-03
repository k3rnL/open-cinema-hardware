"""Verify single-component STEP, cradle clashes, and an alignment-hole rigid joint.
Run inside Fusion with CHECK_ROOT set to the hardware repository path.
Uses unsaved temporary documents and restores the owner's document.
"""
import adsk.core,adsk.fusion,json,math
from pathlib import Path

def verify():
 original=app.activeDocument;doc=None
 try:
  out=Path(CHECK_ROOT)/'boards/rear-io/exports'
  doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(str(out/'rear-io-A6-rigid.step')))
  d=adsk.fusion.Design.cast(app.activeProduct);r=d.rootComponent;bodies=list(r.bRepBodies)
  assert r.allOccurrences.count==0 and len(bodies)==123
  assert all(b.isSolid for b in bodies)
  cradle=next(b for b in bodies if abs(b.boundingBox.minPoint.x*10-12.99)<.05 and abs(b.boundingBox.maxPoint.x*10-63.01)<.05)
  coll=adsk.core.ObjectCollection.create();coll.add(cradle)
  for b in bodies:
   if b!=cradle and cradle.boundingBox.intersects(b.boundingBox):coll.add(b)
  inp=d.createInterferenceInput(coll);inp.areCoincidentFacesIncluded=False
  results=d.analyzeInterference(inp);pairs=[]
  for i in range(results.count):
   q=results.item(i)
   if q.entityOne==cradle or q.entityTwo==cradle:pairs.append({'a':q.entityOne.name,'b':q.entityTwo.name,'volume_mm3':q.interferenceBody.volume*1000})
  report={'revision':'A6','root_bodies':len(bodies),'child_occurrences':0,'all_solid':True,'cradle_body':cradle.name,'cradle_interferences':pairs,'scope':'support versus modeled connector assembly only, not enclosure/PSU'}
  (out/'cradle-interference-A6.json').write_text(json.dumps(report,indent=2)+'\n')
  assert not pairs,pairs
  # Put imported root bodies into one occurrence to simulate insertion in an assembly.
  d.designType=adsk.fusion.DesignTypes.DirectDesignType
  assy=r.occurrences.addNewComponent(adsk.core.Matrix3D.create());assy.component.name='Single component integration test'
  for b in bodies:assert b.copyToComponent(assy)
  for b in bodies:assert b.deleteMe()
  pcb=max(assy.bRepBodies,key=lambda b:b.boundingBox.maxPoint.x-b.boundingBox.minPoint.x)
  holes={}
  for edge in pcb.edges:
   circle=adsk.core.Circle3D.cast(edge.geometry)
   if circle and abs(circle.radius-.15)<1e-6:
    x,y,z=circle.center.x*10,circle.center.y*10,circle.center.z*10
    if abs(abs(x)-115)<.01 and any(abs(y-h)<.01 for h in [44,59]):holes[(round(x),round(y))]=edge
  assert set(holes)=={(-115,44),(-115,59),(115,44),(115,59)}
  report['alignment_holes_xz_mm']=sorted([list(p) for p in holes])
  fixture=r.occurrences.addNewComponent(adsk.core.Matrix3D.create());fixture.component.name='Temporary joint target'
  mgr=adsk.fusion.TemporaryBRepManager.get()
  # A ring whose hole is displaced from HREF1 by 10 mm horizontally / 5 mm vertically.
  p1=adsk.core.Point3D.create(-10.5,4.9,0);p2=adsk.core.Point3D.create(-10.5,4.9,-.2)
  ring=mgr.createCylinderOrCone(p1,.5,p2,.5);bore=mgr.createCylinderOrCone(p1,.15,p2,.15)
  assert mgr.booleanOperation(ring,bore,adsk.fusion.BooleanTypes.DifferenceBooleanType)
  fixture.component.bRepBodies.add(ring);fixture.isGrounded=True
  target=next(e for e in fixture.bRepBodies.item(0).edges if adsk.core.Circle3D.cast(e.geometry) and abs(adsk.core.Circle3D.cast(e.geometry).radius-.15)<1e-6)
  before=[b.vertices.item(0).geometry.copy() for b in assy.bRepBodies]
  g1=adsk.fusion.JointGeometry.createByCurve(holes[(-115,44)],adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
  g2=adsk.fusion.JointGeometry.createByCurve(target,adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
  assy.isGroundToParent=False;assy.isGrounded=False
  ji=r.joints.createInput(g1,g2);ji.setAsRigidJointMotion();joint=r.joints.add(ji);assert joint
  d.computeAll();adsk.doEvents();app.activeViewport.refresh()
  after=[b.vertices.item(0).geometry for b in assy.bRepBodies]
  changed=sum(a.distanceTo(b)>1e-6 for a,b in zip(before,after));assert changed==123,{'changed':changed,'transform':assy.transform2.asArray()}
  for a,b in zip(before,after):
   predicted=a.copy();predicted.transformBy(assy.transform2);assert predicted.distanceTo(b)<1e-5
  report['joint_test']={'type':'rigid','picked_feature':'HREF1 circular edge','all_bodies_moved':changed,'single_occurrence_transform_matches_all_body_vertices':True}
  (out/'fusion-integration-A6.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report))
 finally:
  if doc:doc.close(False)
  original.activate()
verify()
