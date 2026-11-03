# Open Cinema Hardware

Editable hardware for [Open Cinema](https://github.com/k3rnL/open-cinema). The [resources repository](https://github.com/k3rnL/open-cinema-resources) owns searchable knowledge and decision history.

## Rear connector fit study — A4

The owner rejected A2's downward speaker pins because they approach the PSU. A3 uses **straight rear-facing terminals through the vertical PCB**, with the owner's updated **220 × 35 mm R5 opening**. Surface-mount construction is not required to achieve this direction.

![A4 assembly with two alignment holes](boards/rear-io/exports/rear-io-A4-front.png)

| Qty | Interface | Reference / status |
| --- | --- | --- |
| 2 | Six-contact red/black speaker block | **Dragon City PT-603B** — mechanical candidate; current rating and small-quantity supply unconfirmed |
| 2 | Optical receiver, each on a small horizontal daughterboard | Cliff **FCR684205R / ORJ5** |
| 1 | Coaxial S/PDIF RCA | Same Sky **RCJ-021** |
| 1 | Vertical HDMI Type A | Amphenol FCI **10078837-001LF** |

Open [rear-io.kicad_pro](boards/rear-io/rear-io.kicad_pro) in KiCad 10. The **228 × 32 × 1.6 mm vertical PCB body**, now with two small left alignment tabs (233 mm overall width), carries twelve provisional speaker pads, RCA and HDMI. Optical assembly instances point to the separate [optical daughterboards](boards/optical-input). Speaker STEP models are project reconstructions from the manufacturer drawing, not vendor CAD.

[Speaker selection, drawing and assumptions](docs/connector-selection-A3.md) · [Audio-input sources](docs/connector-selection-A1.md).

## Integration files

- [A4 assembly STEP for Fusion](boards/rear-io/exports/rear-io-A4-assembly.step)
- [A4 PCB-only STEP](boards/rear-io/exports/rear-io-A4-board-only.step)
- [A4 PCB outline DXF](boards/rear-io/exports/rear-io-A4-outline.dxf)
- [A4 layout SVG](boards/rear-io/exports/rear-io-A4-layout.svg)
- [A4 exterior view](boards/rear-io/exports/rear-io-A4-front.png)
- [Mechanical coordinates and fit limits](docs/rear-io-mechanical.md)
- [Verification and source hashes](docs/verification-A4.md)

**Placement study only.** No nets, tracks, schematic, decoding, LVDS or speaker-current distribution. Manufacturer current rating, supply, sample dimensions, final drills, support, connection-plate apertures and full enclosure clearance need qualification before purchase or fabrication. The two owner reference points now have real **Ø3 mm non-plated holes**, at x−115,z44/59, to align the STEP model with the plate. They are provisional mounting geometry; the four speaker-component holes are separate.

A0–A3 exports remain historical. A1 industrial terminals and A2 downward-tail speaker blocks are rejected. [A2 mechanical history](docs/rear-io-mechanical-A2.md).

## Working on the project

Keep this checkout beside `open-cinema-resources` in `Documents/Open Cinema`; use its memory skill. All models resolve through project-relative paths.

`tools/check_connectors_A4.py` checks saved geometry and native DRC evidence. `tools/export_review.py` exports the saved A4 board. `tools/add_alignment_holes_A4.py --apply` applies the alignment update to an A3 board while preserving connector footprints; do not run historical rebuilds over the current design. Older tools are historical and require explicit flags.

## License

No project hardware license has been selected. Rights remain with contributors. Historical Phoenix files retain their [KiCad attribution](docs/sources/README.md). Drawing-derived connector models are project-authored, not manufacturer-supplied CAD.
