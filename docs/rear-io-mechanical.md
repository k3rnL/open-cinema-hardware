# Rear I/O mechanical study A0

Date: 2026-11-03. Units: millimetres. **No manufacturing tolerances are released.**

## Evidence and scope

The owner designed a rear frame to accept a separate connection plate and PCB.
The owner requested KiCad work limited to shape and connector placement, with
logic and LVDS electronics deferred, and confirmed **six speaker pairs** on the
same connector strip as the four audio inputs. The mains inlet/switch remains a
separate panel assembly, without a placement assigned here.

[Original screenshots and extracted sketch](../mechanical/reference/README.md)
are the dimensional evidence. The latest resources memory also selects 3 mm
aluminium 5052 and JLCCNC S-M3-2 fasteners for the frame/chassis joint; that is a
different joint from the PCB mounting holes proposed below.

## Measured geometry versus proposals

Coordinates below are **outside rear view**: x increases right, z increases up;
zero is at the panel bottom centre. The captured Fusion sketch's horizontal axis
is reversed: `rear_x = -sketch_x`, `rear_z = sketch_y`.

| Feature | Geometry | Authority |
| --- | --- | --- |
| Frame outer limits | x −130…130; z 0…80 | Current sketch |
| Rear opening | x −105…105; z 39…64; R5 | Current sketch |
| Opening centre | x 0; z 51.5 | Derived from sketch |
| PSU reference top | z 33 | Sketch line; not a complete PSU solid |
| PCB limits | x −114…114; z 37…69; R2 | Proposed A0 |
| PCB thickness | 1.6 nominal | Proposed A0; stackup not a production choice |
| PCB holes | Ø3.2 at x ±109, z 42 and 64 | Proposed A0 |
| Connector faces | z 51.5 centreline | Proposed A0 |
| Connector depth | 20 from PCB component surface | Common provisional envelope, not actual parts |

The projected PCB lower edge is only **4 mm above the sketch's PSU-top line**.
This is a 2D geometric observation, not an approved thermal or electrical
clearance. No PCB setback from the plate, terminal exposure, airflow, standoff
length or lid clearance has been established.

The frame sketch's six circles are currently Ø4.5, while the accepted fastening
memory calls for nominal Ø3.8 rear-panel through holes. This discrepancy is
retained for review; the existing frame sketch was not changed.

The PCB's two hole columns are 218 apart and its rows are 22 apart. They sit
outside the 210-wide opening. They need matching provisions in the connection
plate or brackets. They are not automatically aligned to any existing frame
fixings. A 228-wide PCB overlaps the opening by 9 on each side; it is installed
from inside or with the removable plate, not passed through the opening face-on.

## Proposed connectors

All entries below are **movable mechanical envelopes without electrical pads**.
`SPK 1`…`SPK 6` avoid assigning speaker roles before the channel map is selected.

| Refs | Interface | Centre x positions | Envelope W × H × depth |
| --- | --- | --- | --- |
| J1…J6 | Six two-contact speaker spring connectors | −88, −70, −52, −34, −16, 2 | 14 × 18 × 20 each |
| J7, J8 | Two TOSLINK optical receivers | 28, 48 | 14 × 14 × 20 each |
| J9 | Coaxial S/PDIF, RCA assumed | 68 | 12 × 12 × 20 |
| J10 | HDMI Type A | 91 | 18 × 9 × 20 |

These are packaging allowances, not measurements from supplier drawings. The
visual socket details are symbolic. Exact connector variants, current/wire
ratings, plug shrouds, finger access, cable bends, insertion force and mating
reach through the plate must still be checked. The narrowest gap between body
envelopes is 4 mm; that does not prove sufficient access for speaker wires.

This vertical-board arrangement needs ports normal to the PCB, or a suitable
panel-mounted/daughterboard arrangement. Common right-angle PCB connectors
cannot be substituted blindly. Selecting real parts may change the PCB size,
depth and mounting, and may require separate speaker and input boards sharing
the same plate. This study approves no common electrical speaker return.

## KiCad layers and files

- `Edge.Cuts`: closed R2 board outline only.
- `User.Drawings` / `Dwgs.User`: frame opening and explanatory text, **not** a
  routed cutout in the PCB.
- `F.Fab` and `F.Courtyard`: connector envelopes and space reservations.
- `F.Silkscreen`: readable connector names and mechanical-draft identification.
- Four non-plated mounting-hole pads are the only pads in the design.
- F.Cu faces the exterior of the enclosure in this study. Reserve the interior
  side for later circuitry only after connector pin/body and PSU clearances are
  known; no usable electronics area is guaranteed yet.
- Local library and models use `${KIPRJMOD}` and travel with the project.

Open the `.kicad_pro` project, then the `.kicad_pcb`. There is intentionally no
schematic at this mechanical stage. Placeholders can be moved directly in KiCad.
[placement.json](../boards/rear-io/placement.json) records the generated A0 seed;
do not rerun the generator over subsequent manual design changes.

## Import into Fusion

The STEP export uses the PCB auxiliary origin so **STEP X = rear x** and
**STEP Y = rear z**. STEP Z is board thickness and connector projection, pointing
outwards from the front face of the PCB. Connector centre coordinates match the
table above. The nominal 1.6 mm stackup exports a 1.51 mm dielectric board body;
KiCad places the model bases at STEP Z = 1.595. Use the nominal full stackup in
clearance planning. The model's 20 mm port depth is provisional.

For the captured standalone Fusion `Rear Panel v4` document, the sketch maps to
world `(−sketch_x, 100, sketch_y)` in millimetres. Rotate the imported STEP
**+90° about world X** to put its board in that vertical XZ plane. Translation
along Y then sets the still-undecided plate-to-PCB spacing. No exact Y placement
is supplied or claimed. Preserve the current frame and fit a separate component.
Other assembly contexts may have different occurrence transforms.

The board-only STEP is useful when checking outline and hole positions. The
assembly STEP includes simplified rectangular connector solids. The DXF contains
the board perimeter only; the placement SVG includes the reference opening and
mounting-hole drawing. Neither is a connection-plate cutting file.

## Next integration work

1. Choose obtainable connectors with supplier drawings and suitable mounting
   orientation, contact ratings and mating access.
2. Replace each envelope with the verified footprint and manufacturer model.
3. Set the connection plate thickness, connector protrusion, PCB setback and
   mechanical support, then check the complete enclosure for interference.
4. Resolve the frame-hole discrepancy and existing fastening baseline separately.
5. Design the eARC/ARC, optical/coax reception, protection, power and LVDS circuits
   in a later revision, including separation from speaker output currents.
6. Check thermal, airflow and mains-separation constraints against the selected
   PSU and complete assembly before ordering anything.
