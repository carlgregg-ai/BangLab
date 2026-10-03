# BangLab state

| Stage | Status | Note |
|---|---|---|
| Contract audit | PASS | Claude v1.1/v0.1 contract reviewed |
| Full contract materialised in repo | PASS | Full artifact physically present under docs/evidence; independently verified on 2026-10-03 against pinned SHA-256 `9647717afa835afe1c5e79c86d1b01e93bb6c8804d8d8b2b81b5a00b4015085f`; artifact committed in `774fb0c5184a4f0da43a75da193943b84f5aabb3` |
| Committed primary evidence binary | PASS | Independently verified by Codex on 2026-10-03: working-tree and HEAD PDF SHA-256 both match `5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7`; main and clean working tree confirmed before housekeeping updates; see DEP Appendix B evidence receipt |
| Repository pre-build skeleton | IN PROGRESS | E0/E1 controls, frozen E2/E3 timing and E4 lateral calibration; E5 not started |
| DEP B1 fixture | PREPARED | source values available in contract |
| DEP load fixture | PREPARED | source values available in contract |
| DEP p.82 fixture | PASS | refs 1–20 transcribed from primary printed p.82 |
| Fixture hashes verified | PASS | Canonical file-byte SHA-256 values frozen after E1 PASS in receipt.json; historical Git blob IDs retained in data/fixtures/INTEGRITY.md |
| E0 | PASS | 8 schema/units tests; explicit metadata and exact converters; no silent scientific defaults |
| E1 | PASS | 9 fixture integrity/receipt tests; primary tables, labels, source metadata, energies at source print precision, population p.82 summaries, and hashes verified |
| E2 | PASS | 13 DEV-only data-boundary/PCHIP tests; separate t2/t3 interpolants in SI seconds; positive duration, strict monotonicity, domain and locked guards; frozen E2 checkpoint 9c98d3d |
| E3 locked validation | PASS | One-shot evaluation of frozen 9c98d3d on 2026-10-04 (Europe/London); all nine t2/t3/duration comparisons at 25/35/45 m within 1.0 ms; maximum absolute error 0.06419300367179304 ms (35 m duration); predictions persisted before opening; docs/evidence/e3/receipt.json and opened.json |
| E4 | PASS | 13 lateral tests; Gaussian circle-fraction calibration, linear sigma law, proportional variant k, positive domain and extrapolation flags; 48-test suite PASS; docs/evidence/e4/receipt.json |
| E5–E8 | TODO | |
| v0.1 | NOT RELEASED | |

**E0/E1/E2 checks passed and the first, only E3 evaluation passed. The frozen DEV-only PCHIP predicted the held-out DEP 25/35/45 m t2, t3 and duration within the predeclared 1.0 ms tolerance. This supports only the contract E3 timing claim, not lateral validation, general physical validation, other loads, breakage, scoring or DTL validity. E2 and fixture values are unchanged; no refitting, tuning or second evaluation occurred. E4 calibration checks also passed: lateral spread reproduces the DEP circle fractions at 30 and 40 yd. Gaussian shape, centred placement and linear range law remain assumptions; local/clay-scale distribution, clumping, asymmetry and shot-to-shot spatial structure remain unresolved. E3 was audited only, not rerun. E5 NOT STARTED. Stop for human review; no commit or push.**
