"""Run in Fusion with MODEL_OUTPUT_DIR set. Drawing-derived models, not vendor CAD.
Uses an unsaved temporary design and restores the active document on success/error.
"""
import adsk.core, adsk.fusion, math, pathlib, json
def build_optical_support_models():
 app=adsk.core.Application.get()
 original=app.activeDocument
 out=pathlib.Path(MODEL_OUTPUT_DIR)
 out.mkdir(parents=True,exist_ok=True)
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
 try:
  design=adsk.fusion.Design.cast(app.activeProduct)
  design.designType=adsk.fusion.DesignTypes.DirectDesignType
  root=design.rootComponent
  mgr=adsk.fusion.TemporaryBRepManager.get()
  def pt(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
  def box(x,y,z,w,d,h):
   return mgr.createBox(adsk.core.OrientedBoundingBox3D.create(pt(x,y,z),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,d/10,h/10))
  def cyl(x,y,z,r,h,axis='z'):
   return mgr.createCylinderOrCone(pt(x,y,z),r/10,pt(x+(h if axis=='x' else 0),y+(h if axis=='y' else 0),z+(h if axis=='z' else 0)),r/10)
  def cut(a,b):
   if not mgr.booleanOperation(a,b,adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('Boolean failed')
   return a
  def comp(n):
   c=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component;c.name=n;return c
  colors={}
  for lib in app.materialLibraries:
   for n in ['Plastic - Matte (Black)','Steel - Satin','Plastic - Matte (Green)','Brass - Polished']:
    try:
     a=lib.appearances.itemByName(n)
     if a and n not in colors:colors[n]=a
    except RuntimeError:pass

  def add(c,b,n,material='Plastic - Matte (Black)'):
   ob=c.bRepBodies.add(b);ob.name=n
   if material in colors:ob.appearance=colors[material]
   return ob
  reports={}
  def save(c,n):
   path=str(out/(n+'.step'));opts=design.exportManager.createSTEPExportOptions(path,c);design.exportManager.execute(opts)
   bb=c.boundingBox
   reports[n]={'bodies':c.bRepBodies.count,'min_mm':[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],'max_mm':[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10]}

  c=comp('Cliff_FCR684205R')
  add(c,box(0,2.5,6.55,11.5,12,13.1),'Body 11.5 x 12')
  tab=box(0,4.25,16.05,9.5,8.5,5.9)
  tab=cut(tab,cyl(0,-.1,16,1.25,8.7,'y'))
  add(c,tab,'Mounting tab D2.5 bore; no screw selected')
  lip=box(0,9.65,6.9,9.5,2.3,10)
  lip=cut(lip,box(0,10.3,6.9,7.3,1.5,8.2))
  add(c,lip,'Mating bezel')
  add(c,box(0,9.9,6.9,7.2,.25,8.1),'Hinged shutter simplified')
  for x in [-2.54,0,2.54]:add(c,box(x,0,-2.05,.5,.5,4.1),'Signal lead','Steel - Satin')
  for x,y in [(-4.6,-2.1),(4.6,-2.1),(0,3.9)]:add(c,cyl(x,y,-3.6,.9,3.6),'Locating peg simplified')


  m=comp('Optical_daughterboard_assembly')
  transform=adsk.core.Matrix3D.create();transform.setWithArray([-1,0,0,0, 0,0,1,-.6, 0,1,0,-.035, 0,0,0,1])
  for b in c.bRepBodies:
   cp=mgr.copy(b);mgr.transform(cp,transform);add(m,cp,b.name,'Steel - Satin' if 'lead' in b.name else 'Plastic - Matte (Black)')
  board=box(0,-3.5,-.8,16,24,1.6)
  for x,y,r in [(-2.54,0,.4),(0,0,.4),(2.54,0,.4),(-4.6,-2.1,1),(4.6,-2.1,1),(0,3.9,1)]:board=cut(board,cyl(x,y,-1.7,r,1.9))
  for x in [-5,5]:board=cut(board,cyl(x,-12,-1.7,1.1,1.9))
  mgr.transform(board,transform);add(m,board,'Daughterboard 16x24x1.6','Plastic - Matte (Green)')
  save(m,'optical-daughterboard-supported-A6')
  # Shared cradle in integration coordinates X=rear x, Y=rear height, Z=outward.
  # Positive plug loads go via socket lug -> upper bridge -> carrier fasteners.
  cradle=comp('OC-OPTICAL-CRADLE-A6')
  parts=[box(18,52.45,-9.225,2,25.1,15.25),box(57.75,52.45,-9.225,2,25.1,15.25),
         box(37.875,41.4,-11.85,41.75,3,10),box(37.875,61.5,-3.1,41.75,6.8,3)]
  for x in [16,60]:
   for y in [42,62]:parts.append(box(x,y,-3.1,6,6,3))
  for x in [28,48]:parts.append(cyl(x,60.5,-1.6,2.8,1.25))
  solid=parts[0]
  for b in parts[1:]:assert mgr.booleanOperation(solid,b,adsk.fusion.BooleanTypes.UnionBooleanType)
  def orient(body,x,y,z,axis):
   t=adsk.core.Matrix3D.create()
   if axis=='y':t.setToRotation(-math.pi/2,adsk.core.Vector3D.create(1,0,0),pt(0,0,0))
   t.translation=adsk.core.Vector3D.create(x/10,y/10,z/10);mgr.transform(body,t);return body
  def hexagon(x,y,z,af,h,axis='z'):
   b=cyl(0,0,0,af/math.sqrt(3),h)
   for i in range(6):
    c=box(af/2+5,0,h/2,10,10,h+2)
    t=adsk.core.Matrix3D.create();t.setToRotation(i*math.pi/3,adsk.core.Vector3D.create(0,0,1),pt(0,0,0));mgr.transform(c,t);cut(b,c)
   return orient(b,x,y,z,axis)
  for x in [16,60]:
   for y in [42,62]:
    cut(solid,cyl(x,y,-5,1.2,4));cut(solid,hexagon(x,y,-4.61,4.3,1.81))
  for x in [28,48]:
   cut(solid,cyl(x,60.5,-5,1.2,5));cut(solid,hexagon(x,60.5,-4.61,4.3,1.81))
  for x in [23,33,43,53]:
   cut(solid,cyl(x,39.8,-12.35,1.2,3.2,'y'));cut(solid,hexagon(x,39.89,-12.35,4.3,1.81,'y'))
  add(cradle,solid,'Insulating PA12 cradle / prototype geometry')
  save(cradle,'optical-cradle-A6')
  # Separate STL is millimetres by Fusion exporter (recorded below).
  stl=design.exportManager.createSTLExportOptions(cradle,str(out/'optical-cradle-A6.stl'))
  stl.sendToPrintUtility=False;assert design.exportManager.execute(stl)
  hardware=comp('Cradle_and_M2_fasteners')
  add(hardware,mgr.copy(cradle.bRepBodies.item(0)),'Cradle')
  def screw(x,y,z,length,axis='z'):
   # z is seating plane; positive axis is the head direction.
   a=cyl(0,0,-length,1,length);head=cut(cyl(0,0,0,1.9,2),hexagon(0,0,.8,1.5,1.3))
   assert mgr.booleanOperation(a,head,adsk.fusion.BooleanTypes.UnionBooleanType)
   add(hardware,orient(a,x,y,z,axis),'M2 x '+str(length)+' cap screw / simplified','Steel - Satin')
  def nut(x,y,z,axis='z'):
   b=cut(hexagon(0,0,0,4,1.6),cyl(0,0,-.1,1,1.8));add(hardware,orient(b,x,y,z,axis),'M2 nut / simplified','Steel - Satin')
  for x in [16,60]:
   for y in [42,62]:screw(x,y,0,6);nut(x,y,-4.4)
  for x in [28,48]:screw(x,60.5,8.15,14);nut(x,60.5,-4.4)
  for x in [23,33,43,53]:screw(x,44.5,-12.35,6,'y');nut(x,40.1,-12.35,'y')
  save(hardware,'optical-cradle-with-fasteners-A6')
  reports['scope']='Prototype support design; hardware geometry simplified; PA12 process/tolerances, temperature, cable-load tests and JLC sourcing not qualified.'
  (out/'optical-support-geometry-A6.json').write_text(json.dumps(reports,indent=2)+'\n')
  print(json.dumps(reports))
 finally:
  doc.close(False)
  original.activate()
build_optical_support_models()
