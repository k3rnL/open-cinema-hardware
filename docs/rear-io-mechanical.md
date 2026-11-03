# Rear I/O mechanical integration — A7

2026-11-03 · millimetres · fit study, no released manufacturing tolerances.

The owner rejected downward speaker terminals near the PSU and supplied a **220 × 35 R5** opening. Read-only measurement of the updated Fusion Sketch3 confirms **z34…69**, not A2's assumed z39…74. [Original evidence](../mechanical/reference/README.md). The assistant did not edit the owner's frame.

## Coordinates and placements

Exterior rear view: x right, z up, origin at panel bottom centre. STEP X = rear x, STEP Y = rear z, STEP Z = outward main-PCB normal. Use the Sketch3 basis, not the reversed Sketch2 X.

| Feature | A7 geometry | Status |
| --- | --- | --- |
| Frame opening | x−110…110, z34…69, R5 | Updated owner geometry, measured read-only |
| Main PCB body | x−114…114, z37…69, R2; 228 × 32 × 1.6 | Vertical, F.Cu toward exterior |
| Alignment tabs | R4, centres x±115,z44/59; outer extents x±119 | Overall PCB width 238; provisional |
| Speaker centres | x−77 / −11, z52 | Two Cliff FE6930, eight contacts each |
| Speaker bodies | 30 high, z37…67 | Straight tails point behind PCB, not down |
| Speaker pin grid | 13 column pitch × 18.6 ±1 row spacing | Two rows of four; front-view numbering from Cliff drawing |
| Optical assemblies | x32 / 52, optical axis z50.5 | A1 receivers retained; A6 supported horizontal child boards |
| RCA / HDMI | x69 / 91, z51.5 | A1 pads/models retained |
| Optical windows | 17 wide, z39.9…64, R0.5 | A6 cradle added; electrical interconnect deferred |
| Owner alignment holes HREF1–HREF4 | x±115,z44/59, Ø3 | Real non-plated holes through PCB; provisional mounting |

A7 preserves all four owner alignment holes and the main outline. Each tab has a 4 mm outer radius around a Ø3 hole. Speaker/RCA/HDMI and optical positions follow the table above. The A6 optical cradle and all its holes move 4 mm right; the physical part remains unchanged. The optical windows follow their sockets. Fastening to the connection plate is still provisional.

Straight speaker tails extend 3.5 mm behind the component seating plane, normal to the board. They do not extend below the body toward the PSU; this alone does not establish full PSU clearance.

## Optical support and Fusion placement

Use the A7 rigid STEP/F3D, not the raw KiCad component hierarchy, for enclosure joints. The new optical cradle bolts to the main PCB and both child boards and captures the receiver mounting lugs. See [assembly instructions](assembly-and-optical-support-A7.md), [verification](verification-A7.md) and [sourcing](sourcing-A7.md). The support is a modeled prototype pending material, tolerance, thermal and load validation.

## Attachment and depth

The FE6930 flange front is 9.5 mm outward from its PCB seating plane; the highest lever is 23.5 mm outward, with 2 mm flange thickness. Different input connectors have different projections. Final plate setback, connector cutouts and screw stack are still required; no plate cut file is supplied.

Each FE6930 footprint has eight provisional plated slots 2.2 ×3.2 and two Ø3.2 component fixing holes at 58 mm pitch. These are project-derived lands, not a vendor production footprint. See [drawing, mapping and tolerances](connector-selection-A7.md). Main-board component fixing holes remain distinct from the owner's Ø3 alignment holes.

Six working pairs plus two spare pairs give sixteen independent contacts. Current paths and amplifier harness remain deferred; do not common negatives or chassis by assumption.

## Fit limits

- Nominal modeled connector outlines fit the measured 220 × 35 R5 opening without overlap. The left speaker ear has 0.5 mm nominal clearance; adjacent speaker ears have 1 mm. This excludes plug/finger travel, wiring bends and manufacturing tolerances.
- The upper frame holes at x±40,z75, Ø4.5 have lower edges at z72.75, **3.75 mm above** the opening top69. A2's upper-hole intersection is superseded by this actual geometry. This is not a fastening-strength assessment.
- PCB bottom37 is 4 mm above the old PSU-top line33 in projection. Actual depth, solder clearance, insulation, airflow and thermal performance are unverified.
- Frame thickness 2 mm versus the 3 mm material baseline, and Ø4.5 frame holes versus nominal Ø3.8 baseline, remain open.
- FE6930 is selected with a published 7 A rating and a distributor source. Physical sample geometry, plated slots, solder process, attachment loads and full production qualification remain open. [Selection evidence](connector-selection-A7.md).
- No full enclosure interference check, electrical function, thermal test or proof of available area for future eARC/LVDS logic is claimed. Mains remains separate.

[A2 geometry and rejected downward-tail approach](rear-io-mechanical-A2.md) remain historical.
