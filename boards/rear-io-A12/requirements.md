# A12 circuit requirements and interface contract

Routed prototype, 2026-11-04. Read [current format scope](../../docs/arc-v1-requirements.md), [sources](source-register.json) and [verification](verification.md). This document specifies intended behavior, not measured performance.

## Signal path and responsibility

HDMI ARC → ADV7511 SPDIF_OUT → AC-coupled CS8416 RXP3. Optical1/2 and coax occupy RXP0/1/2. One selected source supplies the CS8416 serial output → DS90LV047A → future HAT receiver → Pi capture. No codec decoder, sample-rate conversion, volume or Atmos renderer is on this PCB. The Pi processes the preserved payload and outputs to the amplifier by USB.

Targets: stereo PCM, AC-3, conventional DTS and DD+ including JOC. TV passthrough is conditional. eARC, TrueHD, DTS-HD MA, MAT and multichannel HDMI PCM are deferred. The ADV7511 ARC documentation does not establish DD+ carrier-rate compatibility; that is a blocking measurement, not an advertised capability.

“Unchanged” refers to payload words. S/PDIF framing is removed and words packed for capture; prove that mapping bit-for-bit. Receiver channel status travels separately. Codec metadata stays in the encoded payload.

## ARC candidate and supporting circuit

U7 is ADV7511KSTZ, LQFP100, 14 × 14 mm / 0.5 mm pitch. Public [hardware guide Rev D](https://www.analog.com/media/en/technical-documentation/user-guides/ADV7511_Hardware_Users_Guide.pdf) supplies the pin map and ARC circuit. The draft uses 1 µF coupling on HEAC+/−, 49.9 Ω bias resistors to 1.8 V, and connector-side HPD sensing. R_EXT is 887 Ω. MVDD is 3.3 V; other supplies are 1.8 V with three filtered domains. Unused video/audio inputs are grounded and TMDS outputs open. There is no video output function.

CEC uses the 12 MHz ASV oscillator and a 27 kΩ pull-up through BAS116. DDC is pulled to HDMI 5 V. TPD4E05U06 devices provision line protection. Grounding the PD/address strap selects main I2C address 0x39 (7-bit). See [programming guide Rev G](https://www.analog.com/media/en/technical-documentation/user-guides/ADV7511_Programming_Guide.pdf): wait at least 200 ms after power-up; configure auxiliary maps without a CS8416 address collision. ARC register 0xDF bit7 selects mode; bit0 disables/enables reception. This alone does not negotiate ARC.

The Pi must implement CEC audio-system discovery, physical/logical addressing, capability responses, System Audio / ARC initiation and termination, standby and reconnect handling. ADI's [public API documentation](https://developer.analog.com/docs/system-level/solutions/reference-designs/adv7511/transmitter_api/) describes ARC/CEC operations; it is not completed project firmware. Qualify DDC/EDID and ARC startup with VCLK grounded; if the chip requires another clock or startup path, revise the circuit before layout freeze. [ADI support](https://ez.analog.com/video/f/q-a/9245/setting-for-adv7511-arc-audio-return-channel) confirms the need for CEC interaction.

Some ADI evaluation circuits use a different HEAC termination reference. A12 follows the hardware guide's 1.8 V bias. Compare actual common-mode levels and reception on the bench; do not mix variants silently. [ADI termination discussion](https://ez.analog.com/video/f/q-a/10016/arc-termination-circuits).

## Shared receiver and payload settings

U1 CS8416K-CZZR retains the [A10 Cirrus requirements](../rear-io-A10/requirements.md#u1--cs8416k-czzr), with RXP3 changed from ground to ARC. Three 3.3 V supplies; I2C maximum 100 kHz; address 0x20. Retain software-mode/address straps, AC coupling, PLL filter, reset timing and local decoupling.

Required configuration: serial clock producer, 64 × carrier Fs BCLK, 24-bit words in 32-bit slots, I2S one-bit delay and matching Pi clock edge. Disable de-emphasis, truncation, forced clock switching and valid non-audio muting. Review HOLD/error settings so software reports discontinuities rather than accepting replaced payload. A10's proposed register05h=0x85 and HOLD=10 remain untested settings, not working firmware.

Optical FCR684205R remains limited to16 Mbps; do not promise 192 kHz optical PCM. Keep its specified 100 nF local decoupling and 30 pF output load. Coax has75 Ω termination and AC coupling; A12 adds a TPD1E10B06DYAR clamp at the coax input; system ESD and ground-loop treatment remain unqualified. OMCK is low, so the clock-ratio register cannot measure carrier rate. Use status plus real clock measurement at the HAT; RMCK is exposed for that investigation.

## Control, source switching and status

J20 is a custom 3.3 V header, **not Raspberry Pi physical pin numbering**. R1/R2 are DNP: use a single I2C pull-up set at the HAT. Both boards must be powered together until partial-power behavior is designed and tested.

| J20 pin | A12 function | Direction relative to rear board |
|---:|---|---|
|1,3,11|GND|Reference|
|2|I2C_SDA|Bidirectional|
|4|I2C_SCL|From Pi|
|5|CS_RESET_N|From Pi; default low|
|6|CS_INT|To Pi; configure GPO0|
|7|ADV_INT|To Pi; **replaces A10 AUDIO_SEL**|
|8|HDMI_5V_EN|From Pi; default low; **replaces A10 MUX_DISABLE**|
|9|LVDS_EN|From Pi; default low|
|10|CS_RMCK_MON|Diagnostic clock to HAT|
|12|CS_RERR|To Pi; configure GPO1|

J24:1=HDMI_5V_FAULT_N,2=GND. Include this fault in the eventual HAT or revise the main header. Source selection uses CS8416 I2C register control; there is no external clock mux in A12.

Lock means transport synchronization, even during silence. Rate means carrier/capture rate, which may differ from programme rate. Format means serial packing/PCM-non-audio status, not universal codec identification. Report source, status changes and errors. Sequence: mute processed output → stop capture/disable LVDS → select → wait for stable lock/read status → configure capture → enable link/restart decoder → unmute. Never send encoded words directly to speakers as PCM.

## LVDS and future HAT

One DS90LV047ATMTC/NOPB now drives three pairs. J22:1/2=BCLK+/−,5/6=LRCLK+/−,7/8=DATA0+/−. Pins3/4/9/10/15/16/19/20 are GND. Pins11/12/13/14/17/18 are NC. The fourth driver input is grounded and outputs unused. This is not an HDMI/Ethernet cable pinout.

The future HAT needs one DS90LV048A-family receiver and nominal 100 Ω termination at each of the three used pairs, then short 3.3 V traces to Pi clock-consumer pins. Locking connector, cable construction/length and GPIO allocation remain provisional. No direct LVDS-to-GPIO connection. Validate propagation/skew and setup/hold across all carrier rates; 192 kHz with 64 Fs BCLK means 12.288 MHz. Device tree alone does not validate bit-perfect capture. eARC would need a separate interface reassessment.

## Power, placement and EMI

J21 provides regulated 5 V, never 24 V or mains. U6 TLV75533PDRVR supplies 3.3 V; U8 TLV75518PDRVR supplies 1.8 V from 3.3 V. Their WSON exposed pads must connect to adequate ground copper. Local 4.7 µF capacitors are candidates requiring effective capacitance checks after bias/tolerance. Three 10 µH SRN4018-100M filters feed the ADV domains, each with 10 µF and per-pin 100 nF.

Illustrative allocations, **not measured loads**: 300 mA through U6 implies 0.51 W; 180 mA through U8 implies 0.27 W. Confirm actual ARC consumption, rail tolerances, LC transient response, startup and junction temperatures. Do not use the 500 mA headline as the thermal budget. TPS2553DBVR controls connector 5 V; 226 kΩ ILIM gives approximately 101–142 mA across the datasheet table's tolerance case. Check drop, reverse behavior, fault response and hotplug. A 5 V input with adequate margin for these loads and HDMI supply is required.

Keep four layers with a continuous ground reference. Put U7/ESD near HDMI, PLL/filter and decouplers at their IC pins, and high-current BTL pairs away from this region. A12 placement is routed, with continuous inner ground in the electronics region and outer ground fills; routing is documented in verification.md. LVDS addresses cable susceptibility, not PSU conducted noise or magnetic coupling. Confirm grounding/shield bonding, power-off leakage, ESD and immunity with PSU and amplifier loaded. R51 is a DNP chassis-bond option, not the final grounding plan.

The KLS clips remain unqualified for 4 Ω/mixed loads; 50 W into 4 Ω is 3.54 A rms before margin. All six speaker negatives remain independent. A12 uses 2.5 mm copper on both outer layers for every speaker conductor; loaded temperature rise, wire strain relief and final clip sourcing remain open. Mains inlet/protection/earth bonding stay off this signal PCB.

## Mechanical boundary

Outline 228 ×39.8 ×1.6 mm and four Ø3 holes retained: installation x ±110 mm, inward depths 12/30 mm. The owner's latest window is 250 ×51 mm; no new plate or brackets are supplied. The rigid model is a nominal space study in the older installation datum. It does not certify revised-enclosure clearance, airflow, tolerances or cable access. Existing power-supply cooling must remain unobstructed after final placement.

## A12 header and layout details

J20 uses Samtec TSW-106-07-G-D; J22 TSW-110-07-G-D; J21/J24 TSW-102-07-G-S. These are unkeyed prototype headers. The future retained/locking LVDS harness remains a separate design task. Generic KiCad header models are conservative envelopes, not vendor-specific CAD. Pin 1, polarity and the custom pinout must be checked before connection. All components are on KiCad F.Cu even though the installed component side faces down.

The [stackup](manufacturing-review/stackup.md) fixes the impedance assumptions. Pair path lengths and asymmetry are measured from copper, not simulated or tested timing. Never infer bit-perfect capture, current capacity or immunity from DRC alone.
