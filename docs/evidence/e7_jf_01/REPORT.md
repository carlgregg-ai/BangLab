# E7-JF-01 — Lowry source-regression report

**Status:** SOURCE REGRESSION IMPLEMENTED — STOP FOR REVIEW  
**E6:** unchanged  
**BangLab longitudinal outputs:** not evaluated  
**Model adoption:** none

## Recovered primary worked example

Lowry's recovered 1979 worked example states:

- range: 40 yd
- L80: 80 in
- stationary pattern: 75%
- pellet-cloud velocity: 700 ft/s
- target speed: 70 ft/s
- crossing angle: 90 degrees
- published arithmetic: `80 × 70 / 700 = 8`
- Table B loss at factor 8 / 75% pattern: 4.8 percentage points
- effective moving-target pattern: `75 - 4.8 = 70.2%`

## Regression result

The bounded implementation reproduces:

- factor = **8.0**
- loss = **4.8 percentage points**
- moving-target pattern = **70.2%**

## Important source-convention observation

The recovered source/recovery record labels the factor as dimensionless but the worked arithmetic uses the numerical value `80` for an L80 reported in inches while the velocities are reported in ft/s.

For this compatibility regression we preserve the **published arithmetic exactly**.

We deliberately do **not** convert 80 in to 6.666... ft before evaluating the factor, because doing so would produce approximately 0.6667 and would no longer reproduce Lowry's published worked example.

This is recorded as a source-convention issue, not silently repaired.

## Guardrails

The implementation:
- contains only the recovered factor-8 / 75%-pattern Table-B anchor;
- refuses to interpolate unrecovered Table-B values;
- does not apply Lowry to BangLab longitudinal output;
- does not alter E6;
- does not claim Lowry represents modern ammunition;
- does not turn pattern-density loss into clay-break probability.

## Decision against predeclared gate

**PASS — source regression.**

The authorised source example can be reproduced without changing its stated numerical inputs.

This PASS establishes compatibility with the recovered Lowry worked calculation only.

## STOP

Per the E7-JF-01 authorisation, stop here for human review before applying L80 to BangLab longitudinal distributions.
