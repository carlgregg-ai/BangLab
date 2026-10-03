# Clay target damage, fracture and scoring — recovery report

**Date:** 2026-10-03  
**Status:** discovery/evidence record; no implementation authority.

## 1. Question

What empirical evidence connects shotgun pellet impacts on clay targets to physical damage and competition-scoring-visible fracture?

The investigation explicitly separates:

1. strike/contact without obvious damage;
2. penetration or pellet mark without scoring-visible break;
3. small visible chip sufficient for a scoring hit under applicable rules;
4. fracture after several pellet strikes;
5. catastrophic fragmentation.

No step is assumed to imply the next.

## 2. Executive finding

The central negative result is robust enough for BangLab's evidence layer: **pellet contact is not equivalent to scoring damage**.

Two independent recovered sources are especially important:

- Tom Roster's 2018 Clay Target Nation test deliberately recovered apparent misses until it accumulated 100 White Flyer targets demonstrably struck by No. 9 lead shot at 25–30 yd. Five percent of those struck targets produced no chip visible from the shooting station and therefore would have been scored lost under the test's scoring endpoint. A repeat using No. 8 shot in the same general load produced zero such cases in its 100-target struck sample.
- US6428007B2 reports pickup inspection of unbroken conventional pitch targets after a 27 yd shooting test. The unbroken pitch targets included examples carrying 1, 2, 3, 4, 5 and 7 pellet marks. Multiple observed pellet marks therefore did not guarantee breakage in that experiment.

These observations rule out deterministic `N >= 1 → scoring break` and even demonstrate that several pellet contacts can coexist with an intact target.

James Anthony Pautler's patent family is potentially the most valuable calibration lead. It states that a laboratory setup fired pellets at clay targets at controlled velocities, varied pellet number, visually observed break/no-break, and empirically measured a break distribution as a function of pellet kinetic energy. However, the inspected patent text does not expose the raw trials, sample sizes, target geometry, pellet specification, complete velocity matrix, impact locations, or fitted empirical parameters needed for defensible independent calibration.

Lei Zhao's 2013 Brunel PhD thesis supplies primary material-property evidence. Commercial Clay Pigeon Company target material was used as a control in flexural and Charpy testing. This supports the proposition that target material has measurable mechanical properties relevant to brittleness, but the specimens and tests are not equivalent to pellet impacts on intact flying targets.

**Gate implication:** the investigation supports retaining GEOMETRIC_CONTACT and treating CONTACT_WITHOUT_SCORING_DAMAGE as physically real. It does not justify promotion to a production clay-break probability model.

## 3. Scoring endpoint

A physics model and a scoring model are different objects. A pellet can contact, mark, penetrate, crack or otherwise damage a target without necessarily satisfying a referee-observable competition endpoint.

### ISSF

The inspected ISSF shotgun rule text defines a HIT when a regular target is hit and at least one visible piece is broken from it. A target that is only dusted, with no visible piece seen, is not a HIT; the referee has final authority. Source: ISSF Shotgun Rules Book, 2023 approved version.

### FITASC

The inspected 2025 FITASC rule text likewise uses a visible-piece endpoint and distinguishes dust-only observations from a scored hit/one.

### CPSA version control

A CPSA **2026 Booklet 1** edition has been identified in the CPSA downloads index, dated 27 April 2026, together with a 2026 changes document.

The wording actually inspected during this investigation is from the **2023 Booklet 1** edition. The 2023 rules are therefore evidence for the 2023 rule state only.

**Current 2026 CPSA scoring wording remains UNVERIFIED in this record until the 2026 Booklet 1 text itself is inspected.** No 2023 wording is silently attributed to 2026.

Historical CPSA material has included a visible-hole provision in some scoring definitions. That historical fact is not used here as evidence of the current 2026 rule.

## 4. Direct experimental/practitioner evidence

### 4.1 Roster — recovered struck targets

Roster used standard White Flyer targets and Winchester AA 20-gauge 7/8 oz No. 9 loads through a skeet-choked Remington 3200. Targets were left-to-right crossers struck at 25–30 yd. Apparent misses were recovered and inspected; a target was classified as struck when it showed one or more pellet holes or tiny pellet-caused chips. Replacement targets were fired until the struck-target sample reached 100.

Result: 5% of the 100 demonstrably struck No. 9 targets produced no chip visible from the shooting station and would have been scored lost in the stated skeet context. Roster repeated the test with No. 8 shot in the same Winchester AA load and reported zero struck targets without a visible chip in that 100-target sample.

This is direct evidence for the existence of contact/penetration or tiny damage without scoring-visible fragment. It is not an instrumented single-pellet energy threshold experiment.

### 4.2 Roster — stationary sporting-clays matrix

Roster also tested stationary, non-spinning standard White Flyer targets at 30, 40 and 50 yd, in edge-on and dome-on attitudes, using 12-gauge 1 oz loads with American No. 7½, 8 and 8½ lead shot. A target counted as broken when at least one visible chip could be seen coming off.

The published 25-target result matrix is preserved in `quantitative_evidence.md`. The experiment also reports a larger test regimen of 1,350 rounds across shot size, choke, distance and target attitude and 60 counted patterns. The sidebar matrix reports the selected/best choke condition described by the author, not all 1,350 individual outcomes.

Roster associates approximately 285 pellets in a 30-inch pattern for edge-on targets and approximately 230 for dome-on targets with the minimum pattern density found associated with 100% breaking in his test regime. This is an **AUTHOR_CLAIM / SOURCE_DERIVED test-specific association**, not a universal break threshold and not an individual-target pellet-hit count.

### 4.3 Skeuse & Spencer patent — conventional pitch target pickup data

US6428007B2, *Environmentally safe projectable targets*, reports comparative shooting at 27 yd. For conventional pitch targets, 449 of 500 targets were broken (89.8%). Pickup inspection of unbroken pitch targets reported the exact pellet-mark distribution preserved in `quantitative_evidence.md`.

Important limitation: 449/500 is a break rate among targets fired at, **not** a per-contact break probability because the experiment does not establish that every fired-at target was struck. The pickup data are more directly informative: targets remained unbroken with observed pellet marks, including one with seven marks.

### 4.4 Pautler patent family

US20210270567A1 / US12264896B2 / WO2020006095A1, *Analysis of Skeet Target Breakage*, describes a laboratory setup in which pellets were fired at clay targets at controlled velocities while pellet number was varied and break/no-break was visually observed. The disclosure says these measurements were used to represent break probability as a function of pellet kinetic energy for different pellet-count cases.

This is a direct statement that an empirical dataset existed. The inspected patent does **not** disclose enough underlying observations to reproduce or independently validate the calibration. The patent's mathematical/probability construction is therefore **MODEL_DERIVED / AUTHOR_CLAIM** unless and until the underlying measurements are recovered.

### 4.5 Zhao thesis

Lei Zhao's 2013 Brunel PhD thesis, *Novel Bio-Composites Based on Whole Utilisation of Wheat Straw*, used commercial Clay Pigeon Company material as a benchmark/control for candidate bio-target materials. Flexure testing used six specimens per formulation; Charpy testing used six specimens per group and a 2 J striker.

This is primary quantitative material-property evidence. It is not a pellet-impact test on intact competition targets and must not be converted into a pellet-break threshold without an independently validated mechanical bridge.

### 4.6 FourTen practitioner observations

Earlier recovery identified FourTen practitioner material describing steel or very-small-shot impacts in which targets could receive multiple strikes yet remain intact or only chipped. These observations are useful adversarial evidence but are not peer-reviewed controlled datasets. During this repository-write verification the FourTen pages were not successfully re-fetched, so they remain **practitioner / partial-recovery evidence**, not upgraded direct calibration data.

## 5. Competing mechanisms supported or suggested by evidence

### Pellet characteristics

Roster's No. 9 versus No. 8 struck-target experiments support an empirical association between ammunition/pellet choice and scoring-visible break outcomes under his test conditions. They do not isolate kinetic energy from pellet diameter, hardness, deformation, retained velocity or other correlated variables.

### Pellet count

Pautler explicitly varies pellet number in the described laboratory work. Skeuse/Spencer independently show that several pellet marks can exist on an unbroken target. Pellet count therefore matters plausibly but is not a deterministic threshold in the recovered evidence.

### Target presentation / attitude

Roster's edge-on and dome-on matrix shows different outcomes at some distance/shot-size combinations. This supports presentation as a potentially relevant variable. It does not isolate exact impact location on the rim, dome, rings or underside.

### Spin

Roster states that spinning targets are easier to break and gives a fracture-propagation interpretation. In the recovered source this is an author explanation rather than a separately instrumented spin-rate experiment. It is retained as **AUTHOR_CLAIM**, not a calibrated spin coefficient.

### Target material

Zhao and target-manufacturing patents establish that target composition and mechanical properties can differ and are deliberately engineered. This supports target material/state as a relevant family of variables, but no universal mapping to scoring-visible pellet damage has been recovered.

## 6. Contradictions and negative evidence

The evidence resists a simple scalar threshold narrative.

- CONTACT → BREAK is contradicted directly by recovered struck/unbroken targets.
- MULTIPLE CONTACTS → BREAK is contradicted by unbroken pitch targets with up to seven observed pellet marks.
- PENETRATION → SCORING DAMAGE is contradicted by Roster's struck-target classification, which included pellet holes, combined with cases lacking a chip visible from the station.
- Pattern-density associations cannot be interpreted as individual-target pellet-count thresholds.
- A patent's engineering definition or model variable is not automatically a competition scoring definition.
- Material toughness measurements are not equivalent to intact-target terminal-ballistics measurements.

## 7. Variables not adequately calibrated

No recovered source provides a defensible general quantitative calibration across all of:

- individual pellet impact energy/momentum/velocity;
- pellet diameter, deformation and hardness;
- impact angle;
- exact impact location;
- target spin rate;
- multiple-hit spacing/timing;
- target manufacturer/material/thickness;
- manufacturing variability;
- temperature;
- moisture;
- age/storage history.

Absence of a calibration is recorded as missing evidence, not filled by assumption.

## 8. BangLab implications

### Supported now

- Keep **GEOMETRIC_CONTACT** distinct from every damage/scoring state.
- Record that physical pellet contact can occur without scoring-visible damage.
- If later evidence work records physical observables such as contact count, relative impact velocity or pellet impact energy, those observables must remain measurements/model outputs rather than being relabelled as breakage.
- Any future scoring layer must respect rule-version and discipline-specific endpoints.

### Plausible but unvalidated

- A probabilistic Level-1 relationship conditioned on pellet count and impact energy is scientifically motivated by Pautler's disclosed experimental design.
- Target attitude/location and material are plausible conditioning variables.
- Spin may influence fracture propagation.

### Unsupported for implementation

- `KE > threshold → HIT`
- `N >= 1 → HIT`
- `N >= 3 → HIT`
- `penetration → HIT`
- `crack → HIT`
- a universal break probability transferred across target types/ammunition/presentations;
- a mechanistic FEA model claimed to predict referee-visible scoring fragments.

## 9. Model-level assessment

- **L0 GEOMETRIC_CONTACT:** supported as the existing bounded state; not breakage.
- **L1 simple empirical probability from pellet count + energy:** scientifically motivated, but calibration data not yet recovered sufficiently.
- **L2 + impact location:** plausible; insufficient controlled data recovered.
- **L3 + angle/spin/target variation:** plausible; insufficient calibration recovered.
- **L4 mechanistic fracture/FEA:** unsupported as a competition-scoring predictor by the present evidence.

The simplest justified action is therefore **no model promotion**.

## 10. Limitations

This recovery is heterogeneous: peer-reviewed/doctoral material-property work, patents, governing-body rules and practitioner experiments answer different questions. Patent disclosure establishes what an inventor says was done but does not substitute for raw data. Practitioner experiments can establish existence of a phenomenon without establishing a population rate. Governing-body rules define scoring endpoints, not fracture mechanics.

No E2/E3 evaluation was performed. No LOCKED E3 observations were accessed or exposed.
