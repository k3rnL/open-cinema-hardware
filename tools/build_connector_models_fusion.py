"""Run in Fusion with MODEL_OUTPUT_DIR set. Drawing-derived models, not vendor CAD.
Uses an unsaved temporary design and restores the active document on success/error.
"""
import adsk.core, adsk.fusion, math, pathlib, json
def build_connector_models():
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

  c=comp('SameSky_RCJ-021')
  add(c,cut(cyl(0,0,3.5,4.15,12.3),cyl(0,0,5,1.75,11)),'Barrel OD8.3 / mating plane 15.8','Steel - Satin')
  add(c,cut(box(0,0,3.5,10.7,10,.5),cyl(0,0,3.1,2,.9)),'Mounting flange','Steel - Satin')
  add(c,cut(cyl(0,0,0,3.5,3.5),cyl(0,0,0,1.75,3.6)),'Insulator')
  for x in [-5.15,5.15]:add(c,box(x,0,0,1.35,1.55,6),'Shell clip simplified','Steel - Satin')
  add(c,box(0,1.6,-3.15,1.35,.4,6.3),'Signal tail','Steel - Satin')
  save(c,'RCJ-021')

  c=comp('Amphenol_10078837-001LF')
  b=box(0,-.825,3.95,28.1,6.65,7.9)
  for x in [-11.5,11.5]:b=cut(b,cyl(x,-.825,2,1.5,6))
  add(c,b,'Base shell and M3 bores; threads cosmetic','Steel - Satin')
  neck=box(0,-.825,9.175,14.5,6.65,2.55)
  neck=cut(neck,box(0,-.825,9.7,13.3,4.8,2.8))
  add(c,neck,'Mating shell; cavity simplified','Steel - Satin')
  add(c,box(0,-.825,9.15,11.8,1,1.6),'Contact tongue simplified')
  for x,y in [(-13.25,2.5),(13.25,2.5),(-7.25,0),(7.25,0),(0,-3.3)]:
   add(c,box(x,y,-.95,.9,.5,1.9),'Shell stake','Steel - Satin')
  for i in range(21):add(c,box(-5.21+i*.5,2.52,.15,.2,3.3,.3),'Solder tail','Steel - Satin')
  save(c,'10078837-001LF')

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
  save(c,'FCR684205R')

  m=comp('Optical_daughterboard_assembly')
  transform=adsk.core.Matrix3D.create();transform.setWithArray([-1,0,0,0, 0,0,1,-.6, 0,1,0,-.035, 0,0,0,1])
  for b in c.bRepBodies:
   cp=mgr.copy(b);mgr.transform(cp,transform);add(m,cp,b.name,'Steel - Satin' if 'lead' in b.name else 'Plastic - Matte (Black)')
  board=box(0,-3.5,-.8,16,24,1.6)
  for x,y,r in [(-2.54,0,.4),(0,0,.4),(2.54,0,.4),(-4.6,-2.1,1),(4.6,-2.1,1),(0,3.9,1)]:board=cut(board,cyl(x,y,-1.7,r,1.9))
  mgr.transform(board,transform);add(m,board,'Daughterboard 16x24x1.6','Plastic - Matte (Green)')
  save(m,'optical-daughterboard-assembly')
  (out/'model-geometry.json').write_text(json.dumps(reports,indent=2)+'\n')
  print(json.dumps(reports))
 finally:
  doc.close(False)
  original.activate()
build_connector_models()
