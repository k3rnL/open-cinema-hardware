# A1 connector selection and sources

2026-11-03 · units mm · selection for mechanical integration, not production qualification.

**Speaker selection superseded:** the owner rejected Phoenix 1732496 in favour of conventional red/black finger-operated clips. J1–J6 below document historical A1 only. See [correction and candidate references](speaker-clips-correction.md); replacement integration is pending.

The owner requested real parts in the existing 210 × 25 R5 rear opening, six speaker pairs plus audio inputs, and explicitly chose **a vertical main PCB with small optical daughterboards**. Mains inlet/switch remains separate. No parts were purchased in this session.

## Order references

| Qty | Ref / role | Manufacturer part | Source / supplier example |
| --- | --- | --- | --- |
| 6 | J1–J6, two poles each | **Phoenix Contact 1732496** / SPT 2,5/ 2-V-5,0-EX | [Manufacturer](https://www.phoenixcontact.com/en-gb/products/printed-circuit-board-terminal-spt-25-2-v-50-ex-1732496) · [Newark](https://mexico.newark.com/en-MX/phoenix-contact/1732496/pcb-terminal-block-spt-2-5-2-v/dp/89X9001) |
| 2 | J7/J8 assemblies; child J1 | **Cliff FCR684205R / ORJ5** | [Manufacturer range](https://www.cliffuk.co.uk/products/optical/opticaljacks.htm) · [Farnell France](https://fr.farnell.com/cliff-electronic-components/fcr684205r/conn-r-cepteur-optique-90-male/dp/2991608) |
| 1 | J9, coax | **Same Sky RCJ-021** (formerly CUI Devices) | [Manufacturer](https://www.sameskydevices.com/product/interconnect/connectors/rca-connectors/rcj-021) · [Newark](https://www.newark.com/same-sky/rcj-021/rca-conn-jack-2pos-8-3mm-black/dp/59AM2952) |
| 1 | J10, HDMI | **Amphenol FCI 10078837-001LF** | [Manufacturer](https://www.amphenol-cs.com/product/10078837001lf.html) · [DigiKey](https://www.digikey.com/en/products/detail/amphenol-icc-fci/10078837-001LF/4238753) |

Supplier links are sourcing leads, not confirmed local inventory or price quotes. Use the exact manufacturer number when ordering.

## Speaker terminals

1732496 is a vertical two-pole spring terminal, 5 mm pitch, rated nominally 22 A / 2.5 mm² by Phoenix. Its wire access faces outwards when mounted on the vertical board. Body footprint 11.4 × 13.5; installed height 14.4. Six units give twelve independent speaker contacts.

The local footprint derives from KiCad `PhoenixContact_SPT_2.5_2-V-5.0-EX_1x02_P5.0mm_Vertical`; its four drill diameters are changed from 1.1 to the manufacturer's **1.2 mm**. Two tails belong to each pole. The STEP model is copied from the matching KiCad library. [Manufacturer dimensional drawing](https://caas.phoenixcontact.com/caas/v1/stable/media/42906/full/b1500?format=jpg).

These green industrial terminals differ from red/black consumer spring clips. Provide access to both wire entry and the clamping-space actuator; the manufacturer describes screwdriver opening. Wire preparation, wire size, PCB current capacity and insertion/tool clearances remain to be qualified. No common speaker return is assumed.

## Optical modules

[Cliff drawing FCR684205R](https://www.cliffuk.co.uk/products/optical/FCR684205R.pdf), version 2.0 dated 2023-06-29, pages 3 and 7, defines the package and recommended PCB layout. Each receiver is on its own **16 × 24 × 1.6** horizontal board. The main board retains mechanical assembly footprints J7/J8 and two routed clearance windows; actual solder pads are child-board J1.

Three PTH holes Ø0.8 at 2.54 pitch, plus three locating holes Ø2. Pin mapping is 1 OUT / 2 GND / 3 VCC. The footprint mouth points towards negative KiCad Y. The manufacturer's mating-face view shows pin 1 at right; consequently it is at negative X in this top/component view.

The receiver is specified at **16 Mbit/s**, supply 2.7–5.5 V. This rate accommodates 96 kHz stereo PCM S/PDIF (12.288 Mbit/s biphase channel rate), not 192 kHz (24.576 Mbit/s). Those are rate-budget calculations, not an end-to-end audio test. It has a Ø2.5 panel-mount tab, but no screw or support system is selected. Receiver decoupling, output connection and daughterboard retention are future work.

## RCA

[Same Sky RCJ-02 drawing](https://www.sameskydevices.com/product/resource/rcj-02.pdf), revision 2026-06-25, page 2. Vertical RCJ-021 has black insulation, barrel Ø8.3, mating plane 15.8 above PCB and maximum clip span 12.65. Signal hole Ø1.7 at (0, −1.6); shell holes Ø2 at (±5.15, 0). Coordinates use the component-side footprint view.

A drawing-derived model represents barrel, flange, insulation and tails. Clip bends are simplified and its rendered clip span is smaller than the full 12.65 drawing envelope, which is reserved in F.Fab/courtyard. This is an RCA intended for the coax input, **not a manufacturer-certified 75 Ω socket**. The input termination/isolation circuit remains to be designed.

## HDMI

Manufacturer drawing **10078837 revision H**, sheets 1–5: [official URL](https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/10078837.pdf), [readable mirror of the manufacturer drawing](https://pdf.hitech-semi.com/403288/10078837-001LF.pdf). The official drawing and CAD endpoints rejected access during this session; the mirrored drawing was inspected visually.

This vertical Type A receptacle has 19 mating contacts, **21 signal/ground solder tails plus five shell stakes**, and two M3 × 0.5 mounting ears at ±11.5. Body span 28.1; mating plane 10.45 above PCB. The drawing's 11.45 dimension includes the removable dust cover, excluded from the model.

The footprint follows the component-side recommended pattern. Physical tail order is 19, 1…18, 20, 21. Pads 19/21 use the wider land with its asymmetric offset; pads 20/21 are extra board ground tails. Shell stakes use `SH` identifiers. No electrical nets are assigned yet.

Two deliberate fabrication-stage items remain: plated stakes use the larger bottom-side annulus on both sides, and SMT pads currently have ordinary rectangular paste apertures rather than the drawing's segmented pin-in-paste stencil. Review pad stack, paste/stencil and assembly process before release. The library is suitable for this placement study, not approved production artwork.

The manufacturer currently describes the connector as HDMI 2.0. The socket itself does not provide or validate eARC/legacy ARC reception, CEC, audio formats or compatibility; those depend on the future receiver circuitry.

## Model provenance and precision

Phoenix STEP: KiCad library model. Other STEP files: **project-authored reconstructions from the cited mechanical drawings**, created in Fusion. They are part-specific mechanical models, not manufacturer CAD downloads. Dimensions, locating pins, protrusions and mounting features are represented; contact internals, threads, shells and flexing clip details are simplified. The optical assembly model includes the perpendicular board and receiver.

Keep nominal dimensions, drawing tolerances and rendering/STEP bounding-box tolerances distinct. Validate samples, actual plug envelopes, mating reach, part revisions and the complete enclosure before cutting the connection plate. No manufacturing output is supplied.
