# A5 alignment holes on both sides

2026-11-03 · KiCad 10.0.5. [Saved-source hashes and geometry checks](../boards/rear-io/exports/geometry-A5.json).

The owner clarified that alignment holes are required on both sides. A5 mirrors A4's left pair onto the right: **four Ø3 mm NPTH holes at x±115,z44/59**, 230 mm between sides and 15 mm vertically. R4 tabs make the overall board extent238 ×32 mm; the main body remains228 ×32. These remain provisional mounting features.

Native DRC reports zero violations with the recorded defaults. Closed outlines and all four hole positions are checked; the six connector footprints, pads, models and positions remain identical to A3. Both assembly and board-only STEP exports were imported into temporary Fusion documents and all four Ø3 cylindrical hole faces measured at their intended coordinates. The assembly has102 solid-body instances. [Fusion evidence](../boards/rear-io/exports/fusion-import-A5.json). The original owner document was restored unchanged.

The native front render shows the matching pairs. No full enclosure interference, fastening-strength or electrical validation is claimed. Reproduce saved-board checks with `python3 tools/check_connectors_A5.py`; exports with `python3 tools/export_review.py`.
