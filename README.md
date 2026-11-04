# Open Cinema Hardware

Editable hardware for [Open Cinema](https://github.com/k3rnL/open-cinema). The [resources repository](https://github.com/k3rnL/open-cinema-resources) holds searchable knowledge and decision history.

## Current work: A11 ARC electrical study

[Open A11](boards/rear-io-A11/README.md). The draft connects an **ADV7511 ARC candidate → CS8416 four-source selector → three-pair LVDS link → Raspberry Pi**. The Pi decodes/processes audio and sends output by USB to the amplifier. Optical ×2, coax, HDMI and six speaker pairs remain on one horizontal board.

- [Editable KiCad project](boards/rear-io-A11/rear-io-A11.kicad_pro)
- [Schematic PDF](boards/rear-io-A11/exports/rear-io-A11-schematic.pdf)
- [Rigid STEP for Fusion](boards/rear-io-A11/exports/rear-io-A11-rigid.step) / [Fusion archive](boards/rear-io-A11/exports/rear-io-A11-rigid.f3d)
- [Part references and sourcing](boards/rear-io-A11/sourcing.md), [circuit/interface requirements](boards/rear-io-A11/requirements.md), [verification](boards/rear-io-A11/verification.md)

![A11 electronics underside](boards/rear-io-A11/exports/rear-io-A11-installed-underside.png)

**This is an unrouted prototype draft, not ready to order.** Two static review passes found zero ERC and zero geometry-DRC violations, but 318 connections remain unrouted. ARC/CEC startup, DD+ Atmos payload preservation and Pi capture have not been demonstrated. ADI specifies an HDMI-adopter purchasing condition for ADV7511; JLC listing C179459 does not settle eligibility. Horizontal KLS speaker-terminal current rating and supply are still unqualified.

The [accepted ARC scope](docs/arc-v1-requirements.md) defers eARC/lossless return audio while retaining DD+ Atmos as a validation target. A11 does not claim those tests have passed.

## Mechanical integration

A11 preserves the 228 × 39.8 × 1.6 mm PCB, connector positions and four Ø3 holes at installation x ±110 mm, depths 12/30 mm. Its rigid files contain one component with 161 solid bodies and no child components. Both formats were reimported and geometry-checked. The owner designs the backplate and L brackets; neither is included. Mains remains separate.

The latest owner opening is 250 × 51 mm. Clearance, airflow, cable access, tolerances and thermal/EMI behavior in that enlarged enclosure remain to be checked. The new files are in the previous component-down installation datum, nominal z 67 mm.

The linked `rear-io-A5-assembly v2` contained unsaved owner edits when inspected. This session exported A11 separately and did not overwrite/save it or the enclosure. Git publication does not update that Fusion cloud component automatically.

## Previous revisions and reproducibility

- [A10 electrical draft](boards/rear-io-A10/README.md): historical optical/coax, muxes and LVDS; HDMI unwired.
- [A9 PCB/connector mechanical baseline](docs/pcb-only-assembly-A9.md) and [A8 horizontal connector study](docs/horizontal-assembly-A8.md). Their old clearance results do not qualify the enlarged enclosure or A11.
- [Original mechanical KiCad project](boards/rear-io/rear-io.kicad_pro): manual edits preserved.
- [A7 vertical design in Git history](https://github.com/k3rnL/open-cinema-hardware/tree/eae54aa79c94255bdad5aaae5bf087d2b4166b0e).

JLCPCB is preferred; pre-order/Global Sourcing and external suppliers are allowed. No purchase or supplier contact is authorized by a catalogue audit. Do not regenerate over manual edits. A11 has [reproduction instructions](boards/rear-io-A11/verification.md).

No project hardware license has been selected. Redistributed KiCad assets retain their [attribution and license](docs/sources/README.md).
