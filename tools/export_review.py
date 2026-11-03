#!/usr/bin/env python3
"""Export A4 review artifacts from saved PCBs; never regenerates the design."""
import argparse,shutil,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1];project=root/'boards/rear-io';child=root/'boards/optical-input'
p=argparse.ArgumentParser();p.add_argument('--cli',default=shutil.which('kicad-cli') or '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli');a=p.parse_args()
def run(folder,board,*cmd):subprocess.run([a.cli,'pcb',*cmd,str(folder/board)],cwd=folder,check=True)
def main(*cmd):run(project,'rear-io.kicad_pcb',*cmd)
def out(name):return str(project/'exports'/name)
main('drc','--format','json','--exit-code-violations','-o',out('rear-io-A4-drc.json'))
main('export','step','--force','--drill-origin','-o',out('rear-io-A4-assembly.step'))
main('export','step','--force','--board-only','--drill-origin','-o',out('rear-io-A4-board-only.step'))
main('export','dxf','--layers','Edge.Cuts','--mode-single','--output-units','mm','--use-drill-origin','-o',out('rear-io-A4-outline.dxf'))
main('export','svg','--layers','F.Silkscreen,F.Fab,Edge.Cuts,User.Drawings','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','-o',out('rear-io-A4-layout.svg'))
main('render','--width','2400','--height','700','--zoom','2.8','--side','top','--quality','high','--background','opaque','-o',out('rear-io-A4-front.png'))
main('render','--width','2400','--height','1000','--zoom','1.7','--rotate','325,0,15','--quality','high','--background','opaque','-o',out('rear-io-A4-oblique.png'))
