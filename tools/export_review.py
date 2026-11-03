#!/usr/bin/env python3
"""Export review artifacts from the saved PCB, without regenerating the design."""
import argparse
from pathlib import Path
import shutil
import subprocess

root=Path(__file__).resolve().parents[1]
project=root/'boards/rear-io'
parser=argparse.ArgumentParser()
parser.add_argument('--cli',default=shutil.which('kicad-cli') or '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
args=parser.parse_args()
def run(*cmd):
    subprocess.run([args.cli,'pcb',*cmd,str(project/'rear-io.kicad_pcb')],cwd=project,check=True)
def out(name): return str(project/'exports'/name)
run('drc','--format','json','--exit-code-violations','-o',out('rear-io-A0-drc.json'))
run('export','step','--force','--subst-models','--drill-origin','-o',out('rear-io-A0-envelopes.step'))
run('export','step','--force','--board-only','--drill-origin','-o',out('rear-io-A0-board-only.step'))
run('export','dxf','--layers','Edge.Cuts','--mode-single','--output-units','mm','--use-drill-origin','-o',out('rear-io-A0-outline.dxf'))
run('export','svg','--layers','F.Silkscreen,F.Fab,Edge.Cuts,User.Drawings','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','-o',out('rear-io-A0-layout.svg'))
run('render','--width','2200','--height','600','--zoom','3.35','--side','top','--quality','high','--background','opaque','-o',out('rear-io-A0-top.png'))
