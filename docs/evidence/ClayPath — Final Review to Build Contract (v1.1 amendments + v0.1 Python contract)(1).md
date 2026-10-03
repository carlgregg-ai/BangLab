# ClayPath — Final Review to Build Contract (v1.1 amendments + v0.1 Python contract)

Oct 3, 2026 · @Carl Gregg

## 1. Executive decision

**CONDITIONAL GO.** Build the v0.1 encounter landscape now as an intensity field at the clay's range, driven by the DEP main-string timing (t2, t3; Fig B1) and a lateral spread calibrated to the DEP 30/40 yd circle counts (p.82). The primary pages close cleanly: the fixture transcribes exactly, 293 m/s is correct, and every derived column reproduces from t2/t3 and ½mv². What the pages cannot supply is the arrival shape inside the string, the true lateral profile, the coupling between the two, and clay-scale clumping; my sensitivity checks show the lateral profile and clumping can move outputs past the materiality thresholds, so those must ship as declared variants that turn a point answer into a band. STOP is not justified: no single missing quantity makes a bounded, banded geometric-contact trainer misleading.

The conditions are build conditions, not research:

1. **E1 fixture integrity passes** with 293 m/s, hash-locked values, and derived columns never counted as validation.
2. **Locked rows (25/35/45 m) are evaluated once** at the tolerance declared here (1.0 ms); a failure restricts the range, it is never tuned away.
3. **Every output is GEOMETRIC\_CONTACT, labelled MODEL\_PREDICTION**, under the claim ceiling in §7 (A13).
4. **The E7 sensitivity variants run on every landscape**; any MATERIAL flag replaces the point value with a displayed band.
5. **Carl's own cartridge enters only as a USER\_LATERAL profile**; its string timing is the DEP proxy, labelled ASSUMED.

## 2. DEP primary-source closure

Figure B1 (printed p.77) is verified cell-for-cell against the page image. The only mismatch with the brief is the 20 m leading velocity: **the primary value is 293 m/s**.

### Fixture as transcribed (main section of the cloud only)

| R (m) | t2 lead (ms) | t3 trail (ms) | vL (m/s) | vT (m/s) | EL (J) | ET (J) | L (m) | Split |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 60.8 | 68.4 | 293 | 250 | 8.0 | 5.9 | 1.9 | DEV |
| 25 | 78.7 | 89.2 | 265 | 230 | 6.6 | 4.9 | 2.5 | LOCKED |
| 30 | 98.4 | 111.8 | 242 | 213 | 5.5 | 4.2 | 2.9 | DEV |
| 35 | 120.0 | 136.2 | 223 | 198 | 4.6 | 3.7 | 3.3 | LOCKED |
| 40 | 143.3 | 162.4 | 206 | 185 | 4.0 | 3.2 | 3.6 | DEV |
| 45 | 168.4 | 190.3 | 192 | 173 | 3.4 | 2.8 | 3.9 | LOCKED |
| 50 | 195.3 | 220.0 | 180 | 163 | 3.0 | 2.5 | 4.1 | DEV |

t2 and t3 are MEASURED\_PRIMARY flight times from the muzzle. That they are ten-round means is INFERRED from the p.76 design (10 rounds per range); p.77 does not say so. v, E and L are SOURCE\_DERIVED: the caption calls them outputs of the analysis program.

### Mismatches

- **20 m vL: brief 292, primary 293.** Primary governs. Arithmetic cannot discriminate: ½mv² gives 7.97 J vs 8.03 J (both print 8.0), and 20→30 m kinematics give 37.63–37.71 ms vs 37.57–37.65 ms against a measured 37.6 ms. The correction rests on the printed digit, which is legible.
- **Impact:** zero for the encounter engine, which uses t2/t3 directly. For a V5 synthesis run started at 20 m, 1 m/s moves the 50 m leading-edge arrival by about 0.46 ms, above the 0.1 ms print resolution, so V5 must use 293.
- p.82, 30 yd Ref 2 paper count has an overstrike artifact. It reads 192, confirmed by the printed mean (column sum 1877).
- No conflict with the frozen spec §7 load description.

### Locators and column semantics

- p.75 load and gun: 35.8 g, 192 pellets, 187 mg, 3.15 mm, 363 m/s at 2.5 m; 29" proof barrel, 18.4 mm bore, 0.030" choke; 23 °C, 1006 mb, 56.5% RH. p.76: wind 1 m/s from 225°; 20–50 m in 5 m steps, 10 rounds per range.
- p.77 footnote 1: L is quoted when the leading edge is at the range shown. Reconstructing L = R − x\_trail(t2(R)) gives 1.93/2.92/3.59/4.14 m at the dev rows against printed 1.9/2.9/3.6/4.1.
- Velocities reproduce the dev-interval flight-time differences within 0.2 ms. Energies reproduce ½mv² for pellet mass 186.5–187.5 mg in all 14 cells.
- **Consequence: v, E and L carry no information beyond t2, t3 and pellet mass.** They are consistency checks, never independent validation observations.
- p.80 Figs B6–B8: single-round detector traces at 30/40/50 m. Sparse arrivals continue past t3 (to about 168 ms at 40 m; 226–240 ms at 50 m; figure-read ±2 ms).
- p.81 Figs B9–B11: 40 yd dot plots (rounds 18/11/14 at 70/77/83%). At 150 ppi, about 5 mm per pixel at pattern scale, they cannot be digitised reliably.
- p.82 footnote 2: % is of the average 192 pellets per cartridge.

### Repeatability and sig/avg (p.82 is the only dispersion data in Appendix B)

| Range | Paper count mean (SD) | 30" circle mean (SD) | Circle % mean (SD) | sig/avg paper / circle | Dispersion vs binomial, D (95% CI) |
| --- | --- | --- | --- | --- | --- |
| 30 yd | 187.7 (3.8) | 180.5 (4.2) | 94 (2.2) | 2.0% / 2.3% | 1.77 (0.84–5.91) |
| 40 yd | 191.1 (4.5) | 145.3 (7.8) | 76 (4.1) | 2.3% / 5.4% | 1.91 (0.90–6.37) |

- Verified semantics: SD is the population SD (÷n; a sample SD would print 4.0/4.4/4.7/8.2). sig/avg = SD/mean. Every % equals round(100 × count/192), all 20 reproduce.
- Allowing per-cartridge count variation (paper SD as an INFERRED proxy), the excess disappears: variance ratio 0.76 at 30 yd, 1.40 at 40 yd, neither significant. This is consistent with conditionally independent pellets plus modest round-to-round variation; ten rounds cannot exclude moderate clustering.
- **No dispersion statistic for t2, t3, v, E or L appears in Appendix B.** The spec §6 values (≈1.2%/1.5%) are Compton-sourced and unverified by this pack.
- The 30 yd paper mean sits below the 40 yd one. That is count-level noise; paper counts are not tail calibration.

### Tolerance implications

- **Can justify:** a reproduction check of every p.82 statistic (E1); an empirical between-round spread on circle % (SD 2.2 and 4.1 points); the dispersion index used by the clumping stress variant (PROPOSED use).
- **Cannot justify:** any tolerance on t2, t3, Δt or velocity; any Gaussian sigma for timing; any clay-scale clumping value; any lateral validation, because both ranges are consumed by calibration.
- **So the locked-row tolerance is a training-materiality tolerance, declared now: |error| ≤ 1.0 ms on t2, t3 and Δt.** At a 20 m/s crossing speed, 1 ms moves the clay 0.02 m, under half the 0.055 m materiality threshold in §6.

## 3. Shot-density feasibility

**Compton + DEP support a training-grade, range-dependent pellet density at the clay for the DEP reference load over 20–50 m.** They do not pin the arrival shape inside the string, the lateral profile shape, the coupling between them, clay-scale clumping, or anything outside 20–50 m. Those stay ASSUMED and ship as variants.

| Model element | Evidence in the pack | Label |
| --- | --- | --- |
| Main-string window t2(R), t3(R) | Fig B1 dev rows; locked rows test the interpolant | MEASURED\_PRIMARY rows; interpolant MODEL\_PREDICTION |
| String duration Δt = t3 − t2 (7.6 / 13.4 / 19.1 / 24.7 ms at 20/30/40/50 m) | Arithmetic on Fig B1 | SOURCE\_DERIVED |
| Pellet count 192, diameter 3.15 mm | p.75 | MEASURED\_PRIMARY |
| Lateral spread σ(R) | Gaussian form (spec §6, Compton's lateral analysis) fitted to p.82 circle fractions: σ = 0.1606 m at 30 yd, 0.2266 m at 40 yd | INFERRED; circle centred on pattern ASSUMED; linear in R ASSUMED (2 points, 0 dof) |
| Arrival shape inside \[t2, t3\] | None in the pack; Compton prefers Rayleigh but no parameters here, and below-30 m profile fits carry the saturation qualification | UNKNOWN; uniform ASSUMED |
| Pellets outside the main section | Visible in B6–B8; fraction not given | UNKNOWN; baseline assigns all 192 to the main section (ASSUMED) |
| Longitudinal–lateral coupling | Sign only: Compton's 3-D reconstruction puts deformed pellets trailing/outer | Sign SOURCE\_DERIVED; magnitude UNKNOWN |
| Clumping at clay scale | p.82 is consistent with independence plus round-to-round variation at 30" scale | UNKNOWN at clay scale |
| Muzzle to 20 m, beyond 50 m | Compton warns against muzzle-start free-flight clouds | UNSUPPORTED |
| Carl's own cartridge | Not in the pack | UNKNOWN; enters as USER\_LATERAL |

**Why this is enough to build.** The training levers (lead, timing, vertical error) act through Δt, σ(R) and the clay's crossing speed v⊥, and the first two are anchored in primary data. The biggest single lever is that the density-optimal lead points the pattern centre at mid-string, not the leading edge. That offset is v⊥·Δt/2: 0.134 m at 30 m and 0.191 m at 40 m for a 20 m/s crosser. It exceeds every variant shift I computed (largest 0.082 m), so it survives the unknowns.

**What does not survive the unknowns:** absolute E\[N\], P(N≥k) and window widths. Lateral profile shape alone moves peak E\[N\] by −30% to +38%, and clumping moves P(N≥3) by up to 0.10 (full table in §5). That is why the condition in §1 is a band, not a single number.

**Compton's equations are not needed for v0.1.** Inside 20–50 m the DEP observables give t2, t3 and spread directly. Compton's synthesis and stochastic models (V5, V8) earn their place only when ClayPath must extrapolate to another load or range. They stay on their own track, behind the C/gamma gate for cube-law.

## 4. v0.1 architecture decision

**Choose B: an Eulerian intensity field evaluated at the clay's range.** Hits are counted from a closed-form arrival-and-spread density, not from simulated pellet flights.

```latex
\lambda(\mathbf{x},t\mid R)=N_p\,h_R(t)\,\varphi_R(\mathbf{x}),\qquad \pi(\mathbf{e})=\int_0^1 h(q)\,G\big(\mathbf{c}(q;\mathbf{e})\big)\,dq,\qquad N\sim\mathrm{Binomial}(N_p,\pi)
```

Here x is position in the plane normal to the line of fire at range R, q = (t − t2)/Δt is the fraction of the way through the main string, and G(c) is the lateral probability mass inside the pellet-dilated clay silhouette centred at c. The baseline is deterministic quadrature; it needs no Monte Carlo.

| Criterion | A: explicit stochastic pellet paths | B: intensity field (chosen) |
| --- | --- | --- |
| Evidence needed | Per-pellet initial states plus forcing constants (Compton's, for his loads, not in the pack), or a muzzle cloud, which spec §9 bars | t2/t3(R) and σ(R), both in the pack |
| Reproduces DEP observables | Only after tuning, which turns prediction into calibration | t2/t3 by construction, circle % by calibration; locked rows still test timing |
| Contact counts | Monte Carlo estimates with sampling error | E\[N\] by quadrature; P(N = n) from the Binomial |
| Cost per landscape | 192 pellets × M realisations × ODE steps | 1-D quadrature of a closed form; milliseconds per point |
| Falsifiability | Assumptions buried in forcing parameters | Each assumption is a named, switchable variant |
| Training utility | Same landscape, plus animation | Same landscape; animation frames sampled from the field |

**Why A is not required yet.** The one observable that needs explicit paths is pellet identity across planes: the same pellet's position at two ranges. No v0.1 output needs it. The nearest case is a receding clay, whose effect is a window stretch of v/(v − v\_r): about +11% at v\_r = 20 m/s and 40 m, reported as a diagnostic (O7).

**Explicit pellets still appear in two bounded roles.** The E6 oracle samples pellet times and positions from the same field and counts hits by brute force, to check the quadrature. Animation frames are sampled at the encounter plane only, never drag-propagated from the muzzle. Both carry MODEL\_PREDICTION with the receipt role "realisation, not the fired cloud".

&#91;embedded content: v0.1 encounter engine · 3 inputs, 6 modules, 2 side checks\]

The baseline runs straight down from the two DEP tables and the scenario; the dashed side paths are the E7 variants and the E6 oracle, which test it without feeding it.

## 5. Joint longitudinal/lateral treatment

**v0.1 uses the factorised approximation P(r\_lateral | z\_string, R) ≈ φ(r | σ(R)): lateral spread does not depend on where a pellet sits in the string. Label: ASSUMED.** Its sensitivity test is a coupling variant that lets spread grow from leading to trailing edge while keeping the measured circle fractions fixed.

The pack gives the sign of the coupling but not its size. Compton's 3-D reconstruction puts deformed pellets toward the trailing and outer region (spec §6), which implies spread rising toward the trailing edge. DEP gives no conditional data: Fig B1 is timing only, p.82 is whole-pattern counts, and B9–B11 carry no timing.

**Coupling variant (PROPOSED stress values, not measurements):** σ(q) = σ̄(R)·(1 + κ(q − ½)). A trailing/leading spread ratio of 1.5 gives κ = 0.4; a ratio of 2.0 gives κ = 2/3. σ̄ is re-fitted at 30 and 40 yd so the marginal circle fractions still equal p.82, so any output change is due to coupling alone.

**Falsifier.** The physical falsifier would be a measured lateral spread for leading versus trailing pellets at one range; the pack has none. v0.1 can therefore establish whether the assumption matters, not whether it holds. Where a variant crosses a materiality threshold, the factorised value is shown inside a band.

### Effect sizes of every v0.1 variant

Computed at the dev ranges 30 and 40 m, face-on clay, crossing speed 0 and 20 m/s, against the baseline (uniform arrival, Gaussian, linear σ, factorised, independent pellets). Thresholds are the PROPOSED materiality values in §6.

| Variant | Peak E\[N\] change | Optimum lead shift (m) | Window FWHM change (m) | Verdict |
| --- | --- | --- | --- | --- |
| Coupling, ratio 1.5 (κ = 0.4) | +3% to +6% | −0.036 to −0.050 at 20 m/s (toward leading edge) | −0.02 | Not material; borderline at 40 m, 20 m/s |
| Coupling, ratio 2.0 (κ = 2/3) | +9.5% to +19% | −0.058 to −0.082 at 20 m/s | −0.05 to −0.06 | **MATERIAL** |
| Arrival front- or back-loaded (triangular) | 0% to +3% | ±0.046 (30 m), ±0.066 (40 m) at 20 m/s; 0 static | −0.01 to −0.02 | **MATERIAL** for the optimum at 40 m, 20 m/s |
| 10% of pellets trailing past t3 | 0% static, −6% at 20 m/s | +0.012 to +0.018 | +0.03 | Not material |
| Lateral shape, generalised Gaussian β = 1.5 / 3.0 | +17% to +38% / −16% to −30% | 0 | −0.07 to −0.14 / +0.11 to +0.15 | **MATERIAL** |
| Proportional σ law instead of linear | −5% (30 m), +6% (40 m); −22% (20 m), +12% (50 m) static | 0 | ≤ 0.02 | **MATERIAL** outside the 27–37 m calibration span |
| Clumping, negative binomial D = 1.91 | 0 (mean unchanged) | 0 | 0 | **MATERIAL** for P(N≥3): −0.07 to −0.10 at E\[N\] 2.9–4.8 |

Two readings matter for training. First, coupling pulls the optimum toward the leading edge while back-loading pushes it the other way, so the optimum-lead band is about ±0.08 m around mid-string at 40 m and 20 m/s. That band is still narrower than the 0.191 m gap between mid-string and front-of-string lead, so the headline lesson holds. Second, absolute contact numbers are only good to roughly ±30%, so the trainer must show bands and compare scenarios, not quote single counts.

**Gravity across the string** is the other joint effect. Trailing pellets fall further: 0.5, 1.4, 2.9 and 5.0 cm more at 20, 30, 40 and 50 m (vacuum-in-time estimate, INFERRED). That stays under the 5.5 cm threshold everywhere, so it is reported as a diagnostic (O7), not modelled.

## 6. Probability-landscape outputs

**Seven outputs are frozen, and the reported tail probabilities are predeclared now: P(N≥2), P(N≥3) and P(N≥5). P(N≥1) is computed but is diagnostic only, never a headline.** The window reference is k = 3 at probability 0.5. These k values are reporting choices (PROPOSED), not breakage thresholds; nothing in the pack links a contact count to a broken clay.

All outputs live on a grid of aim offset e = (e\_h, e\_v) in a pattern-centred frame at the clay's range. e = 0 means the clay centre sits on the pattern centre at mid-string time. Every output is GEOMETRIC\_CONTACT, labelled MODEL\_PREDICTION.

| ID | Output | Definition |
| --- | --- | --- |
| O1 | Expected contacts EN | N\_p·π(e); the primary map |
| O2 | Count distribution P(N = n) | Binomial(N\_p, π); negative binomial under the clumping variant |
| O3 | P(N≥k), k ∈ {2, 3, 5} | Upper tail of O2; k = 1 diagnostic only |
| O4 | Encountered density | E\[N\]/A\_eff, pellets per m², A\_eff = dilated silhouette area |
| O5 | Tolerance windows | Along- and cross-track FWHM of E\[N\]; region where P(N≥3) ≥ 0.5, reported EMPTY when none exists |
| O6 | Optimum | e\* = argmax E\[N\]; density-optimal lead L\* = v⊥·t\_mid + e\*\_a, shown beside the front-of-string lead v⊥·t2; timing equivalent δt = e\_a/v⊥ |
| O7 | Diagnostics | Smear S = v⊥Δt and S/σ; gravity drop across the string; centroid drop ½g·t\_mid² (INFERRED upper bound) for sight-picture conversion; receding stretch v/(v − v\_r); applicability and variant flags |

**Materiality thresholds (PROPOSED, training-based, fixed before any evaluation):** an optimum or window edge moving more than 0.055 m (half a clay); P(N≥k) changing by more than 0.05 absolute; E\[N\] at the optimum changing by more than 10%. A variant that crosses any threshold sets that output's MATERIAL flag, and the display shows the baseline inside the min–max band across variants.

**Lead and timing share one axis.** A timing error δt with unchanged aim is indistinguishable from an along-track lead error v⊥·δt in this frame. v0.1 therefore reports timing as a relabelled lead axis and does not model range change from late shots.

**Monte Carlo is not in the baseline.** It appears only in the E6 oracle and in animation frames. Any Monte Carlo probability is reported with SE = √(p̂(1 − p̂)/M), its seed and M.

## 7. Required v1.1 amendments

**v1.1 = frozen v1.0 + the twenty named amendments below; nothing else changes.** The integration brief is not in the pack, so every instruction is anchored to a v1.0 clause. Brief test IDs other than C4/C5 are left for the editor to map in A2 (flagged, not guessed).

1. **A1 Precedence (insert new §0).** "Authority order: (1) primary source pages, for what a source says; (2) v1.1 clauses that name the v1.0 clause they override; (3) remaining v1.0 clauses; (4) the integration brief; (5) review comments, never canon until reconciled. Every detected conflict is logged in the run receipt with both locators and the winner."
2. **A2 Test crosswalk (new §12.1).** Add a table: V0–V10 and E0–E8 down the side, brief IDs beside them. Fixed entries: E3 is Track E's V7 run (each model gets exactly one locked evaluation, logged separately); C4 maps to the clay-kernel regression that precedes V9; C5 is REPORT-ONLY. The editor fills the P/HM column; a brief test with no V/E home is mapped or deleted, never left floating.
3. **A3 Restore V5 (§12).** "V5: Compton synthesis regression, after complete transcription of the synthesis expressions. Reproduce Compton's published synthesis outputs at their print precision. For DEP use, initialise downstream at Fig B1 20 m: leading 60.8 ms, 293 m/s; trailing 68.4 ms, 250 m/s."
4. **A4 Restore V8 (§12).** "V8: Compton stochastic width/length regression. Square-law forms (5.22, 5.23, 5.34, 5.52, 5.60) run once Compton's fitted parameters and W/L data are transcribed with locators. Cube-law forms stay behind A6. V8 is source regression, not DEP validation."
5. **A5 Restore Allen continuity (§8 tests 5–6 → V4a/V4b).** "V4a: numerical vs analytical, each Allen branch. V4b: evaluate drag either side of every branch boundary and report the jump against a tolerance declared before running. A jump present in the source relation is recorded as SOURCE\_DERIVED, never smoothed."
6. **A6 C/gamma gate (§4, add status).** "Status at v1.1: CLOSED. C and gamma are not transcribed. Cube-law code (5.56, 5.63) is not written, stubbed with guessed constants, or chosen by a square/cube selector until both are transcribed with page locators. Running both laws is sensitivity analysis, not evidence."
7. **A7 CN gate (§10).** "CN is absent by default, not 100. Code that reads CN while absent raises. CN enters only after its equation, definition and units are verified on the source page. No Andert coefficient fitting in v0.1."
8. **A8 DEP 293 correction (§7).** "20 m leading-edge velocity = 293 m/s. Locator: DEP 99/953 Appendix B, printed p.77, Figure B1. The primary extract is not altered; the brief value 292 is logged as a conflict, primary wins."
9. **A9 Downstream cloud start (§9).** "Any cloud propagated in range starts at the DEP 20 m state or later. A muzzle-start cloud is ASSUMED and runs only as a labelled sensitivity, never as Compton regression. The encounter engine refuses ranges outside 20–50 m."
10. **A10 Collision convention (new §9B).** "Contact = pellet centre inside the clay silhouette dilated by r\_p = d\_p/2 (1.575 mm for DEP), approximated by the ellipse (a + r\_p, b + r\_p). Area error ≤ 1.4% at b = 12.5 mm; exact for a circle. Closed set: tangency is contact. Numerical tolerance 1e-12 in normalised coordinates. Contact is GEOMETRIC\_CONTACT, not breakage."
11. **A11 C4/C5 treatment (§10).** "C4 = clay-kernel implementation and limiting-case regression, pass/fail, cases declared before running; precondition to V9. C5 = comparison against Andert's measured flights, REPORT-ONLY: no pass/fail, no tuning, no validation claim."
12. **A12 Monte Carlo uncertainty (§9, receipt).** "Every Monte Carlo estimate reports M, generator (PCG64), seed and SE = √(p̂(1 − p̂)/M). Oracle rules: rounds, |p̂ − P\_quadrature| ≤ 4·SE + 1e-3 at 20,000 rounds; single pellets, |p̂ − π| ≤ 4·SE at 10^6 pellets. Variant bands are not sampling error and are displayed separately."
13. **A13 Claim ceiling (new §17).** "ClayPath v0.1 outputs are model predictions of geometric pellet contacts with a declared clay silhouette, for the DEP 99/953 reference load at 20–50 m, under declared assumptions, with variant bands. They are not predictions of breakage, scoring, Carl's cartridge, a DTL trajectory, or any actual fired cloud."
14. **A14 Column semantics (new §7.1).** "t2/t3 are MEASURED\_PRIMARY main-section flight times from the muzzle. vL, vT, EL, ET and L are SOURCE\_DERIVED analysis outputs; L is quoted when the leading edge is at R. Derived columns are consistency checks, never independent validation observations."
15. **A15 Repeatability (new §7.2; qualifies §6 bullet 2).** "Appendix B gives dispersion only for pattern counts (p.82: population SD; sig/avg = SD/mean; % = count/192). It gives none for t2, t3, v, E or L. The ≈1.2%/1.5% values are Compton-sourced and unverified by DEP; they never become a Gaussian sigma, a truncation rule or an acceptance tolerance."
16. **A16 Track E (new §9A; amends §15).** "Add Track E, the encounter landscape, per the v0.1 contract. Code order: after steps 1–2 and 6, run E0–E8. Track E does not depend on the pellet ODE (steps 3–5) or Compton (steps 7–8)."
17. **A17 Locked split for Track E (§7).** "Track E calibration reads dev rows only. A guard raises on any access to 25/35/45 m before E3. E3 runs once; its ledger goes in the receipt."
18. **A18 Leading/trailing treatment (§9 rule 3).** "t2 and t3 are interpolated separately, so their different deceleration is carried by construction. The physics track keeps separate leading and trailing initial states from Fig B1."
19. **A19 Saturation qualification (§3.1, restated).** "The below-30 m saturation qualification applies to longitudinal density-profile fits only. Track E fits no profiles, so it is not triggered."
20. **A20 Anti-drift additions (§14).** Do not say: "the landscape shows where the clay breaks"; "P(N≥1) is the hit probability"; "the realisation is the fired cloud"; "the Jones software validates ClayPath" (cross-check only); "the lateral fit validates the Gaussian"; "DEP repeatability gives timing tolerances".

## 8. Coder-ready Python contract (v0.1, Track E)

**Build one deterministic package, `claypath`, whose Track E computes O1–O7 by quadrature and passes gates E0–E8 in order.** Random numbers exist only in the oracle and animation. Python ≥ 3.11 with numpy and scipy; nothing else.

### 8.1 Module boundaries

| Module | Owns | Must not |
| --- | --- | --- |
| `config.py` | Frozen dataclasses; every parameter carries value, unit, label, locator | Supply a silent default |
| `units.py` | SI internals; exact yd, in and ms converters; dimension checks | — |
| `fixtures/` | `dep_b1.json`, `dep_p82.json`, `dep_load.json`, each with a SHA-256 | Hold anything not on the cited page |
| `receipt.py` | JSON receipt, hashes, conflict log | — |
| `encounter/longitudinal.py` | t2(R), t3(R), Δt, h(q); domain and locked-row guards | Read locked rows before E3 |
| `encounter/lateral.py` | σ calibration, σ(R) laws, profile families, coupling | Touch timing rows |
| `encounter/geometry.py` | Dilated silhouette; Gaussian mass in circle or ellipse; inside test | — |
| `encounter/field.py` | π(e) by Gauss–Legendre quadrature | Use random numbers |
| `encounter/landscape.py` | Aim grid and O1–O7 | Choose k after seeing results |
| `encounter/variants.py` | E7 registry, materiality flags, bands | Promote a variant to baseline |
| `encounter/oracle.py` | E6 brute-force sampling; animation frames | Be imported by `landscape.py` |
| `gates.py` | E0–E8 runners and verdicts | Re-run E3 |
| `claims.py` | Claim ceiling, per-gate claims, banned-phrase lint | — |

### 8.2 Equations and source mapping

1. **Timing.** t2(R), t3(R) = monotone cubic (PCHIP) through the Fig B1 dev rows at 20/30/40/50 m (MEASURED\_PRIMARY rows; MODEL\_PREDICTION between them). Δt = t3 − t2 and t\_mid = (t2 + t3)/2. The domain is 20–50 m; any other range raises.
2. **Arrival shape.** q = (t − t2)/Δt. Baseline h(q) = 1 on \[0, 1\] (ASSUMED). Variants: 2(1 − q), 2q, and a 10% tail, 0.9 on \[0, 1\] plus 0.1 on \[1, 2\] (PROPOSED).
3. **Lateral calibration.** σ\_i = ρ/√(−2 ln(1 − P\_i)) with ρ = 0.381 m (30 in) and P\_i = mean circle count/192 at 27.432 m and 36.576 m (p.82). Expected σ = 0.1606 and 0.2266 m (INFERRED). Baseline σ(R) is the straight line through both (ASSUMED). Variant σ = kR, with k least-squares on the two circle fractions (expected 0.00611). R outside 27.432–36.576 m sets EXTRAPOLATED\_LATERAL.
4. **Lateral profile.** Baseline isotropic Gaussian φ(x) = exp(−|x|²/2σ²)/(2πσ²), Compton's lateral form (spec §6). Variant: generalised Gaussian φ(r) ∝ exp(−(r/s)^β), β ∈ {1.5, 3.0}, s re-fitted per range to the same circle fraction (PROPOSED).
5. **Coupling.** Variant σ(q) = σ̄(1 + κ(q − ½)), κ ∈ {0.4, 2/3}, with σ̄ re-fitted so that ∫h(q)·\[1 − exp(−ρ²/2σ(q)²)\]dq = P\_i (PROPOSED).
6. **Clay and contact.** Silhouette ellipse (a, b, ψ) is USER\_INPUT; default a = b = 0.055 m (face-on, ASSUMED). Dilated semi-axes are a + r\_p and b + r\_p, with r\_p = 1.575 mm (p.75). Clay centre relative to pattern centre: c(q; e) = v⊥·Δt·(q − ½)·û − e, where û is the clay's in-plane direction of travel and e is the pattern-centre offset at t\_mid. e\_a = e·û is along-track (positive = more lead); e\_c is perpendicular.
7. **Mass inside the silhouette.** Circle: G = F\_ncx2(ρc²/σ²; 2, |c|²/σ²) with ρc = a + r\_p. Ellipse with the Gaussian profile: rotate to the ellipse frame and integrate in one dimension, x = A·sin θ with 48 Gauss–Legendre nodes, the other coordinate in closed form via the normal CDF Φ. Non-Gaussian profiles (β variants): 2-D Gauss–Legendre, 24 radial × 96 angular, on 1-D scans only, because E7 needs optima and window edges, not full maps.
8. **Counts.** π(e) = Σ w\_j·h(q\_j)·G(c(q\_j; e)), 64 Gauss–Legendre nodes per unit of q. N \~ Binomial(192, π), conditional independence ASSUMED. Clumping variant: negative binomial with mean 192π and variance D·192π; D is computed at run time from the p.82 40 yd counts (expected 1.91; its use at clay scale is PROPOSED).
9. **Diagnostics.** S = v⊥Δt; gravity across the string ½g(t3² − t2²); centroid drop ½g·t\_mid² (both INFERRED vacuum-in-time upper bounds); receding stretch v/(v − v\_r), with v = 1/(dt\_mid/dR) from the interpolant.

### 8.3 Config and units

- SI internally. Fixtures load milliseconds and convert once; 1 yd = 0.9144 m and 1 in = 0.0254 m exactly.
- **Load profiles.** `DEP_REF` uses p.75 and p.82 values. `USER_LATERAL` takes Carl's pellet count, pellet diameter and 40 yd 30-inch circle % (USER\_INPUT); then σ\_user(R) = σ\_DEP(R)·σ\_user(40 yd)/σ\_DEP(40 yd), and string timing is borrowed from DEP. Both are ASSUMED and flagged DEP\_PROXY.
- **Scenario (USER\_INPUT):** R (20–50 m), crossing speed v⊥ (m/s), in-plane travel direction (degrees), optional receding speed v\_r (diagnostic only).
- **Frozen for v0.1 (version bump to change):** reported k = {2, 3, 5}, k = 1 diagnostic; window reference k = 3 at 0.5; materiality 0.055 m, 0.05 and 10%.
- **Solver:** aim grid ±0.6 m at 10 mm for maps; optimum (golden section) and FWHM edges (root-finding along and across track) to 0.1 mm; oracle 10^6 pellets and 20,000 rounds per case, PCG64, seed required.

### 8.4 Inputs and outputs

Inputs are one config file plus the three fixtures. Each run writes `landscape.npz` (O1, O3 per k and O4 grids, baseline plus band edges), `summary.json` (O2 at the optimum, O5–O7, MATERIAL flags) and `receipt.json`. Figures come only after E8 passes.

### 8.5 Deterministic and stochastic handling

- Baseline and every variant are deterministic quadrature. The same config must give a byte-identical `landscape.npz`; a test compares hashes across two runs.
- Random numbers live only in `oracle.py`, for E6 and animation frames. Frames sample q from h and x from φ at the encounter plane and are never propagated from the muzzle; seed and M go in the receipt.

## 9. Material unknowns

**Nine unknowns can change what the trainer teaches; v0.1 carries each as an input, a variant or a flag rather than waiting for it.**

| Unknown | Effect on training outputs | v0.1 handling |
| --- | --- | --- |
| Clay presentation (a, b, ψ) | Dilated area face-on 10,055 mm² vs edge-on 2,502 mm²: E\[N\] changes about 4× | USER\_INPUT per scenario; face-on default ASSUMED |
| Carl's own load (count, size, choke) | E\[N\] scales with N\_p/σ² | USER\_LATERAL profile; flagged DEP\_PROXY |
| Carl's string duration Δt | Mid-string lead offset v⊥Δt/2 scales with Δt; a 30% change at 40 m and 20 m/s moves it 0.057 m | DEP timing borrowed, ASSUMED |
| Lateral profile shape | Peak E\[N\] −30% to +38% (§5) | β variants; band |
| p.82 circle placement (centred or maximum-count) | Maximum-count placement would bias σ low and overstate E\[N\] | Centred ASSUMED; listed in receipt warnings |
| Arrival shape and long/lat coupling | Optimum lead about ±0.08 m at 40 m, 20 m/s | Triangular and κ variants; band |
| Clay-scale clumping | P(N≥3) down 0.07–0.10; E\[N\] unchanged | Negative-binomial variant; band |
| DTL encounter state (R, v⊥, direction, v\_r) | Places a DTL clay on the landscape | USER\_INPUT now; clay kernel later, MODEL\_PREDICTION - UNVALIDATED FOR DTL |
| Point of impact and its change with range | Centroid drop alone spans about 2–21 cm over 20–50 m (upper bound) | Landscape is pattern-centred; sight-picture conversion needs Carl's measured POI at one range |

The fraction of pellets outside the main section is also unknown. A 10% tail is not material (−6% E\[N\] at 20 m/s), but a tail near 20% would cross the 10% threshold for fast crossers.

## 10. Things to stop chasing

**Stop anything that cannot move an output past a materiality threshold or unblock a gate.**

- **More t2/t3 repeatability evidence.** The locked check uses a materiality tolerance, and a repeatability % cannot become a tolerance anyway.
- **Per-pellet ODE clouds for the encounter.** No v0.1 output needs pellet identity across planes.
- **Rayleigh versus Gaussian longitudinal shape.** The arrival-shape variants already bracket the centroid, and the headline lead lesson survives them.
- **Cube-law and C/gamma for the landscape.** Track E never calls them; they stay gated on the physics track.
- **Andert fitting and CN for v0.1.** C5 is report-only, and Track E needs no clay aerodynamics.
- **Bailey–Hiatt drag validation.** Not a blocker (spec §8) and unused by Track E.
- **Breakage thresholds.** Nothing in the pack links a contact count to a broken clay.
- **Sub-threshold physics.** Gravity across the string (≤ 5.0 cm), receding stretch (≈ +11%), a 10% tail (−6%) and the dilation approximation (≤ 1.4% area) all stay diagnostics.
- **Digitising B6–B8 amplitudes or B9–B11 dots at 150 ppi.** Single rounds, detector volts, about 5 mm per pixel. The dot plots earn a look only from a scan of 300 ppi or better whose counts agree with p.82 within ±3%.
- **Post-hoc choice of k.** K = {2, 3, 5} is frozen.
- **Further 292/293 resolution.** The printed digit is legible and governs.

## 11. Prompts That Check

**All seven checks pass for a conditional build; none passes for any claim above the ceiling.**

- **USE — PASS.** The deliverable is executable: a Track E package that turns a scenario (range, crossing speed, presentation) into a contact landscape Carl can compare across lead, timing and vertical error.
- **COULD / CAN / DID / WORKED.** COULD: yes, the field model can produce the landscape. CAN: yes, its inputs exist and verify, for the DEP load at 20–50 m. DID: not yet; every number here came from a throwaway review script, not from ClayPath. WORKED: only after E0–E8 pass, and then it means "computed correctly for the declared model", not "matches real shots". Reliable needs the F4 snapshot to hold across versions.
- **FALSIFIERS — PARTIAL, sufficient to build.** E3 can falsify the timing interpolant on untouched data, and E5–E6 can falsify the implementation. The review's sensitivity runs already falsified "the assumptions don't matter" for lateral shape, coupling, clumping and σ-law extrapolation. The lateral model has no falsifier in the pack, because calibration consumes both p.82 ranges; Carl's own plates at two ranges would supply one.
- **EFFECT SIZE — PASS.** The headline lesson, density-optimal lead 0.13–0.19 m ahead of the front-of-string lead at 20 m/s, exceeds the largest variant shift (0.082 m). Absolute E\[N\] moves by up to 38% and P(N≥3) by up to 0.10, so those ship as bands. Gravity across the string, a 10% tail and the dilation approximation fall below threshold.
- **RECEIPT — PASS IF IMPLEMENTED.** §8.8 records labelled inputs with locators, hashes, the split, the once-only locked ledger, seeds, variants, conflicts and the claim ceiling.
- **FRAME — PASS, with three named traps.** A contact landscape is the right frame for a trainer because it shows tolerance, not hit or miss. The traps: reading E\[N\] as break probability; reading DEP as Carl's cartridge; polishing V5/V8 physics the landscape does not use. The claim ceiling, the DEP\_PROXY flag and the Track E code order block them.
- **ANTI-0.03 — PASS, with disclosure.** I saw the printed locked rows; only source-integrity arithmetic (energy rounding) touched them. No interpolant, σ law or landscape was evaluated at 25/35/45 m. The 1.0 ms tolerance and the materiality thresholds come from clay geometry, not from residuals, and are fixed before any run. The circular moves to refuse: calling the two-point σ fit a validation, and relaxing a threshold after seeing E7.

## 12. Final freeze

**CONDITIONAL GO.**

The v1.1 amendments (§7) and the v0.1 contract (§8) are frozen as written; the conditions are the five build conditions in §1.

Next artifact: Python + tests, not another general evidence review.

### 8.6 Fixtures

- **F1 `dep_b1.json`:** the seven Fig B1 rows of §2 with split flags, per-column labels and locator "DEP 99/953 App. B, p.77, Fig B1"; vL at 20 m = 293.
- **F2 `dep_p82.json`:** per-round paper and circle counts for refs 1–20, plus the printed means, SDs, sig/avg and %. Ref 2 carries the note "overstrike, read 192, confirmed by mean".
- **F3 `dep_load.json`:** p.75–76 load, gun and environment values.
- **F4 reviewer check values** (MODEL\_PREDICTION computed for this package; regression targets, not evidence): face-on static E\[N\] at pattern centre 25.08, 9.34, 4.80, 2.91 at 20/30/40/50 m; peak E\[N\] at 20 m/s of 8.56 (30 m) and 4.38 (40 m); along-track FWHM 0.424 m (30 m, static) and 0.652 m (40 m, 20 m/s); dispersion D 1.77 (30 yd) and 1.91 (40 yd). Tolerance ±0.01 on E\[N\] and ±0.004 m on FWHM.

### 8.7 Exact test order and pass/fail/stop rules

&#91;embedded content: Track E gate ladder · 9 gates, 2 recordable failures\]

Gates run top to bottom. A STOP halts the run and publishes nothing; the two FAIL-RECORD exits record the failure, narrow or band the outputs, and let the run continue.

| Gate | Checks | On failure |
| --- | --- | --- |
| E0 Schema | Every parameter has value, unit, allowed label, locator; converters exact | STOP |
| E1 Fixture integrity | Hashes match; vL(20 m) = 293; ½mv² consistent for m 186.5–187.5 mg; p.82 summaries reproduce (population SD, sig/avg, round(100·count/192)) | STOP |
| E2 Interpolant | Exact at dev rows (< 1e-9 s); t2 and t3 strictly increasing; t3 > t2; out-of-domain raises; locked guard raises (tested) | STOP |
| E3 = V7 Locked timing | Once only: interpolant at 25/35/45 m vs Fig B1; \|error\| ≤ 1.0 ms on t2, t3 and Δt; ledger written | FAIL-RECORD: engine limited to the four dev ranges; never re-tuned or re-run |
| E4 Lateral calibration | Circle fractions reproduced to 1e-9; σ = 0.1606 / 0.2266 ± 1e-4; k = 0.00611 ± 1e-5; σ(R) > 0 on 20–50 m; extrapolation flags set | STOP |
| E5 Analytic geometry | Ellipse method with a = b vs ncx2, relative ≤ 1e-6 wherever G > 1e-8; symmetry in e\_a (uniform h) and e\_c; v⊥ = 0 equals static mass; at v⊥ = 0, e = 0, σ = 100a, G equals A\_eff·φ(0) within 1e-3; a boundary point counts as contact; doubling all node counts changes π by < 1e-6 relative; Binomial sums to 1 within 1e-12 | STOP |
| E6 Oracle | Six predeclared cases: single pellets \|p̂ − π\| ≤ 4·SE at 10^6 pellets; rounds P(N≥k) for k = 1, 2, 3, 5 within 4·SE + 1e-3 at 20,000 rounds; F4 values reproduced | STOP |
| E7 Sensitivity | Every variant over R ∈ {20, 30, 40, 50} (plus 25/35/45 if E3 passed) × v⊥ ∈ {0, 10, 20} m/s × face-on and edge-on (b = 12.5 mm); MATERIAL flags and bands | FAIL-RECORD: flag and band, never STOP |
| E8 Labels and claims | Every output labelled; claim ceiling verbatim; banned-phrase lint (spec §14 + A20); receipt validates against schema | STOP; nothing is displayed |

**E6 cases (fixed now):** (1) 30 m, static, face-on, e = 0; (2) 40 m, 20 m/s, face-on, e\_a = +0.10 m; (3) 40 m, 20 m/s, edge-on, e\_c = 0.05 m; (4) 50 m, 10 m/s, face-on, e = (0.2, −0.1) m; (5) 20 m, 20 m/s, b = 30 mm, ψ = 30°, e\_a = −0.15 m; (6) 30 m, 20 m/s, κ = 0.4 with the 10% tail, e = 0.

**Global STOP triggers:** an unlabelled parameter; any read of a locked row before E3; any call into a cube-law, C/gamma or CN path. Once E3 has run, any change to `longitudinal.py` forfeits the locked claim, and the ledger marks later timing results post-hoc. Visualisation runs only after E8 passes.

### 8.8 Run receipt schema

```json
{
  "run_id": "uuid4",
  "timestamp_utc": "ISO-8601",
  "versions": {"code": "git sha", "spec": "v1.1", "contract": "v0.1"},
  "hashes": {"config": "sha256", "dep_b1": "sha256", "dep_p82": "sha256", "dep_load": "sha256"},
  "inputs": [{"name": "", "value": null, "unit": "", "label": "", "locator": ""}],
  "load_profile": "DEP_REF | USER_LATERAL",
  "model": {"architecture": "intensity_field", "arrival": "uniform", "lateral": "gaussian",
            "sigma_law": "linear", "coupling": "none", "counts": "binomial"},
  "solver": {"n_q": 64, "n_x": 48, "n_r": 24, "n_theta": 96, "grid_step_m": 0.01, "opt_tol_m": 0.0001},
  "split": {"dev_m": [20, 30, 40, 50], "locked_m": [25, 35, 45], "locked_read_before_E3": false},
  "v7_ledger": {"run_once": true, "code_sha": "", "tolerance_ms": 1.0,
                "residuals_ms": {"25": [], "35": [], "45": []}, "verdict": "PASS | FAIL", "post_hoc_changes": []},
  "stochastic": {"generator": "PCG64", "seed": null, "M_pellets": 1000000, "M_rounds": 20000},
  "outputs": [{"id": "O1", "label": "MODEL_PREDICTION", "role": "geometric_contact", "file": "landscape.npz"}],
  "variants": [{"name": "", "params": {}, "label": "PROPOSED", "deltas": {}, "material": false}],
  "gates": [{"id": "E0", "verdict": "PASS | STOP | FAIL-RECORD", "detail": ""}],
  "warnings": [],
  "conflicts": [{"item": "vL_20m", "brief": 292, "primary": 293, "winner": "primary",
                 "locator": "DEP 99/953 App. B p.77 Fig B1"}],
  "applicability": {"range_m": [20, 50], "lateral_span_m": [27.432, 36.576], "flags": []},
  "claims_allowed": [],
  "claim_ceiling": "A13 text, verbatim"
}
```

### 8.9 Claims allowed after each gate

| After | Allowed claim | Still not allowed |
| --- | --- | --- |
| E0–E1 | Fixtures match the primary pages as transcribed; derived columns are internally consistent | Anything about the model |
| E2 | The timing interpolant reproduces the dev rows and is monotone | That it predicts unseen ranges |
| E3 pass | Main-string timing matched the locked DEP rows within 1.0 ms | That the lateral model is validated |
| E3 fail | Timing failed the locked check; outputs limited to 20/30/40/50 m | Any between-row output |
| E4 | Lateral spread reproduces the DEP circle fractions at 30 and 40 yd (calibration) | Lateral validation |
| E5–E6 | The landscape is computed correctly for the stated model | That the model matches real shot clouds |
| E7 | Which outputs are robust to the declared variants, with bands | Robustness to undeclared effects |
| E8 | The A13 claim ceiling and nothing above it | Breakage, scoring, Carl's cartridge, DTL validity |
