# Open Cinema hardware guidance

- This repository owns editable hardware implementation. The sibling
  `../open-cinema-resources` owns the reference book, research and durable history.
- Read the resources reference index and relevant topics before hardware changes.
  Use its `.agents/skills/open-cinema-memory/SKILL.md` for memory updates.
- Current rear-io revision A0 is a mechanical study. All connector footprints and
  models are placeholders without part numbers or electrical pads. Preserve that
  distinction in reviews and exports until actual parts are qualified.
- Use millimetres. Keep exterior-view, PCB and Fusion axes explicit.
- Do not regenerate a board over manual edits. The generator recreates the A0
  study from placement.json; review differences and preserve later design work.
- Check native files, placements, board outline and exported geometry before
  claiming fit. A clean DRC on this padless board is not electrical verification.
- No mains circuitry belongs on this low-voltage study. Do not connect speaker
  negatives together or to chassis by assumption; amplifier topology is separate.
- Keep project-relative libraries/models portable. Exclude caches, lock files,
  personal paths and account information from commits.
