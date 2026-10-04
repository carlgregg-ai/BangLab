# BangLab state

| Stage | Status | Note |
|---|---|---|
| Contract audit | PASS | Claude v1.1/v0.1 contract reviewed |
| Full contract materialised in repo | PASS | Full artifact physically present under docs/evidence; independently verified on 2026-10-03 against pinned SHA-256 `9647717afa835afe1c5e79c86d1b01e93bb6c8804d8d8b2b81b5a00b4015085f`; artifact committed in `774fb0c5184a4f0da43a75da193943b84f5aabb3` |
| Committed primary evidence binary | PASS | Independently verified by Codex on 2026-10-03: working-tree and HEAD PDF SHA-256 both match `5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7`; main and clean working tree confirmed before housekeeping updates; see DEP Appendix B evidence receipt |
| Repository pre-build skeleton | IN PROGRESS | E0-E6 preserved; E6 contact-oracle verification PASS; historical F4-v1 FAIL/FAIL and F4-v2 results preserved separately; E7/E8 not started |
| DEP B1 fixture | PREPARED | source values available in contract |
| DEP load fixture | PREPARED | source values available in contract |
| DEP p.82 fixture | PASS | refs 1–20 transcribed from primary printed p.82 |
| Fixture hashes verified | PASS | Canonical file-byte SHA-256 values frozen after E1 PASS in receipt.json; historical Git blob IDs retained in data/fixtures/INTEGRITY.md |
| E0 | PASS | 8 schema/units tests; explicit metadata and exact converters; no silent scientific defaults |
| E1 | PASS | 9 fixture integrity/receipt tests; primary tables, labels, source metadata, energies at source print precision, population p.82 summaries, and hashes verified |
| E2 | PASS | 13 DEV-only data-boundary/PCHIP tests; separate t2/t3 interpolants in SI seconds; positive duration, strict monotonicity, domain and locked guards; frozen E2 checkpoint 9c98d3d |
| E3 locked validation | PASS | One-shot evaluation of frozen 9c98d3d on 2026-10-04 (Europe/London); all nine t2/t3/duration comparisons at 25/35/45 m within 1.0 ms; maximum absolute error 0.06419300367179304 ms (35 m duration); predictions persisted before opening; docs/evidence/e3/receipt.json and opened.json |
| E4 | PASS | 13 lateral tests; Gaussian circle-fraction calibration, linear sigma law, proportional variant k, positive domain and extrapolation flags; 48-test suite PASS; docs/evidence/e4/receipt.json |
| E5 | PASS | 8 geometry + 10 field tests; 66-test suite PASS; D-007 symmetry clarification; 48/64-node deterministic quadrature, circular analytic checks, boundary and Binomial checks; docs/evidence/e5/receipt.json |
| E6 | PASS | First authoritative contact-oracle execution: all 6 single-pellet and 24 round-tail comparisons PASS; 8 non-dispersion F4 regressions PASS; 96-test suite PASS, zero skips; receipt SHA-256 `a2e08baf238d1adb8e9923bd98c8c2f918be8a672e56194fb4c17e348958fa05`. Historical F4-v1 FAIL/FAIL remains preserved and is not overwritten by this PASS. |
| E7–E8 | TODO | Not started |
| v0.1 | NOT RELEASED | |

**E0-E6 computational build/verification status is now closed through the E6 contact-oracle gate. E3 remains the one-shot held-out longitudinal timing validation; E4 is lateral calibration, not validation of Gaussian local structure; E5 establishes numerical behaviour of the declared deterministic encounter model; and E6 establishes agreement between that deterministic calculation and an independent direct Monte Carlo route for the predeclared verification cases. E6 does not establish physical truth. Historical D-009/D-010 F4-v1 FAIL/FAIL remains immutable; D-011/F4-v2 separately found no significant overdispersion at 30 yd and evidence of overdispersion relative to the fitted independent-pellet binomial reference at 40 yd. Those results are not overwritten or rerun by E6 PASS. Gaussian local structure, pellet independence, shot-to-shot spatial variation, longitudinal arrival shape, coupling/tails, other loads, breakage, scoring and DTL validity remain unresolved. E7 NOT STARTED. E8 NOT STARTED.**

## D-011 / F4-v2 — first prospective null test (2026-10-04)
COMPLETE; stopped for human review. This is new prospective methodology, not recovery of the historical CI method and not an E6 PASS. First results frozen in docs/evidence/f4_v2/receipt.json after the plan and implementation preflight were recorded.

- 30 yd: D_binomial=1.772853185595567; p_MC=0.06735093264906736; no significant overdispersion at alpha=0.05. This does not validate binomial independence.
- 40 yd: D_binomial=1.9118386090360198; p_MC=0.045098954901045096; evidence of overdispersion relative to the fitted independent-pellet binomial count model under this specified test. No physical mechanism or general validation follows.
- Each range: 1,000,000 ten-pattern experiments, PCG64 seeds 30192/40192, upper-tail >= comparison with +1 correction. The reported central 95% intervals are NULL REFERENCE INTERVALS, not confidence intervals for physical D.
- Historical D-009/D-010 FAIL/FAIL, E0-E5, fixtures, dependencies and original oracle.py preserved unchanged. Complete suite: 77 tests PASS (69 historical + 8 new); no E3 or historical F4 scientific rerun. Remaining E6 contact oracle, E7 and E8 not started. No commit or push.

## E6 contact-oracle implementation preflight — STOP (2026-10-04)
The final human authorisation fixed PCG64 seeds 60001–60006; the complete prospective plan was persisted in docs/evidence/e6/contact_oracle/plan.json before implementation. The accepted D-013 geometry is unchanged. The independent direct-contact sampler, isolated D-008 deterministic reference and one-shot runner have been drafted, but are not authorised by a passing software preflight yet.

The initial 11 focused synthetic tests passed. The expanded complete suite ran 96 tests: 94 passed, 2 errors, zero assertion failures, zero skips. Both errors were PermissionError while accessing temporary directories in two new runner fault-injection tests (including cleanup). No baseline E6 or isolated case-6 scientific comparison was executed; no authoritative contact-oracle receipt was reserved. Per the human implementation-failure STOP rule, no repair, retry or scientific execution followed. This is a software-preflight STOP, not an E6 scientific FAIL. See docs/evidence/e6/contact_oracle/preflight_stop.json.

Frozen E5, geometry, fixtures and historical receipts remain unchanged. E3 was audit-only; F4-v1 remains FAIL/FAIL and neither F4-v1 nor F4-v2 was scientifically rerun. E7/E8 not started. No stage, commit or push. Stop for human review.

## E6 contact oracle — first authoritative execution PASS (2026-10-04)
The human-authorised first contact-oracle execution completed once using the frozen six-case plan, PCG64 seeds 60001–60006, 1,000,000 single pellets and 20,000 rounds per case. All six single-pellet and 24 round-tail comparisons passed; all eight non-dispersion F4 reviewer regressions passed. Case 6 remains the isolated D-008 verification variant, not the E5 baseline. The complete immutable first result is docs/evidence/e6/contact_oracle/receipt.json (SHA-256 a2e08baf238d1adb8e9923bd98c8c2f918be8a672e56194fb4c17e348958fa05).

For the predeclared E6 verification cases, the independent Monte Carlo oracle agrees with the deterministic encounter calculation within the predeclared numerical tolerances. This is computational verification only. Historical D-009/D-010 F4-v1 FAIL/FAIL and D-011/F4-v2 remain unchanged; neither was scientifically rerun. The earlier preflight STOP records remain historical evidence. E5 remains frozen; E3 audit-only. Post-result full suite: 96 tests passed, zero skips. No scientific comparison was rerun. E7/E8 not started; no commit or push. STOP FOR HUMAN REVIEW.
