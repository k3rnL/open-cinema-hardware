# Speaker clip correction — 2026-11-03

## Owner requirement

The owner rejected A1's Phoenix Contact 1732496 industrial terminals and supplied a photograph of conventional **red/black finger-operated speaker spring clips**, with solder tabs behind a panel-mount strip. Retain **six pairs / twelve independent contacts**. A spring-clamp mechanism alone does not satisfy the intended style and operation.

The vertical main PCB and optical daughterboard decisions remain active. The owner subsequently allowed a taller opening. A2 evaluates two KLS six-contact blocks mechanically; electrical qualification and mounting remain open. **A1 J1–J6 and their exports are historical rejected selections; do not order them.** The current KiCad file now shows the KLS mechanical candidate with explicit qualification limits.

## Drawing-backed candidates

Dimensions are nominal millimetres, not required cutouts or validated assembly clearances.

| Reference | Contacts | Front size including flange | Evidence and assessment |
| --- | --- | --- | --- |
| Shallin **K283** | 4, single row | 70.2 × 24 | [Manufacturer](https://www.shallin.com.tw/en/product/show.aspx?num=3231). Panel mount with solder tabs; closest style to the supplied image. Three units total 210.6 mm before spacing, leaving no space for audio inputs in the 210 mm opening. Current rating still to verify. |
| KLS **L-KLS1-WP-6P-03B-B/R** | 6, two rows | 52 × 30 | [Manufacturer](https://klsele.com/products/Audio-Video-Connectors/Loudspeaker-Terminals/12425.html), [manufacturer drawing V1, 2025-09-19](https://img.klsele.com/admin/product_upload/20250923112109L-KLS1-WP-6P-03B.pdf). Two units supply twelve contacts in 104 mm of combined width. Promising packaging candidate, **not selected**. |
| Cliff **FE6930** | 8, two rows | 65 × 30 | [Manufacturer drawing](https://www.cliffuk.co.uk/products/springterminals/FE6930.pdf). Rated 7 A at 60 V AC. Raised front is 51 × 27, still taller than the existing 25 mm opening if recessed through it. Eight contacts do not match the twelve-contact requirement alone. |

KLS drawing specifies 45 mm fixing pitch, Ø2.5 fixing holes, 13 mm contact pitch, 22–16 AWG wire, and right-angle PCB tails. The 30 mm face excludes tails extending below it. These tails do **not** directly fit the existing vertical carrier. A panel-supported assembly with a separate termination arrangement is required; do not invent a vertical-PCB solder footprint. The drawing gives contact resistance and withstand voltage but **no operating current rating**. Manufacturer current confirmation, obtainable quantity, exact colour arrangement and samples are prerequisites to final selection.

The original photo's solder-tab strips can be wired directly to the amplifier; speaker power need not travel through the digital input PCB. This is a proposed mounting/wiring approach, not a chosen implementation. Keep every speaker return independent unless the amplifier documentation establishes otherwise.

## Fit question

Existing opening: **210 × 25 mm, R5**, z39…64. A provisional **210 × 35 mm**, enlarged upward to z74 while retaining z39 at the bottom, would allow a 30 mm-high two-row speaker face to be considered. The owner approved allowing this height, but this is **not a fabrication-approved cutout**; PCB outline, supports, fixing references, plug/finger access, connector depth and full enclosure clearance require a new layout. Do not alter the owner's frame automatically.

The width calculation above compares packaged front sizes; flange overlap, setback and actual plate apertures must be checked separately. It is not proof that every possible red/black clip arrangement fails in the original opening.

## State of implementation

A2 replaces the six Phoenix instances with two panel-supported KLS mechanical instances and a drawing-derived STEP model. The input PCB is shortened to 99 × 32 mm beside them; all audio-input footprints, positions and optical daughterboards are preserved. Historical A1 exports remain unchanged. The taller opening conflicts with the old upper frame holes, and rear tail/frame clearance is unresolved; see [mechanical notes](rear-io-mechanical.md). No replacement was ordered and no manufacturing files were released.
