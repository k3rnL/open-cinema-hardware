#!/usr/bin/env python3
"""Two separate A10 review passes: schematic topology, then PCB/net/model consistency.
Uses KiCad Python. Takes --board-dir and --reports (KiCad XML/ERC/DRC output folder).
This is a static draft review, not a timing, EMC, thermal or audio fidelity test.
"""
import argparse,json,hashlib,xml.etree.ElementTree as E
from pathlib import Path
import pcbnew as p
a=argparse.ArgumentParser();a.add_argument('--board-dir',required=True);a.add_argument('--reports',required=True);o=a.parse_args();d=Path(o.board_dir);r=Path(o.reports)
xml=E.parse(r/'netlist.xml').getroot();nodes={};nets={}
for n in xml.findall('./nets/net'):
    name=n.attrib['name'];nets[name]=set()
    for v in n.findall('node'):
        k=(v.attrib['ref'],v.attrib['pin']);nodes[k]=name;nets[name].add(k)
def check(ref,pin,net):assert nodes.get((ref,str(pin)))==net,(ref,pin,nodes.get((ref,str(pin))),net)
def network(ref,pins):
    for pin,net in pins.items():check(ref,pin,net)
network('U1',{4:'RX_OPT1',3:'RX_OPT2',2:'RX_COAX',5:'RXN_AC',6:'+3V3_A',7:'GND',8:'PLL_FILT',9:'CS_RESET_N',14:'AD0_STRAP',15:'AD1_STRAP',16:'I2C_SCL',17:'I2C_SDA',18:'AD2_STRAP',19:'CS_RERR',20:'CS_INT',21:'+3V3',22:'GND',23:'+3V3',24:'CS_RMCK_MON',25:'GND',26:'SPDIF_D0',27:'SPDIF_BCLK',28:'SPDIF_LRCLK'})
for pin in [1,10,11,12,13]:check('U1',pin,'GND')
for ref,n1,n2 in [('R12','SPDIF_D0','+3V3'),('R13','AD2_STRAP','GND'),('R14','AD0_STRAP','GND'),('R15','AD1_STRAP','GND'),('R11','PLL_FILT','PLL_RC'),('C24','PLL_RC','GND'),('C23','PLL_FILT','GND'),('C18','RXN_AC','GND'),('R10','COAX_IN','GND'),('C17','COAX_IN','RX_COAX')]:network(ref,{1:n1,2:n2})
for k,ref in enumerate(['J7','J8'],1):network(ref,{1:f'OPT{k}_OUT',2:'GND',3:'+3V3'});network('C'+str(10+k),{1:f'OPT{k}_OUT',2:f'RX_OPT{k}'})
network('U6',{1:'+5V_IN',2:'GND',3:'+5V_IN',5:'+3V3'})
for ref in ['U2','U3']:network(ref,{1:'AUDIO_SEL',8:'GND',15:'MUX_DISABLE',16:'+3V3'})
for ref,channels in [('U2',[('BCLK','BCLK'),('LRCLK','LRCLK'),('D0','D0'),(None,'D1')]),('U3',[(None,'D2'),(None,'D3'),(None,None),(None,None)])]:
    for (sa,sb),pa,pb,py in zip(channels,[2,5,11,14],[3,6,10,13],[4,7,9,12]):
        check(ref,pa,'SPDIF_'+sa if sa else 'GND');check(ref,pb,'EARC_'+sb+'_3V3' if sb else 'GND')
        if sb:check(ref,py,'TX_'+sb)
for ref,signals in [('U4',['BCLK','LRCLK','D0','D1']),('U5',['D2','D3',None,None])]:
    network(ref,{1:'LVDS_EN',4:'+3V3',5:'GND',8:'GND'})
    for sig,ip,plus,minus in zip(signals,[2,3,6,7],[15,14,11,10],[16,13,12,9]):
        check(ref,ip,'TX_'+sig if sig else 'GND')
        if sig:check(ref,plus,'LVDS_'+sig+'_P');check(ref,minus,'LVDS_'+sig+'_N')
for sig,pin in [('BCLK',1),('LRCLK',5),('D0',7),('D1',11),('D2',13),('D3',17)]:network('J22',{pin:'LVDS_'+sig+'_P',pin+1:'LVDS_'+sig+'_N'})
for i in [3,4,9,10,15,16,19,20]:check('J22',i,'GND')
for ref,n1,n2 in [('R3','CS_RESET_N','GND'),('R4','AUDIO_SEL','GND'),('R5','MUX_DISABLE','+3V3'),('R6','LVDS_EN','GND')]:network(ref,{1:n1,2:n2})
for k in range(1,7):
    for sign in ['P','N']:
        nn=nets[f'SPK{k}_{sign}'];assert len(nn)==2 and not any(x[0]=='GND' for x in nn)
for k,v in nodes.items():
    if k[0]=='J10':assert v.startswith('unconnected-'),(k,v)
erc=json.loads((r/'erc.json').read_text());assert not any(s['violations'] for s in erc['sheets'])
pass1={'scope':'Schematic topology plus ERC; independent datasheet pin transcription in this reviewer','status':'pass for implemented draft sections only','erc_violations':0,'checked':['CS8416 TSSOP pins / 0x20 straps / 47k software-mode strap','Optical supply/OUT/GND and AC coupling','75-ohm coax termination and input AC coupling','3k + 22nF branch and parallel 1nF PLL topology','5V to 3.3V regulator pin map','Both mux banks and both LVDS drivers / six pair polarities','Boot-disabled controls and separate speaker returns'],'not_implemented':['HDMI/eARC electrical circuit and firmware','Coax/HDMI ESD qualification and chassis bond network','Future HAT and production harness'],'bench_tests_run':False}
# Second pass: compare independently exported schematic nets to actual PCB pads/models.
b=p.LoadBoard(str(d/'rear-io-A10.kicad_pcb'));boardmap={};fps={f.GetReference():f for f in b.GetFootprints()};models=0
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
for ref,x,depth in [('H1',-110,12),('H2',-110,30),('H3',110,12),('H4',110,30)]:
    f=fps[ref];assert abs(150-p.ToMM(f.GetPosition().x)-x)<1e-6 and abs(p.ToMM(f.GetPosition().y)-100-depth)<1e-6
    pads=list(f.Pads());assert len(pads)==1 and abs(p.ToMM(pads[0].GetDrillSize().x)-3)<1e-6
assert b.GetCopperLayerCount()==4 and len(b.GetTracks())==0
drc=json.loads((r/'drc.json').read_text());assert not drc['violations']
pass2={'scope':'PCB versus exported schematic; placement/holes/models; routing deliberately absent','status':'pass for nominal unrouted placement only','footprints':len(fps),'electrical_pad_keys':len(boardmap),'resolved_model_links':models,'drc_geometry_violations':len(drc['violations']),'unrouted_connections':len(drc['unconnected_items']),'tracks':len(b.GetTracks()),'copper_layers':b.GetCopperLayerCount(),'mounting_holes_retained':True,'physical_prototype_tested':False}
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob('*.kicad_*')) if p.suffix != '.kicad_prl'}
report={'revision':'A10 draft','date':'2026-11-03','kicad':p.Version(),'pass_1':pass1,'pass_2':pass2,'source_sha256':hashes,'overall_release_status':'BLOCKED / NOT FOR FABRICATION; review passes do not validate unresolved sections'}
(r/'review-two-passes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass1':pass1['status'],'pass2':pass2,'release':report['overall_release_status']}))
