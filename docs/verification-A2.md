# A2 fit-study verification

2026-11-03 · KiCad 10.0.5. Exact source/model SHA-256 values: [geometry-A2.json](../boards/rear-io/exports/geometry-A2.json).

- Saved native PCB parsed and exported by KiCad; native DRC returned **0 violations / 0 unconnected items** with the default exclusions listed in its [report](../boards/rear-io/exports/rear-io-A2-drc.json). No nets exist, so this does not validate circuitry.
- Closed 99 × 32 outer perimeter and two closed optical windows; 29 main electrical pads (RCA3 + HDMI26). SP1/SP2 and optical assemblies are mechanical instances without main-board pads.
- Six rejected Phoenix instances are absent; two KLS six-contact blocks are present. Project-relative STEP paths resolve. Nominal front package bounds do not overlap and fit the proposed 210 × 35 R5 opening.
- A2 assembly STEP reimported into an unsaved Fusion document: **96 solid-body instances**. The temporary document was closed and the original Rear Panel v4 document restored unchanged. This was an import test, not full enclosure interference analysis.
- Full-width front and angled native KiCad renders inspected. Optical child source is unchanged from A1; previous verification applies only to that unchanged source.

Known failures of integration: enlarged opening intersects old upper frame fixing holes; speaker tails descend below the opening and need depth/insulation review. Current rating, wire access, attachment, exact supplier variant and full enclosure checks remain open. No fabrication approval is implied.

Reproduce saved-board checks with `python3 tools/check_connectors_A2.py`; export with `python3 tools/export_review.py` using installed KiCad CLI. Both are read/export workflows; the separate rebuild script requires an explicit flag.
