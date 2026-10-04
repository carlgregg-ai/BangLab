# Decisions

## D-001 — v0.1 architecture
Use the deterministic Eulerian encounter/intensity field from the build contract. Do not implement pellet ODE, DEM or CFD for v0.1.

## D-002 — replaceable shot model
Preserve the conceptual boundary `FireEvent -> ShotModel -> evaluable ShotState/encounter field -> consumers`. Track E is the first implementation, not the permanent definition of a shot.

## D-003 — BangLab namespace
Repository/package namespace is `banglab`. The contract calls its package `claypath`; this is a non-scientific naming difference. Equations, fixtures, gates, tolerances and claim scope do not change.

## D-004 — Deng boundary
Deng supports plausibility of an evolving 3-D pellet swarm and radial-dispersion modelling. It does not independently validate BangLab longitudinal shot-string behaviour. DEM/CFD reproduction is future work.

## D-005 — locked rows
25/35/45 m may not be exposed to calibration/interpolation construction before E3. Access must be mediated by a one-shot gate capability; ordinary model code sees DEV rows only. E3 failure is a scientific result, not a coding defect.

## D-006 — missing p.82 raw rows
The supplied contract specifies 20 per-round p.82 observations but does not reproduce those observations. Do not reconstruct them from aggregates. Resolved: primary refs 1–20 are supplied in committed `data/fixtures/dep_p82.json`; the DEP Appendix B receipt records independent reproduction of published summaries. The source-data blocker is cleared. The prohibition on reconstructing observations from aggregates remains in force; E1 fixture integrity verification is still required.

## D-007 — E5 symmetry verification clarification (2026-10-04)
Human-authorised clarification before E5 implementation/results, against checkpoint `cf8d95923c35bacae3446b9bdeabba13bcbdf751`. The E5 STOP was legitimate: no failed scientific evaluation occurred, no E5 implementation existed at clarification, and no numerical result motivated this decision.

This clarifies the verification invariant in contract section 8.7; it does not change the physical/model specification in section 8.2.6. Under the isotropic baseline field and uniform arrival, arbitrary ellipse orientations require joint inversion: pi(e_a,e_c,psi) = pi(-e_a,-e_c,psi). Separate e_a and e_c reflections are required only when the target has those symmetries relative to the travel axes (principal axes aligned, including relative psi=0 or pi/2 modulo pi). Circular geometry is orientation-independent; rotational comparisons rotate the travel direction and offsets together for a moving target. General rotated non-circular ellipses must not be forced to satisfy separate reflections, nor may geometry/orientation be changed to satisfy a test. Use the existing numerical tolerances; no scientific tolerance changes.

Historical E0-E4 receipts remain unchanged. E6, E7 and E8 are not authorised by this clarification.

## D-008 — isolated E6 case-6 verification variant (2026-10-04)
Human-authorised clarification at `29d0d234eb126f5f280fc06c99fc07009d4bba88`. The original E6 STOP was legitimate and occurred before E6 implementation/results. No Monte Carlo comparison had been run; no numerical result motivated this clarification.

Contract section 8.7 case 6 is retained, not deleted or substituted. It is an isolated CONTRACT-SPECIFIED VERIFICATION VARIANT (kappa=0.4 and 10% tail both PROPOSED), not part of the frozen E5 baseline. Cases 1-5 compare an independent oracle against frozen E5; case 6 compares a separate deterministic variant reference against an independent variant oracle. E5 and historical E0-E5 receipts remain frozen and unchanged. The variant must not become the baseline; this is not commencement of general E7 sensitivity analysis.

For case 6 only, authorisation covers the minimum separate reference and oracle for the exact contract definitions (8.2.2 and 8.2.5): h(q)=0.9 on [0,1] plus 0.1 on [1,2]; sigma(q,R)=sigma_bar(R)*(1+0.4*(q-1/2)); sigma_bar calibration preserves each p.82 marginal circle fraction under that h. These are model/stress definitions, not measurements. A material missing definition requires another STOP. No seed, sample count, tolerance, parameter, case or failed first result may be changed to obtain a pass. E7/E8 remain unauthorised.

## D-009 — F4 dispersion statistic and prospective uncertainty rule (2026-10-04)
Human-authorised clarification at `29d0d234eb126f5f280fc06c99fc07009d4bba88`. The preceding F4/E6 STOP was legitimate and occurred before F4/E6 numerical evaluation. No estimator was tested against the targets before selection; no Monte Carlo comparison or E6 scientific PASS/FAIL result had occurred. No numerical result motivated this clarification.

For the replicate count variable N, define mean(N)=sum(N_i)/n and s_N^2=sum((N_i-mean(N))^2)/(n-1). F4 D=s_N^2/mean(N), using SAMPLE variance, ddof=1; do not substitute population variance. The contract targets remain 1.77 (30 yd) and 1.91 (40 yd), unchanged. Do not replace this variance-to-mean definition with binomial-normalised dispersion.

Acceptance at each range requires its target to lie within a prospectively defined 95% uncertainty interval for the Monte Carlo estimate of D. The exact interval method, replicate/sample structure, fixed parameters and any RNG/seeds must be fixed before evaluation. No fixed tolerance was reverse-engineered from the targets. If the existing design does not unambiguously determine that interval, STOP before calculating D and obtain the missing prospective decision; never select a method after seeing which interval contains a target.

D is a contract verification statistic, not a directly measured physical shotgun parameter or evidence establishing clumping, independence or physical validity. Historical E0-E5 receipts remain unchanged. D-008 and other E6 controls remain in force. E7/E8 are not started or authorised.

Pending design clarification: the existing E6 contact-count simulations do not specify an F4 Monte Carlo replicate experiment at 30/40 yd, its sampling/resampling law or its 95% interval construction. D-009 fixes the estimator and target-in-interval rule, but does not supply those remaining definitions. No D calculation or E6 comparison has been performed.

## D-010 — F4 physical replicates and bootstrap design (2026-10-04)
Human-authorised clarification before F4 D calculation, bootstrap, target comparison or E6 scientific result. The preceding STOP was legitimate and occurred before D was calculated; no target comparison had occurred. No design, estimator or uncertainty method was selected after inspecting D or target inclusion.

N is the canonical raw DEP p.82 30-inch-circle pellet count per physical shot, not paper counts, rounded percentages, E5 expectations or E6 simulated contacts. Use refs 1-10 at 30 yd and refs 11-20 at 40 yd: n=10 independently observed patterns per range. Calculate arithmetic mean, sample variance (n-1, ddof=1), and D=sample variance/mean directly from these observations, separately by range. D-009 targets remain 1.77 and 1.91.

Use the ordinary nonparametric shot-level bootstrap: sample ten complete count observations with replacement per replicate; B=100000; D*=sample variance(ddof=1)/mean. Use the percentile 95% interval (empirical 2.5th and 97.5th percentiles). RNG is numpy.random.Generator(numpy.random.PCG64(seed)), independently seeded 30030 at 30 yd and 40040 at 40 yd. Both inclusive target-in-interval checks must pass, at full precision. No seed, B, ddof, method, confidence level, target or tolerance changes after results.

This interval addresses finite-observation uncertainty under resampling these ten physical shot counts. It does not quantify measurement error, denominator uncertainty, Gaussian-model uncertainty, other-load uncertainty, E6 oracle Monte Carlo error or physical validation. E6's separate 20000-round contact comparison remains distinct. Historical E0-E5 receipts and frozen E5 remain unchanged. D-008 and D-009 remain binding. E7/E8 remain unstarted.

## D-011 — F4-v2 prospective binomial-reference dispersion test (2026-10-04)
NEW PROSPECTIVE SCIENTIFIC DECISION authorised by the human after the historical D-009/D-010 FAIL/FAIL and provenance investigations. This is not recovered historical methodology. The probable original central statistic and printed historical intervals are known; the original CI algorithm, exact estimator conventions, script and full-precision endpoints remain unrecovered. No new F4-v2 null simulation has been evaluated at this declaration. Historical D-009/D-010 and their first failure remain immutable.

Use only canonical raw p.82 30-inch-circle counts: refs 1-10 at 30 yd and 11-20 at 40 yd, ten physical fired patterns separately at each range; nominal pellet count 192. Set mean_N=arithmetic mean, p_hat=mean_N/192, s_squared=sample variance (ddof=1), and D_binomial=s_squared/[mean_N*(1-mean_N/192)]. No rounded percentages or printed SDs enter the primary calculation. D greater/less than one describes over/underdispersion relative to this fitted reference, not a mechanism.

At each range generate 1,000,000 experiments of ten independent Binomial(192,p_hat) counts, fixing p_hat from that range's observations. Every simulated D uses ddof=1 and its own experiment mean in the denominator. Use numpy.random.Generator(PCG64), seeds 30192 (30 yd), 40192 (40 yd), one binomial call of shape (1000000,10) per range. The one-sided upper-tail p_MC=(1+count(simulated_D >= observed_D))/(1000000+1), including ties and mandatory +1 correction. Evidence of overdispersion iff p_MC < 0.05, separately per range; no claim of joint/familywise control.

Report the simulated D distribution's 2.5th and 97.5th percentiles with NumPy method="linear" (index (B-1)*q/100 and adjacent-value interpolation), fixed before evaluation. This is a NULL REFERENCE INTERVAL, not a confidence interval for true physical D and not recovery of historical CIs. The historical central values may be compared only after the first new result is frozen. Neither historical central targets nor historical interval endpoints determine the new decision.

Implementation handling fixed prospectively: if any observed/simulated denominator is zero (mean 0 or 192), STOP and preserve the condition; never exclude or redraw experiments. Reserve the first run before calculation and refuse another run. Preserve each range result immediately. No change to seed, B, estimator, alpha or method after evaluation; no rerun seeking a different result. The complete predeclaration and preservation hashes are in docs/evidence/f4_v2/plan.json. An isolated oracle_f4_v2 module owns this authorised randomness; historical oracle.py and E0-E5 stay unchanged.

The strongest significant-result claim is: "The DEP p.82 30-inch-circle counts at this range show greater shot-to-shot dispersion than predicted by the fitted independent-pellet binomial count model under the prospectively specified F4-v2 test." Do not infer clumping, spatial clustering, cartridge/barrel/aerodynamic mechanisms, a particular physical independence failure, other-load behaviour or physical validation. Nonsignificance does not validate independence. This decision does not convert historical E6 FAIL to PASS or authorise remaining E6 contact-oracle cases, E7 or E8. Stop for human review after the first F4-v2 evaluation; no commit or push.
