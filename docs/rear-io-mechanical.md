# Rear I/O mechanical integration — A2

2026-11-03 · mm · placement study, no released fabrication tolerances.

The owner requires conventional red/black speaker clips and permitted a taller opening. A2 uses two **L-KLS1-WP-6P-03B-B/R** six-contact blocks for mechanical evaluation. [Sources and part qualifications](speaker-clips-correction.md). A1's Phoenix terminals are rejected; [A1 geometry](rear-io-mechanical-A1.md) remains historical.

## Coordinates

Exterior rear view: x right, z up, origin at panel bottom centre. STEP X = rear x, STEP Y = rear z, STEP Z = outward main-PCB normal. Keep the earlier Sketch3 basis; do not reuse reversed Sketch2 X.

| Feature | A2 geometry | Status |
| --- | --- | --- |
| Owner frame | x ±130, z0…80 | Original CAD unchanged |
| Opening | x ±105, z39…74, R5 | Owner permits growth; A2 study only |
| Input PCB | x15…114, z37…69; 99 × 32 × 1.6 | Vertical, F.Cu faces exterior |
| Speaker centres | x−77 and −21, z56.5 | Two six-contact blocks; panel-supported |
| Speaker front envelope | Each 52 × 30 | Nominal drawing dimensions |
| Speaker tail lower extent | z36 nominal | Below opening; clearance unresolved |
| Optical assemblies | x28/48, optical axis z50.5 | Same A1 parts and daughterboards |
| RCA and HDMI | x65/88, z51.5 | Same A1 pads/models |
| Optical board windows | 17 wide, z39.9…64, R0.5 | Same A1 cutouts |
| Owner fixing references | x−110,z44/59, Ø3 | Graphics only; no PCB drill |

The input PCB no longer runs behind the speaker clips. This accommodates the actual rear body/tails and lets speaker current go directly to the amplifier through separate wiring. The six pairs are illustrative column pairs; exact terminal colour order, channel labels and harness pinout remain unverified. No common negative/chassis return is assumed.

## Mounting and depth

Speaker blocks are **mechanical assembly footprints**, without invented solder pads on the vertical input PCB. Their right-angle tails require independent insulated termination and strain relief if handwired. No daughterboard for these tails or rear harness is designed. The KLS drawing's PCB pattern is not rotated into an invalid vertical footprint.

For visual integration only, speaker flange front is 12.95 mm outward from the main-PCB seating surface, with assumed flange back at 10.45. Flange thickness and rear details are simplified in the reconstructed model. The audio mating projections remain RCA15.8 / HDMI10.45 / optical10.45. These are not a chosen plate stack or a validated flush mounting scheme. No connection-plate cut file is supplied.

The narrower input board needs new supports. Optical daughterboards still need retention and interconnects. The owner-supplied frame fixing references do not automatically become PCB mounts.

## Known frame conflicts and remaining checks

- Enlarging upward to z74 intersects the original **Ø4.5 frame holes at x±40,z75**: their lower edge is z72.75. Relocate/rework those fixings before editing or cutting the frame. The original Fusion design is unchanged.
- KLS tails reach z36 below the opening bottom z39. Their depth relative to the frame, insulation and wire bends require explicit clearance checks; a nominal front-face fit does not resolve this. The old PSU-top line is z33, only 3 mm lower in projection, not a validated electrical/thermal gap.
- Front package rectangles fit the 210 × 35 R5 opening at nominal dimensions without overlapping. Finger travel, plugs, tolerances, plate support and the complete enclosure are unverified.
- The KLS operating current rating is absent from the inspected drawing. Obtain evidence and test representative samples before ordering or designing speaker-current paths.
- Existing frame thickness 2 mm versus the 3 mm material baseline, and outer holes Ø4.5 versus nominal Ø3.8 baseline, remain open. Mains stays separate.

The input circuitry and eventual board area need review later; A2 is not a claim that all eARC/LVDS logic fits the smaller PCB.
