# A11 sourcing — exact candidates and remaining constraints

Checked 2026-11-04. These are catalogue references, not reserved stock, accepted JLC sourcing or a completed order. Global Sourcing/pre-order and outside suppliers are permitted. No supplier was contacted and no purchase was made.

| Ref / quantity | Exact part | Purchasing reference | Qualification |
|---|---|---|---|
|U7 /1|Analog Devices **ADV7511KSTZ**|[JLC C179459](https://jlcpcb.com/partdetail/AnalogDevices-ADV7511KSTZ/C179459)|ARC test candidate; listing confirmed, stock/eligibility not confirmed.|
|U1 /1|Cirrus **CS8416K-CZZR**|[JLC C17403532](https://jlcpcb.com/partdetail/CirrusLogic-CS8416KCZZR/C17403532)|Retained A10 documented receiver; qualify actual capture.|
|U4 /1|TI **DS90LV047ATMTC/NOPB**|[JLC C2860140](https://jlcpcb.com/partdetail/3064817-DS90LV047ATMTCNOPB/C2860140)|Retained A10 candidate; prior zero-stock observation, allow outside/pre-order.|
|U6 /1|TI **TLV75533PDRVR**|[JLC C2861750](https://jlcpcb.com/partdetail/TexasInstruments-TLV75533PDRVR/C2861750)|WSON6 with exposed pad; replaces A10 DBV package.|
|U8 /1|TI **TLV75518PDRVR**|[JLC C2868686](https://jlcpcb.com/partdetail/TexasInstruments-TLV75518PDRVR/C2868686)|1.8 V WSON6; cascaded supply and thermals need qualification.|
|U9 /1|TI **TPS2553DBVR**|[JLC C55266](https://jlcpcb.com/partdetail/TexasInstruments-TPS2553DBVR/C55266)|HDMI5 V current-limited switch, SOT23-6.|
|U10/U11 /2|TI **TPD4E05U06DQAR**|[JLC C138714](https://jlcpcb.com/partdetail/TexasInstruments-TPD4E05U06DQAR/C138714)|Four-line low-capacitance protection; exact TI manufacturer required.|
|D1 /1|Nexperia **BAS116,215**|[Manufacturer ordering family](https://www.nexperia.com/chemical-content/BAS116.html)|SOT23 low-leakage CEC diode. Exact JLC/distributor purchase route not yet confirmed.|
|Y1 /1|Abracon **ASV-12.000MHZ-E-T**|[Symmetry catalogue](https://www.symmetryelectronics.com/products/abracon/asv-12-000mhz-e-t/)|12 MHz 3.3 V oscillator, 7 ×5.08 mm. External/Global Sourcing candidate; recheck stock.|
|L1–L3 /3|Bourns **SRN4018-100M**|[JLC C503307](https://jlcpcb.com/partdetail/BOURNS-SRN4018100M/C503307)|10 µH; exact LC response and DC drop to validate.|
|FB1 /1|Murata **BLM18AG601SN1D**|[JLC C19330](https://jlcpcb.com/partdetail/BLM18AG601SN1D/C19330)|Retained receiver analog-supply ferrite.|

**Material ADV7511 constraint:** ADI's [product page](https://www.analog.com/en/products/adv7511.html) says customers must be HDMI adopters to purchase this part. A catalogue entry does not waive that requirement or guarantee support. Resolve an eligible supply route before committing the board. The prototype is not a claim of a low-barrier, fully qualified ARC solution. The public guides also do not explicitly validate the DD+ carrier rate; bench proof is required.

The future HAT needs one receiver, e.g. **DS90LV048ATMTCX/NOPB**, [LCSC C87137](https://lcsc.com/product-detail/LVDS-ICs_Texas-Instruments-DS90LV048ATMTCX-NOPB_C87137.html), not populated on this PCB. A10 used two; ARC needs only three lanes.

## Connectors and passives

J7/J8 Cliff FCR684205R, J9 Same Sky RCJ-011, J10 Amphenol10029449-001RLF and KLS L-KLS1-WP-6P-03B-B/R mechanical candidates are unchanged. See [A8 sourcing and geometry](../../docs/horizontal-assembly-A8.md). **KLS current rating and exact supply remain unresolved.** No claim of the former Cliff FE6930's 7 A rating applies here. J20/J21/J22/J24 are provisional headers; J31/J32 are wire solder holes, not separate parts.

The [CSV](bom-draft.csv) names the implemented parts and DNP options. A11 corrects the inherited 10 µF part-number typo to Samsung **CL10A106KP8NNNC** ([manufacturer](https://product.samsungsem.com/cn/mlcc/CL10A106KP8NNN.do), [LCSC C19702](https://www.lcsc.com/product-detail/C19702.html)); it is 10 µF 10 V X5R 0603. CL10A475KO8NNNC is the 4.7 µF candidate. A10 remains historical and was not silently rewritten. Remaining entries labelled TBD require exact passive selection, dielectric/bias checks and supplier confirmation. This is not a PCBA-ready BOM.

## Assets and alternative research

Footprints and STEP packages are KiCad library assets; pin-map symbols and wiring are project-authored. Existing connector reconstructions retain their uncertainty. [Attribution](../../docs/sources/README.md).

PCM9211's public datasheet is useful but does not alone provide the ARC physical receiver and CEC solution. EP91H0 public briefs were insufficient for this implementation. No unlicensed third-party schematic was copied. eARC alternatives remain historical/deferred, not part of A11.
