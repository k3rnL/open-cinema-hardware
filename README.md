# Open Cinema Hardware

Editable hardware for [Open Cinema](https://github.com/k3rnL/open-cinema). The [resources repository](https://github.com/k3rnL/open-cinema-resources) owns searchable knowledge and decision history.

## Rear connector fit study — A3

The owner rejected A2's downward speaker pins because they approach the PSU. A3 uses **straight rear-facing terminals through the vertical PCB**, with the owner's updated **220 × 35 mm R5 opening**. Surface-mount construction is not required to achieve this direction.

![A3 connector assembly](boards/rear-io/exports/rear-io-A3-oblique.png)

| Qty | Interface | Reference / status |
| --- | --- | --- |
| 2 | Six-contact red/black speaker block | **Dragon City PT-603B** — mechanical candidate; current rating and small-quantity supply unconfirmed |
| 2 | Optical receiver, each on a small horizontal daughterboard | Cliff **FCR684205R / ORJ5** |
| 1 | Coaxial S/PDIF RCA | Same Sky **RCJ-021** |
| 1 | Vertical HDMI Type A | Amphenol FCI **10078837-001LF** |

Open [rear-io.kicad_pro](boards/rear-io/rear-io.kicad_pro) in KiCad 10. The **228 × 32 × 1.6 mm vertical PCB** carries twelve provisional speaker pads, RCA and HDMI. Optical assembly instances point to the separate [optical daughterboards](boards/optical-input). Speaker STEP models are project reconstructions from the manufacturer drawing, not vendor CAD.

[Speaker selection, drawing and assumptions](docs/connector-selection-A3.md) · [Audio-input sources](docs/connector-selection-A1.md).

## Integration files

- [A3 assembly STEP for Fusion](boards/rear-io/exports/rear-io-A3-assembly.step)
- [A3 PCB-only STEP](boards/rear-io/exports/rear-io-A3-board-only.step)
- [A3 PCB outline DXF](boards/rear-io/exports/rear-io-A3-outline.dxf)
- [A3 layout SVG](boards/rear-io/exports/rear-io-A3-layout.svg)
- [A3 exterior view](boards/rear-io/exports/rear-io-A3-front.png)
- [Mechanical coordinates and fit limits](docs/rear-io-mechanical.md)
- [Verification and source hashes](docs/verification-A3.md)

**Placement study only.** No nets, tracks, schematic, decoding, LVDS or speaker-current distribution. Manufacturer current rating, supply, sample dimensions, final drills, support, connection-plate apertures and full enclosure clearance need qualification before purchase or fabrication. Owner frame-fixing references remain graphics only; the four new component-mounting holes belong to the speaker footprints, not the frame.

A0–A2 exports remain historical. A1 industrial terminals and A2 downward-tail speaker blocks are rejected. [A2 mechanical history](docs/rear-io-mechanical-A2.md).

## Working on the project

Keep this checkout beside `open-cinema-resources` in `Documents/Open Cinema`; use its memory skill. All models resolve through project-relative paths.

`tools/check_connectors_A3.py` checks saved geometry and native DRC evidence. `tools/export_review.py` exports the saved A3 board. `tools/revise_rear_io_A3.py --rebuild` explicitly rebuilds the fit study using saved input footprints; do not run it over manual edits. Older tools are historical and require explicit flags.

## License

No project hardware license has been selected. Rights remain with contributors. Historical Phoenix files retain their [KiCad attribution](docs/sources/README.md). Drawing-derived connector models are project-authored, not manufacturer-supplied CAD.
