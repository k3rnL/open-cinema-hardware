# ARC first-version implementation contract

Accepted scope: 2026-11-04. Requirements/proposal, not a schematic or manufacturing release.

[Resources decision 0014](https://github.com/k3rnL/open-cinema-resources/blob/main/docs/decisions/0014-use-arc-for-first-version.md) supersedes the initial eARC/lossless input obligation. Target stereo PCM, AC-3, conventional DTS, and DD+ including unchanged Atmos/JOC payload, subject to source/TV passthrough. Multichannel PCM, TrueHD, DTS-HD MA and MAT over HDMI are deferred with eARC. The rear board still only receives/selects/transports; all processing remains on the Pi with USB output to the amplifier.

## Existing draft and next revision

- Preserve the horizontal board, connector positions and four mounting holes until actual parts justify a reviewed geometry change. The owner designs the backplate/brackets.
- A10 optical/coax, Pi control and LVDS circuits are reusable candidates. Its HDMI socket is unwired. The provisional eARC header and static checks do not establish ARC functionality.
- ARC requires one data lane plus BCLK/LRCLK: three active LVDS pairs. A10 DATA1–3 provision may remain for a future upgrade; no fitted hardware or harness pinout changes are made here. eARC is not promised as a drop-in upgrade.
- Compare retaining CS8416K behind an ARC physical receiver against a shared ARC/optical/coax receiver-selector. A10 RXP3 is currently grounded; using it requires a real circuit revision and appropriate input conditioning. Do not connect HDMI lines directly to A10 from this proposal.
- Receiver supplies clocks; Pi is clock consumer. Qualify actual carrier rates, word packing and clock/data skew. A 192 kHz two-slot carrier with 32-bit slots requires 12.288 MHz BCLK; programme sample rate alone cannot determine capture setup.
- Preserve payload bits, including codec/Atmos metadata. Only receiver status belongs on the separate control interface. Disable valid-stream resampling, truncation, de-emphasis or non-audio muting. Error recovery must report discontinuity, not pretend altered words are valid input.

## Receiver and control requirements

| Function | Required evidence |
|---|---|
| ARC electrical reception | Single/common-mode behavior, coupling/termination, HDMI levels and HPD interaction |
| HDMI/CEC control | ARC initiation/termination, audio-system identity/capabilities, reconnect and standby; controller/interface/firmware ownership |
| Digital output | PCM/non-PCM word mapping, DD+ carrier rates, validity/error behavior and preserved JOC payload |
| Selection/status | Pi command/readback, lock/carrier rate/transport mode/errors; coordinated mute, capture stop, selection, re-lock and restart |
| Integration | Exact part/package, supply/reset/clocks, procurement, footprints, ESD, sequencing and PSU interaction |

High-level Pi control software remains deferred as requested, but receiver testing requires a working way to initiate ARC/CEC. No chip/controller or firmware has been selected by this scope decision.

## Documented receiver candidate

**TI PCM9211PT / PCM9211PTR**, LQFP48: [datasheet SBAS495D](https://www.ti.com/lit/ds/symlink/pcm9211.pdf), [product](https://www.ti.com/product/PCM9211), [ordering reference](https://www.ti.com/product/PCM9211/part-details/PCM9211PTR). Public documentation includes pinout, electrical requirements, register map, non-PCM detection and application circuits; the overview includes ARC. This is not a complete HDMI/CEC solution or tested DD+ path. Revision C removed an older eARC-compatibility claim. Availability/JLC acceptance has not been checked for this candidate. A10's CS8416K is not replaced by this document.

Any alternative module must preserve DD+ Atmos at its digital output. A stereo PCM DAC or AC-3/DTS-only extractor does not meet the target merely by supporting ARC.

## Two reviews and physical qualification

1. Circuit/interface review against exact datasheets: pinout, rails, reset, clocks, ARC/CEC/HPD, protection, source selection and raw-word settings; ERC and visual schematic review.
2. Board/model review: exported netlist versus pads, footprints/models, DRC/routing/returns, mounting datums and enlarged enclosure. Export/reimport rigid STEP/F3D after actual component/geometry changes.

Then measure PCM patterns; AC-3/DTS/DD+ payload equality after documented depacking; preserved JOC in a known DD+ Atmos fixture; source/rate/format changes; loss/re-lock/hotplug; CEC interoperability; boot/shutdown/back-powering; and timing/thermal/EMI with PSU/amplifier loaded. A format badge or PCM capture alone does not prove DD+ Atmos preservation.

## Revision boundary

This scope update changes documentation only. A10 KiCad, STEP/F3D, firmware and existing Fusion assembly are unchanged. Prior verification applies only to A10. eARC documentation no longer gates the ARC prototype; complete ARC circuitry/CEC, routing/protection, component qualification and physical tests still do.
