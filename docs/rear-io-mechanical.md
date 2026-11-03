# Rear I/O mechanical integration — A4

2026-11-03 · millimetres · fit study, no released manufacturing tolerances.

The owner rejected downward speaker terminals near the PSU and supplied a **220 × 35 R5** opening. Read-only measurement of the updated Fusion Sketch3 confirms **z34…69**, not A2's assumed z39…74. [Original evidence](../mechanical/reference/README.md). The assistant did not edit the owner's frame.

## Coordinates and placements

Exterior rear view: x right, z up, origin at panel bottom centre. STEP X = rear x, STEP Y = rear z, STEP Z = outward main-PCB normal. Use the Sketch3 basis, not the reversed Sketch2 X.

| Feature | A3 geometry | Status |
| --- | --- | --- |
| Frame opening | x−110…110, z34…69, R5 | Updated owner geometry, measured read-only |
| Main PCB body | x−114…114, z37…69, R2; 228 × 32 × 1.6 | Vertical, F.Cu toward exterior |
| Alignment tabs | R4, centres x−115,z44/59; leftmost x−119 | Overall PCB width233; provisional |
| Speaker centres | x−77 / −21, z52 | Two Dragon City PT-603B, six contacts each |
| Speaker bodies | 30 high, z37…67 | Straight tails point behind PCB, not down |
| Speaker pin grid | 13 column pitch × 19.5 row pitch | Two rows of three; numbering project-defined |
| Optical assemblies | x28 / 48, optical axis z50.5 | A1 parts and horizontal child boards retained |
| RCA / HDMI | x65 / 88, z51.5 | A1 pads/models retained |
| Optical windows | 17 wide, z39.9…64, R0.5 | Child supports and interconnects undecided |
| Owner alignment holes HREF1/HREF2 | x−115,z44/59, Ø3 | Real non-plated holes through PCB; provisional mounting |

A4 restores the owner-requested alignment holes as actual STEP geometry. Each left tab has a 4 mm outer radius around a Ø3 hole, leaving nominal 2.5 mm radial material. The tab geometry is a project fit allowance, not a chosen fastening system. There are no added mirrored holes. Connector footprints and placements are identical to A3.

The straight speaker pins project **3.4 mm behind the component seating plane**, perpendicular to the board. The speaker body stays within the opening's height. This solves the rejected downward-tail geometry; it does not establish full PSU clearance.

## Attachment and depth

The PT-603B reconstruction places the flange front **9.6 mm outward** from its PCB seating plane and the mating face **21.1 mm outward**. Flange thickness is 2 mm. The face and flange differ from the audio-input projections, so a final connection-plate setback/cutout arrangement is still needed. No plate cut file is supplied.

Each speaker footprint includes six provisional Ø2.2 signal drills and two Ø3.2 component-fixing clearance holes at 45 mm pitch. The manufacturer gives a panel-cutout pattern, not a PCB pad recipe; these PCB drills and pad sizes remain project assumptions pending samples. The component fixing holes are separate from the owner's Ø3 frame references. Neither the assembly fastening stack nor support against cable/finger loads is selected.

Speaker-current paths and amplifier harness remain deferred. Six pairs are illustrative; verify supplied colour arrangement and channel assignment. Keep twelve independent conductors; do not common negative contacts or chassis by assumption.

## Fit limits

- Conservative front package envelopes fit the measured 220 × 35 R5 opening without overlap. This excludes plug/finger travel, wiring bends and manufacturing tolerances.
- The upper frame holes at x±40,z75, Ø4.5 have lower edges at z72.75, **3.75 mm above** the opening top69. A2's upper-hole intersection is superseded by this actual geometry. This is not a fastening-strength assessment.
- PCB bottom37 is 4 mm above the old PSU-top line33 in projection. Actual depth, solder clearance, insulation, airflow and thermal performance are unverified.
- Frame thickness 2 mm versus the 3 mm material baseline, and Ø4.5 frame holes versus nominal Ø3.8 baseline, remain open.
- PT-603B current rating, obtainable quantity, sample geometry and production footprint qualification are open. [Selection evidence](connector-selection-A3.md).
- No full enclosure interference check, electrical function, thermal test or proof of available area for future eARC/LVDS logic is claimed. Mains remains separate.

[A2 geometry and rejected downward-tail approach](rear-io-mechanical-A2.md) remain historical.
