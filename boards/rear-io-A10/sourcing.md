# A10 sourcing — candidates, not an order

Checked 2026-11-03. Catalogue listings are not inventory reservations or JLC assembly acceptance. Some web results are cached; recheck exact stock at ordering. Global Sourcing/pre-order and external distributors are permitted. No order or supplier message was sent.

| Function | Qty | Exact part | Route / evidence | Status |
|---|---:|---|---|---|
| Optical/coax receiver |1|CS8416K-CZZR|[JLC C17403532](https://jlcpcb.com/partdetail/CirrusLogic-CS8416KCZZR/C17403532)|Implemented draft; full manufacturer datasheet. Small stock appeared in search, live extracted page did not expose a quantity. Confirm before purchase.|
| Parallel source mux |2|SN74LVC157APWR|[LCSC C406871](https://lcsc.com/product-detail/74-Series_Texas-Instruments-TI-SN74LVC157APWR_C406871.html)|Implemented draft; stock displayed by supplier results. JLC acceptance/stock not independently confirmed.|
| LVDS transmitter |2|DS90LV047ATMTC/NOPB|[JLC C2860140](https://jlcpcb.com/partdetail/3064817-DS90LV047ATMTCNOPB/C2860140)|Implemented draft; JLC page displayed 0 stock. Pre-order/Global Sourcing or outside distributor required.|
| Local 3.3 V regulator |1|TLV75533PDBVR|[LCSC C404027](https://www.lcsc.com/product-detail/C404027.html), [TI](https://www.ti.com/product/TLV755P/part-details/TLV75533PDBVR)|Implemented draft; exact supplier listing verified. Thermal budget is limited; not an eARC rail commitment.|
| Analog supply ferrite |1|BLM18AG601SN1D|[JLC C19330](https://jlcpcb.com/partdetail/BLM18AG601SN1D/C19330)|600 Ω @ 100 MHz, 500 mA, 0603; supplier page displayed stock.|
| Pi-side LVDS receiver |2 later|DS90LV048ATMTCX/NOPB|[LCSC C87137](https://lcsc.com/product-detail/LVDS-ICs_Texas-Instruments-DS90LV048ATMTCX-NOPB_C87137.html)|Future HAT only; supplier result displayed stock; not in this PCB.|
| HDMI eARC/ARC receiver |1 candidate|SII9437CNUC|[JLC C19979224](https://jlcpcb.com/partdetail/Lattice-SII9437CNUC/C19979224), [DigiKey](https://www.digikey.my/en/products/detail/lattice-semiconductor-corporation/SII9437CNUC/7672175)|Catalogue and distributor stock found. **Not selected or connected:** public brief lacks an implementation-ready pinout and electrical/control details.|
| HDMI alternative |1 candidate|EP92H1|[Explore manufacturer](https://www.epmi.com.tw/hdmi-arc-earc/ep92h1/)|QFN56 product description supports relevant functions; full documentation and procurement remain open. Not interchangeable with SiI9437.|

The older WM8804 is retained in historical resources. CS8416K is the working A10 proposal because it has documented multi-input selection and software status access. It is not an eARC decoder and cannot carry uncompressed multichannel eARC through its S/PDIF path.

## Existing connectors

FCR684205R optical receivers, RCJ-011 RCA, 10029449-001RLF HDMI and KLS speaker-block mechanical candidates are retained from A8/A9. Source references and their current limitations are in [A8](../../docs/horizontal-assembly-A8.md). KLS current rating/supply is still unresolved; do not apply FE6930's 7 A rating to this part. Header models J20–23 are generic prototypes without approved purchasing references; J23 is DNP. J31/J32 are PCB solder holes, not purchased connectors.

## Passive requirements

0603 nominal footprints. Selected public catalogue candidates: 100 nF, 50 V X7R Samsung [CL10B104KB8NNNC / C1591](https://jlcpcb.com/partdetail/CL10B104KB8NNNC/C1591); 30 pF, 50 V C0G [CL10C300JB8NNNC / C22397](https://www.lcsc.com/es/product-detail/C22397.html); 22 nF, 50 V X7R [CL10B223KB8NNNC / C21122](https://jlcpcb.com/partdetail/21834-CL10B223KB8NNNC/C21122); 10 µF, 10 V X5R [CL10A106KP8NNNC / C19702](https://lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-SMD-SMT_SAMSUNG_CL10A106KP8NNNC_10uF-106-10-10V_C19702.html). Exact bias/temperature derating still needs checking.

Remaining BOM entries intentionally say TBD: 4.7 µF input/output capacitors, 10 nF X7R/C0G coupling capacitors, 1 nF C0G PLL capacitor, 3 kΩ 1% PLL resistor, 75 Ω 1% termination, 10 kΩ / 47 kΩ bias resistors and optional 4.7 kΩ I2C pull-ups. Use at least 0.1 W resistors and suitable voltage rating; do not substitute high-drift dielectrics in the PLL. This is not a complete procurement BOM.

## eARC document request prepared for the next step

No contact has been made. Obtain a complete, shareable design package for SiI9437 or EP92H1: exact ordering/lifecycle status; electrical pinout and exposed-pad assignment; supply rails, sequencing and current; reference schematic and HDMI eARC/ARC/CEC protection network; required crystal/clock and external memory; I2C/SPI register map and firmware licence/redistribution terms; EDID/eARC capabilities and ARC fallback control; explicit output mapping/timing for 8-channel PCM, IEC61937, TrueHD/DTS-HD HBR and Dolby MAT; Linux capture examples and evaluation hardware.

If these are NDA-only or unsupported for small quantity, evaluate a documented module with the same raw-output requirements. [Circal's advertised receiver module](https://www.circalengineering.com/earc-arc-audio-receiver-module.html) is one lead, not an acquired or verified solution. Do not substitute an S/PDIF-only extractor for the required lossless/multichannel path.
