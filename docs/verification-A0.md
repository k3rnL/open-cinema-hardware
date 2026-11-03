# A0 mechanical verification

Checked on 2026-11-03 with KiCad 10.0.5 and the owner's running Fusion.
The exact PCB hash is in [geometry-check.json](../boards/rear-io/exports/geometry-check.json).

## Completed

- Native PCB load, DRC, STEP/DXF/SVG export and 3D render succeeded.
- Geometry check confirms a closed 228 × 32 R2 outline, nominal 1.6 thickness,
  four Ø3.2 non-plated mounting holes, ten connector envelopes at the recorded
  coordinates, no tracks/zones and no electrical connector pads.
- All connector face envelopes fit in projection within the measured 210 × 25 R5
  opening, without overlapping each other.
- [DRC](../boards/rear-io/exports/rear-io-A0-drc.json) reports zero violations and
  zero unconnected items at default error/warning severities. Default ignored
  checks are listed there. This padless study has no connectivity to validate.
- The STEP assembly imported into a temporary Fusion document. All four distinct
  connector envelope shapes and the PCB were solid bodies; all **11 solid
  instances** (10 connectors plus PCB) were verified. The temporary document
  was closed unsaved and the owner's
  original `Rear Panel v4` document restored without changes.
- The imported board limits are X −114…114, Y 37…69, dielectric Z 0…1.51.
  Nominal stackup is 1.6 and connector bases are at Z 1.595. Connector depth is
  an assumed 20. The STEP bodies are rectangular allowances, not selected parts.
- The rendered KiCad view was inspected for all connectors, labels and holes.

## Limits

No actual connector fit, full enclosure interference, cable/finger access,
plate cutouts, screw/standoff stack, setback, logic/LVDS, EMI, thermal or mains
separation has been validated. No manufacturing release is provided.

## Recheck

Run `tools/check_mechanical.py` with a Python interpreter providing KiCad's
`pcbnew`. Run `python3 tools/export_review.py --cli <kicad-cli>` to export the
saved PCB without regenerating it. `tools/generate_mechanical.py` recreates the
initial study from `placement.json` and must not overwrite later manual edits.

The bundled macOS pcbnew interpreter emits a wx initialization diagnostic in
standalone scripts. Native CLI load, DRC, exports and render independently check
the saved file. No schematic parity/electrical test is claimed.
