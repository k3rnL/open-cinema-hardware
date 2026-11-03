# Rear-panel source evidence

Owner-provided on 2026-11-03:

- [Rear frame in enclosure](rear-panel-frame.png)
- [Free-space sketch](rear-panel-free-space.png)

The original PNG pixels are preserved without editing. They show the new rear
frame and the opening intended to accept the connection plate plus PCB.

[rear-panel-v4-sketch2.json](rear-panel-v4-sketch2.json) is a read-only geometry
extraction from the active Fusion document **Rear Panel v4 / Sketch2** on the
same date. Distances were converted from Fusion's internal centimetres to mm.
It records line endpoints, circles, arc centres/radii, construction flags and
the sketch-to-world basis. No original sketch or body was changed. This is an
evidence snapshot, not a parametric CAD replacement or full enclosure assembly.

The source screenshots' temporary clipboard filenames are recorded in the
[provenance manifest](provenance.json), together with SHA-256 checksums.

## A1 fixing-point update

[Owner fixing sketch](rear-panel-fixing-reference.png) and [read-only Sketch3 extraction](rear-panel-v4-sketch3.json), 2026-11-03. Opening remains 210 × 25 R5. The two Ø3 locations are x−110, z44/59; reference only, mounting undecided. Sketch3 x maps directly to world x, unlike earlier Sketch2. The frame model currently reads 2 mm thickness; this is not a resolution of the 3 mm fabrication baseline.

Screenshot SHA-256: `2a704b6d77c4633a9e3cea828d2220e2e0fd3b93f9108aa573a1412bb5d96c6a`. Original filename: `codex-clipboard-1f56ddfc-1dab-400c-bd6f-d7715f76eec1.png`.

## A3 owner opening update

[Updated owner sketch](rear-panel-220x35.png) and [read-only Sketch3 extraction](rear-panel-220x35-sketch3.json), 2026-11-03. Opening is **220 × 35 R5**, x−110…110,z34…69. Owner Ø3 fixing references are x−115,z44/59. Upper actual Ø4.5 frame holes remain x±40,z75, now clear of the opening in projection. This supersedes A2's assumed upward enlargement. The assistant did not modify the owner frame. Screenshot provenance and SHA-256 are in the manifest.
