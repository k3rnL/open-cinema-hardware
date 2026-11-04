"""Run in Fusion execute_code. Only creates temporary documents; existing user CAD is read-only.
RAW = raw KiCad STEP path; OUT = export directory; BOARD = PCB file path.
"""
import adsk.core,adsk.fusion,pathlib,json,hashlib
def run():
    app=adsk.core.Application.get();original=app.activeDocument;doc=None
    out=pathlib.Path(OUT);out.mkdir(parents=True,exist_ok=True)
    def signature(root):
        return sorted([round(b.volume,8),*[round(v,6) for v in (b.boundingBox.minPoint.x,b.boundingBox.minPoint.y,b.boundingBox.minPoint.z,b.boundingBox.maxPoint.x,b.boundingBox.maxPoint.y,b.boundingBox.maxPoint.z)]] for b in root.bRepBodies)
    try:
        doc=app.importManager.importToNewDocument(app.importManager.createSTEPImportOptions(RAW))
        d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'));d.designType=adsk.fusion.DesignTypes.DirectDesignType;r=d.rootComponent
        mgr=adsk.fusion.TemporaryBRepManager.get();matrix=adsk.core.Matrix3D.create();matrix.setWithArray([-1,0,0,0,0,1,0,0,0,0,-1,6.8595,0,0,0,1])
        entries=[(occ.fullPathName,b) for occ in r.allOccurrences for b in occ.bRepBodies]
        roots=list(r.bRepBodies)
        for name,b in entries:
            cp=mgr.copy(b);mgr.transform(cp,matrix);ob=r.bRepBodies.add(cp);ob.name=name+' / '+b.name;ob.appearance=b.appearance
        for b in roots:
            cp=mgr.copy(b);mgr.transform(cp,matrix);ob=r.bRepBodies.add(cp);ob.name=b.name;ob.appearance=b.appearance;b.deleteMe()
        for occ in list(r.occurrences):occ.deleteMe()
        assert r.occurrences.count==0 and all(b.isSolid for b in r.bRepBodies)
        expected=signature(r);report={'revision':'A11-draft','status':'unrouted ARC candidate / functional qualification pending','root_bodies':r.bRepBodies.count,'child_occurrences':0,'all_solid':True,'pcb_sha256':hashlib.sha256(pathlib.Path(BOARD).read_bytes()).hexdigest(),'reimports':[],'bodies':[]}
        for b in r.bRepBodies:
            bb=b.boundingBox;report['bodies'].append({'name':b.name,'min_mm':[v*10 for v in [bb.minPoint.x,bb.minPoint.y,bb.minPoint.z]],'max_mm':[v*10 for v in [bb.maxPoint.x,bb.maxPoint.y,bb.maxPoint.z]]})
        assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(str(out/'rear-io-A11-rigid.step'),r))
        assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(out/'rear-io-A11-rigid.f3d')))
        for name,eye in [('installed-oblique',(24,25,24)),('installed-front',(0,40,5.4)),('installed-underside',(20,25,-20))]:
            cam=app.activeViewport.camera;cam.isPerspective=False;cam.eye=adsk.core.Point3D.create(*eye);cam.target=adsk.core.Point3D.create(0,0,5.4);cam.upVector=adsk.core.Vector3D.create(0,0,1);cam.isFitView=True
            app.activeViewport.camera=cam;app.activeViewport.fit();adsk.doEvents();assert app.activeViewport.saveAsImageFile(str(out/('rear-io-A11-'+name+'.png')),1800,800)
        for name in ['rear-io-A11-rigid.step','rear-io-A11-rigid.f3d']:
            opts=app.importManager.createFusionArchiveImportOptions(str(out/name)) if name.endswith('.f3d') else app.importManager.createSTEPImportOptions(str(out/name))
            tmp=app.importManager.importToNewDocument(opts)
            try:
                rr=adsk.fusion.Design.cast(tmp.products.itemByProductType('DesignProductType')).rootComponent
                assert rr.occurrences.count==0 and rr.bRepBodies.count==len(expected)
                assert signature(rr)==expected,name
                report['reimports'].append({'file':name,'geometry_matches':True,'children':0,'bodies':rr.bRepBodies.count})
            finally:tmp.close(False)
        (out/'fusion-check.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='bodies'}))
    finally:
        if doc:doc.close(False)
        if original:original.activate()
run()
