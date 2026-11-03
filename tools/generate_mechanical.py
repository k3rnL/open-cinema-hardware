#!/usr/bin/env python3
"""Generate the A0 KiCad mechanical study. Requires KiCad 10 pcbnew Python.

Explicitly regenerates the board from placement.json: do not run over unmerged
manual PCB edits. Connector envelopes have no electrical pads or assigned part.
"""
raise SystemExit('Historical A0 generator: use generate_connectors.py for A1; restore the A0 commit to regenerate A0.')
import csv
import json
import math
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'boards/rear-io'
CFG = json.loads((PROJECT / 'placement.json').read_text())
LIB = PROJECT / 'OpenCinema_Mechanical.pretty'
MODELS = PROJECT / 'models'
for folder in (LIB, MODELS, PROJECT / 'exports'):
    folder.mkdir(parents=True, exist_ok=True)
PLUGIN = p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP)

def v(x, y):
    return p.VECTOR2I(p.FromMM(x), p.FromMM(y))

def shape(parent, start, end, layer, width=0.15, kind=p.SHAPE_T_SEGMENT, mid=None):
    sh = p.PCB_SHAPE(parent)
    sh.SetShape(kind)
    sh.SetLayer(layer)
    sh.SetWidth(p.FromMM(width))
    if mid is None:
        sh.SetStart(v(*start))
        sh.SetEnd(v(*end))
    else:
        sh.SetArcGeometry(v(*start), v(*mid), v(*end))
    parent.Add(sh)
    return sh

def rounded(parent, x, y, w, h, r, layer):
    for a,b in [((x+r,y),(x+w-r,y)), ((x+w,y+r),(x+w,y+h-r)),
                ((x+w-r,y+h),(x+r,y+h)), ((x,y+h-r),(x,y+r))]:
        shape(parent,a,b,layer)
    q=r/math.sqrt(2)
    for a,m,b in [((x+w-r,y),(x+w-r+q,y+r-q),(x+w,y+r)),
                  ((x+w,y+h-r),(x+w-r+q,y+h-r+q),(x+w-r,y+h)),
                  ((x+r,y+h),(x+r-q,y+h-r+q),(x,y+h-r)),
                  ((x,y+r),(x+r-q,y+r-q),(x+r,y))]:
        shape(parent,a,b,layer,kind=p.SHAPE_T_ARC,mid=m)

def text(parent, label, x, y, size=1.1, layer=p.F_SilkS):
    t=p.PCB_TEXT(parent)
    t.SetText(label)
    t.SetPosition(v(x,y))
    t.SetTextSize(v(size,size))
    t.SetTextThickness(p.FromMM(0.15))
    t.SetLayer(layer)
    parent.Add(t)

def step_box(name, w, h, d):
    """An exact rectangular FACETED_BREP envelope, millimetres, base at z=0."""
    records=[]
    def add(s):
        records.append(s)
        return '#'+str(len(records))
    def refs(items): return ','.join(items)
    app=add("APPLICATION_CONTEXT('automotive_design')")
    add("APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,"+app+")")
    pc=add("PRODUCT_CONTEXT('',"+app+",'mechanical')")
    product=add("PRODUCT('"+name+"','"+name+"','Mechanical envelope, NOT a selected connector',("+pc+"))")
    formation=add("PRODUCT_DEFINITION_FORMATION('A0','',"+product+")")
    dc=add("PRODUCT_DEFINITION_CONTEXT('part definition',"+app+",'design')")
    pd=add("PRODUCT_DEFINITION('design','',"+formation+","+dc+")")
    pds=add("PRODUCT_DEFINITION_SHAPE('','',"+pd+")")
    unit=add('(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))')
    rad=add('(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))')
    sr=add('(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())')
    unc=add("UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-7),"+unit+",'distance_accuracy_value','')")
    ctx=add("(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT(("+unc+")) GLOBAL_UNIT_ASSIGNED_CONTEXT(("+refs([unit,rad,sr])+")) REPRESENTATION_CONTEXT('','3D'))")
    coords=[(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0),
            (-w/2,-h/2,d),(w/2,-h/2,d),(w/2,h/2,d),(-w/2,h/2,d)]
    points=[add("CARTESIAN_POINT('',("+','.join(f'{c:.6f}' for c in xyz)+"))") for xyz in coords]
    faces=[]
    for order in [(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]:
        loop=add("POLY_LOOP('',("+refs([points[i] for i in order])+"))")
        bound=add("FACE_OUTER_BOUND('',"+loop+",.T.)")
        a,b,c=[coords[i] for i in order[:3]]
        u=[b[i]-a[i] for i in range(3)]
        vv=[c[i]-a[i] for i in range(3)]
        normal=[u[1]*vv[2]-u[2]*vv[1],u[2]*vv[0]-u[0]*vv[2],u[0]*vv[1]-u[1]*vv[0]]
        def direction(vec):
            length=math.sqrt(sum(n*n for n in vec))
            return add("DIRECTION('',("+','.join(f'{n/length:.6f}' for n in vec)+"))")
        axis=add("AXIS2_PLACEMENT_3D('',"+points[order[0]]+","+direction(normal)+","+direction(u)+")")
        plane=add("PLANE('',"+axis+")")
        faces.append(add("FACE_SURFACE('',("+bound+"),"+plane+",.T.)"))
    shell=add("CLOSED_SHELL('',("+refs(faces)+"))")
    brep=add("FACETED_BREP('"+name+"',"+shell+")")
    rep=add("FACETED_BREP_SHAPE_REPRESENTATION('"+name+"',("+brep+"),"+ctx+")")
    add("SHAPE_DEFINITION_REPRESENTATION("+pds+","+rep+")")
    header="ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('Mechanical connector envelope only'),'2;1');\nFILE_NAME('"+name+".step','2026-11-03T00:00:00',('Open Cinema'),('Open Cinema'),'Open Cinema generator','Open Cinema','');\nFILE_SCHEMA(('AUTOMOTIVE_DESIGN'));\nENDSEC;\nDATA;\n"
    return header+'\n'.join('#'+str(i+1)+'='+s+';' for i,s in enumerate(records))+'\nENDSEC;\nEND-ISO-10303-21;\n'

def vrml_model(name,w,h,d):
    # KiCad legacy VRML units are 0.1 inch, unlike STEP millimetres.
    def box(x,y,z,dx,dy,dz,color):
        pos=' '.join(str(a/2.54) for a in (x,y,z))
        size=' '.join(str(a/2.54) for a in (dx,dy,dz))
        return f'Transform {{ translation {pos} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor {color} }} }} geometry Box {{ size {size} }} }} ] }}\n'
    data='#VRML V2.0 utf8\n# MECHANICAL ENVELOPE ONLY; not a manufacturer model.\n'
    data+=box(0,0,d/2,w,h,d,'0.18 0.20 0.23')
    if name=='speaker':
        for x,col in [(-w/4,'0.8 0.08 0.06'),(w/4,'0.035 0.035 0.035')]:
            data+=box(x,0,d-0.1,w*.38,h*.65,0.25,col)
    elif name=='optical':
        data+=box(0,0,d-0.1,8,8,0.25,'0.025 0.025 0.025')
    elif name=='hdmi':
        data+=box(0,0,d-0.1,w-1,h-1,0.25,'0.65 0.68 0.70')
        data+=box(0,0,d+0.04,w-3,h-3,0.1,'0.015 0.015 0.015')
    else:
        data+=box(0,0,d-0.1,8,8,0.25,'0.75 0.53 0.16')
    return data

for name,env in CFG['connector_envelopes'].items():
    w,h,d=(env[k] for k in ('width','height','depth'))
    (MODELS/(name+'.step')).write_text(step_box(name,w,h,d))
    (MODELS/(name+'.wrl')).write_text(vrml_model(name,w,h,d))
    fp=p.FOOTPRINT(None)
    fp.SetFPID(p.LIB_ID('OpenCinema_Mechanical',name+'_ENVELOPE'))
    fp.SetLibDescription(env['description']+'; NO PADS; NOT FOR FABRICATION')
    fp.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
    fp.SetReference('REF**')
    fp.SetValue(name.upper()+'_ENVELOPE')
    fp.Reference().SetPosition(v(0,-h/2-1.4))
    fp.Reference().SetTextSize(v(1,1))
    fp.Reference().SetTextThickness(p.FromMM(.15))
    fp.Value().SetVisible(False)
    shape(fp,(-w/2,-h/2),(w/2,h/2),p.F_Fab,kind=p.SHAPE_T_RECT)
    shape(fp,(-w/2-.5,-h/2-.5),(w/2+.5,h/2+.5),p.F_CrtYd,.05,kind=p.SHAPE_T_RECT)
    shape(fp,(-w/2,-h/2),(w/2,h/2),p.F_SilkS,kind=p.SHAPE_T_RECT)
    model=p.FP_3DMODEL()
    model.m_Filename='${KIPRJMOD}/models/'+name+'.wrl'
    fp.Add3DModel(model)
    PLUGIN.FootprintSave(str(LIB),fp)

board=p.BOARD()
board.SetFileName(str(PROJECT/'rear-io.kicad_pcb'))
settings=board.GetDesignSettings()
settings.SetBoardThickness(p.FromMM(CFG['board']['thickness']))
# Board drawing origin offset leaves readable positive coordinates in KiCad.
OX,OY=150.0,100.0
W,H=CFG['board']['width'],CFG['board']['height']
TOP=CFG['board']['top_z']
def pos(x,z): return (OX+x,OY+TOP-z)
settings.SetAuxOrigin(v(*pos(0,0)))
settings.SetGridOrigin(v(*pos(0,CFG['opening']['centre_z'])))
rounded(board,OX-W/2,OY,W,H,CFG['board']['corner_radius'],p.Edge_Cuts)
op=CFG['opening']
rounded(board,OX-op['width']/2,OY+TOP-op['centre_z']-op['height']/2,
        op['width'],op['height'],op['radius'],p.Dwgs_User)
text(board,'210 x 25 R5 FRAME OPENING (reference only)',OX,OY-4,1.3,p.Dwgs_User)
text(board,'OPEN CINEMA / REAR I-O / A0',OX-52,OY+3,1.2)
text(board,'MECHANICAL DRAFT - NO CIRCUIT',OX+52,OY+3,1.05)
text(board,'EXTERIOR REAR VIEW - CONNECTOR FACES TOWARD VIEWER',OX,OY+H+4,1.3,p.Dwgs_User)
text(board,'PROPOSED PCB 228 x 32 x 1.6 mm / 4x DIA 3.2 / DO NOT FABRICATE',OX,OY+H+7,1.2,p.Dwgs_User)

for i,(x,z) in enumerate(CFG['mounting_holes']['positions_xz'],1):
    fp=p.FOOTPRINT(board)
    fp.SetFPID(p.LIB_ID('OpenCinema_Mechanical','Mount_M3_Proposed'))
    fp.SetReference('H'+str(i))
    fp.SetValue('M3 PROPOSED')
    fp.Value().SetVisible(False)
    fp.Reference().SetVisible(False)
    fp.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
    pad=p.PAD(fp)
    pad.SetAttribute(p.PAD_ATTRIB_NPTH)
    pad.SetShape(p.PAD_SHAPE_CIRCLE)
    pad.SetSize(v(3.2,3.2))
    pad.SetDrillSize(v(3.2,3.2))
    pad.SetLayerSet(p.LSET.AllCuMask())
    fp.Add(pad)
    shape(fp,(0,0),(3.2,0),p.F_CrtYd,.05,kind=p.SHAPE_T_CIRCLE)
    shape(fp,(0,0),(3.0,0),p.F_Fab,.1,kind=p.SHAPE_T_CIRCLE)
    # Save a library copy before positioning for clean library comparison.
    if i==1: PLUGIN.FootprintSave(str(LIB),fp)
    fp.SetPosition(v(*pos(x,z)))
    board.Add(fp)

for c in CFG['connectors']:
    fp=p.FootprintLoad(str(LIB),c['type']+'_ENVELOPE')
    fp.SetReference(c['ref'])
    fp.SetPosition(v(*pos(c['x'],c['z'])))
    board.Add(fp)
    text(board,c['label'],*pos(c['x'],39.3),size=1.15)

p.SaveBoard(str(PROJECT/'rear-io.kicad_pcb'),board)
(PROJECT/'rear-io.kicad_pro').write_text(json.dumps({'meta':{'filename':'rear-io.kicad_pro','version':1},'text_variables':{'REVISION':CFG['revision']}},indent=2)+'\n')
(PROJECT/'fp-lib-table').write_text('(fp_lib_table\n  (version 7)\n  (lib (name "OpenCinema_Mechanical")(type "KiCad")(uri "${KIPRJMOD}/OpenCinema_Mechanical.pretty")(options "")(descr "Mechanical placeholders only"))\n)\n')
with (PROJECT/'connector-placement.csv').open('w',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['reference','label','type','rear_x_mm','rear_z_mm','envelope_width_mm','envelope_height_mm','envelope_depth_mm','part_number','status'])
    for c in CFG['connectors']:
        e=CFG['connector_envelopes'][c['type']]
        writer.writerow([c['ref'],c['label'],c['type'],c['x'],c['z'],e['width'],e['height'],e['depth'],'UNSELECTED','MECHANICAL ENVELOPE ONLY'])
print('Generated',PROJECT/'rear-io.kicad_pcb')
