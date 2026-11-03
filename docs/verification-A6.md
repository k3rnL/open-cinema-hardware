# A6 verification — supported optics and rigid Fusion insertion

2026-11-03. Mechanical prototype only. KiCad10.0.5 native CLI and local Fusion360 API. [Exact file hashes](../boards/rear-io/exports/geometry-A6.json).

- Main and optical daughterboard native DRC: zero violations. No nets, routes or circuit exist; this is not electrical validation.
- Main board now has41 electrical pads and12 non-plated holes: four speaker component fixings, four retained Ø3 owner alignment holes, and four new Ø2.2 cradle attachments. Each child gets two Ø2.2 rear mounting holes.
- Speaker, RCA and HDMI footprint contents are unchanged from A3. Optical positions and main outline are retained. J7/J8 refer to the supported child models; CRADLE1 is mechanical-only and excluded from placement/BOM exports.
- The raw STEP contains123 solid instances (A5's102 plus the cradle and20 simplified screws/nuts). The rigid STEP and F3D have123 root bodies and **zero child occurrences**. Flattening preserves each body bounding box. F3D was reimported and its structure checked too.
- Fusion measured all four alignment-hole centres: (−115,44),(−115,59),(115,44),(115,59), radius1.5mm.
- A temporary Fusion host placed the imported solids in one occurrence, disabled Ground to Parent, and created a rigid joint from HREF1 to an offset fixture hole. **All123 bodies moved**, and a vertex on every body matched the single occurrence transform. [Machine-readable result](../boards/rear-io/exports/fusion-integration-A6.json).
- Fusion interference analysis found **no positive-volume overlap involving the cradle** and the modeled connector assembly. [Result](../boards/rear-io/exports/cradle-interference-A6.json). This deliberately does not certify pre-existing simplified connector solids, real parts, the connection plate, PSU or enclosure.
- KiCad front/oblique renders and an isolated Fusion inside view were visually inspected. Original user Fusion documents were restored without editing/saving them.

## Reproduce

1. From the saved boards, run `python3 tools/export_review.py` with native KiCad10 installed.
2. In Fusion, run `tools/build_rigid_integration_fusion.py` with `SOURCE_STEP` pointing to the raw A6 assembly and `OUTPUT_PREFIX` to `rear-io-A6-rigid`.
3. In Fusion, run `tools/verify_rigid_A6_fusion.py` with `CHECK_ROOT` pointing to this repository. It uses and closes an unsaved temporary test document.
4. Run `python3 tools/check_connectors_A6.py`. It checks geometry, unchanged connector footprints, relative model paths, DRC and Fusion evidence and records source/export hashes.

`tools/add_optical_support_A6.py` is a one-time A5-to-A6 migration; it refuses to run twice. `tools/build_optical_support_A6_fusion.py` reconstructs the prototype support and child models with `MODEL_OUTPUT_DIR` set to `boards/rear-io/models`. Do not run old rebuild/migration tools over manual changes. Historical A0–A5 evidence is retained.

No load, thermal, tolerance or complete-enclosure test has passed. PA12 process acceptance, the approximately0.4mm nominal RCA-tail gap, speaker supply/current rating and final production footprints remain open. See [assembly limits](assembly-and-optical-support-A6.md) and [sourcing audit](sourcing-A6.md).
