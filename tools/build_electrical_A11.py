#!/usr/bin/env python3
"""Build a separate, unrouted A11 electrical study. Never replaces the A9 board.
Run with KiCad's Python: python build_draft.py --output DIRECTORY --source REPO
ADV7511 ARC prototype candidate; DD+ bandwidth and firmware are unqualified.
"""
import argparse,json,uuid,shutil,re,csv
from pathlib import Path
import pcbnew as p
import faulthandler
faulthandler.enable()
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--source',required=True);a=ap.parse_args()
D=Path(a.output);SRC=Path(a.source);D.mkdir(parents=True,exist_ok=True)
N=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')
NS=uuid.UUID('9e8c1071-a60b-42d2-b983-8f8f3c1b1e10')
uid=lambda s:str(uuid.uuid5(NS,s));q=lambda s:json.dumps(str(s));rootid=uid('root')
def eff(size=1.0,extra=''):return f'(effects (font (size {size} {size})) {extra})'
types={};parts=[];sheets={k:[] for k in ['power-control','spdif','selection-lvds','speakers','arc-receiver','arc-connector','arc-power','arc-decoupling']}
def typ(key,left,right,fp='',kind='box'):
    pins={}; count=max(len(left),len(right)); h=max(5.08,(count+1)*2.54/2)
    for side,arr in [('L',left),('R',right)]:
        for i,item in enumerate(arr):
            n,name,t=item;pins[str(n)]=dict(name=name,type=t,x=-15.24 if side=='L' else 15.24,y=(len(arr)-1)*1.27-i*2.54,angle=0 if side=='L' else 180)
    types[key]=dict(pins=pins,h=h,fp=fp,kind=kind)
typ('R',[(1,'1','passive')],[(2,'2','passive')],'Resistor_SMD:R_0603_1608Metric','resistor')
typ('C',[(1,'1','passive')],[(2,'2','passive')],'Capacitor_SMD:C_0603_1608Metric','capacitor')
typ('FB',[(1,'1','passive')],[(2,'2','passive')],'Inductor_SMD:L_0603_1608Metric','resistor')
typ('PWR_FLAG',[(1,'POWER','power_out')],[])
typ('LDO',[(1,'IN','power_in'),(3,'EN','input'),(2,'GND','power_in')],[(5,'OUT','power_out'),(4,'NC','no_connect')],'Package_TO_SOT_SMD:SOT-23-5')
typ('CS8416K',[(4,'RXP0','input'),(3,'RXP1','input'),(2,'RXP2','input'),(1,'RXP3','input'),(10,'RXP4','input'),(11,'RXP5','input'),(12,'RXP6','input'),(13,'RXP7','input'),(5,'RXN','input'),(6,'VA','power_in'),(23,'VD','power_in'),(21,'VL','power_in'),(7,'AGND','power_in'),(22,'DGND','power_in')],[(28,'OLRCK','bidirectional'),(27,'OSCLK','bidirectional'),(26,'SDOUT','output'),(24,'RMCK','output'),(25,'OMCK','input'),(20,'GPO0','output'),(19,'GPO1','output'),(18,'AD2/GPO2','bidirectional'),(17,'SDA','bidirectional'),(16,'SCL','input'),(15,'AD1','input'),(14,'AD0','input'),(9,'RST_N','input'),(8,'FILT','passive')],'Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm')
typ('MUX',[(2,'1A','input'),(3,'1B','input'),(5,'2A','input'),(6,'2B','input'),(11,'3A','input'),(10,'3B','input'),(14,'4A','input'),(13,'4B','input')],[(4,'1Y','output'),(7,'2Y','output'),(9,'3Y','output'),(12,'4Y','output'),(1,'SEL','input'),(15,'G_N','input'),(16,'VCC','power_in'),(8,'GND','power_in')],'Package_SO:TSSOP-16_4.4x5mm_P0.65mm')
typ('LVDS',[(2,'DIN1','input'),(3,'DIN2','input'),(6,'DIN3','input'),(7,'DIN4','input'),(1,'EN','input'),(8,'EN_N','input'),(4,'VCC','power_in'),(5,'GND','power_in')],[(15,'D1+','output'),(16,'D1-','output'),(14,'D2+','output'),(13,'D2-','output'),(11,'D3+','output'),(12,'D3-','output'),(10,'D4+','output'),(9,'D4-','output')],'Package_SO:TSSOP-16_4.4x5mm_P0.65mm')
typ('OPT',[(3,'VCC','power_in'),(2,'GND','power_in')],[(1,'OUT','output')],'OpenCinema_Connectors:Cliff_FCR684205R')
typ('RCA',[(2,'SHIELD','passive')],[(1,'CENTRE','passive')],'OpenCinema_Connectors:SameSky_RCJ_011_Horizontal_A8')
typ('SPEAKER',[(i,f'SPK{(i+1)//2}{"-" if i%2 else "+"}','passive') for i in range(1,7)],[],'OpenCinema_Connectors:KLS1_WP_6P_03B_Horizontal_A8')
typ('HDMI',[(i,f'PIN{i}','passive') for i in range(1,11)],[(i,f'PIN{i}','passive') for i in range(11,20)]+[('SH','SHELL','passive')],'OpenCinema_Connectors:HDMI_A_Amphenol_10029449-x01xLF_Horizontal')
for n in [2,12,20]:typ('CON'+str(n),[(i,str(i),'passive') for i in range(1,n+1,2)],[(i,str(i),'passive') for i in range(2,n+1,2)],('Connector_PinHeader_2.54mm:PinHeader_2x%02d_P2.54mm_Vertical'%(n//2)) if n>2 else 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical')
typ('WIRE6',[(i,str(i),'passive') for i in range(1,7)],[],'Connector_Wire:SolderWire-1sqmm_1x06_P5.4mm_D1.4mm_OD2.7mm')
def part(sheet,ref,key,value,nets,x,y,bx=None,by=None,angle=0,mpn='',source='',dnp=False):
    t=types[key];net={str(k):v for k,v in nets.items()};assert set(net)==set(t['pins']),(ref,set(t['pins'])-set(net))
    o=dict(sheet=sheet,ref=ref,key=key,value=value,nets=net,x=round(x/1.27)*1.27,y=round(y/1.27)*1.27,bx=bx,by=by,angle=angle,mpn=mpn or value,source=source,dnp=dnp,fp=t['fp'],uuid=uid(ref));parts.append(o);return o
def passive(sheet,ref,key,val,n1,n2,x,y,bx,by,mpn='',dnp=False):
    known={'100nF':'CL10B104KB8NNNC','30pF C0G':'CL10C300JB8NNNC','22nF X7R':'CL10B223KB8NNNC','10uF':'CL10A106KP8NNNC','4.7uF':'CL10A475KO8NNNC'}
    return part(sheet,ref,key,val,{1:n1,2:n2},x,y,bx,by,mpn=mpn or known.get(val,'TBD - '+val+' '+key+' 0603'),dnp=dnp)
# Power / controls: GPIO numbering intentionally unassigned. Both boards must be powered together.
part('power-control','U6','LDO','TLV75533PDBVR',{1:'+5V_IN',2:'GND',3:'+5V_IN',4:None,5:'+3V3'},105,55,154,128,mpn='TLV75533PDBVR',source='https://www.ti.com/lit/ds/symlink/tlv755p.pdf')
part('power-control','J21','CON2','5V regulated input',{1:'+5V_IN',2:'GND'},40,55,165,130,mpn='HEADER_1X02_P2.54_PROVISIONAL')
part('power-control','J20','CON12','PI CONTROL / NOT PI PINOUT',{1:'GND',2:'I2C_SDA',3:'GND',4:'I2C_SCL',5:'CS_RESET_N',6:'CS_INT',7:'ADV_INT',8:'HDMI_5V_EN',9:'LVDS_EN',10:'CS_RMCK_MON',11:'GND',12:'CS_RERR'},270,65,151,134,90,mpn='HEADER_2X06_P2.54_PROVISIONAL')
for i,net in enumerate(['+5V_IN','GND','+3V3_A']):part('power-control','#FLG'+str(i+1),'PWR_FLAG','POWER PROVIDED',{1:net},340,100+i*35)
for i,(net,val,bx,by) in enumerate([('+5V_IN','4.7uF',159,128),('+3V3','4.7uF',149,128),('+3V3','10uF',145,128)],1):passive('power-control','C'+str(i),'C',val,net,'GND',65+(i-1)*75,110,bx,by)
for ref,val,n1,n2,x,y,bx,by,dnp in [('R1','4.7k','I2C_SDA','+3V3',70,155,144,136,True),('R2','4.7k','I2C_SCL','+3V3',160,155,144,139,True),('R3','10k','CS_RESET_N','GND',70,190,139,136,False),('R4','10k','AUDIO_SEL','GND',160,190,123,130,False),('R5','10k','MUX_DISABLE','+3V3',250,190,119,130,False),('R6','10k','LVDS_EN','GND',340,190,85,130,False)]:passive('power-control',ref,'R',val,n1,n2,x,y,bx,by,dnp=dnp)
# Optical/coax, receiver. Local analog ferrite and loop filter follow DS578F5 Fig5/Table6.
cs={1:'RX_ARC',2:'RX_COAX',3:'RX_OPT2',4:'RX_OPT1',5:'RXN_AC',6:'+3V3_A',7:'GND',8:'PLL_FILT',9:'CS_RESET_N',10:'GND',11:'GND',12:'GND',13:'GND',14:'AD0_STRAP',15:'AD1_STRAP',16:'I2C_SCL',17:'I2C_SDA',18:'AD2_STRAP',19:'CS_RERR',20:'CS_INT',21:'+3V3',22:'GND',23:'+3V3',24:'CS_RMCK_MON',25:'GND',26:'SPDIF_D0',27:'SPDIF_BCLK',28:'SPDIF_LRCLK'}
part('spdif','U1','CS8416K','CS8416K-CZZR',cs,240,85,124,121,source='https://statics.cirrus.com/pubs/proDatasheet/CS8416_DS578F5.pdf')
for j,(ref,x,bx) in enumerate([('J7',40,125),('J8',110,106)],1):
    part('spdif',ref,'OPT','FCR684205R',{1:f'OPT{j}_OUT',2:'GND',3:'+3V3'},x,45,bx,109)
    passive('spdif','C'+str(10+j),'C','100nF',f'OPT{j}_OUT',f'RX_OPT{j}',x,80,bx,114)
    passive('spdif','C'+str(12+j),'C','100nF','+3V3','GND',x,110,bx+5,114)
    passive('spdif','C'+str(14+j),'C','30pF C0G',f'OPT{j}_OUT','GND',x,140,bx-5,114)
part('spdif','J9','RCA','RCJ-011',{1:'COAX_IN',2:'GND'},40,185,86,107)
passive('spdif','R10','R','75R 1%','COAX_IN','GND',105,185,86,114)
passive('spdif','C17','C','10nF','COAX_IN','RX_COAX',105,215,91,114)
passive('spdif','C18','C','10nF','RXN_AC','GND',185,215,117,124)
passive('spdif','FB1','FB','600R @100MHz','+3V3','+3V3_A',310,145,132,123,'BLM18AG601SN1D')
for ref,val,n1,n2,x,y,bx,by in [('C19','100nF','+3V3_A','GND',235,145,128,127),('C20','10uF','+3V3_A','GND',235,170,132,127),('C21','100nF','+3V3','GND',310,170,120,116),('C22','100nF','+3V3','GND',310,195,128,116),('C23','1nF C0G','PLL_FILT','GND',235,195,116,120),('C24','22nF X7R','PLL_RC','GND',235,220,116,127)]:passive('spdif',ref,'C',val,n1,n2,x,y,bx,by)
for ref,val,n1,n2,x,y,bx,by in [('R11','3k 1%','PLL_FILT','PLL_RC',310,220,116,123),('R12','47k','SPDIF_D0','+3V3',40,250,133,118),('R13','47k','AD2_STRAP','GND',125,250,133,121),('R14','10k','AD0_STRAP','GND',210,250,137,118),('R15','10k','AD1_STRAP','GND',295,250,137,121)]:passive('spdif',ref,'R',val,n1,n2,x,y,bx,by)
# CS_RERR monitor test point is routed to a labelled test pad in later layout; no automatic fault gate yet.
# One receiver selects all four S/PDIF sources. Only three LVDS pairs are used.
lvds={1:'LVDS_EN',8:'GND',4:'+3V3',5:'GND',2:'SPDIF_BCLK',3:'SPDIF_LRCLK',6:'SPDIF_D0',7:'GND',15:'LVDS_BCLK_P',16:'LVDS_BCLK_N',14:'LVDS_LRCLK_P',13:'LVDS_LRCLK_N',11:'LVDS_D0_P',12:'LVDS_D0_N',10:None,9:None}
part('selection-lvds','U4','LVDS','DS90LV047ATMTC/NOPB',lvds,135,80,100,125,source='https://www.ti.com/lit/ds/symlink/ds90lv047a.pdf')
j22={i:('GND' if i in [3,4,9,10,15,16,19,20] else None) for i in range(1,21)}
for sig,i in [('BCLK',1),('LRCLK',5),('D0',7)]:j22[i]='LVDS_'+sig+'_P';j22[i+1]='LVDS_'+sig+'_N'
part('selection-lvds','J22','CON20','3 LVDS PAIRS / PROVISIONAL',j22,280,80,115,137,90,mpn='HEADER_2X10_P2.54_PROVISIONAL')
passive('selection-lvds','C32','C','100nF','+3V3','GND',135,140,105,125)
parts[:]=[o for o in parts if o['ref'] not in ['R4','R5']]
# Existing connector fit candidates. No common BTL return. HDMI circuit added below.
for k,ref,bx in [(1,'SP1',225),(2,'SP2',168)]:
    nets={i:f'SPK{(k-1)*3+(i+1)//2}_{"N" if i%2 else "P"}' for i in range(1,7)}
    part('speakers',ref,'SPEAKER','KLS1-WP-6P-03B / UNQUALIFIED',nets,65,55+(k-1)*80,bx,100,mpn='L-KLS1-WP-6P-03B-B/R')
    part('speakers','J'+str(30+k),'WIRE6','AMP WIRE SOLDER PADS',nets,180,55+(k-1)*80,bx-13.5,123,mpn='PCB_SOLDER_PADS_1SQMM')
ADV_HW='https://www.analog.com/media/en/technical-documentation/user-guides/ADV7511_Hardware_Users_Guide.pdf'
adv_names={};adv_kind={};adv_nets={}
def advpins(pins,name,kind,net):
    for i in pins:adv_names[i]=name;adv_kind[i]=kind;adv_nets[i]=net
advpins([1,19,49,76,77],'DVDD','power_in','+1V8_D')
advpins([24,25],'PVDD','power_in','+1V8_D')
advpins([29,34,41],'AVDD','power_in','+1V8_A')
advpins([21],'PLVDD','power_in','+1V8_P')
advpins([26],'BGVDD','power_in','+1V8_P')
advpins([47],'MVDD','power_in','+3V3')
advpins([18,20,22,23,27,31,37,44,75,99,100],'GND','power_in','GND')
for i,n,net,kind in [(28,'R_EXT','ADV_REXT','passive'),(30,'HPD','HDMI_HPD_HEAC_N','input'),(38,'PD_AD','ADV_PD','input'),(45,'INT','ADV_INT','output'),(46,'SPDIF_OUT','ARC_SPDIF','output'),(48,'CEC','HDMI_CEC','bidirectional'),(50,'CEC_CLK','CEC_CLK','input'),(51,'HEAC_N','ADV_HEAC_N','input'),(52,'HEAC_P','ADV_HEAC_P','input'),(53,'DDCSCL','HDMI_DDC_SCL','open_collector'),(54,'DDCSDA','HDMI_DDC_SDA','bidirectional'),(55,'SCL','I2C_SCL','input'),(56,'SDA','I2C_SDA','bidirectional')]:advpins([i],n,kind,net)
for i,n in [(32,'TXC_N'),(33,'TXC_P'),(35,'TX0_N'),(36,'TX0_P'),(39,'TX1_N'),(40,'TX1_P'),(42,'TX2_N'),(43,'TX2_P')]:advpins([i],n,'output',None)
for i,n in [(2,'VSYNC'),(3,'DSD0'),(4,'DSD1'),(5,'DSD2'),(6,'DSD3'),(7,'DSD4'),(8,'DSD5'),(9,'DSD_CLK'),(10,'SPDIF_IN'),(11,'MCLK'),(12,'I2S0'),(13,'I2S1'),(14,'I2S2'),(15,'I2S3'),(16,'SCLK'),(17,'LRCLK'),(79,'VCLK'),(97,'DE'),(98,'HSYNC')]:advpins([i],n,'input','GND')
for bit,i in zip(range(35,-1,-1),list(range(57,75))+[78]+list(range(80,97))):advpins([i],'D'+str(bit),'input','GND')
assert set(adv_names)==set(range(1,101))
# A11 prototype candidate: public ADI Hardware Guide Rev D / Programming Guide Rev G.
# This is an unqualified, unrouted study. ARC 192 kHz/DD+ is an explicit bench gate.
typ('ADV7511',[(i,adv_names[i],adv_kind[i]) for i in range(1,51)],[(i,adv_names[i],adv_kind[i]) for i in range(51,101)],'Package_QFP:LQFP-100_14x14mm_P0.5mm')
typ('LDOW',[(6,'IN','power_in'),(4,'EN','input'),(3,'GND','power_in'),(7,'EP_GND','power_in')],[(1,'OUT','power_out'),(2,'NC','no_connect'),(5,'NC','no_connect')],'Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm')
typ('OSC',[(1,'EN','input'),(2,'GND','power_in'),(4,'VDD','power_in')],[(3,'OUT','output')],'Oscillator:Oscillator_SMD_Abracon_ASV-4Pin_7.0x5.1mm')
typ('SW5V',[(1,'IN','power_in'),(2,'GND','power_in'),(3,'EN','input')],[(6,'OUT','power_out'),(4,'FAULT_N','open_collector'),(5,'ILIM','passive')],'Package_TO_SOT_SMD:SOT-23-6')
typ('ESD4',[(1,'IO1','passive'),(2,'IO2','passive'),(4,'IO3','passive'),(5,'IO4','passive'),(3,'GND','power_in')],[(6,'NC','passive'),(7,'NC','passive'),(9,'NC','passive'),(10,'NC','passive'),(8,'GND','power_in')],'Package_SON:USON-10_2.5x1.0mm_P0.5mm')
typ('DIO',[(1,'A','passive')],[(3,'K','passive'),(2,'NC','no_connect')],'Package_TO_SOT_SMD:SOT-23')
typ('L',[(1,'1','passive')],[(2,'2','passive')],'Inductor_SMD:L_Bourns-SRN4018','resistor')

# Upgrade U6 to an exposed-pad package for the increased 3.3 V load.
u6=next(o for o in parts if o['ref']=='U6')
u6.update(key='LDOW',value='TLV75533PDRVR',mpn='TLV75533PDRVR',fp=types['LDOW']['fp'],nets={'6':'+5V_IN','3':'GND','4':'+5V_IN','1':'+3V3','2':None,'5':None,'7':'GND'})

part('arc-receiver','U7','ADV7511','ADV7511KSTZ / ARC candidate',adv_nets,205,110,61,125,mpn='ADV7511KSTZ',source=ADV_HW)
passive('arc-receiver','R40','R','887R 1%','ADV_REXT','GND',80,210,50,123,'RC0603FR-07887RL')
passive('arc-receiver','R41','R','2k 1%','ADV_PD','GND',180,210,72,128,'RC0603FR-072KL')
passive('arc-receiver','R42','R','2k 1%','ADV_INT','+3V3',280,210,72,131,'RC0603FR-072KL')
part('arc-receiver','Y1','OSC','12 MHz / ASV-12.000MHZ-E-T',{1:'+3V3',2:'GND',3:'CEC_CLK_RAW',4:'+3V3'},80,60,80,126,mpn='ASV-12.000MHZ-E-T',source='https://abracon.com/Oscillators/ASV.pdf')
passive('arc-receiver','R43','R','33R','CEC_CLK_RAW','CEC_CLK',80,105,76,126,'RC0603FR-0733RL')
passive('arc-receiver','C40','C','100nF','+3V3','GND',80,140,80,131)

# Connector pins follow HDMI Type A. TMDS is deliberately unused (ARC-only, no video).
hdmi={i:None for i in range(1,20)}
for i in [2,5,8,11,17]:hdmi[i]='GND'
hdmi.update({13:'HDMI_CEC',14:'HDMI_HEAC_P',15:'HDMI_DDC_SCL',16:'HDMI_DDC_SDA',18:'HDMI_5V',19:'HDMI_HPD_HEAC_N','SH':'CHASSIS_HDMI'})
part('arc-connector','J10','HDMI','10029449-001RLF / ARC ONLY',hdmi,70,65,61,102.7,180,mpn='10029449-001RLF')
for ref,n1,n2,x,y,bx,by in [('C41','HDMI_HEAC_P','ADV_HEAC_P',190,45,54,114),('C42','HDMI_HPD_HEAC_N','ADV_HEAC_N',190,80,68,114)]:passive('arc-connector',ref,'C','1uF 16V',n1,n2,x,y,bx,by,'CL10B105KO8NNNC')
for ref,n1,x,y,bx,by in [('R44','ADV_HEAC_P',310,45,54,116),('R45','ADV_HEAC_N',310,80,68,116)]:passive('arc-connector',ref,'R','49.9R 1%',n1,'+1V8_D',x,y,bx,by,'RC0603FR-0749R9L')
# HPD branches on the connector side of C42: do not remove its DC component.
passive('arc-connector','R46','R','10k','HDMI_HPD_HEAC_N','GND',190,115,72,114,'RC0603FR-0710KL')
passive('arc-connector','R47','R','2k 1%','HDMI_DDC_SCL','HDMI_5V',310,115,72,117,'RC0603FR-072KL')
passive('arc-connector','R48','R','2k 1%','HDMI_DDC_SDA','HDMI_5V',310,145,72,120,'RC0603FR-072KL')
passive('arc-connector','R49','R','27k 1%','+3V3','CEC_PULLUP_A',70,145,48,115,'RC0603FR-0727KL')
part('arc-connector','D1','DIO','BAS116,215',{1:'CEC_PULLUP_A',2:None,3:'HDMI_CEC'},70,180,48,119,source='https://assets.nexperia.com/documents/data-sheet/BAS116.pdf')
passive('arc-connector','R50','R','33R','ARC_SPDIF','ARC_SPDIF_SER',190,180,75,121,'RC0603FR-0733RL')
passive('arc-connector','C43','C','100nF','ARC_SPDIF_SER','RX_ARC',310,180,116,116)
# No new ground/common return for the speaker outputs. Shell bond selected during EMC review.
passive('arc-connector','R51','R','0R / chassis bond DNP','CHASSIS_HDMI','GND',70,235,49,112,'RC0603JR-070RL',dnp=True)
esd_source='https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf'
for ref,names,x,bx in [('U10',['HDMI_HEAC_P','HDMI_HPD_HEAC_N','HDMI_DDC_SCL','HDMI_DDC_SDA'],190,57),('U11',['HDMI_CEC','HDMI_5V',None,None],310,65)]:
    en={1:names[0],2:names[1],4:names[2],5:names[3],3:'GND',8:'GND',6:None,7:None,9:None,10:None}
    part('arc-connector',ref,'ESD4','TPD4E05U06DQAR',en,x,235,bx,112,source=esd_source)

# Separate 1.8 V regulator and three LC power domains per ADI reference.
part('arc-power','U8','LDOW','TLV75518PDRVR',{6:'+3V3',4:'+3V3',3:'GND',7:'GND',1:'+1V8_RAW',2:None,5:None},70,50,76,135,source='https://www.ti.com/lit/ds/symlink/tlv755p.pdf')
passive('arc-power','C44','C','4.7uF','+3V3','GND',190,50,73,135,'CL10A475KO8NNNC')
passive('arc-power','C45','C','4.7uF','+1V8_RAW','GND',310,50,79,135,'CL10A475KO8NNNC')
for k,(rail,bx) in enumerate([('+1V8_D',76),('+1V8_A',83),('+1V8_P',90)]):
    part('arc-power','L'+str(k+1),'L','10uH / SRN4018-100M',{1:'+1V8_RAW',2:rail},70,95+k*50,bx,117,mpn='SRN4018-100M',source='https://www.bourns.com/docs/product-datasheets/srn4018.pdf')
    passive('arc-power','C'+str(46+k),'C','10uF',rail,'GND',190,95+k*50,bx,121)
    part('arc-power','#FLG'+str(10+k),'PWR_FLAG','FILTERED SUPPLY',{1:rail},310,95+k*50)
# One decoupler per supply pin; adjacent pairs may share but are not combined in this draft.
power_pins=[(1,'+1V8_D'),(19,'+1V8_D'),(49,'+1V8_D'),(76,'+1V8_D'),(77,'+1V8_D'),(24,'+1V8_D'),(25,'+1V8_D'),(29,'+1V8_A'),(34,'+1V8_A'),(41,'+1V8_A'),(21,'+1V8_P'),(26,'+1V8_P'),(47,'+3V3')]
for k,(pin,rail) in enumerate(power_pins):
    o=passive('arc-decoupling','C'+str(50+k),'C','100nF',rail,'GND',60+(k%4)*95,55+(k//4)*50,48+(k%7)*4,136+(k//7)*2)
    o['value']=f'100nF / U7 pin {pin}'

# HDMI +5 V is an output to the TV, independently switchable from Pi.
part('arc-power','U9','SW5V','TPS2553DBVR',{1:'+5V_IN',2:'GND',3:'HDMI_5V_EN',4:'HDMI_5V_FAULT_N',5:'HDMI_ILIM',6:'HDMI_5V'},70,250,92,135,source='https://www.ti.com/lit/ds/symlink/tps2553.pdf')
passive('arc-decoupling','R52','R','226k 1%','HDMI_ILIM','GND',60,255,94,131,'RC0603FR-07226KL')
passive('arc-decoupling','R53','R','10k','HDMI_5V_EN','GND',155,255,96,135,'RC0603FR-0710KL')
passive('arc-decoupling','R54','R','10k','HDMI_5V_FAULT_N','+3V3',250,255,96,138,'RC0603FR-0710KL')
passive('arc-decoupling','C63','C','1uF 16V','+5V_IN','GND',155,205,89,135,'CL10B105KO8NNNC')
passive('arc-decoupling','C64','C','100nF','HDMI_5V','GND',250,205,89,138)
part('arc-decoupling','J24','CON2','HDMI POWER FAULT / GND',{1:'HDMI_5V_FAULT_N',2:'GND'},345,210,100,137,90,mpn='HEADER_1X02_P2.54_PROVISIONAL')

# Standard/custom symbol source. All physical pins represented, explicit no-connects.
def libsym(key,name):
    t=types[key];pins=t['pins'];h=t['h'];body=f'(rectangle (start -10.16 {h}) (end 10.16 {-h}) (stroke (width 0.254) (type default)) (fill (type background)))'
    if t['kind'] in ['resistor','capacitor']:
        for pin in pins.values():pin['x']=-5.08 if pin['angle']==0 else 5.08
        h=1.27
        if t['kind']=='resistor':body='(rectangle (start -2.54 1.016) (end 2.54 -1.016) (stroke (width 0.254) (type default)) (fill (type none)))'
        else:body=''.join(f'(polyline (pts (xy {x} 1.524) (xy {x} -1.524)) (stroke (width 0.254) (type default)) (fill (type none)))' for x in [-.635,.635])
    s=f'(symbol {q(name)} (pin_names (offset 0.508)'+(' (hide yes)' if t['kind']!='box' else '')+') (in_bom yes) (on_board yes)'
    for nm,val in [('Reference','U'),('Value',key),('Footprint',t['fp'])]:s+=f'(property {q(nm)} {q(val)} (at 0 {h+2.54} 0) {eff(1.0,"(hide yes)" if nm=="Footprint" else "")})'
    s+=f'(symbol {q(key+"_0_1")} {body}) (symbol {q(key+"_1_1")} '
    for n,pin in pins.items():
        le=5.08 if t['kind']=='box' else (2.54 if t['kind']=='resistor' else 4.445)
        s+=f'(pin {pin["type"]} line (at {pin["x"]} {pin["y"]} {pin["angle"]}) (length {le}) (name {q(pin["name"])} {eff(.9)}) (number {q(n)} {eff(.9)}))'
    return s+'))'
alllibs=''.join(libsym(k,'OpenCinema_A11:'+k) for k in types)
(D/'OpenCinema_A11.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "open-cinema")'+''.join(libsym(k,k) for k in types)+')\n')
notes={
'power-control':[(20,20,'A11 ARC STUDY - 5V power and Pi control'),(20,235,'5V regulated input only. U6 is now WSON-6 with grounded thermal pad.'),(20,244,'R1/R2 DNP: use one I2C pull-up set at HAT; bus <=100 kHz. Both boards powered together.'),(20,253,'J20 changed: pin7 ADV_INT, pin8 HDMI_5V_EN. Boot: CS reset low, LVDS and HDMI5V off.'),(20,262,'I2C: CS8416 0x20, ADV7511 0x39 (7-bit). Auxiliary ADV maps must not collide.')],
'spdif':[(20,20,'A11 ARC STUDY - optical/coax/ARC shared selector'),(20,275,'RXP0 OPT1 / RXP1 OPT2 / RXP2 coax / RXP3 ARC. No resampling or codec decoding here.'),(20,283,'OMCK unused: carrier-rate measurement via RMCK needs Pi/HAT validation. Coax ESD remains open.')],
'selection-lvds':[(20,20,'A11 ARC STUDY - three active LVDS pairs'),(20,180,'CS8416 owns source selection. A10 muxes, second transmitter and external eARC header removed.'),(20,192,'LVDS carries BCLK / LRCLK / DATA0. J22 retains old pair positions; unused lanes are NC.'),(20,204,'Pi is clock consumer. Receiver-side 100R termination and capture timing still need qualification.'),(20,216,'Disable LVDS and stop capture before changing source. Never play encoded words as PCM.')],
'speakers':[(20,20,'A11 ARC STUDY - six independent speaker pairs'),(20,210,'Six independent BTL pairs: speaker negatives must never share a return or connect to ground.'),(20,220,'KLS clip current rating and exact supply remain unqualified. No fabrication/order release.')],
'arc-receiver':[(20,20,'A11 ARC STUDY - ADV7511KSTZ (100-pin LQFP)'),(20,235,'All 100 pins represented. Unused video/audio data inputs grounded; TMDS outputs not connected.'),(20,245,'PD low at power-up selects 7-bit 0x39. Wait >=200 ms before register access.'),(20,255,'12 MHz clock drives CEC; ARC-only operation / EDID access without video clock needs bench proof.'),(20,265,'Public guides establish ARC function, not guaranteed DD+ 192 kHz carrier or Atmos passthrough.')],
'arc-connector':[(20,20,'A11 ARC STUDY - HDMI coupling, CEC, DDC and protection'),(20,275,'HEAC bias follows HW guide Fig17; eval variants differ. Verify bias, ESD loading and HPD on bench.'),(20,283,'Connector-side ESD is provisioned; system ESD/CEC leakage, shell bond and back-powering not qualified.')],
'arc-power':[(20,20,'A11 ARC STUDY - 1.8V supply filters and HDMI +5V'),(20,278,'U9 ILIM=226k: approximately 101..142mA limit incl resistor tolerance (TI table). Not 75mA strap.')],
'arc-decoupling':[(20,20,'A11 ARC STUDY - local decoupling and HDMI power control'),(20,278,'Placement is a space study. Route decouplers at their named U7 pins with short ground vias.')]
}

def txt(s,x,y,size=1.27):return f'(text {q(s)} (at {x} {y} 0) {eff(size,"(justify left)")} (uuid {q(uid(s+str(x)+str(y)))}))'
for sheet in sheets:
    sid=uid(sheet); content=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(sid)}) (paper "A3") (title_block (title {q("Open Cinema - "+sheet)}) (rev "A11 DRAFT") (date "2026-11-04")) (lib_symbols {alllibs})'
    for o in [o for o in parts if o['sheet']==sheet]:
        t=types[o['key']];x=o['x'];y=o['y'];ref=o['ref'];h=t['h'] if t['kind']=='box' else 1.27
        content+=f'(symbol (lib_id {q("OpenCinema_A11:"+o["key"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp {"yes" if o["dnp"] else "no"}) (uuid {q(o["uuid"])})'
        for nm,val,dy,hide in [('Reference',ref,-h-5,False),('Value',o['value'],-h-2.5,False),('Footprint',o['fp'],0,True),('Datasheet',o['source'],0,True),('MPN',o['mpn'],0,True)]:content+=f'(property {q(nm)} {q(val)} (at {x} {y+dy} 0) {eff(.9,"(hide yes)" if hide else "")})'
        for n in t['pins']:content+=f'(pin {q(n)} (uuid {q(uid(ref+"pin"+n))}))'
        content+=f'(instances (project "rear-io-A11" (path {q("/"+rootid+"/"+sid)} (reference {q(ref)}) (unit 1)))))'
        for n,pin in t['pins'].items():
            px=x+pin['x'];py=y-pin['y'];net=o['nets'][n]
            if net is None:content+=f'(no_connect (at {px} {py}) (uuid {q(uid(ref+"nc"+n))}))';continue
            ex=px+(-5.08 if pin['x']<0 else 5.08)
            content+=f'(wire (pts (xy {px} {py}) (xy {ex} {py})) (stroke (width 0) (type default)) (uuid {q(uid(ref+"wire"+n))}))'
            ang=180 if pin['x']<0 else 0
            justify='(justify right)' if pin['x']<0 else '(justify left)'
            content+=f'(global_label {q(net)} (shape passive) (at {ex} {py} {ang}) {eff(.9,justify)} (uuid {q(uid(ref+"label"+n))}) (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {ex} {py} {ang}) {eff(1,"(hide yes)")}))'
    content+=''.join(txt(s,x,y) for x,y,s in notes[sheet])+')\n';(D/(sheet+'.kicad_sch')).write_text(content)
root=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(rootid)}) (paper "A3") (title_block (title "Open Cinema rear I/O electrical study") (rev "A11 DRAFT") (date "2026-11-04")) (lib_symbols)'
root+=txt('A11 / ELECTRICAL DRAFT - NOT A MANUFACTURING RELEASE',20,20,1.5)
root+=txt('All decoding/DSP stays on Raspberry Pi; processed output goes to amplifier by USB.',20,30)
root+=txt('ARC candidate + four-input selector + LVDS. Unrouted; DD+ and firmware not qualified.',20,38)
for i,sheet in enumerate(sheets):
    x=25+(i%2)*130;y=60+(i//2)*55
    root+=f'(sheet (at {x} {y}) (size 115 30) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0)) (uuid {q(uid(sheet))}) (property "Sheetname" {q(sheet)} (at {x} {y-1} 0) {eff(1.27,"(justify left bottom)")}) (property "Sheetfile" {q(sheet+".kicad_sch")} (at {x} {y+31} 0) {eff(1.27,"(justify left top)")}) (instances (project "rear-io-A11" (path {q("/"+rootid)} (page {q(i+2)})))))'
root+=txt('See requirements.md, sourcing.md and verification.md before using the model.',20,278)
root+='(sheet_instances (path "/" (page "1"))))\n';(D/'rear-io-A11.kicad_sch').write_text(root)
(D/'sym-lib-table').write_text('(sym_lib_table (lib (name "OpenCinema_A11") (type "KiCad") (uri "${KIPRJMOD}/OpenCinema_A11.kicad_sym") (options "") (descr "Project-authored datasheet pin maps")))\n')
(D/'rear-io-A11.kicad_pro').write_text(json.dumps({'meta':{'filename':'rear-io-A11.kicad_pro','version':3},'text_variables':{'REVISION':'A11 DRAFT / UNROUTED'}},indent=2))
# Populate a new board from A9, retaining original geometry and holes.
b=p.LoadBoard(str(SRC/'boards/rear-io/rear-io.kicad_pcb'));b.SetFileName(str(D/'rear-io-A11.kicad_pcb'));b.SetCopperLayerCount(4)
for dr in b.GetDrawings():
    if isinstance(dr,p.PCB_TEXT):dr.SetVisible(False);dr.SetLayer(p.Dwgs_User)
for f in b.GetFootprints():
    mm=list(f.Models());f.Models().clear()
    for m in mm:
        m.m_Filename=m.m_Filename.replace('${KIPRJMOD}/models/','${KIPRJMOD}/../rear-io/models/');f.Add3DModel(m)
nets={net for o in parts for net in o['nets'].values() if net};netobjs={}
for net in sorted(nets):ni=p.NETINFO_ITEM(b,net);b.Add(ni);netobjs[net]=ni
existing={f.GetReference():f for f in b.GetFootprints()};modeldir=D/'models';modeldir.mkdir(exist_ok=True)
for o in parts:
    ref=o['ref'];f=existing.get(ref)
    if not o['fp']:continue
    if f is None:
        lib,name=o['fp'].split(':');f=p.FootprintLoad(str(N/'footprints'/(lib+'.pretty')),name)
        if not f:raise ValueError(o['fp'])
        f.SetReference(ref);f.SetPosition(p.VECTOR2I(p.FromMM(o['bx']),p.FromMM(o['by'])));f.SetOrientationDegrees(o['angle']);b.Add(f)
        mm=list(f.Models());f.Models().clear()
        for m in mm:
            src=Path(re.sub(r'^\$\{KICAD\d+_3DMODEL_DIR\}',str(N/'3dmodels'),m.m_Filename));step=src.with_suffix('.step')
            if step.exists():shutil.copy2(step,modeldir/step.name);m.m_Filename='${KIPRJMOD}/models/'+step.name
            if o['key']!='WIRE6':f.Add3DModel(m)
    f.SetValue(o['value']);f.Reference().SetVisible(True);f.Reference().SetLayer(p.F_Fab);f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(1),p.FromMM(1)));f.Value().SetVisible(False)
    f.SetPath(p.KIID_PATH('/'+rootid+'/'+uid(o['sheet'])+'/'+o['uuid']))
    for pad in f.Pads():
        n=pad.GetNumber()
        if n in o['nets'] and o['nets'][n]:pad.SetNet(netobjs[o['nets'][n]])
        elif n and n not in o['nets']:raise ValueError((ref,'footprint extra pad',n))
    if o['dnp']:f.SetAttributes(f.GetAttributes() | p.FP_DNP)
# Resolve nominal courtyard clashes before export. Keep all original connector/hole positions fixed.
def bbox(f):
    items=[s.GetBoundingBox() for s in f.GraphicalItems() if s.GetLayer()==p.F_CrtYd]
    if not items:items=[pad.GetBoundingBox() for pad in f.Pads()]
    return (min(p.ToMM(s.GetX()) for s in items),min(p.ToMM(s.GetY()) for s in items),max(p.ToMM(s.GetRight()) for s in items),max(p.ToMM(s.GetBottom()) for s in items))
def clash(a,b):return a[0]<b[2]+.1 and a[2]>b[0]-.1 and a[1]<b[3]+.1 and a[3]>b[1]-.1
allfp={f.GetReference():f for f in b.GetFootprints()}
occupied=[bbox(f) for ref,f in allfp.items() if ref in existing]
preferred={'U7':(61,125),'J20':(180,136),'J21':(200,132),'J22':(115,137),'U4':(104,125)}
newparts=[o for o in parts if o['fp'] and o['ref'] not in existing]
newparts.sort(key=lambda o:(0 if o['ref']=='U7' else 1 if o['ref'].startswith('J') else 2 if o['ref'].startswith('U') or o['ref']=='Y1' else 3))
for o in newparts:
    f=allfp[o['ref']];tx,ty=preferred.get(o['ref'],(o['bx'],o['by']))
    offsets=sorted([(i*.5,j*.5) for i in range(-40,41) for j in range(-30,31)],key=lambda a:a[0]**2+a[1]**2)
    for dx,dy in offsets:
        x,y=tx+dx,ty+dy;f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));bb=bbox(f)
        if bb[0]<37 or bb[2]>263 or bb[1]<111.5 or bb[3]>139:continue
        if any(clash(bb,k) for k in occupied):continue
        occupied.append(bb);o['bx']=x;o['by']=y;break
    else:raise ValueError('No placement space for '+o['ref'])
def boardtext(s,x,y,size=1):
    t=p.PCB_TEXT(b);t.SetText(s);t.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));t.SetTextSize(p.VECTOR2I(p.FromMM(size),p.FromMM(size)));t.SetLayer(p.Dwgs_User);b.Add(t)
boardtext('A11 ELECTRICAL DRAFT - UNROUTED - ARC CANDIDATE / DD+ UNQUALIFIED',150,91,1.4)
boardtext('A9 outline and four D3 holes retained; connectors face down when installed',150,147,1.1)

p.SaveBoard(str(D/'rear-io-A11.kicad_pcb'),b)
libs=sorted({o['fp'].split(':')[0] for o in parts});(D/'fp-lib-table').write_text('(fp_lib_table '+''.join(f'(lib (name {q(l)}) (type "KiCad") (uri {q("${KIPRJMOD}/../rear-io/OpenCinema_Connectors.pretty" if l=="OpenCinema_Connectors" else "${KICAD10_FOOTPRINT_DIR}/"+l+".pretty")}) (options "") (descr ""))' for l in libs)+')\n')
# Normalize upstream model file-name metadata; preserve geometry and attribution.
for step in modeldir.glob('*.step'):
    raw=step.read_bytes()
    if b'/Users/' in raw or b'/home/' in raw:
        before=raw.split(b'DATA;',1)[1]
        raw=re.sub(rb"FILE_NAME\(\s*'[^']*'",b"FILE_NAME('"+step.name.encode()+b"'",raw,count=1)
        assert raw.split(b'DATA;',1)[1]==before
        step.write_bytes(raw)
(D/'design-manifest.json').write_text(json.dumps({'revision':'A11-draft','parts':parts,'pin_definitions':types,'status':'unrouted ARC candidate; DD+ / CEC firmware / capture not qualified'},indent=2)+'\n')
with (D/'bom-draft.csv').open('w',newline='') as out:
    w=csv.DictWriter(out,fieldnames=['ref','value','mpn','fp','dnp','source']);w.writeheader();w.writerows({k:o[k] for k in w.fieldnames} for o in parts if o['fp'])
print('Generated',len(parts),'components / eight sheets + root. Original board/project untouched.')
