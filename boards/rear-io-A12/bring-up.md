# A12 qualification and bring-up record

Status 2026-11-04: **no powered board, audio capture or physical enclosure test has been performed**. These are pending procedures and acceptance criteria, not completed tests.

| Gate | Required evidence | Status |
|---|---|---|
|ARC candidate / supply|Eligible ADV7511 supply; documented ARC-only startup with grounded VCLK; required DD+ carrier demonstrated on evaluation hardware or a controlled prototype|Open|
|Speaker blocks|Manufacturer operating-current rating with margin for 50 W /4 Ω (3.54 A RMS), actual samples/dimensions, wire retention and heat rise|Open|
|Assembler review|Exact accepted MPNs, model/land tolerances, JLC substitutions, pin1/rotation review, through-hole plan and impedance stack/coupon approval|Open|
|Mechanical integration|Actual connector mating/cable bodies, underside clearance, wire bend/strain relief, PSU airflow and lid clearance in the enlarged enclosure|Open|
|Powered operation|Rails/startup/temperature, ARC/CEC, four-source reception, HAT capture and payload comparison|Open|
|Product qualification|Loaded speaker paths, EMI/ESD/hotplug/partial-power behavior and long-run operation|Open|

## Bench sequence

1. Inspect assembly, polarity and solder bridges. Check each supply to ground and each independent speaker conductor; keep mains and amplifier power disconnected from this low-voltage PCB. Check J21 polarity and custom J20/J22 pin numbering.
2. Use a regulated, current-limited 5 V bench source with a reviewed current budget. Start with LVDS disabled, receiver reset asserted and HDMI5V disabled. Measure 3.3 V and every filtered 1.8 V domain, startup overshoot, idle current and regulator/filter temperatures. Confirm effective capacitor values and stability. Do not apply 24 V to J21.
3. Bring up I2C at no more than 100 kHz. Confirm CS8416 address 0x20 and ADV main address 0x39; configure auxiliary addresses without collisions. Validate reset timing, interrupts, HDMI5V current limit/fault handling and CEC clock before attaching a TV.
4. Prove optical1, optical2 and coax lock/status at supported carrier rates. Confirm optical 16 Mbps limits. Verify error handling, mute/relock/source transitions and discontinuity reporting.
5. Implement CEC ARC initiation/termination, standby/reconnect and required discovery/capabilities. Test several TVs and their passthrough modes. Prove PCM, AC-3, DTS and required DD+ modes, including JOC metadata. Do not advertise a format merely because the TV reports it.
6. With the HAT's LVDS receivers and far-end 100 Ω terminations, inspect BCLK/LRCLK/data timing and capture without modification. Compare expected IEC61937 burst/payload words bit-for-bit, including channel packing and non-audio status. Verify source/rate changes and lock loss. Encoded data must never be played directly as PCM.
7. Connect the Pi decode/DSP pipeline and USB amplifier path only after capture validation. Check output channel mapping. Load each isolated BTL speaker pair with an appropriate test load and measure clip, solder joint and copper temperatures, including simultaneous channels.
8. Repeat with the real PSU and amplifier loaded: supply ripple, nearby magnetic/electric interference, continuous playback, enclosure temperatures/airflow, ESD at external ports, cable hotplug and partial-power/back-feed behavior. Document firmware, hardware hash, test setup and results before changing release status.

The LVDS cable/HAT and system software are separate work; a device-tree change alone does not complete these tests. If ADV7511 cannot meet the required mode or procurement condition, revise the front end before a production layout is frozen.
