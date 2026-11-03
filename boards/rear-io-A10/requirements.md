# A10 electrical requirements and interface contract

Status: design draft, 2026-11-03. Values and pin maps derive from the [source register](source-register.json). Neither a powered prototype nor full transport compatibility has been tested.

## Responsibility boundary

The rear electronics extract, select and transport. Raspberry Pi 5 receives unaltered audio payload, pcm-auto-decoder performs decoding, and the Pi performs all DSP. Processed audio reaches the WONDOM amplifier by USB. No rear-board decoder, renderer, resampler or volume stage is planned.

“Unaltered” refers to payload bits. Removing S/PDIF framing and packing sample/encoded words into an I2S capture container is necessary; the mapping must be documented and bit-tested. Channel-status metadata is delivered separately. Supporting eARC in a chip brief does not establish a correct Pi HBR/MAT capture path.

## Status meaning — preserve this distinction

- **Lock**: the receiver is synchronized to the input transport. Valid digital silence can remain locked. Lock is neither “audible audio” nor confirmation that the Pi decoded the stream.
- **Rate**: the rate of the transport presented to the Pi, with BCLK/word-clock relationship. Encoded carrier rate can differ from the decoded programme's sample rate. Never derive ALSA setup from a codec label alone.
- **Format**: serial transport mode, valid lanes, slot/word width, alignment, clock edges and PCM/non-audio indication when available. This does not require the rear board to identify/decode every Dolby/DTS codec.
- Report the selected source, receiver errors and status changes. Only advertise fields the chosen receiver can actually provide.

## U1 — CS8416K-CZZR

Working draft alternative to WM8804, not a released substitution. TSSOP28; nominal 3.3 V VA/VD/VL. I2C at **100 kHz maximum**, 7-bit address 0x20 from AD0/1/2 low. SDOUT 47 kΩ pull-up selects software mode; AD2 has 47 kΩ pull-down; AD0/1 use 10 kΩ pull-downs. RST held low by default; software must meet at least 200 µs low and stable supply conditions before release.

RXP0=optical1, RXP1=optical2, RXP2=coax. All active RXP inputs and RXN use AC coupling. Coax has75 Ω 1% termination; its shield is currently circuit GND (no galvanic isolation). VA uses a ferrite and local 10 µF / 100 nF. FILT has a 3 kΩ 1% series22 nF branch to AGND and a parallel 1 nF C0G to AGND. AGND/DGND join a continuous ground area under the IC, not a split plane with digital returns crossing a gap.

Firmware requirements, not implemented firmware:

1. Configure before RUN: serial port master, 64×Fs BCLK, 24-bit words in 32-bit slots, I2S one-bit delay, left channel on low LRCLK and capture on rising BCLK. DS578F5 register05h fields imply 0x85 for this specific mode; validate on the bench.
2. Disable de-emphasis, truncation, forced clock switching and normal-path muting. Set HOLD=10 so receive-error handling does not silently hold/rewrite payload words; report errors and discard/restart the capture segment in software as appropriate. Do not mistake this for making corrupt data valid.
3. Configure GPO0 as INT (selector 0010) and GPO1 as receiver error (0101), choose interrupt polarity, then enable the relevant error/status masks. The two GPIO signals default low until configured.
4. Select the RX input, set RUN, wait for stable lock, inspect status, establish the capture configuration, then enable the link. Source switching must stop capture and mute the Pi's amplifier output first.

OMCK is tied low; SWCLK and FSWCLK must remain 0. The OMCK/RMCK-ratio register cannot measure rate without an OMCK reference. Use trustworthy channel-status information plus an actual clock measurement/validation path at the Pi/HAT. RMCK is exposed only for diagnostic measurement; it is not a required Pi audio input. On unlock the CS8416 clocks can run at its idle VCO rate, so software must not treat clocks alone as valid audio.

Optical FCR684205R:3.3 V, OUT1/GND2/VCC3;100 nF within 7 mm of leads and30 pF from OUT to GND as specified. Receiver limit 16 Mbps: plan optical up to 96 kHz stereo PCM, not192 kHz. S/PDIF compressed surround uses one two-channel carrier; DATA1–3 are forced low for this source.

## U2/U3 — source mux

Two SN74LVC157APWR at 3.3 V switch BCLK, LRCLK and DATA0–3 together. SEL0 chooses S/PDIF; SEL1 chooses a future **normalized 3.3 V** eARC interface. G_N high forces mux outputs low. A 1.8 V eARC chip needs a correctly designed level interface; no such interface has been assumed or added.

These are ordinary logic multiplexers, not glitch-free clock switches. Capture must be stopped before changing source or enable state. They do not merge asynchronous clocks. Boot pulls select S/PDIF and disable outputs. An inter-board connection, if adopted later, needs a defined ground return and timing budget; J23 is only a DNP test header.

## U4/U5 — LVDS link

Two DS90LV047ATMTC/NOPB, 3.3 V±0.3V, local 100 nF each. EN starts low and EN_N is grounded; unused inputs are grounded and unused outputs open. Six active pairs carry BCLK, LRCLK and four data lanes. They do not serialize or decode. Route each pair as a nominal 100 Ω differential pair referenced to a continuous ground plane.

J22 provisional pinout (numbered pairs):1/2 BCLK+/−;3/4 GND;5/6 LRCLK+/−;7/8 DATA0+/−;9/10 GND;11/12 DATA1+/−;13/14 DATA2+/−;15/16 GND;17/18 DATA3+/−;19/20 GND. This is neither HDMI nor Ethernet pinout. Generic headers only represent the prototype connection; locking harness connector, exact wire construction, shielding, cable length and skew limits remain open.

Future HAT:2×DS90LV048ATMTCX/NOPB at 3.3 V with one 100 Ω 1% termination per used pair, at the receiver. Convert LVDS before GPIO. No termination is populated on the transmitter board. There is no galvanic isolation. Validate common-mode range, edge timing, skew across both ICs/cable pairs and Pi setup/hold at every supported transport rate. Eight-channel 192 kHz PCM with 32-bit slots needs 12.288 MHz BCLK; HBR/MAT packing can impose different requirements and remains unverified.

## Power, EMI and physical allocation

J21 supplies regulated 5 V, not 24 V. U6 TLV75533PDBVR supplies 3.3 V;4.7 µF input/output are provisional values requiring at least the datasheet's effective capacitance after bias/tolerance. Do not extend this rail to an unbudgeted eARC module or Pi. A provisional 150 mA allocation dissipates 0.255 W; with the datasheet's 231.1 °C/W DBV JEDEC figure that is about 59 °C rise. Actual copper and temperature must be measured. The 500 mA headline rating is not a usable thermal budget beside the PSU.

Use a four-layer stack with an uninterrupted ground reference. Keep PLL filter/VA away from high-current speaker paths, mux clocks and the PSU switching field. Route each amplifier output as its own +/− pair with adequate copper and no shared negative. Six 50 W / 4 Ω channels imply 3.54 A rms per channel before margin; the KLS clip rating and copper sizing are still unresolved. No speaker routing exists yet.

Ground-referenced LVDS improves cable noise immunity but does not solve conducted supply noise, chassis bonding, ESD or PSU coupling. Retain separation from mains wiring, plan chassis/connector shields deliberately, and validate with powered PSU and amplifier load. No fixed safe spacing can be concluded from the screenshot alone. No shielding plate, insulation clearance, thermal or EMC compliance is certified by this model.

## Gates before fabrication

Full eARC pin/register/firmware documentation and supply route; eARC power rails/CEC/ESD/coupling components and HBR/MAT output mapping; source-loss state machine; final HAT/harness and power sequencing; coax protection/ground strategy; speaker-current qualification and wire retention; complete PCB routing/stackup; renewed enclosure/airflow/thermal check; bit-exact capture tests across sources and formats. Mains inlet and power-control board remain separate assemblies.
