# A3 fit-study verification

2026-11-03 · KiCad 10.0.5. [Exact saved-source hashes and geometry checks](../boards/rear-io/exports/geometry-A3.json).

- Native KiCad parsed the saved PCB and exported STEP, DXF, SVG and renders. [DRC](../boards/rear-io/exports/rear-io-A3-drc.json): **0 violations / 0 unconnected items**, under recorded default exclusions. No nets exist, so this does not verify a circuit.
- Closed **228 × 32** outer board outline and two closed optical windows. **41 electrical pads**: speaker12 + RCA3 + HDMI26. Four additional NPTH holes belong to component fixing patterns; owner frame references remain drawing graphics.
- Two PT-603B straight-tail instances replace A2's KLS assemblies. Pin grid13 ×19.5, model alignment and rear pin projection3.4 checked. No downward extension beyond the 30 mm speaker body. Project-relative model paths resolve.
- Conservative front envelopes fit the measured **220 × 35 R5** opening without overlap. Owner references x−115,z44/59 match the read-only Fusion snapshot.
- The A3 assembly STEP reimported into an unsaved Fusion document as **102 solid-body instances**, all solid. The temporary document was closed and the original Rear Panel v4 restored unchanged. [Import report](../boards/rear-io/exports/fusion-import-A3.json).
- Full-width front and angled native renders inspected. Optical child PCB source remains unchanged from A1.

This is not a full enclosure interference, tolerance, strength, thermal or electrical test. Current rating, supply and production pad/drill geometry remain unqualified. See [model assumptions](connector-selection-A3.md) and [mechanical limitations](rear-io-mechanical.md).

Reproduce saved-board checks with `python3 tools/check_connectors_A3.py`; export with `python3 tools/export_review.py` using installed KiCad CLI. The separate rebuild tool requires `--rebuild` and must not run over manual edits.
