# A12 manufacturing review — HOLD

**NOT RELEASED FOR ORDERING.** This folder is for DFM, assembly review and prototype planning. Zero DRC does not establish that the ARC implementation works or that the speaker clips are suitable.

## Contents

- `gerbers/`: four copper layers, front/back masks and paste, silkscreens and board outline; separate plated/non-plated drill files and drill maps.
- `rear-io-A12-gerbers-REVIEW-ONLY.zip`: the same fabrication data with this hold notice and stackup.
- `bom-all-review.csv`: all implemented circuit/connector references, DNP and manual solder terminations.
- `bom-smt-review.csv` / `cpl-smt-review.csv`: SMT-only assembly candidates; DNP omitted. Catalogue IDs are populated only where already identified.
- `positions-kicad.csv`: native position export for comparison.
- `SHA256SUMS`: source/export identities for stale-file checks.

## Fabrication assumptions

228 × 39.8 mm, nominal 1.6 mm FR-4, four layers, outer 1 oz / inner 0.5 oz, ENIG, green mask and white silkscreen, through vias 0.30 mm drill / 0.60 mm diameter. Minimum routed width/clearance 0.15 mm; minimum copper-to-edge 0.30 mm. No blind/buried vias. Use [the specified stackup and impedance request](stackup.md); supplier approval/coupon remains required.

Gerbers, drill data and CPL share the KiCad auxiliary origin at board coordinates (150,100) mm. Negative coordinates are intentional. **Do not mirror the artwork.** All populated parts are on Top/F.Cu; mounting the whole board upside down in the enclosure does not change the assembly side.

Validate pin 1, diode orientation, optical connector pin numbering, vendor footprint/model tolerances, SMT centroid/rotation mapping and every through-hole operation with the assembler. Generic KiCad rotations are not automatically JLC's part rotations. Through-hole connectors, headers and speaker wires require separate assembly planning. DNP R1/R2/R51 must remain unpopulated unless the interface/grounding plan is revised.

## Release conditions

See [bring-up and release gates](../bring-up.md). Before committing a board order, settle ADV7511 eligible supply and prove the required ARC/DD+ mode on documented evaluation hardware or a controlled prototype plan; confirm the speaker clips' current rating and actual dimensions; review final component substitutions and enclosure clearances. A production release additionally requires powered audio, thermal, current, EMI/ESD and hotplug testing. This package neither places an order nor grants test results.
