# A4 alignment-hole verification

2026-11-03 · KiCad 10.0.5. [Saved source hashes and checks](../boards/rear-io/exports/geometry-A4.json).

The owner requested actual reference holes to align the imported assembly to the plate. A4 adds **two Ø3 mm non-plated holes at rear-view x−115,z44/59**, with R4 left tabs. The rectangular body remains228 ×32; the tabs extend overall width to233. The final fastener and support stack remain undecided.

- Native DRC: **0 violations / 0 unconnected items**, under the defaults recorded in [the report](../boards/rear-io/exports/rear-io-A4-drc.json). No electrical nets exist.
- Closed main outline and two optical windows checked. The six A3 connector footprints, including their positions, pads and models, are unchanged against [the A3 baseline hashes](../boards/rear-io/exports/alignment-baseline-A3.json).
- Both board-only and assembly STEP files were imported into temporary Fusion documents. Each contains **two real Ø3 cylindrical hole faces** at exactly (−115,44) and (−115,59) mm, with circular edges usable for alignment. The board-only bounds confirm x−119…114 and z37…69. The assembly has102 solid-body instances. [Fusion import evidence](../boards/rear-io/exports/fusion-import-A4.json).
- Native front render inspected: both left reference holes and tabs are visible. Original owner frame document restored unchanged.

No extra mirrored holes were added. These are alignment provisions, not final fastening approval. Connector qualification and full enclosure clearance limits from A3 still apply. Reproduce saved-board checks with `python3 tools/check_connectors_A4.py`; exports with `python3 tools/export_review.py`.
