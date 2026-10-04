# Jones → BangLab crosswalk

**Status:** evidence review / E7 input, not model adoption  
**Date:** 2026-10-04  
**Jones source:** Bangleian `research/jones_2005/JONES_RECOVERED_MODEL_SPEC.md` and `PROVENANCE.md`

## Evidence boundary

The Jones material is a forensic reconstruction from four recovered compiled Java archives, not Jones's original source. The original JAR hashes and retrieval routes are recorded in Bangleian, but the Bangleian provenance record says the original binary bytes were not committed there in that transaction. Reconstructed equations/Python are derived evidence and must not be promoted to ground truth.

Jones is therefore an **external reference/challenger** to BangLab. It does not validate BangLab merely by agreeing with it.

## Crosswalk

| Jones recovered behaviour | BangLab analogue | Agreement / tension | E7 use |
|---|---|---|---|
| Independent Gaussian x/y pellet locations | E4 isotropic 2-D Gaussian lateral field | Strong structural agreement | Benchmark the same idealised baseline independently |
| D75 converted to sigma using 75% Rayleigh radial quantile | E4 sigma calibrated from DEP 30-inch fractions | Different parameterisation of the same Gaussian family | Convert both to common sigma/circle-fraction quantities and compare |
| Local expected strikes = density × pellet count × target area | E5 integrates density over an explicit pellet-dilated clay silhouette | BangLab geometry is more resolved; Jones optimiser uses scalar target area locally | Quantify small-target approximation error across BangLab cases |
| k-or-more strikes via very-large-n/small-p binomial ≈ Poisson(lambda) | E5/E6 round-tail probabilities use finite pellet-count Binomial from integrated per-pellet probability | Different count models | Compare Poisson/Jones vs finite-N BangLab tails where p is not tiny |
| Perfect Pattern Generator draws independent Gaussian pellets | E6 independent MC draws declared stochastic pellet positions | Conceptually close baseline | Use Jones-style generator as a compatibility benchmark, not a new physical claim |
| One-realisation gap scan using equivalent circular target | BangLab explicit ellipse/circle contact geometry | Jones scan is grid/equivalent-circle based; BangLab can represent orientation/translation | Use only as qualitative/compatibility cross-check |
| POI offset supported | E5 offsets e_a/e_c | Direct conceptual overlap | Check offset response and symmetry against Jones-compatible cases |
| Shooter placement model, including D95 skill dispersion | Not yet a BangLab physical input; eventual ShotKam move/replay will supply movement/placement uncertainty | Jones models aggregate shooter error; BangLab aims eventually to observe/replay movement | Keep outside E7 shotgun-physics baseline; useful later for shooter-model comparison |
| Jones default “Rayleigh” shooter integration actually weights 2-D point density with dr | No BangLab equivalent | Recovered implementation appears to overweight central placements relative to true radial Rayleigh | Do not copy; retain as adversarial compatibility case only |
| Statistical Confidence Tester compares pattern samples | F4-v2 directly tests shot-to-shot dispersion vs fitted binomial reference | Same epistemic concern, different test | Use Jones as historical motivation for replication/statistical-noise discipline |
| Statistical tester branch appears reversed relative to help text | No BangLab equivalent | Implementation discrepancy | Warning against treating legacy executable as authority |
| Pattern Optimiser allows POI + shooter skill + pattern spread | BangLab currently isolates shotgun encounter geometry | Jones has broader shooter-gun-target system scope | Future integration reference, not E7 baseline |
| Jones software does not establish Gaussian truth, pellet independence or break-from-contact | BangLab claim ceiling says the same | Strong epistemic agreement | Preserve explicitly through E7 |

## What Jones adds now

Jones independently converged on the same useful **baseline abstraction** BangLab currently uses: a radially symmetric Gaussian long-run pellet field and stochastic pellet outcomes. That makes his recovered executable valuable as a historical benchmark.

More importantly, Jones repeatedly treated **pattern-to-pattern variation** as something that must be measured rather than inferred from one pattern. This aligns directly with BangLab's unresolved F4-v2 result: at 40 yd the DEP p.82 counts showed prospectively significant overdispersion relative to the fitted independent-pellet binomial count model; 30 yd did not.

That does **not** establish a mechanism such as clumping. It establishes that E7 should challenge the independent-identically-distributed pellet baseline rather than silently promote it.

## Do not import

Do not import Jones's shooter-skill weighting, statistical-test branching, equivalent-circle target simplification, or Poisson approximation merely because they are historical Jones behaviour. Each is either a compatibility target, a simplification, or contains a recovered implementation concern.

## E7 consequence

E7 should begin with the frozen BangLab baseline and ask how encounter outputs change under bounded alternatives for:

1. shot-to-shot spread variation;
2. overdispersion / local clustering or other non-IID structure, without claiming a mechanism;
3. heavy-tail / flyer behaviour;
4. longitudinal arrival shape inside the E3-supported t2–t3 envelope;
5. longitudinal/lateral coupling;
6. target motion and geometry.

The decision criterion is **sensitivity of the practical encounter outputs**, not which model looks more realistic.

## Claim ceiling

A Jones/BangLab agreement means only that two implementations/approaches share or reproduce a declared mathematical behaviour. It is not independent physical validation. A Jones/BangLab disagreement is useful diagnostic evidence and must not be tuned away.
