#!/usr/bin/env python3
"""Static reviews of exported schematic and actual PCB; not a functional certification.
Run with KiCad Python, --board-dir, --reports and --baseline (A9 PCB path).
The reviewer does not import the builder or its design manifest.
"""
import argparse,json,hashlib,xml.etree.ElementTree as E
from pathlib import Path
import pcbnew as p
a=argparse.ArgumentParser();a.add_argument('--board-dir',required=True);a.add_argument('--reports',required=True);a.add_argument('--baseline',required=True);o=a.parse_args();d=Path(o.board_dir);r=Path(o.reports)
xml=E.parse(r/'netlist.xml').getroot();nodes={};nets={}
for n in xml.findall('./nets/net'):
    name=n.attrib['name'];nets[name]=set()
    for v in n.findall('node'):
        k=(v.attrib['ref'],v.attrib['pin']);nodes[k]=name;nets[name].add(k)
def check(ref,pin,net): assert nodes.get((ref,str(pin)))==net,(ref,pin,nodes.get((ref,str(pin))),net)
def network(ref,pins):
    for pin,net in pins.items():check(ref,pin,net)
def nc(ref,pins):
    for pin in pins: assert nodes.get((ref,str(pin)),'').startswith('unconnected-'),(ref,pin,'expected NC')
def pair(ref,a,b):network(ref,{1:a,2:b})
# Cirrus DS578F5 TSSOP pin table / Fig 5 / Table 6. RXP3 is now the ARC input.
network('U1',{1:'RX_ARC',2:'RX_COAX',3:'RX_OPT2',4:'RX_OPT1',5:'RXN_AC',6:'+3V3_A',7:'GND',8:'PLL_FILT',9:'CS_RESET_N',14:'AD0_STRAP',15:'AD1_STRAP',16:'I2C_SCL',17:'I2C_SDA',18:'AD2_STRAP',19:'CS_RERR',20:'CS_INT',21:'+3V3',22:'GND',23:'+3V3',24:'CS_RMCK_MON',25:'GND',26:'SPDIF_D0',27:'SPDIF_BCLK',28:'SPDIF_LRCLK'})
for pin in [10,11,12,13]:check('U1',pin,'GND')
for ref,a,b in [('R12','SPDIF_D0','+3V3'),('R13','AD2_STRAP','GND'),('R14','AD0_STRAP','GND'),('R15','AD1_STRAP','GND'),('R11','PLL_FILT','PLL_RC'),('C24','PLL_RC','GND'),('C23','PLL_FILT','GND'),('C18','RXN_AC','GND'),('R10','COAX_IN','GND'),('C17','COAX_IN','RX_COAX'),('FB1','+3V3','+3V3_A')]:pair(ref,a,b)
for k,ref in enumerate(['J7','J8'],1):
    network(ref,{1:f'OPT{k}_OUT',2:'GND',3:'+3V3'});pair('C'+str(10+k),f'OPT{k}_OUT',f'RX_OPT{k}');pair('C'+str(12+k),'+3V3','GND');pair('C'+str(14+k),f'OPT{k}_OUT','GND')
# ADI HW Rev D pp19-20 and support network sections6.2/7/8. All 100 physical pins covered.
u7={}
for rail,pins in {'+1V8_D':[1,19,24,25,49,76,77],'+1V8_A':[29,34,41],'+1V8_P':[21,26],'+3V3':[47]}.items():
    for pin in pins:u7[pin]=rail
for pin in [18,20,22,23,27,31,37,44,75,99,100]+list(range(2,18))+list(range(57,75))+[78,79]+list(range(80,99)):u7[pin]='GND'
u7.update({28:'ADV_REXT',30:'HDMI_HPD_HEAC_N',38:'ADV_PD',45:'ADV_INT',46:'ARC_SPDIF',48:'HDMI_CEC',50:'CEC_CLK',51:'ADV_HEAC_N',52:'ADV_HEAC_P',53:'HDMI_DDC_SCL',54:'HDMI_DDC_SDA',55:'I2C_SCL',56:'I2C_SDA'})
network('U7',u7);open_pins=[32,33,35,36,39,40,42,43];nc('U7',open_pins);assert set(u7)|set(open_pins)==set(range(1,101))
for ref,a,b in [('R40','ADV_REXT','GND'),('R41','ADV_PD','GND'),('R42','ADV_INT','+3V3'),('C41','HDMI_HEAC_P','ADV_HEAC_P'),('C42','HDMI_HPD_HEAC_N','ADV_HEAC_N'),('R44','ADV_HEAC_P','+1V8_D'),('R45','ADV_HEAC_N','+1V8_D'),('R46','HDMI_HPD_HEAC_N','GND'),('R47','HDMI_DDC_SCL','HDMI_5V'),('R48','HDMI_DDC_SDA','HDMI_5V'),('R49','+3V3','CEC_PULLUP_A'),('R50','ARC_SPDIF','ARC_SPDIF_SER'),('C43','ARC_SPDIF_SER','RX_ARC'),('R51','CHASSIS_HDMI','GND')]:pair(ref,a,b)
pair('D2','COAX_IN','GND')
network('D1',{1:'CEC_PULLUP_A',3:'HDMI_CEC'});nc('D1',[2])
network('Y1',{1:'+3V3',2:'GND',3:'CEC_CLK_RAW',4:'+3V3'});pair('R43','CEC_CLK_RAW','CEC_CLK');pair('C40','+3V3','GND')
network('J10',{2:'GND',5:'GND',8:'GND',11:'GND',13:'HDMI_CEC',14:'HDMI_HEAC_P',15:'HDMI_DDC_SCL',16:'HDMI_DDC_SDA',17:'GND',18:'HDMI_5V',19:'HDMI_HPD_HEAC_N','SH':'CHASSIS_HDMI'});nc('J10',[1,3,4,6,7,9,10,12])
network('U10',{1:'HDMI_HEAC_P',2:'HDMI_HPD_HEAC_N',4:'HDMI_DDC_SCL',5:'HDMI_DDC_SDA',3:'GND',8:'GND'});nc('U10',[6,7,9,10])
network('U11',{1:'HDMI_CEC',2:'HDMI_5V',3:'GND',8:'GND'});nc('U11',[4,5,6,7,9,10])
# TI DRV package has a different pinout from the removed A10 SOT23-5 regulator.
for ref,vin,vout in [('U6','+5V_IN','+3V3'),('U8','+3V3','+1V8_RAW')]:
    network(ref,{6:vin,4:vin,3:'GND',7:'GND',1:vout});nc(ref,[2,5])
for ref,rail in [('L1','+1V8_D'),('L2','+1V8_A'),('L3','+1V8_P')]:pair(ref,'+1V8_RAW',rail)
for i,rail in enumerate(['+1V8_D']*7+['+1V8_A']*3+['+1V8_P']*2+['+3V3'],50):pair('C'+str(i),rail,'GND')
network('U9',{1:'+5V_IN',2:'GND',3:'HDMI_5V_EN',4:'HDMI_5V_FAULT_N',5:'HDMI_ILIM',6:'HDMI_5V'})
for ref,a,b in [('R52','HDMI_ILIM','GND'),('R53','HDMI_5V_EN','GND'),('R54','HDMI_5V_FAULT_N','+3V3'),('C63','+5V_IN','GND'),('C64','HDMI_5V','GND')]:pair(ref,a,b)
network('J24',{1:'HDMI_5V_FAULT_N',2:'GND'})
network('J20',{1:'GND',2:'I2C_SDA',3:'GND',4:'I2C_SCL',5:'CS_RESET_N',6:'CS_INT',7:'ADV_INT',8:'HDMI_5V_EN',9:'LVDS_EN',10:'CS_RMCK_MON',11:'GND',12:'CS_RERR'})
network('U4',{1:'LVDS_EN',4:'+3V3',5:'GND',8:'GND',2:'SPDIF_BCLK',3:'SPDIF_LRCLK',6:'SPDIF_D0',7:'GND',15:'LVDS_BCLK_P',16:'LVDS_BCLK_N',14:'LVDS_LRCLK_P',13:'LVDS_LRCLK_N',11:'LVDS_D0_P',12:'LVDS_D0_N'});nc('U4',[9,10])
for sig,pin in [('BCLK',1),('LRCLK',5),('D0',7)]:network('J22',{pin:'LVDS_'+sig+'_P',pin+1:'LVDS_'+sig+'_N'})
for i in [3,4,9,10,15,16,19,20]:check('J22',i,'GND')
nc('J22',[11,12,13,14,17,18]);pair('R3','CS_RESET_N','GND');pair('R6','LVDS_EN','GND')
for k in range(1,7):
    for sign in ['P','N']:
        nn=nets[f'SPK{k}_{sign}'];assert len(nn)==2 and {x[0] for x in nn}==({'SP1','J31'} if k<=3 else {'SP2','J32'})
comps={c.attrib['ref']:c for c in xml.findall('./components/comp')}
for ref in ['U2','U3','U5','J23','R4','R5']:assert ref not in comps
values={'R11':'3k 1%','C24':'22nF X7R','C23':'1nF C0G','R12':'47k','R13':'47k','R10':'75R 1%','R40':'887R 1%','R41':'2k 1%','R42':'2k 1%','C41':'1uF 16V','C42':'1uF 16V','R44':'49.9R 1%','R45':'49.9R 1%','R49':'27k 1%','R52':'226k 1%'}
for ref,value in values.items():assert comps[ref].findtext('value')==value,(ref,value)
assert all('CL10A126' not in E.tostring(c,encoding='unicode') for c in comps.values())
erc=json.loads((r/'erc.json').read_text());assert not any(s['violations'] for s in erc['sheets'])
pass1={'scope':'Exported schematic topology, pin tables, values and ERC; separate reviewer script','status':'pass for static draft connectivity','erc_violations':0,'checked':['CS8416 four selected AC-coupled inputs, PLL and startup straps','ADV7511 all 100 pins, rails, ground and unused pin assignments','ARC coupling/bias, connector-side HPD tap, R_EXT and address strap','CEC clock and low-leakage pull-up diode orientation','HDMI DDC, switchable current-limited 5V and ESD channel assignment','WSON regulator pin map including thermal pad','Three LVDS pair polarities, new control pins, separate BTL pairs'],'unproven':['ARC-only startup without video clock','DD+ carrier / JOC bit preservation','CEC negotiation firmware and TV interoperability','Power, ESD, back-powering and thermal behavior'],'bench_tests_run':False}
# Pass 2: actual saved PCB pads, connector geometry, models and native DRC.
b=p.LoadBoard(str(d/'rear-io-A12.kicad_pcb'));base=p.LoadBoard(o.baseline);fps={f.GetReference():f for f in b.GetFootprints()};old={f.GetReference():f for f in base.GetFootprints()};boardmap={};models=0
for ref,f in fps.items():
    for pad in f.Pads():
        num=pad.GetNumber()
        if not num:continue
        actual=pad.GetNetname();expected=nodes.get((ref,num),'')
        if expected.startswith('unconnected-'):expected=''
        assert actual==expected,(ref,num,actual,expected);boardmap[(ref,num)]=actual
    for m in f.Models():
        path=Path(m.m_Filename.replace('${KIPRJMOD}',str(d)));assert path.is_file(),path;models+=1
for k,net in nodes.items():
    if not k[0].startswith('#'):assert k in boardmap,(k,'missing PCB pad')
for ref in ['SP1','SP2','J7','J8','J9','J10','H1','H2','H3','H4']:
    f,g=fps[ref],old[ref];assert f.GetPosition()==g.GetPosition() and f.GetOrientationDegrees()==g.GetOrientationDegrees(),ref
for ref,x,depth in [('H1',-110,12),('H2',-110,30),('H3',110,12),('H4',110,30)]:
    f=fps[ref];assert abs(150-p.ToMM(f.GetPosition().x)-x)<1e-6 and abs(p.ToMM(f.GetPosition().y)-100-depth)<1e-6
    pads=list(f.Pads());assert len(pads)==1 and abs(p.ToMM(pads[0].GetDrillSize().x)-3)<1e-6
for ref in ['U6','U8']:
    ep=next(pad for pad in fps[ref].Pads() if pad.GetNumber()=='7');assert abs(p.ToMM(ep.GetSize().x)-1)<1e-6 and abs(p.ToMM(ep.GetSize().y)-1.6)<1e-6
for ref in ['R1','R2','R51']:assert fps[ref].GetAttributes() & p.FP_DNP
assert b.GetCopperLayerCount()==4 and len(b.GetTracks())>0
assert all(isinstance(t,p.PCB_VIA) or t.GetLayer() in [p.F_Cu,p.B_Cu] for t in b.GetTracks())
assert len([z for z in b.Zones() if not z.GetIsRuleArea() and z.GetNetname()=='GND'])==4
for channel in range(1,7):
    for polarity in ['P','N']:
        ts=[t for t in b.GetTracks() if t.GetNetname()==f'SPK{channel}_{polarity}']
        assert ts and all(not isinstance(t,p.PCB_VIA) and p.ToMM(t.GetWidth())>=2.5 for t in ts)
        assert {t.GetLayer() for t in ts}=={p.F_Cu,p.B_Cu}
lengths={}
for sig in ['BCLK','LRCLK','D0']:
    lengths[sig]={}
    for sign in ['P','N']:
        ts=[t for t in b.GetTracks() if t.GetNetname()==f'LVDS_{sig}_{sign}']
        assert all(isinstance(t,p.PCB_VIA) or abs(p.ToMM(t.GetWidth())-.182626)<1e-6 for t in ts)
        lengths[sig][sign]=sum(p.ToMM(t.GetLength()) for t in ts if not isinstance(t,p.PCB_VIA))
    lengths[sig]['skew_mm']=abs(lengths[sig]['P']-lengths[sig]['N'])
    assert lengths[sig]['skew_mm']<4

assert b.GetBoardEdgesBoundingBox()==base.GetBoardEdgesBoundingBox()
drc=json.loads((r/'drc.json').read_text());assert not drc['violations'] and not drc['unconnected_items']
pass2={'scope':'PCB versus exported schematic, nominal placement, unchanged connectors/holes and models; routed','status':'pass for routed connectivity and model consistency','footprints':len(fps),'electrical_pad_keys':len(boardmap),'resolved_model_links':models,'drc_geometry_violations':len(drc['violations']),'unrouted_connections':len(drc['unconnected_items']),'tracks_and_vias':len(b.GetTracks()),'lvds_lengths_mm':lengths,'speaker_paths':'12 independent nets, 2.5 mm on both outer layers, no vias','copper_layers':b.GetCopperLayerCount(),'mounting_holes_retained':True,'physical_prototype_tested':False}
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob('*.kicad_*')) if p.suffix != '.kicad_prl'}
report={'revision':'A12 draft','date':'2026-11-04','kicad':p.Version(),'reviewer':'Two static passes by same assistant; not independent engineer approval','pass_1':pass1,'pass_2':pass2,'source_sha256':hashes,'overall_release_status':'HOLD FOR QUALIFICATION: routed prototype; functional, current-rating and procurement gates remain'}
(r/'review-two-passes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass1':pass1['status'],'pass2':pass2,'release':report['overall_release_status']}))
