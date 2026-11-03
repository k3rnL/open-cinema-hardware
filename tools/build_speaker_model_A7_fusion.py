"""FE6930 drawing-derived mechanical model. Run in Fusion with MODEL_OUTPUT_DIR.
XY is the rear view, Y up, Z outward; PCB seating at Z0. Not vendor CAD.
"""
import adsk.core, adsk.fusion, pathlib, json

def build():
 app=adsk.core.Application.get();original=app.activeDocument
 out=pathlib.Path(MODEL_OUTPUT_DIR);out.mkdir(parents=True,exist_ok=True)
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
 try:
  d=adsk.fusion.Design.cast(app.activeProduct);d.designType=adsk.fusion.DesignTypes.DirectDesignType
  c=d.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component;c.name='Cliff FE6930 - 8 contacts - straight rear tails'
  mgr=adsk.fusion.TemporaryBRepManager.get()
  def pt(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
  def box(x,y,z,w,h,t):return mgr.createBox(adsk.core.OrientedBoundingBox3D.create(pt(x,y,z),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,h/10,t/10))
  def cyl(x,y,z,r,t):return mgr.createCylinderOrCone(pt(x,y,z),r/10,pt(x,y,z+t),r/10)
  def boolean(a,b,op):
   assert mgr.booleanOperation(a,b,op);return a
  cut=lambda a,b:boolean(a,b,adsk.fusion.BooleanTypes.DifferenceBooleanType)
  union=lambda a,b:boolean(a,b,adsk.fusion.BooleanTypes.UnionBooleanType)
  colors={}
  for lib in app.materialLibraries:
   for n in ['Plastic - Matte (Black)','Plastic - Matte (Red)','Steel - Satin']:
    try:
     a=lib.appearances.itemByName(n)
     if a and n not in colors:colors[n]=a
    except RuntimeError:pass
  def add(b,n,color='Plastic - Matte (Black)'):
   body=c.bRepBodies.add(b);body.name=n
   if color in colors:body.appearance=colors[color]
   return body
  flange=box(0,0,8.5,58,30,2)
  for x in [-29,29]:
   flange=union(flange,cyl(x,0,7.5,3.5,2))
   flange=cut(flange,cyl(x,0,7.4,1.25,2.2))
  add(flange,'Flange 58x30 with ears overall65; fixing pitch58 D2.5')
  # The 51x27 raised body and 14 maximum lever projection are drawing dimensions.
  # Taper, wire openings and lever ribs are simplified, not tooling geometry.
  front=box(0,0,15.25,51,27,11.5)
  for x in [-19.5,-6.5,6.5,19.5]:
   for y in [-4,4]:front=cut(front,box(x,y,19.5,4,3,4))
  add(front,'Raised housing51x27; cosmetic wire entries')
  for col,x in enumerate([-19.5,-6.5,6.5,19.5]):
   color='Plastic - Matte (Red)' if col in [0,3] else 'Plastic - Matte (Black)'
   for y in [-10,10]:
    lever=box(x,y,22.25,7,7,2.5)
    for yy in [-2,-1,0,1,2]:lever=cut(lever,box(x,y+yy,23.45,7.1,.22,.3))
    add(lever,'Finger lever R B B R in each row',color)
   for y in [-9.3,9.3]:
    add(box(x,y,3.75,7,4,7.5),'Rear insulating support; simplified')
    add(box(x,y,-1.75,1.5,.5,3.5),'Straight solder tail1.5x0.5; rear projection3.5','Steel - Satin')
  for x in [-29,29]:add(cut(cyl(x,0,0,3.35,7.5),cyl(x,0,-.1,1.25,7.7)),'Fixing boss D6.7 conservative cylindrical envelope')
  assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/'Cliff_FE6930.step'),c))
  bb=c.boundingBox
  report={'part':'Cliff FE6930','source':'https://www.cliffuk.co.uk/products/springterminals/FE6930.pdf','drawing_issue':2,'provenance':'Project reconstruction, not vendor CAD','body_count':c.bRepBodies.count,'min_mm':[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],'max_mm':[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10],'published_rating':'7 A at60 V AC','limitations':['lever, entry and rear insulation profiles simplified','nominal fit model; tolerances and physical sample not qualified','signal tails solder tags; PCB land pattern is project-derived']}
  (out/'speaker-model-geometry-A7.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
 finally:
  doc.close(False);original.activate()
build()
