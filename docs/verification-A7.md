# A7 verification — FE6930 fit model

2026-11-03, KiCad 10.0.5 and local Fusion 360 API. [Exact file hashes and results](../boards/rear-io/exports/geometry-A7.json).

- Native main and optical board DRC: zero violations under saved settings. Main board: 45 electrical pads and 12 NPTH holes; no nets, tracks or circuitry. Optical child source unchanged from A6.
- Two eight-contact FE6930 footprints use the drawing's nominal pin/fixing coordinates and project-derived plated slots. Four owner Ø3 holes remain x±115,z44/59. A3 speaker pads are intentionally superseded.
- The [packing check](../boards/rear-io/exports/packing-A7.json) subtracts a solid representing the 220 ×35 R5 aperture from each connector body. No connector material lies outside the aperture projection. This includes the real ear outline, not an incorrect 65 ×30 rectangular flange assumption.
- No positive-volume intersection was found between new speaker blocks and other modeled assembly components (16 body pairs had overlapping bounding boxes), or between the optical cradle and modeled assembly. Internal cosmetic solids within a single component are outside that interference check.
- The left speaker ear has only 0.5 mm nominal aperture margin; speaker-to-speaker ear gap is 1 mm. Cradle/RCA-tail gap remains approximately 0.4 mm. These checks do not include real-part tolerances, plate setback, plugs, finger clearance or PSU/enclosure geometry.
- Raw STEP contains 135 solid instances. [Rigid STEP/F3D](../boards/rear-io/exports/rear-io-A7-rigid.step) contain 135 root bodies and zero child occurrences. Copies preserve bounding boxes; the F3D was reimported and its structure checked.
- A temporary rigid joint from HREF1 moved **all 135 bodies together**; a vertex on every body matched the single occurrence transform. All four alignment-hole centres/radii were measured. [Joint evidence](../boards/rear-io/exports/fusion-integration-A7.json).
- Front and oblique renders were inspected. Owner Fusion documents were restored without editing or saving them.

## Reproduce

1. Run `python3 tools/export_review.py` on the saved A7 boards.
2. In Fusion run `tools/build_rigid_integration_fusion.py`, with `SOURCE_STEP` set to the raw A7 assembly and `OUTPUT_PREFIX` to the A7 rigid path.
3. In Fusion run `tools/verify_rigid_A7_fusion.py` and `tools/verify_packing_A7_fusion.py`, each with `CHECK_ROOT` set to this checkout.
4. Run `python3 tools/check_connectors_A7.py` to check geometry/evidence and record hashes.

The one-time `revise_rear_io_A7.py --apply` migrates an A6 board and refuses an already-updated revision. `build_speaker_model_A7_fusion.py` reconstructs the drawing-derived model, with `MODEL_OUTPUT_DIR` set to the models folder. Preserve manual edits and historical artifacts.

No full enclosure, sample, solder-process, load, temperature, airflow, electrical or production qualification is claimed.
