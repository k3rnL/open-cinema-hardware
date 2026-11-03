# Rear I/O mechanical integration — A1

2026-11-03 · mm · no released manufacturing tolerances.

A1 supersedes the [A0 envelopes and proposed mounting holes](rear-io-mechanical-A0.md). The owner chose to keep the main board vertical and use small optical daughterboards. See [selected parts and sources](connector-selection-A1.md).

## Coordinate system and geometry

Outside rear view: x increases right and z increases up, origin at panel bottom centre. Latest `Rear Panel v4 / Sketch3` maps `(x,z)` directly to world `(x,100,z)` mm. The earlier Sketch2 had reversed horizontal sketch coordinates; do not reuse that sketch-axis sign for Sketch3.

| Feature | Geometry | Status |
| --- | --- | --- |
| Frame | x ±130, z 0…80 | Owner CAD evidence |
| Opening | x ±105, z 39…64, R5 | Owner CAD evidence |
| Main PCB | x ±114, z 37…69, R2; nominal 1.6 thick | A1 proposal, vertical F.Cu outward |
| Optical clearance windows | centres x 28/48; width 17, z 39.9…64, R0.5 | Actual Edge.Cuts cutouts |
| Owner fixing references | x −110, z 44/59, Ø3; vertical pitch 15 | Dwgs.User only; **not PCB drills** |
| Optical daughterboards | 16 wide × 24 deep × 1.6 | Two horizontal boards |
| Daughterboard top | z 44.5; optical axis z 50.5 | Proposed placement |

The original four A0 Ø3.2 PCB holes were removed. Do not infer additional mirrored fixing points or a mounting method from the owner's two reference circles.

Connector centres: speaker J1…J6 x = −88, −70, −52, −34, −16, 2 at z51.5; optical J7/J8 x28/48 at z50.5; RCA J9 x65,z51.5; HDMI J10 x88,z51.5. The [placement file](../boards/rear-io/placement.json) distinguishes body/port centres from electrical footprint origins.

## Depth and support remain to be set

Measured from main-board component seating surface, front mating projections are speaker 14.4, RCA 15.8, HDMI 10.45 and optical assembly 10.45. They deliberately do not share a common front plane. The optical daughterboard extends approximately 15.85 behind that surface. RCA tails extend 6.3 behind it; allow drawing tolerances and the actual PCB stack.

The optical tab reaches z63.5 nominal, leaving only **0.5 mm to the opening top**. Receiver leads reach z40.4 nominal; their stated ±0.5 lead-length tolerance matters. These small margins need a tolerance review and physical sample check. A thicker panel, connector bezel, mounting plate or screw can reduce available access further.

Two main-board windows let the perpendicular modules cross its plane. They leave thin board rails; stiffness and assembly support are unvalidated. A daughterboard cannot hang from a purely visual assembly footprint: brackets, spacers or panel-tab retention and a wire/header connection must still be designed. No interboard connector is chosen.

Connector projected envelopes fit within the opening at nominal dimensions. This does not establish cable, screwdriver, finger, screw-head, plugged-connector or lid clearance. The board is wider than the opening and mounts from inside/as part of the removable plate. No plate cutting file is provided.

## Enclosure evidence and unresolved constraints

The current frame solid reads **2 mm** thick in Fusion, while resource memory selected a 3 mm aluminium fabrication baseline. Existing outer frame holes are Ø4.5 versus the baseline nominal Ø3.8 through-hole choice. Both discrepancies remain open; the original document was not changed.

The earlier sketch marks PSU top at z33, giving 4 mm to the proposed main board lower edge. This is only a 2D geometric observation. Actual PSU/terminals, wiring, airflow, electrical separation and loaded temperatures have not been checked. Mains remains separate from this connector board.

## Layers and Fusion exchange

- Edge.Cuts: outer perimeter and two optical windows.
- Dwgs.User: rear opening, two reference fixing circles and notes.
- F.Fab / F.Courtyard: part and assembly envelopes.
- Actual electrical pads on main J1–J6/J9/J10 and optical child J1. Main J7/J8 have no pads because they represent complete separate boards.
- No tracks, nets, schematic, copper pours, decoding or LVDS electronics.

The STEP auxiliary origin gives **STEP X = rear x; STEP Y = rear z; STEP Z = outward board normal**. KiCad exports a 1.51 dielectric body for the nominal 1.6 stack; model seating surfaces are at STEP Z1.595. In the captured standalone Fusion frame context, a +90° rotation about world X maps the board into XZ; set the still-undecided translation along world Y to establish PCB setback. Confirm the outward sign in the final enclosure assembly context.

The [assembly STEP](../boards/rear-io/exports/rear-io-A1-assembly.step) includes six spring terminals, two complete optical modules, RCA and HDMI. The board-only STEP and outline DXF include the optical windows. The placement SVG includes reference geometry. None is fabrication approval.
