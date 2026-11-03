# A1 mechanical verification

2026-11-03 · KiCad 10.0.5 · current saved A1 boards.

## Completed checks

- Both native KiCad boards load; model files resolve through project-relative paths.
- Main outline is 228 × 32 R2 with two 17 × 24.1 R0.5 optical windows. All outline/window endpoints join.
- Main board has 53 connector pads: six four-tail/two-pole terminals, three RCA tails, 21 HDMI tails and five shell stakes. J7/J8 are mechanical optical-assembly instances with no main-board pads.
- The child board has the receiver's three plated signal holes and three nonplated locating holes. Two instances are included in the full assembly.
- The owner fixing points are graphics only. No corresponding mounting drills or inferred mirrored holes were added.
- Independent nominal package-envelope checks fit all connectors within the 210 × 25 R5 opening with no projected body overlaps. These do not include plug/tool access or a manufacturing tolerance stack.
- Native DRC reports **zero violations and zero unconnected items** on both boards. There are no circuit nets, so this does **not** validate connectivity or electrical behavior. Default ignored severities remain listed in the reports.
- Main assembly STEP imported into a temporary Fusion document: **88 solid-body instances** including main PCB, six spring terminals, RCA, HDMI and both complete optical modules. Bounds agree with placements. The original `Rear Panel v4` document was restored without modification. No full-enclosure interference analysis was performed.
- Board-only STEP, outline DXF, placement SVG and native KiCad front/oblique renders were exported. Both renders were visually inspected for all connectors, labels and windows.

Evidence: [native geometry check and PCB hashes](../boards/rear-io/exports/geometry-A1.json), [main DRC](../boards/rear-io/exports/rear-io-A1-drc.json), [child DRC](../boards/optical-input/optical-input-A1-drc.json), [Fusion STEP import and STEP hash](../boards/rear-io/exports/fusion-import-A1.json).

## Important limits

No schematic, routing, prototype, electrical test or manufacturing files are provided. Final footprint/pad-stack/stencil review remains, particularly the HDMI pin-in-paste process. Three custom connector models reconstruct manufacturer drawing geometry and simplify cosmetic details; they are not vendor-certified CAD.

The optical mounting tab is only 0.5 mm below the opening top at nominal dimensions. Its lead length also has ±0.5 mm tolerance. Plate thickness/setback, receiver mounting, child-board support/interconnect, main-board stiffness, mating cables, terminal actuation and the complete enclosure fit remain unverified. Above-PSU heat, airflow and electrical separation remain separate validation work.

## Recheck

Run `tools/check_connectors.py` with a Python interpreter providing `pcbnew`. On macOS KiCad 10 this is the app's bundled `Python.framework/Versions/3.9/bin/python3.9`. Run `python3 tools/export_review.py --cli <path-to-kicad-cli>` to export the saved sources without regeneration. Recheck hashes after design changes; exports and reports become stale when their inputs change.

`tools/generate_connectors.py` rebuilds the A1 seed, footprints and placement files and can overwrite manual edits. It currently loads the installed macOS KiCad Phoenix source footprint; opening and exporting the saved projects requires only the included project libraries/models. The guarded historical A0 generator retains drawing helper functions used by the A1 generator.

The bundled `pcbnew` interpreter emits a wx initialization diagnostic in standalone mode. Native CLI loading, DRC and exports independently succeeded.
