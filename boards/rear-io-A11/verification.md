# A11 verification — two static review passes

KiCad 10.0.5, 2026-11-04. Two passes by the same assistant, **not two independent engineers**. No powered prototype or captured audio was tested. [Machine-readable results and exact source hashes](exports/review-two-passes.json).

## Pass 1 — schematic and interfaces

Compared the manufacturer pin tables/support networks and reviewed the exported netlist with a separate script. Checked all 100 ADV7511 pins, CS8416 four-input mapping/straps/PLL, optical requirements, ARC coupling/bias and connector-side HPD tap, CEC diode/clock, DDC, HDMI current-limited 5 V/ESD, WSON regulators including thermal pads, LVDS polarity, new control-header assignments and independent BTL returns. Critical resistor/capacitor values are asserted. **ERC: 0 violations**, no blanket exclusions. All nine schematic pages were rendered and visually inspected.

The review found/corrected an inherited 10 µF MPN typo and the ADV candidate annotation leaking into its MPN field. Confirmed the TI WSON6 exposed-pad footprint nominal 1 × 1.6 mm against DRV drawing4222173/C. Confirmed I2C ≤100 kHz, revised J20 pins, unproven ARC carrier range and the ADI purchasing condition. These issues are documented rather than hidden behind ERC success.

## Pass 2 — PCB and model consistency

Compared **421 electrical pad keys** against the independently exported schematic ; 97 footprints, 91 resolved model links, 4 layers and all four Ø3 mounting holes. Connector positions/orientations and board bounds match A9. **Geometry/clearance/courtyard DRC: 0 violations. There are 318 unrouted connections, zero tracks and no completed ground planes.** Placement is a space study; decoupler proximity and speaker-current paths still require real layout work.

[STEP](exports/rear-io-A11-rigid.step) and [F3D](exports/rear-io-A11-rigid.f3d) were separately reimported: 161 solid bodies, zero child components, matching per-body volume/bounds. [Fusion evidence](exports/fusion-check.json). The PCB hash matches this review. Exported DNP components are omitted; headers are illustrative. No owner document was edited or saved, and the existing linked Fusion component was not updated because unsaved owner edits were present.

## Remaining qualification

ARC-only startup/EDID without a video clock; CEC firmware and multiple-TV interoperability; DD+ carrier and JOC bit preservation; Pi/HAT clock-consumer capture and skew; hotplug/partial-power behavior; regulator/filter stability and temperatures; coax protection and chassis bond; speaker rating/wire retention/current routing; enclosure clearance/airflow and loaded PSU EMI. Procurement eligibility, exact passive/header sourcing and JLC acceptance remain open. No fabrication package or manufacturing approval is provided.

## Reproduce in a new directory

Use KiCad 10's Python with pcbnew and the installed standard libraries. The generator defaults to the installed macOS KiCad library location; adapt that path on another platform. Preserve sibling `rear-io` connector assets. Never run over manual changes.

```sh
python3 tools/build_electrical_A11.py --source . --output boards/rear-io-A11
kicad-cli sch erc --format json -o boards/rear-io-A11/exports/erc.json boards/rear-io-A11/rear-io-A11.kicad_sch
kicad-cli sch export netlist --format kicadxml -o boards/rear-io-A11/exports/netlist.xml boards/rear-io-A11/rear-io-A11.kicad_sch
kicad-cli pcb drc --format json -o boards/rear-io-A11/exports/drc.json boards/rear-io-A11/rear-io-A11.kicad_pcb
python3 tools/review_electrical_A11.py --board-dir boards/rear-io-A11 --reports boards/rear-io-A11/exports --baseline boards/rear-io/rear-io.kicad_pcb
kicad-cli pcb export step --drill-origin --no-dnp --subst-models -o /tmp/rear-io-A11-raw.step boards/rear-io-A11/rear-io-A11.kicad_pcb
```

For rigid integration, execute `tools/export_electrical_A11_fusion.py` in Fusion with RAW set to that STEP, OUT to a fresh output directory and BOARD to this saved PCB. It creates temporary documents, flattens the assembly, applies the installation transform and verifies both reimports. The raw KiCad STEP is in board coordinates and is not the installed rigid deliverable.
