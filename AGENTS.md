# Open Cinema hardware guidance

- This repository owns editable implementation. The sibling `../open-cinema-resources` owns durable memory. Read its reference index and relevant topics first; use its `.agents/skills/open-cinema-memory/SKILL.md` for memory updates.
- Current A3 mechanically evaluates two Dragon City PT-603B straight-tail red/black six-contact blocks. Current rating, supply and production footprint remain unqualified. A1 Phoenix terminals and A2 KLS downward tails are rejected.
- The vertical main board is 228 × 32 × 1.6. Updated owner opening is 220 × 35 R5, z34…69, measured read-only; A2's upward-opening assumption and top-hole conflict are superseded. Read `docs/rear-io-mechanical.md` before integration.
- Main speaker pads and four component-fixing NPTH holes are provisional drawing-derived geometry. They are not owner frame mounting holes. Owner Ø3 points at x−115,z44/59 remain reference graphics only; do not silently drill or mirror them.
- Preserve the vertical main-PCB choice. Optical receivers use small horizontal daughterboards. Main J7/J8 are mechanical assembly instances; actual receiver pads are in `boards/optical-input`. Support and interconnects remain undecided.
- Distinguish vendor/library CAD from project-reconstructed models. Read `docs/connector-selection-A3.md` for speaker assumptions and `docs/connector-selection-A1.md` for audio-input sources.
- No circuitry or manufacturing release exists. Keep mains separate; do not common speaker negatives or tie them to chassis by assumption.
- Do not regenerate over manual edits. `revise_rear_io_A3.py --rebuild` recreates A3. Older generators/exporters/checkers are historical; do not overwrite historical evidence from the current board.
- Verify native files, pad geometry, model paths and exported solids. DRC without nets does not establish circuit completeness, enclosure fit or fabrication suitability.
- Keep project-relative paths. Exclude personal paths, caches, locks, account data and transient downloads.
