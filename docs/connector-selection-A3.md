# A3 speaker connector candidate — Dragon City PT-603B

2026-11-03. The owner requires conventional red/black finger-operated clips, six pairs, on a vertical PCB above the PSU. Downward terminals are rejected. The suggested surface-mount construction is interpreted as a means to avoid downward pins; **straight through-hole terminals also meet that geometric constraint**.

## Reference and evidence

Use **two Dragon City PT-603B six-contact blocks**, twelve contacts total, for this mechanical study. Manufacturer [six-position catalogue](https://www.dragoncity.com.hk/st6p.html) identifies PT-603B and links its [dimensioned drawing](https://www.dragoncity.com.hk/dwpt603b.pdf), inspected on 2026-11-03. The drawing shows straight terminals behind the face. Do not substitute PT-603, a generic WP6 listing or a similar-looking right-angle variant without inspecting its drawing.

This is a **mechanical candidate, not an order-ready qualified part**. The inspected drawing does not state an operating current rating; small-quantity availability is unconfirmed. No supplier enquiry or order was sent. Ratings for other brands or PT-series variants are not evidence for this part.

## Dimensions versus project assumptions

| Feature | Evidence / implementation |
| --- | --- |
| Flange face height | Drawing: 30 mm |
| Raised front body | Drawing: 37.6 × 26.6 mm |
| Fixing pitch / body holes | Drawing: 45 mm / Ø2.5 mm |
| Front projection from flange front | Drawing: 11.5 mm |
| Flange front to PCB seating surface / rear pin end | Drawing: 9.6 / 13 mm; 3.4 mm straight pin projection beyond seating |
| Flange thickness | Drawing: 2 mm |
| Contact positions | Drawing: 13 ±0.10 mm column pitch, 19.5 mm row spacing |
| Terminal width | Drawing: 1.5 mm; model thickness 0.5 mm is assumed |
| Recommended panel opening | Drawing: 38 × 27 mm plus two Ø3.2 fixings at 45 mm pitch; not a finished connection-plate file |
| Flange ear outside diameter | Undimensioned: model assumes 7 mm; nominal overall width52, courtyard width53 |
| PCB signal drills and pads | Project allowance Ø2.2 / Ø3.6; not manufacturer-prescribed |
| Component-fixing drills | Project NPTH Ø3.2 based on the panel pattern; mounting method undecided |
| Pin numbers / colours | Project numbering top row1–3, bottom4–6, exterior view; black upper/red lower illustrative; verify samples |

The model is **project-authored from the drawing**, not vendor CAD. Lever shape, insulator details and pin thickness are simplified. Its orientation represents the straight rear terminals; there are no downward tails. The model and its geometry manifest live in `boards/rear-io/models`; the local footprint is `DragonCity_PT-603B_Straight`.

Before ordering or fabrication: confirm exact manufacturer suffix, current/wire capability for the amplifier, colour arrangement, supply quantity, body and pin dimensions, solder process, fixing stack and sample fit. The footprint is suitable for the current layout study, not a released land pattern.

[Current assembly geometry](rear-io-mechanical.md) · [A2 rejected KLS research](speaker-clips-correction.md) · [unchanged audio-input references](connector-selection-A1.md).
