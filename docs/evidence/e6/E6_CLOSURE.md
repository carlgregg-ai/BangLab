# E6 closure — pre-Jones baseline

**Status:** PARKED  
**Frozen commit:** `9480c66752f554a1f85a72be5343d87e4e2ab868`  
**Frozen reference:** `archive/e6-pre-jones-frozen`  
**Boundary:** this commit immediately precedes `2e8855ecde4302d9b634f94397c3b16fcdb15364` (`research: add Jones to BangLab crosswalk`).

## What E6 establishes

E6 establishes computational agreement, for the six predeclared verification cases and their predeclared tolerances, between the deterministic encounter calculation and the independent direct Monte Carlo route.

The authoritative E6 contact-oracle receipt records:
- PCG64 seeds 60001–60006;
- 1,000,000 single-pellet trials per case;
- 20,000 rounds per case;
- all 6 single-pellet comparisons PASS;
- all 24 round-tail comparisons PASS;
- all 8 non-dispersion F4 reviewer regressions PASS;
- post-result complete suite: 96 tests PASS, zero skips;
- no scientific comparison rerun.

Authoritative result: `docs/evidence/e6/contact_oracle/receipt.json`  
Post-result audit: `docs/evidence/e6/contact_oracle/verification.json`

## Claim ceiling

E6 does **not** establish physical truth. It does not validate Gaussian local structure, pellet independence, shot-to-shot spatial variation, longitudinal arrival shape, coupling/tails, other loads, clay breakage, scoring, DTL validity, or a physically complete 3-D shot string.

Historical F4-v1 FAIL/FAIL and F4-v2 results remain separate evidence and are not overwritten by E6 PASS.

## Reproduction receipt

Project metadata declares Python >=3.11 with NumPy and SciPy. The preserved verification audit records the complete-suite command:

`python -B -X utf8 -m unittest discover -s tests -v`

No rerun was performed to create this closure record.

## Parking rule

The frozen reference is the authoritative **pre-Jones E6 baseline**. Jones-derived material, comparisons, interpretations, or later E7 work must not be retrofitted into that frozen state. Future comparisons should reference the frozen commit explicitly.

**E6 PARKED — authoritative pre-Jones computational baseline.**
