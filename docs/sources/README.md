# A1 source and license register

Numerical package/pad dimensions come from the manufacturer drawings linked in [connector selection](../connector-selection-A1.md), consulted 2026-11-03. Vendor PDFs are linked rather than redistributed. Original user screenshots live in `mechanical/reference`.

## KiCad material

`boards/rear-io/models/1732496.step` is copied from KiCad 10's `Connector_Phoenix_SPT.3dshapes/PhoenixContact_SPT_2.5_2-V-5.0-EX_1x02_P5.0mm_Vertical.step`.
`Phoenix_1732496.kicad_mod` derives from the matching KiCad footprint: drill diameters changed to 1.2 mm, model path made project-relative, identifier/description changed and reference/value visibility hidden. Other pad/body geometry is retained.

Copyright KiCad library contributors. [Library license](KiCad-library-LICENSE.md), CC BY-SA 4.0 with KiCad's libraries exception. Upstream [footprints](https://gitlab.com/kicad/libraries/kicad-footprints) and [3D models](https://gitlab.com/kicad/libraries/kicad-packages3D). This attribution does not imply vendor endorsement.

## Project-created material

RCA, HDMI, optical receiver and assembled optical STEP models are drawing-derived project work, with the simplifications documented in connector-selection-A1.md. No vendor CAD agreement was accepted or vendor download claimed for these files. Their Fusion construction source is retained in `tools/build_connector_models_fusion.py`; it takes an explicit `MODEL_OUTPUT_DIR` and uses a temporary unsaved design.
