# A9 — PCB and connectors only

On 2026-11-03 the owner requested: “I'll do the backplate and the "L"s myself. remove them from PCB model”. A9 removes exactly three solids from the integration model: the provisional backplate and the two L brackets. The owner will design these enclosure parts independently.

The current deliverables are [rigid STEP](../boards/rear-io/exports/rear-io-A9-rigid.step) and [Fusion archive](../boards/rear-io/exports/rear-io-A9-rigid.f3d). Each contains one component, 67 solid bodies and no child occurrences. All connectors remain directly mounted to the horizontal PCB. Coordinates, connector placement and the four Ø3 PCB mounting holes are unchanged. Hole centers are x±110 mm and 12/30 mm inward from the plate-inner-face datum. The former four vertical plate holes are not PCB holes and disappear with the removed mechanical parts.

The PCB remains the A8 electronic/mechanical layout: no KiCad footprint, copper, board outline or pad edits were needed. Its component side faces down at z67 mm, with solder tails up. Use the actual PCB holes or connector geometry to align the board to the owner's supports. The old plate-inner-face plane remains the coordinate datum only; no plate is included. A9 installed exports retain the same +102 mm Y translation into Home Cinema. The legacy-frame STEP retains the existing linked source's original axes.

## Verification

Both A9 formats were reimported and compared with the prior PCB-and-connectors-only geometry. All 67 solid volumes and bounding boxes match at the recorded precision; one component and zero child occurrences were verified. The KiCad file hash is unchanged. No new electrical tests were needed for removal of three enclosure solids. Evidence: [geometry checks](../boards/rear-io/exports/geometry-check-A9.json).

The existing source component was updated by deleting only the identified plate/bracket bodies. Its 67 retained body volumes were unchanged. The owner’s rear frame and other enclosure parts were not removed. Previous A8 plate/support exports are retained as historical evidence, not current deliverables. `build_integration_A9_fusion.py` rebuilds the current export without adding enclosure parts; the older A8 generator is historical.

## Fusion status

The open `rear-io-A5-assembly` source now contains the 67-body PCB-only model. The earlier source cloud-save problem remains unresolved at this writing: Save returned without creating a new version, and the source is still modified at cloud v2. No close/discard recovery was attempted. The standalone exports are saved and verified; the live source cloud update must not be described as complete. The prior parent v3/Home Cinema v8 saves do not prove source persistence. Private pre-removal and current-source backups are retained outside Git.

Speaker current-rating/supply qualification and the recessed RCA cable fit remain open as documented in [A8](horizontal-assembly-A8.md). Removing supports does not qualify the board, connectors, thermal behavior or future mounting hardware for manufacture.
