"""A8 drawing-derived horizontal models. Run in Fusion with ROOT supplied.
Connector seating plane Z0, front towards +Y. Unsaved temporary documents only.
"""
import adsk.core, adsk.fusion, pathlib, json
def build():
 app=adsk.core.Application.get();original=app.activeDocument
 rootpath=pathlib.Path(ROOT);out=rootpath/'boards/rear-io/models'
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
 try:
  d=adsk.fusion.Design.cast(app.activeProduct);d.designType=adsk.fusion.DesignTypes.DirectDesignType
  root=d.rootComponent;mgr=adsk.fusion.TemporaryBRepManager.get()
  def pt(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
  def box(x,y,z,w,dep,h):return mgr.createBox(adsk.core.OrientedBoundingBox3D.create(pt(x,y,z),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,dep/10,h/10))
  def cyl(x,y,z,r,length,axis='z'):return mgr.createCylinderOrCone(pt(x,y,z),r/10,pt(x,y+(length if axis=='y' else 0),z+(length if axis=='z' else 0)),r/10)
  def cut(a,b):assert mgr.booleanOperation(a,b,adsk.fusion.BooleanTypes.DifferenceBooleanType);return a
  def union(a,b):assert mgr.booleanOperation(a,b,adsk.fusion.BooleanTypes.UnionBooleanType);return a
  colors={}
  for lib in app.materialLibraries:
   for n in ['Plastic - Matte (Black)','Plastic - Matte (Red)','Steel - Satin']:
    try:
     a=lib.appearances.itemByName(n)
     if a and n not in colors:colors[n]=a
    except RuntimeError:pass
  def add(c,b,n,col='Plastic - Matte (Black)'):
   ob=c.bRepBodies.add(b);ob.name=n
   if col in colors:ob.appearance=colors[col]
   return ob
  report={}
  def save(c,name):
   assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/(name+'.step')),c))
   bb=c.boundingBox
   report[name]={'bodies':c.bRepBodies.count,'min_mm':[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],'max_mm':[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10]}
  # Reorient the prior drawing reconstruction to the actual horizontal seating plane.
  # Old X,Y,Z = width,height,outward; new X,Y,Z = width,outward,height+15.
  # A 180-degree X flip preserves handedness; X is mirrored with no effect on symmetric geometry.
  c=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component;c.name='KLS right-angle candidate - current rating UNVERIFIED'
  imported=app.importManager.importToTarget(app.importManager.createSTEPImportOptions(str(out/'KLS1-WP-6P-03B.step')),c)
  mat=adsk.core.Matrix3D.create();mat.setWithArray([-1,0,0,0,0,0,1,0,0,1,0,1.5,0,0,0,1])
  bodies=[]
  for occ in c.allOccurrences:
   for body in occ.bRepBodies:bodies.append(body)
  for body in bodies:
   b=mgr.copy(body);mgr.transform(b,mat)
   n=body.name.replace('handwired proposal, no main-PCB pad','direct through-hole solder tail')
   ob=c.bRepBodies.add(b);ob.name=n;ob.appearance=body.appearance
  for occ in list(c.occurrences):occ.deleteMe()
  save(c,'KLS1-WP-6P-03B_horizontal_A8')
  c=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component;c.name='Same Sky RCJ-011 horizontal'
  # Drawing: 11W x12H body, 6.5 rear body depth, 14.5 overall, barrel8.3, axis6.6.
  # Origin: signal pin. Shell pin row at Y0; fourth shell stake at Y4.5.
  add(c,box(0,.75,6,11,6.5,12),'Insulator; shoulders Y4.0')
  shell=box(0,3.85,6,11,.3,12)
  shell=cut(shell,cyl(0,3.6,6.6,1.8,.7,'y'))
  add(c,shell,'Front shell','Steel - Satin')
  add(c,cut(cyl(0,4,6.6,4.15,8,'y'),cyl(0,3.9,6.6,1.8,8.2,'y')),'Barrel OD8.3; face Y12','Steel - Satin')
  add(c,box(0,0,-2,.8,.4,4),'Signal pin 1','Steel - Satin')
  for x,y in [(-5,0),(5,0),(0,4.5)]:add(c,box(x,y,-2,1.3,.5,4),'Shell pin 2; retaining shape simplified','Steel - Satin')
  save(c,'RCJ-011_A8')
  report['provenance']='Project reconstructions, not vendor CAD. KLS V1 2025-09-19; Same Sky RCJ-01 2026-08-12 p2. Cosmetic shapes approximate.'
  (out/'model-geometry-A8.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report))
 finally:doc.close(False);original.activate()
build()
