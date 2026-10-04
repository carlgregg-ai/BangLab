# D-011 / F4-v2 first-result human review

NEW PROSPECTIVE METHODOLOGY. Historical CI method remains unrecovered.
Historical D-009/D-010 FAIL/FAIL remains unchanged; E6 is not promoted to PASS.

The plan preceded evaluation; implementation hashes were frozen in preflight.json.
The first evaluation was reserved exclusively and completed once. No rerun.

| Range | Observed D_binomial | Historical rounded D | Upper-tail count | p_MC | Central 95% NULL REFERENCE INTERVAL | Per-range decision |
|---|---:|---:|---:|---:|---|---|
| 30 yd | 1.772853185595567 | 1.77 | 67350 | 0.06735093264906736 | 0.3043992838779307 to 2.1098901098901086 | Not significant |
| 40 yd | 1.9118386090360198 | 1.91 | 45098 | 0.045098954901045096 | 0.3004694835680751 to 2.1091919793527887 | Evidence of overdispersion |

Historical central values were compared only after the completed receipt was
frozen. Agreement does not recover historical CI methodology. The historical
CI endpoints are not inputs or acceptance criteria anywhere in the new runner.

Observed estimator: arithmetic mean; sample variance ddof=1;
D=s_squared/[mean*(1-mean/192)]. Null generation fixes p_hat=observed_mean/192,
but each simulated experiment uses its own mean in its D denominator.
B=1000000 experiments of ten Binomial(192,p_hat) observations per range;
Generator(PCG64) seeds 30192 and 40192. One-sided p=(1+count(D_sim>=D_obs))/(B+1),
alpha=0.05 with strict < decision, separately by range, not a familywise test.
NumPy percentile method="linear", 2.5th/97.5th percentiles. These are simulated
NULL REFERENCE INTERVALS, not confidence intervals for true physical D.
The descriptive two-sided reference interval is not the one-sided decision rule.

At 40 yd the permitted claim is: "The DEP p.82 30-inch-circle counts at this
range show greater shot-to-shot dispersion than predicted by the fitted
independent-pellet binomial count model under the prospectively specified
F4-v2 test." This does not identify clumping, spatial clustering, cartridge,
barrel or aerodynamic causes, a particular physical independence failure,
other-load behaviour, or physical validation. At 30 yd, nonsignificance does
not establish binomial independence.

Software verification: 77 tests passed, zero failures/errors/skips after the
first result (69 historical + 8 new). Synthetic tests cover exact rational
arithmetic, ddof=1, fitted denominator, seeded simulations, mandatory +1 and
ties, strict alpha boundary, linear percentiles, rejection of undefined
statistics, exclusive-run refusal and historical-file preservation. The saved
result test audits arithmetic and metadata without another null simulation.
The historical E3 tests audit its saved receipt rather than reopening its gate.

Development history: the test-first import failed before implementation;
a temporary-directory permission issue in a guard test was removed by testing
exclusive-open refusal against an existing immutable receipt; the default
bundled Python lacked SciPy, so the already-present e2-wheel-runtime packages
were used. No dependency declaration, installation, seed or scientific method
was changed. Before evaluation the suite passed with only the saved-result
check skipped because no result yet existed.

Only DECISIONS.md and STATE.md among existing tracked files changed.
New files: banglab/encounter/oracle_f4_v2.py; banglab/f4_v2_gate.py;
tests/test_f4_v2.py; docs/evidence/f4_v2/{plan.json,preflight.json,receipt.json,
review.md,verification.json}. Historical implementation, fixtures and receipts
are byte-preserved. E6 contact-oracle cases, E7 and E8 remain unstarted.
Nothing staged, committed or pushed. Stop for human review.
