# E7-JF-01 — Lowry moving-target shot-string challenge

**Status:** AUTHORISED CANDIDATE — SPECIFICATION ONLY  
**Source family:** Jones Footprint → Lowry 1979 primary recovery  
**E6 status:** FROZEN / UNCHANGED  
**Implementation status:** NOT STARTED

## Purpose

Test whether the BangLab longitudinal representation can reproduce a published Lowry moving-target shot-string benchmark without changing the frozen E6 baseline.

This is a bounded **challenge case**, not adoption of Lowry as physical truth and not a new BangLab baseline.

## Primary source basis

Recovered primary source:
- E. D. Lowry, *The Effect of a Shot String?*, American Rifleman, November 1979, pp. 36–39.
- Bangleian source id: `S-JR-015`.

Recovered claims:
- `C-JR-013`: about 60 shot strings reconstructed at 40 and 60 yd using high-speed motion-picture photography through lead foil.
- `C-JR-014`: practical string-length descriptor is the smallest longitudinal interval containing 80% of pellets (`L80`).
- `C-JR-015`: dimensionless shot-string factor:
  `factor = L80 * target_transverse_velocity / pellet_velocity`.
- `C-JR-016`: worked 40 yd case:
  - `L80 = 80 in`
  - target transverse velocity = `70 ft/s`
  - pellet velocity = `700 ft/s`
  - factor = `8`
  - stationary pattern = `75%`
  - published moving-target result = `70.2%`
  - published loss = `4.8 percentage points`
- `C-JR-017`: Lowry Table C shows losses of only a few percentage points, with the largest displayed value about 6% for the specific historical cases shown.

## Frozen baseline

The following remain fixed:

- frozen E6 baseline;
- E4 lateral calibration;
- current target geometry;
- current reference pellet count;
- existing E3 timing/longitudinal evidence;
- all E6 fixtures, seeds, tolerances, receipts and conclusions.

This candidate must not:
- rerun E6;
- retune E6;
- reinterpret E6;
- replace the existing longitudinal model;
- promote Lowry's historical load behaviour into a universal modern-load law.

## Candidate model operation

Add a **report-only E7 diagnostic** that:

1. accepts or derives a longitudinal pellet-position distribution;
2. computes `L80`, defined as the smallest longitudinal interval containing 80% of pellets/probability mass;
3. computes Lowry's dimensionless factor:
   `F = L80 * V_target / V_pellet`
   using consistent units;
4. reproduces Lowry's published worked example using the recovered source values;
5. reports the corresponding percentage-point loss using the source's published benchmark/table;
6. optionally compares BangLab-derived `L80` values against the historical Lowry effect scale, but does not use that scale as a calibration target.

## Predeclared benchmark

### Lowry worked example

Inputs:
- range: 40 yd
- `L80 = 80 in`
- target transverse velocity: 70 ft/s
- pellet velocity: 700 ft/s
- stationary pattern: 75%

Expected:
- factor: 8
- published loss: 4.8 percentage points
- published moving-target pattern: 70.2%

## Materiality metric

Primary:
- percentage-point change in moving-target pattern density/contact opportunity attributable to longitudinal string extent.

Secondary:
- derived `L80`;
- Lowry factor;
- comparison with source-worked result.

## PASS / FAIL / INCONCLUSIVE

### PASS
- implementation reproduces the source worked case to the source's displayed rounding;
- no frozen E6 input, fixture, output or claim is modified;
- BangLab-derived `L80` can be calculated without introducing an unsupported longitudinal assumption;
- all outputs are labelled as a Lowry compatibility/challenge diagnostic.

### FAIL
- source inputs and formula cannot reproduce factor 8 / 4.8-point loss / 70.2% result as published;
- implementation requires alteration of the source values or formula to make the case pass;
- E6 must be changed to make the challenge work.

### INCONCLUSIVE
- BangLab's current longitudinal representation cannot support a defensible `L80` mapping without adding an unsupported assumption;
- the published Lowry table cannot be represented faithfully enough for the regression.

## Claim ceiling

A successful regression establishes only that BangLab can reproduce the declared Lowry calculation.

It does **not** establish:
- Lowry's 1979 loads represent modern cartridges;
- the historical effect-size range is universal;
- BangLab's longitudinal distribution is physically validated;
- the moving-target pattern loss is a clay-break probability;
- E6 is strengthened or revalidated.

## Stop rule

After the specification and source-regression test are implemented, stop for review before:
- applying the diagnostic to BangLab longitudinal outputs;
- changing E7 baseline behaviour;
- adding new longitudinal physics;
- introducing any fracture/scoring interpretation.

## Decision

**AUTHORISED: E7-JF-01 may proceed to implementation as a bounded report-only challenge.**

No other Jones Footprint delta is authorised for E7 by this decision.
