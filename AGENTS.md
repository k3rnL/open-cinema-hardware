# Open Cinema hardware guidance

- This repository owns editable implementation. The sibling `../open-cinema-resources` owns durable memory; use its open-cinema-memory skill and reference index.
- Current A8 follows the owner's explicit change: **horizontal PCB, every connector directly soldered to it, including speaker clips**. The old vertical-board/daughterboard rule is superseded. Read `docs/horizontal-assembly-A8.md`.
- A8 mounts the component side downward at enclosure z 67 mm, with tails pointing upward. KiCad F.Cu remains the component side; the integration export applies the installation rotation. Never mirror artwork to simulate installation.
- Two KLS L-KLS1-WP-6P-03B-B/R blocks give exactly six pairs. These are mechanical candidates only: operating-current rating, exact retail supply and JLC acceptance remain unverified. Do not claim the prior 7 A Cliff rating for them. The owner has 4 ohm/mixed loads; the rejected 3 A alternative is still unsuitable. FE6930 straight tags cannot directly serve this horizontal board.
- Retain real vertical Ø3 alignment holes on both sides at x±115,z 44/59. A8 carries these in the provisional connection plate/support brackets; four separate PCB holes at x±110, depths 12/30 are horizontal. Mounting hardware remains undecided.
- Main PCB: 228 by 39.8 by 1.6 mm, front lip 208 mm wide, 0.2 mm setback from plate inner plane. Opening 220 by 35 R5 at z 34…69; actual read-only PSU top z 35. Tight gap/tolerances, thermals, RCA cable fit and plate cutouts are not qualified.
- FCR684205R optical receivers now have pads directly on the main PCB. RCJ-011 and10029449-001RLF replace vertical input parts. Historical daughterboard/cradle files are retained, not current assembly dependencies.
- Use A8 rigid STEP/F3D for alignment: one component/70 bodies. Disable Ground to Parent before the joint. Raw KiCad STEP is hierarchical and in different coordinates. User enclosure CAD must not be overwritten by temporary verification work.
- No circuitry or manufacturing release exists. Keep mains separate; do not common speaker negatives. No procurement requests or purchases are authorized.
- JLCPCB is preferred; pre-order/Global Sourcing and external suppliers are allowed. Distinguish exact catalogue listings, stock observations, accepted sourcing and electrical qualification.
- Distinguish project reconstructions from library/vendor CAD. Preserve source URLs and KiCad licensing. Keep project-relative model paths; exclude personal paths, accounts, caches and transient downloads.
- Do not regenerate over manual edits. A8 generation, export and verification sequence is documented. `export_review.py` exports the saved PCB; `check_horizontal_A8.py` verifies pads/models. Older tools and records remain historical.
