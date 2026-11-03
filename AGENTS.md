# Open Cinema hardware guidance

- This repository owns editable implementation. The sibling `../open-cinema-resources` owns durable memory. Read its reference index and relevant topics first; use its `.agents/skills/open-cinema-memory/SKILL.md` for memory updates.
- Current A2 uses two KLS L-KLS1-WP-6P-03B-B/R red/black six-contact blocks as mechanical candidates. Operating current remains unconfirmed. Phoenix 1732496 is rejected.
- A2 has a 99 x 32 vertical input PCB beside panel-supported speaker blocks. The 210 x 35 opening is permitted by the owner but conflicts with old top frame holes. Read `docs/rear-io-mechanical.md` before integration. Frame CAD remains unchanged.
- Speaker blocks and optical assemblies have no main-PCB pads; do not invent solder pads for panel-mounted or perpendicular parts. No circuitry or manufacturing release exists.
- Preserve the owner's vertical main-PCB choice. Optical receivers use separate small horizontal daughterboards. Main J7/J8 are mechanical assembly instances; their electrical footprints are in `boards/optical-input`.
- Distinguish KiCad library models from drawing-derived project models. Consult `docs/connector-selection-A1.md` before changing footprint geometry.
- Use millimetres and explicit axes. Owner Ø3 fixing points are references only; do not silently drill them or mirror additional points. Mounting method remains open.
- Do not regenerate over manual edits. `revise_speaker_clips.py --rebuild` recreates the A2 study; A0/A1 tools are historical.
- Check native files, pad geometry, model paths and exported solids. DRC without nets does not verify circuitry, assembly fit or fabrication suitability.
- Keep mains separate. Do not common speaker negatives or tie them to chassis by assumption.
- Preserve project-relative libraries/models. Exclude personal paths, caches, locks, account data and transient downloads.
