# A8 horizontal connector fit study

**Export scope superseded by [A9](pcb-only-assembly-A9.md):** the owner designs the backplate and L brackets; current exports contain only the unchanged PCB and connectors. The plate/support descriptions below record the earlier A8 study.

The owner changed from a vertical carrier to a horizontal PCB and explicitly required the speaker clips to be soldered to that same PCB. A8 implements that mechanical direction. All six speaker pairs, both optical receivers, the coaxial RCA and HDMI are directly mounted on one board. A7 remains available in Git history and its exports are retained.

**This is a mechanical candidate, not a qualified connector BOM or fabrication release.** In particular, the compact right-angle KLS speaker block has no published operating-current rating in the drawing inspected. Its inclusion does not supersede the project's current requirement with a lower rating. Do not order it as an approved 50 W / 4 Ω solution on the strength of this fit model.

## Installed orientation and dimensions

The horizontal PCB sits above the connector bodies, with its component side facing down. The through-hole tails point upward, away from the PSU. Optical receivers therefore need no daughterboards, cables or separate cradle. The KiCad board is drawn normally on F.Cu; the installation STEP applies the rigid rotation. Do not mirror the PCB artwork to achieve this orientation.

| Datum | A8 nominal value |
| --- | --- |
| Owner rear-frame opening | 220 × 35 mm, R5; z 34…69 |
| Frame inner / outer face in Home Cinema v 7 | y 100 / y 102 mm |
| Connection plate inner / outer face in integration export | y 0 / y 1.5 mm |
| Translation into current enclosure coordinates | +102 mm along Y |
| PCB connector seating surface | z 67 mm |
| Nominal PCB opposite surface | z 68.6 mm |
| PCB footprint | 228 mm wide, 39.8 mm deep, 1.6 mm nominal thickness |
| Front PCB edge to plate inner face | **0.2 mm**, provisional, needs tolerance review |
| Rear PCB edge to plate inner face | 40 mm inward |
| Narrow front lip | 208 mm wide; wider body begins 4 mm inward |
| Highest modeled solder tails | z 72.5 mm; 7.5 mm below assumed z 80 lid |
| Four vertical reference-hole centers | x±115, z 44 and 59 mm; Ø3 mm |

There is no single parallel PCB-to-plate spacer length in this orientation. Position the board using its **height and front-edge setback**. Two provisional side brackets transfer the four original vertical reference holes to four horizontal PCB holes at x±110, depths 12/30 mm. The brackets' shelves touch the nominal connector seating plane; their manufacturing process, fasteners, load capacity and installation sequence remain open. Holes are reference geometry, not a finalized M3 clearance specification.

X is the assembly coordinate, Y points outward, and Z is enclosure height. Viewed from outside along −Y with Z up, increasing X runs left on the image. In the exported rear view the speaker group is on the right. The four symmetric reference-hole positions are unchanged.

## Plate and connector fronts

The included 1.5 mm connection plate is a **provisional fit aid**, distinct from the owner's 2 mm rear frame. Speaker flanges bear against its inner face, with the fingers exposed through two 38.5 × 30.6 mm windows. Their four Ø2.5 fixing holes are separate from the four owner Ø3 alignment holes. Optical bezels and HDMI shells project about 0.3 mm beyond the outer plate in this nominal arrangement.

The RCJ-011 has a forward shell solder stake. A8 moves its shoulder 3 mm inward so all pads land on the PCB, leaving its barrel 3.5 mm beyond the outer plate. A14 × 14 mm cutout makes room for a mating plug to enter the recess. **Cable-body clearance and complete insertion remain unverified**; this is not a production cutout. The 0.2 mm PCB/plate gap and 0.4 mm nominal PCB/frame-opening upper margin are also too close to treat as tolerance-qualified.

## Parts and sources

| Qty | Interface | A8 reference | Evidence / limitation |
| --- | --- | --- | --- |
| 2 | Three speaker pairs per block | **L-KLS1-WP-6P-03B-B/R** | Right-angle tails; 52 × 30 mm flange; 13 mm column pitch; row depths 3.8/8.8 mm; six Ø2.2 PCB holes. Current rating and exact retail supply unverified. |
| 2 | Optical | **Cliff FCR684205R / ORJ5** | Same part as A7, now soldered directly to the main PCB. |
| 1 | Coaxial RCA | **Same Sky RCJ-011** | Horizontal through-hole replacement for vertical RCJ-021. Recess/cable check required. |
| 1 | HDMI A | **Amphenol10029449-001RLF** | Horizontal SMT signal contacts with through-hole shell stakes, replacing vertical 10078837-001LF. |

Speaker geometry is a project reconstruction of [KLS drawing V1, 2025-09-19](https://img.klsele.com/admin/product_upload/20250923112109L-KLS1-WP-6P-03B.pdf), linked from the [manufacturer product page](https://klsele.com/products/Audio-Video-Connectors/Loudspeaker-Terminals/12425.html). Body and pin envelopes follow the drawing; lever shape, flange thickness and rear insulation details are simplified. Pin numbers are project-defined pending physical continuity checks. The drawing supplies contact resistance, insulation resistance and withstand voltage, **not an operating-current rating**. At 50 W into 4 Ω the nominal sine-wave load current is 3.54 Arms; retain appropriate thermal/current margin. The prior 3 A alternative remains rejected.

The [Cliff drawing](https://www.cliffuk.co.uk/products/optical/FCR684205R.pdf) and [Same Sky RCJ-01 drawing, 2026-08-12,p 2](https://www.sameskydevices.com/product/resource/rcj-01.pdf) support their project-reconstructed models and lands. The optical part remains 16 Mbit/s; moving it does not add 192 kHz PCM capability.

The [Amphenol product specification](https://www.amphenol-cs.com/product/10029449001rlf.html) confirms a right-angle Type A receptacle, 19 contacts and 1.6 mm PCB. Its footprint and STEP are copied from KiCad 10's `HDMI_A_Amphenol_10029449-x01xLF_Horizontal` library entry; the model path was made project-relative. See [KiCad attribution](sources/README.md). A connector alone does not implement or qualify ARC/eARC.

### Sourcing audit, 2026-11-03

- RCJ-011: JLC **C4992678**, 21 units shown in the [public RCA catalogue](https://jlcpcb.com/parts/2nd/Connectors/RCA_Connector_2061) at lookup. Exact availability and assembly service require rechecking when ordering.
-10029449-001RLF: JLC **C428493** has an [exact catalogue page](https://jlcpcb.com/partdetail/AmphenolICC-10029449001RLF/C428493). Current purchasable stock was not established; a listing is not a stock guarantee. Amphenol lists external distributors.
- FCR684205R: retain the external distributor route recorded in [A7 sourcing](sourcing-A7.md). JLC sourcing acceptance remains unconfirmed.
- KLS speaker candidate: manufacturer reference exists; no verified operating-current rating, exact small-quantity purchase route or JLC acceptance. **Sourcing remains unresolved.** FE6930 is not a direct horizontal substitute because its pins exit straight rearward.

JLC pre-order/Global Sourcing and outside suppliers remain authorized options. No supplier messages, sourcing requests, orders or reservations were made.

## Verification and integration

KiCad 10.0.5 DRC: **zero violations**. The board has 45 electrical pads and 10 NPTH holes; all pad centers lie on the board, every local model resolves, and there are no assigned nets or tracks. This checks the mechanical footprint study, not circuit completeness.

Fusion reimported the rigid STEP as **one component, 70 solid bodies**, and the F3D reimport gave the same result. A rigid joint to a Ø3 reference hole moved all 70 bodies together. All four reference-hole centers were measured from the exported plate. Disable **Ground to Parent** on the inserted assembly before making the joint.

Using read-only copies of the actual rear-frame and PSU bodies in Home Cinema v 7, the check found **no modeled interference** between frame/PSU/supports/plate and the new assembly. The measured PSU top is z 35 mm, not the older 33 mm assumption. The nearest nominal assembly-to-PSU distance is **2 mm**. That is a geometric result, not validation of airflow, temperature, insulation, tolerances or cable loads. The temporary fit verification did not edit or save owner CAD. A later, explicitly authorized live integration attempt is recorded below.

Evidence: [native DRC](../boards/rear-io/exports/rear-io-A8-drc.json),[pad and source-hash checks](../boards/rear-io/exports/geometry-check-A8.json),[Fusion fit/joint checks](../boards/rear-io/exports/fusion-integration-A8.json),[installed geometry](../boards/rear-io/exports/geometry-A8.json).

Use **rear-io-A8-rigid.f3d** or **rear-io-A8-rigid.step** for the plate/PCB/support assembly; **rear-io-A8-board-rigid.step** contains only the oriented PCB and connectors. Raw `rear-io-A8-assembly.step` is the hierarchical KiCad export in native board coordinates. A7 exports and the [A7 commit](https://github.com/k3rnL/open-cinema-hardware/tree/eae54aa79c94255bdad5aaae5bf087d2b4166b0e) remain historical comparison material.

Rebuild only in a clean/staged checkout: `build_models_A8_fusion.py`, `build_horizontal_A8.py --apply`, `export_review.py`, `build_integration_A8_fusion.py`, `check_horizontal_A8.py`, then `verify_A8_fusion.py`. Fusion scripts use unsaved temporary documents; the last check reads the open Home Cinema v 7 document. No schematic, routing, decoding, LVDS, power circuitry or manufacturing files have been added. Keep mains separate and never common speaker negatives by assumption.


## Live Fusion integration status — 2026-11-03

The owner explicitly authorized updating the existing `rear-io-A5-assembly` cloud file and replacing its linked use in the enclosure. Its open source document now contains the 70-body A8 assembly. Its legacy coordinate system was preserved so the existing placement stays aligned: legacy X = −A8 X; legacy Y = A8 Z; legacy Z = A8 Y + 3.51 mm. `rear-io-A8-legacy-frame.step` uses these legacy axes; the normal A8 rigid exports use the installed axes described above. Do not substitute one coordinate convention for the other without the matching placement.

`Rear Panel Assembly` was saved as **v 3**, replacing the old face-dependent rigid joint with a geometry-independent rigid as-built joint. `Home Cinema` was saved as **v 8** with that parent reference updated. These two uploads completed. The pre-existing Home Cinema edits were retained; the unrelated modified Bottom document was left untouched.

**The source-file cloud update is not complete.** `rear-io-A5-assembly` still reports cloud v 2 while its open document is modified. Save calls did not create a new version, and the native Save dialog's confirmation button was disabled. The open enclosure displays A8, but persistence of A8 through reopening the cloud assembly is not established. Do not treat parent v 3/Home v 8 as proof that the source has uploaded. No file was uploaded by name because two cloud files share the same name.

Original and current source archives were independently reimported and checked (135 and 70 bodies respectively). Private recovery archives also preserve the parent and original Home Cinema state. They are excluded from Git. An automatic approval check rejected closing the modified source without saving, despite those verified backups; it was left open. Completing the same-file cloud version update requires resolving that save state or owner approval for closing/reopening the backed-up source. The native KiCad and standalone A8 STEP/F3D artifacts remain valid independent deliverables.
