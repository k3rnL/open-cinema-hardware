# Stackup and controlled-impedance review

2026-11-04. Proposed JLCPCB **JLC04161H-7628**, nominal 1.6 mm / listed finished 1.59 mm ±10%. Checked with the [official calculator](https://jlcpcb.com/pcb-impedance-calculator) and [calculator guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator). The calculator, supplier stack and finished coupon must be reconciled at quotation; no physical impedance measurement exists.

| Layer | Material / copper | Nominal thickness |
|---|---|---:|
|F.Cu|Outer copper, 1 oz|0.0350 mm|
|Prepreg|7628 RC49%, nominal 8.6 mil material|0.2104 mm|
|In1.Cu|GND, 0.5 oz|0.0152 mm|
|Core|FR-4|1.0650 mm|
|In2.Cu|GND, 0.5 oz|0.0152 mm|
|Prepreg|7628 RC49%|0.2104 mm|
|B.Cu|Outer copper, 1 oz|0.0350 mm|

Mask layers in KiCad are nominal placeholders; dielectric constants/loss values are design placeholders, not a material certificate. The calculator's etch/plating model differs from a simple sum of finished copper thicknesses. Do not substitute a different stack and keep the same widths without recalculation.

## LVDS request

Target **100 Ω differential ±10%**, outer microstrip referenced to its adjacent inner GND plane. Calculator selection: 4 layers, 1.6 mm, outer 1 oz / inner 0.5 oz, non-coplanar differential, 6 mil edge gap. Returned width **7.190 mil = 0.182626 mm**; edge gap **0.1524 mm**. These values are used on the coupled LVDS sections. Outer-zone keepouts around the pair routes maintain copper setback; the inner GND planes remain continuous. Pin/via breakouts and the 2.54 mm header are discontinuities, not uniform controlled-impedance transmission line.

| Pair | P copper length | N copper length | Difference |
|---|---:|---:|---:|
|BCLK|12.231 mm|14.797 mm|2.566 mm|
|LRCLK|9.347 mm|12.838 mm|3.491 mm|
|DATA0|7.791 mm|10.535 mm|2.745 mm|

LRCLK has one via in each conductor; BCLK/DATA0 have none. These are measured layout lengths, not measured skew or a timing sign-off. The future cable, receiver, capture clock edge and Pi setup/hold must be included in validation. Nominal 100 Ω terminations belong at the receiving HAT; they are not fitted across transmitter outputs.

The two GND planes cover the electronics region only; the speaker region has twelve independent conductors and no shared speaker return. Speaker current capability and thermal rise require load testing even with parallel 2.5 mm outer traces.
