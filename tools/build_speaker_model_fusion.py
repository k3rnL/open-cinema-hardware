"""Drawing-derived KLS6 mechanical model; run in Fusion with MODEL_OUTPUT_DIR.
Face is XY, Y up, Z outward. Flange front is Z0. Contact internals and lever
contours are simplified. Never infer exact cutouts from the cosmetic model.
"""
import adsk.core,adsk.fusion,pathlib,json

def build_speaker_model():
 app=adsk.core.Application.get();original=app.activeDocument
 out=pathlib.Path(MODEL_OUTPUT_DIR);out.mkdir(parents=True,exist_ok=True)
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
 try:
  design=adsk.fusion.Design.cast(app.activeProduct);design.designType=adsk.fusion.DesignTypes.DirectDesignType
  c=design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component;c.name='KLS1-WP-6P-03B - mechanical candidate'
  mgr=adsk.fusion.TemporaryBRepManager.get()
  def pt(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
  def box(x,y,z,w,h,d):return mgr.createBox(adsk.core.OrientedBoundingBox3D.create(pt(x,y,z),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,h/10,d/10))
  def cyl(x,y,z,r,d):return mgr.createCylinderOrCone(pt(x,y,z),r/10,pt(x,y,z+d),r/10)
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
  flange=box(0,0,-1.25,45,30,2.5)
  for x in [-22.5,22.5]:
   flange=union(flange,cyl(x,0,-2.5,3.5,2.5))
   flange=cut(flange,cyl(x,0,-2.6,1.25,2.7))
  add(flange,'52 x 30 flange; fixing pitch45 / D2.5')
  body=box(0,0,4,37.5,25,8)
  for x in [-13,0,13]:
   for y in [-3.5,3.5]:body=cut(body,cyl(x,y,3,1.5,5.2))
  add(body,'Body and six wire entries; internal geometry illustrative')
  for x in [-13,0,13]:
   for y,color in [(11,'Plastic - Matte (Black)'),(-11,'Plastic - Matte (Red)')]:
    lever=box(x,y,9.7,8,8,3.4)
    for yy in [-2,-1,0,1,2]:lever=cut(lever,box(x,y+yy,11.3,8.1,.22,.3))
    add(lever,'Finger lever; nominal colour order requires sample check',color)
   for yy in [-3.8,-8.8]:
    add(box(x,-6,-6.5,5,18,6),'Rear insulation envelope') if yy==-3.8 else None
    add(box(x,-17.75,yy,1.3,5.5,.5),'Right-angle tail; handwired proposal, no main-PCB pad','Steel - Satin')
  for x in [-22.5,22.5]:
   add(cut(cyl(x,0,-9.5,2.5,7),cyl(x,0,-9.6,1.25,7.2)),'Rear fixing boss simplified')
  path=str(out/'KLS1-WP-6P-03B.step')
  assert design.exportManager.execute(design.exportManager.createSTEPExportOptions(path,c))
  bb=c.boundingBox
  report={'part':'L-KLS1-WP-6P-03B-B/R','provenance':'Project reconstruction of manufacturer drawing V1 2025-09-19; not vendor CAD','status':'mechanical candidate; current rating unconfirmed','body_count':c.bRepBodies.count,'min_mm':[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],'max_mm':[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10],'simplifications':['lever profiles and wire openings cosmetic','flange thickness and rear boss/insulation shapes approximate','no current or attachment qualification']}
  (out/'speaker-model-geometry-A2.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report))
 finally:
  doc.close(False);original.activate()
build_speaker_model()
