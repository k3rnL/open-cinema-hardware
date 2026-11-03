# Open Cinema hardware guidance

- This repository owns editable implementation. The sibling `../open-cinema-resources` owns durable memory. Read its reference index and relevant topics first; use its `.agents/skills/open-cinema-memory/SKILL.md` for memory updates.
- Current rear-io revision A1 is a connector fit study with actual pads and selected references. It is unrouted, with no electrical netlist, and is not fabrication-ready.
- Preserve the owner's vertical main-PCB choice. Optical receivers use separate small horizontal daughterboards. Main J7/J8 are mechanical assembly instances; their electrical footprints are in `boards/optical-input`.
- Distinguish KiCad library models from drawing-derived project models. Consult `docs/connector-selection-A1.md` before changing footprint geometry.
- Use millimetres and explicit axes. Owner Ø3 fixing points are references only; do not silently drill them or mirror additional points. Mounting method remains open.
- Do not regenerate over manual edits. `generate_connectors.py` recreates the A1 seed; historical A0 tools are not current-design tools.
- Check native files, pad geometry, model paths and exported solids. DRC without nets does not verify circuitry, assembly fit or fabrication suitability.
- Keep mains separate. Do not common speaker negatives or tie them to chassis by assumption.
- Preserve project-relative libraries/models. Exclude personal paths, caches, locks, account data and transient downloads.
