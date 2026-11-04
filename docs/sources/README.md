# A1 source and license register

Numerical package/pad dimensions come from the manufacturer drawings linked in [connector selection](../connector-selection-A1.md), consulted 2026-11-03. Vendor PDFs are linked rather than redistributed. Original user screenshots live in `mechanical/reference`.

## KiCad material

`boards/rear-io/models/1732496.step` is copied from KiCad 10's `Connector_Phoenix_SPT.3dshapes/PhoenixContact_SPT_2.5_2-V-5.0-EX_1x02_P5.0mm_Vertical.step`.
`Phoenix_1732496.kicad_mod` derives from the matching KiCad footprint: drill diameters changed to 1.2 mm, model path made project-relative, identifier/description changed and reference/value visibility hidden. Other pad/body geometry is retained.

Copyright KiCad library contributors. [Library license](KiCad-library-LICENSE.md), CC BY-SA 4.0 with KiCad's libraries exception. Upstream [footprints](https://gitlab.com/kicad/libraries/kicad-footprints) and [3D models](https://gitlab.com/kicad/libraries/kicad-packages3D). This attribution does not imply vendor endorsement.

## Project-created material

RCA, HDMI, optical receiver and assembled optical STEP models are drawing-derived project work, with the simplifications documented in connector-selection-A1.md. No vendor CAD agreement was accepted or vendor download claimed for these files. Their Fusion construction source is retained in `tools/build_connector_models_fusion.py`; it takes an explicit `MODEL_OUTPUT_DIR` and uses a temporary unsaved design.

## A8 HDMI library assets

`HDMI_A_Amphenol_10029449-x01xLF_Horizontal.kicad_mod` and the corresponding STEP model were copied from the installed KiCad 10 libraries. Copyright KiCad library contributors; [CC BY-SA 4.0 with KiCad library exception](KiCad-library-LICENSE.md). The footprint library ID and model path were made project-relative; the manufacturer land geometry and STEP were retained. Upstream: [footprints](https://gitlab.com/kicad/libraries/kicad-footprints/-/tree/master/Connector_Video.pretty), [3D library](https://gitlab.com/kicad/libraries/kicad-packages3D/-/tree/master/Connector_Video.3dshapes).

## A10 package models and schematic symbols

A10 uses KiCad 10 package/connector/passive footprints and copied STEP models from Package_SO, Package_TO_SOT_SMD, Capacitor_SMD, Resistor_SMD, Inductor_SMD and Connector_PinHeader_2.54mm. Copyright KiCad library contributors; the same linked CC BY-SA 4.0 library exception applies. Model paths were localized. A10 custom schematic symbols are project-authored from factual manufacturer pin tables; they are not downloaded vendor symbols. The [A10 source register](../../boards/rear-io-A10/source-register.json) identifies the PDFs and hashes used. Datasheet PDFs are linked, not redistributed here.

## A11 assets

A11 additionally uses KiCad10 footprints/STEP models from Package_QFP, Package_SON, Oscillator and the Bourns SRN4018 inductor library, plus the existing passive/header packages. Copyright KiCad library contributors; the same CC BY-SA4.0 library exception linked above applies. Project symbols are authored from the manufacturer pin tables, not copied from third-party designs. [A11 source register](../../boards/rear-io-A11/source-register.json) records the public references and available local file hashes. Datasheets are linked, not redistributed.

A11 normalizes the upstream oscillator STEP file-name header to its basename, removing the original author workstation path; the DATA/geometry section and attribution are unchanged.
