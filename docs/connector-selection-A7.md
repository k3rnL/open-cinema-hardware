# A7 — Cliff FE6930 speaker connectors

2026-11-03. The owner accepted two spare pairs to permit **two Cliff FE6930 eight-contact blocks**. This replaces the unqualified PT-603B selection; six working pairs plus two spare pairs means **16 independent contacts**, not eight amplifier channels already wired.

The [Cliff specification](https://www.cliffusa.com/products/springterminals/multi.htm) gives **7 A at 60 V AC**. This is a credible connector rating for the stated 4 Ω or mixed-load design basis; it does not qualify the amplifier, wiring, fault protection or unknown load minima. The 3 A WP6-03 alternative remains rejected: 50 W into a resistive 4 Ω load requires about 3.54 A RMS before margin.

## Drawing and model provenance

Source: [Cliff FE6930 drawing, issue 2](https://www.cliffuk.co.uk/products/springterminals/FE6930.pdf), visually inspected. The public repository contains a **project reconstruction**, not vendor CAD or a copy of the proprietary drawing. Lever shapes, entry profiles and rear insulation are simplified.

Key nominal dimensions, mm: overall width 65 including ears; rectangular flange 58 × 30; raised front 51 × 27; fixing pitch 58 with Ø2.5 part bores; four columns at 13 pitch; tail rows 18.6 ±1 apart. Tail sections are 1.5 ±0.2 ×0.5 ±0.04 and project 3.5 behind the seating plane. Flange front is 9.5 outward from that plane; maximum lever projection is another 14. No tail extends below the body toward the PSU.

`Cliff_FE6930_Straight` has eight plated **2.2 ×3.2 slots**, with 3.6 ×4.6 pads. The longer slot direction accommodates the unusually broad published row tolerance better than circular holes. These are **project allowances, not a manufacturer-approved land pattern**. Four Ø3.2 component-fixing holes, two per block, use the published 58 pitch. Sample measurements, solderability and JLC through-hole/slot process review remain required. Component fasteners and cable-load support are not yet selected.

## Contact mapping

Viewed from the rear exterior, the drawing numbers the top row 1–4 and bottom row 5–8, left to right. Both rows have **red, black, black, red** levers. Therefore pairs run horizontally; do not pair vertically aligned contacts of the same colour.

| Block | Upper left | Upper right | Lower left | Lower right |
| --- | --- | --- | --- | --- |
| SP1 | Ch1: 1+ / 2− | Ch2: 4+ / 3− | Ch3: 5+ / 6− | Ch4: 8+ / 7− |
| SP2 | Ch5: 1+ / 2− | Ch6: 4+ / 3− | Spare1: 5+ / 6− | Spare2: 8+ / 7− |

Channel names and polarity are proposed labeling, not a routed circuit. Keep all contacts isolated until the amplifier harness is designed; do not common negatives or chassis. Spare contacts currently have no electrical nets, like the rest of this mechanical prototype.

## Nominal placement and limits

SP1/SP2 centres are x−77/−11,z52. Optics move to x32/52, RCA to69, HDMI to91. The original **220 ×35 R5 opening** and all four owner alignment holes remain unchanged. The optical cradle is the A6 part translated 4 mm right, not a floating board.

Fusion solid checks found the connector projections inside the opening, no new speaker-to-neighbour intersection and no cradle collision. **The left ear has only 0.5 mm nominal clearance to the opening**, and adjacent speaker ears have 1 mm. The inherited approximately 0.4 mm cradle/RCA-tail clearance remains tight. No tolerance, plug/finger-access or complete enclosure fit release is implied. See [verification](verification-A7.md), [coordinates](rear-io-mechanical.md) and [sourcing](sourcing-A7.md).
