# A12 verification

2026-11-04, KiCad 10.0.5. Two static passes by the same assistant; no independent engineer approval or powered testing. [Machine-readable checks and source hashes](exports/review-two-passes.json).

## Schematic pass

Checks the exported netlist independently of the layout generator: all 100 ADV7511 pins; CS8416 inputs, rails, PLL and startup straps; ARC coupling/bias/HPD tap; CEC, DDC and switched HDMI5V; WSON exposed pads; ESD assignments including new coax D2; LVDS polarity/custom headers; independent BTL returns. Critical resistor/capacitor values are asserted. ERC reports 0 violations. The changed S/PDIF sheet and its new diode were rendered and visually inspected; the other circuit sheets retain A11 topology. Exact headers and remaining passive MPNs are now recorded, without claiming supplier acceptance.

## Saved-board pass

The saved PCB matches all 423 electrical pad keys. It has 98 footprints, 92 resolved3D model links and 1572 track/via objects. Final DRC reports 0 violations and 0unconnected items. No exclusion is added to hide routing failures. Continuous inner GND, outer fills/thermal vias, 0.15 mm minimum width/clearance, 0.60/0.30 mm vias and 0.30 mm edge clearance are retained. LVDS routes use the stated stackup geometry; measured lengths are in [stackup.md](manufacturing-review/stackup.md). All 12 speaker nets have 2.5 mm paths on both outer layers with no intervening via and no common return.

Connector positions, orientation, board bounds and all four Ø3 mounting holes match the A9 baseline. Front/back copper plots and installed 3D views were inspected. The rigid STEP/F3D each reimport as one component / 162 solids with matching per-body volume and bounds; [Fusion report](exports/fusion-check.json). The existing owner documents were not saved or overwritten. Header models remain generic envelopes; connector reconstruction and vendor tolerance qualification remain explicit limitations.

## Export consistency

Gerbers include all four copper layers, masks, paste, silkscreens and outline. Separate PTH/NPTH drills and maps use the same auxiliary origin as the position data. BOM/CPL excludes DNP from SMT placement; through-hole and wire operations are separate. Checksums identify the exact source and package. This is a manufacturing-review package, not authorization or proof of fabrication readiness.

## Reproduce checks and exports

The saved A12 PCB is authoritative. Do not run the historical placement generator over it. With KiCad 10's CLI/Python and the sibling `rear-io` model libraries available:

```sh
kicad-cli sch erc --format json -o boards/rear-io-A12/exports/erc.json boards/rear-io-A12/rear-io-A12.kicad_sch
kicad-cli sch export netlist --format kicadxml -o boards/rear-io-A12/exports/netlist.xml boards/rear-io-A12/rear-io-A12.kicad_sch
kicad-cli pcb drc --format json -o boards/rear-io-A12/exports/drc.json boards/rear-io-A12/rear-io-A12.kicad_pcb
python3 tools/review_electrical_A12.py --board-dir boards/rear-io-A12 --reports boards/rear-io-A12/exports --baseline boards/rear-io/rear-io.kicad_pcb
python3 tools/package_electrical_A12.py --board-dir boards/rear-io-A12
kicad-cli pcb export step --drill-origin --no-dnp --subst-models -o /tmp/rear-io-A12-raw.step boards/rear-io-A12/rear-io-A12.kicad_pcb
```

Regenerate Gerbers/drills/positions from the saved board before repackaging if copper or placement changes. Use the layer list/origin documented in manufacturing-review. Run `tools/export_electrical_A12_fusion.py` inside Fusion with RAW, OUT and BOARD set to the raw STEP, fresh export folder and saved PCB; it creates and closes temporary documents only and verifies both rigid reimports. A11/A9 remain unchanged historical references.

Static checks cannot establish ARC/DD+ transport, current/temperature margins, EMI/ESD, actual impedance, Pi timing or assembly fit. See [the pending qualification record](bring-up.md).
