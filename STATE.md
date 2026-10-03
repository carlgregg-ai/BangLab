# BangLab state

| Stage | Status | Note |
|---|---|---|
| Contract audit | PASS | Claude v1.1/v0.1 contract reviewed |
| Full contract materialised in repo | PASS | Full artifact physically present under docs/evidence; independently verified on 2026-10-03 against pinned SHA-256 `9647717afa835afe1c5e79c86d1b01e93bb6c8804d8d8b2b81b5a00b4015085f`; artifact committed in `774fb0c5184a4f0da43a75da193943b84f5aabb3` |
| Committed primary evidence binary | PASS | Independently verified by Codex on 2026-10-03: working-tree and HEAD PDF SHA-256 both match `5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7`; main and clean working tree confirmed before housekeeping updates; see DEP Appendix B evidence receipt |
| Repository pre-build skeleton | IN PROGRESS | E0/E1 controls and E2 empirical timing only; no later encounter model modules |
| DEP B1 fixture | PREPARED | source values available in contract |
| DEP load fixture | PREPARED | source values available in contract |
| DEP p.82 fixture | PASS | refs 1–20 transcribed from primary printed p.82 |
| Fixture hashes verified | PASS | Canonical file-byte SHA-256 values frozen after E1 PASS in receipt.json; historical Git blob IDs retained in data/fixtures/INTEGRITY.md |
| E0 | PASS | 8 schema/units tests; explicit metadata and exact converters; no silent scientific defaults |
| E1 | PASS | 9 fixture integrity/receipt tests; primary tables, labels, source metadata, energies at source print precision, population p.82 summaries, and hashes verified |
| E2 | PASS | 13 DEV-only data-boundary/PCHIP tests; separate t2/t3 interpolants in SI seconds; positive duration, strict monotonicity, domain and locked guards; E3 not evaluated |
| E3 locked validation | TODO | one-shot scientific gate |
| E4–E8 | TODO | |
| v0.1 | NOT RELEASED | |

**E0/E1 and E2 implementation checks have passed. The timing interpolant reproduces DEV rows and is monotone; predictive/physical validity is not established. E3 remains sealed and requires separate human authorisation. Stop for review; no E3 evaluation has occurred.**
