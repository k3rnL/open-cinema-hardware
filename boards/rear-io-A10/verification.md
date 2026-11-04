# A10 verification — two review passes

> **Scope update, 2026-11-04:** next implementation targets [standard ARC](../../docs/arc-v1-requirements.md), including DD+ Atmos, with eARC/lossless HDMI deferred. The circuit, exports and tests below describe unchanged A10. HDMI remains unwired; no ARC receiver/controller is selected yet.

KiCad 10.0.5, 2026-11-03. Exact source hashes are in [review-two-passes.json](exports/review-two-passes.json). These are two static reviews by the same assistant, not two independent engineers or a physical test.

## Pass 1: electrical schematic

Compared CS8416 TSSOP, LVC157, LVDS transmitter and regulator pin functions against manufacturer datasheets. Checked the software-mode/address straps, input AC coupling, 75Ω coax termination, PLL network, decoupling, reset/enable defaults, six clock/data selections, LVDS polarities and independent speaker returns. Rendered and visually inspected the schematic sheets. The separate review script checks the exported KiCad netlist, rather than merely rerunning the builder. **ERC: 0 violations**, with no blanket ERC exclusions.

The source review identified the 100 kHz I2C limit, requirement for 47 kΩ startup straps, 16 Mbps optical ceiling, required 30 pF optical loading capacitor and the risk of default receive-error sample substitution. These are captured in requirements.md. Configuration values remain bench-test requirements, not tested firmware.

## Pass 2: PCB/interface/model consistency

Compared 275 distinct electrical pad keys to the separately exported schematic; verified 62 footprints, four layers, all four retainedØ3holes and 56 resolved model links. Corrected initial placement overlaps and missing model references. **PCB geometry/clearance/courtyard DRC: 0 violations.** There are **186 unrouted connections**, zero tracks and no completed planes. This is explicitly not a clean routed-board sign-off.

STEP and F3D exports were each reimported in Fusion: 114 solid bodies, zero child components, matching per-body volume and bounds. Existing user documents were not edited or saved. Generic headers are illustrative; DNP parts are omitted from the model. Package models are KiCad library assets; existing connector reconstructions retain their prior uncertainty.

## What has not passed

HDMI/eARC circuitry is absent. Full lossless/Atmos extraction, HBR/MAT word mapping, actual Pi capture, powered switching behavior, voltage sequencing/back-powering, receiver-side timing/skew, cable mating and strain relief, speaker current/PCB heating, coax/HDMI ESD, PSU EMI/airflow/thermal interaction and enlarged-enclosure fit have not been tested. The local regulator cannot be assigned an eARC load without a new power budget.

**Original A10 status: draft; blocked for fabrication.** Obtain the full eARC design package before freezing board size or commissioning PCBA. A functional prototype will still need routing, complete protection and the measurements above.

For the next ARC revision, the eARC-specific design-package requirement above is superseded by the [ARC contract](../../docs/arc-v1-requirements.md). The physical verification gaps remain; no manufacturing approval follows from the scope change.
