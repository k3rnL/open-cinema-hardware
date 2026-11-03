# A6 connector sourcing audit

Checked 2026-11-03. The owner initially requested JLCPCB for everything, then allowed pre-order/Global Sourcing, then explicitly allowed AliExpress or other websites for difficult parts. **JLCPCB is preferred, not exclusive.** No purchases, supplier enquiries, uploads or reservations were made.

Quantities below are per finished rear I/O assembly. Stock is a dated observation, not a reservation. This is a sourcing worksheet, not a production BOM or a claim that the unrouted boards can already be assembled.

| Quantity / interface | Exact design reference | Verified source / availability | Next step |
| --- | --- | --- | --- |
| 1 HDMI | Amphenol ICC **10078837-001LF** | [JLCPCB C7159430](https://jlcpcb.com/partdetail/AmphenolICC-10078837001LF/C7159430), live public catalogue: **2400** in-stock parts, Extended, minimum1 | Retain. Recheck stock and solder-process acceptance with the eventual PCBA order |
| 1 RCA | Same Sky / former CUI **RCJ-021** | [JLCPCB C4992555](https://jlcpcb.com/partdetail/CUI-RCJ021/C4992555): **0** public stock; [DigiKey CP-1406-ND](https://www.digikey.co.uk/en/products/detail/same-sky-formerly-cui-devices/RCJ-021/408493): stocked distributor page | Retain. Request JLC pre-order/Global Sourcing or buy externally and hand-solder |
| 2 optical | Cliff **FCR684205R**, ORJ5 | [DigiKey 4654-FCR684205R-ND](https://www.digikey.com/en/products/detail/cliff-electronic-components-ltd/FCR684205R/15283094): active, **1129** shown by opened page. No purchasable JLC public listing verified | Retain. Global Sourcing subject to JLC acceptance, or external purchase; populate the two separate optical boards |
| 2 six-contact speaker blocks | Dragon City **PT-603B** | [Manufacturer catalogue](https://www.dragoncity.com.hk/st6p.html) and [drawing](https://www.dragoncity.com.hk/dwpt603b.pdf); JLC exact public search returned0 results | **Procurement unresolved.** No verified small-quantity retail stock or current rating for the exact modeled part |

## Rejected 3 A speaker alternative

[Harfington item1058833](https://www.harfington.com/products/p-1058833), **Uxcell WP6-03, SKU a19012500ux0044**, is offered singly and the live page says in stock, dispatch in24hours. Two units provide six pairs. Its rear/side photos show straight pins extending normal to the rear mounting face. The seller lists52×30×29mm,45mm mounting pitch,13mm column pitch and1.5mm pin width. These place it in the same packaging class, but the owner subsequently confirmed 4 Ω or mixed/unknown loads. **The 3 A alternative is rejected for the intended full-power use.**

It is **not established as the same part as PT-603B**. The exact row spacing, seating depth, finished drill recipe, flange stack and electrical qualification are missing. The current KiCad model therefore remains identified as PT-603B; it has not been silently relabeled to the Uxcell SKU.

The seller advertises **3A**, not an amplifier-qualified rating. For an illustrative resistive load,50W into4Ω requires about3.54A RMS, already above3A;50W into8Ω gives2.5A before margin or impedance variation. Do not approve this alternative for full50W/4Ω operation. The owner has confirmed 4 Ω or mixed/unknown loads; maximum power, load minima and a suitable current rating must be established before committing the speaker footprint or placing a production order. Stock availability alone is not qualification.

Photos inspected on the seller's page: `ux_a19012500ux0044_ux_d01` (rear dimensions) and `ux_a19012500ux0044_ux_d02` (straight-tail side view). Photos are linked through the product page and not republished here. Generic WP6-03 listings can differ; use the exact SKU and verify samples.

## What JLCPCB sourcing actually covers

[JLCPCB's Global Sourcing guidance](https://jlcpcb.com/help/article/how-to-use-jlcpcb-global-sourcing-parts-service) permits procurement from outside distributors for subsequent PCBA. A distributor's stock is not JLC stock or acceptance. Parts must arrive in the JLC warehouse and pass their assembly review. It is not a loose-parts shopping service. **Consign Parts** entries also do not establish purchasable stock.

The optical PLR135/T8,T9,T10 public searches showed zero-stock/consignment entries (C133351,C264298,C133279); they were not selected as a stocked replacement. A JLC Assembly virtual entry for DLR1111 likewise did not establish a purchasable receiver. Retaining the documented Cliff receiver with an external source is the better supported option under the owner's updated preference.

The [cradle and fasteners](assembly-and-optical-support-A6.md) are mechanical items ordered separately. A JLC3DP PA12 service exists, but this specific cradle has no manufacturing quote or acceptance yet. Standard M2 fasteners may be sourced externally. Assembly of the orthogonal boards, cradle and wiring is a final mechanical operation, not presumed included in PCBA pricing.

## Release gates

Confirm the exact speaker part, sample dimensions and current capability; finish the circuit and production pad qualification; confirm the JLC assembly service/process for through-hole parts; validate cradle tolerances, temperature and cable loads; then freeze the BOM and connection-plate cutouts. The present design is a mechanical integration prototype.

## Higher-current alternative under consideration

The owner confirmed **4 Ω or mixed/unknown speaker loads**. A speaker connector must therefore not be selected on an8Ω-only assumption.

Cliff **FE6930** is a more credible electrical candidate: [manufacturer specification](https://www.cliffusa.com/products/springterminals/multi.htm) states7A at60V AC; [DigiKey4654-FE6930-ND](https://www.digikey.com/en/products/detail/cliff-electronic-components-ltd/FE6930/25552004) lists stock. The [manufacturer drawing](https://www.cliffuk.co.uk/products/springterminals/FE6930.pdf), visually inspected, shows straight rear pins,65mm total width including ears,30mm height,58mm fixing pitch and eight contacts.

Two blocks would provide **eight speaker pairs**, including two spare pairs, rather than the requested six. This requires the owner's preference and a new verified layout/model revision. It is not a drop-in change to A6: current speaker footprints remain PT-603B. A provisional packing idea moves the optical/RCA group about4mm right and HDMI about3mm right, keeping the220×35 opening; this is not yet a verified enclosure layout.

The matching CliffFE6935 two-contact part is also rated7A, but its [drawing](https://www.cliffuk.co.uk/products/springterminals/FE6935.pdf) shows bent/downward PCB terminals and42mm overall width. It does not solve the owner's straight-tail constraint as a direct replacement. No order or substitution has been made.
