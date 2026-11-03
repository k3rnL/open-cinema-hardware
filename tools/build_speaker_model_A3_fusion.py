"""Drawing-derived Dragon City PT-603B mechanical model; run in Fusion with MODEL_OUTPUT_DIR.
Face is XY, Y up, Z outward. PCB seating plane is Z0; flange front is Z9.6. Contact internals and lever
contours are simplified. Never infer exact cutouts from the cosmetic model.
"""
import adsk.core,adsk.fusion,pathlib,json

def build_speaker_model():
 app=adsk.core.Application.get();original=app.activeDocument
 out=pathlib.Path(MODEL_OUTPUT_DIR);out.mkdir(parents=True,exist_ok=True)
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
 try:
  design=adsk.fusion.Design.cast(app.activeProduct);design.designType=adsk.fusion.DesignTypes.DirectDesignType
  c=design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component;c.name='DragonCity_PT-603B - straight rear tails'
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
  # Explicit drawing dimensions: flange-front to rear housing 9.6, overall
  # rear extent13, flange thickness2, front projection11.5, row spacing19.5.
  # Ear outer diameter7 is a conservative fit assumption, not dimensioned.
  flange=box(0,0,8.6,45,30,2)
  for x in [-22.5,22.5]:
   flange=union(flange,cyl(x,0,7.6,3.5,2))
   flange=cut(flange,cyl(x,0,7.5,1.25,2.2))
  add(flange,'Flange; fixing pitch45 / D2.5 / assumed ear envelope52')
  body=box(0,0,13.6,37.6,25,8)
  for x in [-13,0,13]:
   for y in [-3.5,3.5]:body=cut(body,cyl(x,y,12.6,1.5,5.2))
  add(body,'Front body37.6; cosmetic wire entries')
  for x in [-13,0,13]:
   for y,color in [(11,'Plastic - Matte (Black)'),(-11,'Plastic - Matte (Red)')]:
    lever=box(x,y,19.35,8,8,3.5)
    for yy in [-2,-1,0,1,2]:lever=cut(lever,box(x,y+yy,21,8.1,.22,.3))
    add(lever,'Finger lever; colour ordering requires confirmation',color)
   for y in [-9.75,9.75]:
    add(box(x,y,3.8,5,5,7.6),'Rear support; simplified')
    add(box(x,y,-1.7,1.5,.5,3.4),'STRAIGHT REAR TAIL / no extension below housing','Steel - Satin')
  for x in [-22.5,22.5]:
   add(cut(cyl(x,0,0,2.5,7.6),cyl(x,0,-.1,1.25,7.8)),'Rear fixing support simplified')
  path=str(out/'DragonCity_PT-603B.step')
  assert design.exportManager.execute(design.exportManager.createSTEPExportOptions(path,c))
  bb=c.boundingBox
  report={'part':'Dragon City PT-603B','provenance':'Project reconstruction of manufacturer dwpt603b.pdf, accessed 2026-11-03; not vendor CAD','status':'mechanical candidate; current rating unconfirmed','body_count':c.bRepBodies.count,'min_mm':[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],'max_mm':[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10],'simplifications':['lever profiles and wire openings cosmetic','ear diameter, rear boss/insulation and pin thickness approximate; no vendor CAD','no current or attachment qualification']}
  (out/'speaker-model-geometry-A3.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report))
 finally:
  doc.close(False);original.activate()
build_speaker_model()
