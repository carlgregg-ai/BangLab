# Clay-break recovery queue

Ranked by expected information value for resolving the gap between GEOMETRIC_CONTACT and defensible scoring-damage modelling.

No item below authorises implementation.

## Priority 1 — Recover Pautler's underlying laboratory dataset

**Target:** raw experimental observations behind James Anthony Pautler, *Analysis of Skeet Target Breakage* (US20210270567A1 / US12264896B2 / WO2020006095A1).

**Why highest value:** the patent explicitly describes the experiment closest to BangLab's missing Level-1 calibration: controlled pellet velocities, varied pellet count, observed break/no-break, and kinetic-energy-based probability.

**Missing fields:**

- pellet material, diameter/shot size and mass;
- controlled velocity values and measurement method;
- target manufacturer/type/material;
- target orientation/support/spin state;
- exact impact location or targeting method;
- number of trials per condition;
- individual break/fail observations;
- definition of “break” used in the lab;
- fitted distribution parameters and uncertainty;
- rejected/failed trials.

**Next actions:**

1. inspect complete US/PCT prosecution histories, including non-patent literature and submitted exhibits;
2. recover PCT written opinion/search-report attachments where useful;
3. search inventor presentations, conference proceedings, Take Aim Technologies / ShotTracker archives and product technical material;
4. search web archives for earlier company pages;
5. if still absent, contact James Anthony Pautler / Take Aim Technologies requesting the experimental dataset or report.

**Stop condition:** do not reconstruct a numerical curve from patent diagrams or prose if raw/calibration data remain unavailable.

## Priority 2 — Digitally preserve Roster's complete experiment

The critical matrix is already transcribed in `quantitative_evidence.md`.

Next recovery should preserve, with locators:

- complete test protocol;
- all available choke-specific outcomes if published elsewhere;
- the author's pattern-count tables underlying ~285 edge-on and ~230 dome-on associations;
- any original notebooks/article extensions or subsequent Roster publications discussing the same experiment;
- uncertainty/statistical method behind the stated “at least 95 percent confidence” claim.

**Information gain:** improves a real empirical target-break dataset but still will not provide individual pellet impact energy/location unless additional records exist.

## Priority 3 — Complete Skeuse/Spencer patent-family ancestry

**Target:** full family and prosecution material surrounding US6428007B2 and related filings.

Questions:

- exact conventional pitch target manufacturer/formulation;
- ammunition specification;
- firearm/choke;
- target presentation and motion;
- whether “pellet mark” was defined or differentiated from perforation;
- whether pickup inspection recorded mark locations;
- whether raw target-by-target sheets survive;
- whether the 27 yd experiment appears in related technical reports.

The existing distribution is high-value negative evidence and must remain unchanged unless primary records clarify it.

## Priority 4 — Extract Zhao control-material results with uncertainties

The thesis methodology is recovered. A later evidence pass should extract the actual CPC control values and associated error/variation for:

- density;
- flexural strength;
- flexural modulus;
- strain metrics;
- Charpy impact strength.

Keep these explicitly as **material specimen properties**. Do not transform them into pellet-break thresholds without a validated bridge.

## Priority 5 — Recover controlled impact-location evidence

Search specifically for experiments varying:

- rim versus dome versus ring/underside;
- normal versus oblique impact;
- one versus multiple pellets;
- target spin rate;
- supported/stationary versus free-flight target.

Desired output is trial-level break/no-break or fragment data with pellet velocity/energy and target specification.

## Priority 6 — Target-condition effects

No adequate quantitative pellet-impact dataset has yet been recovered for:

- temperature;
- moisture;
- storage duration;
- ageing;
- manufacturing batch variability.

Search manufacturer QA documents, patents, materials papers and shooting-industry technical reports. Keep launcher-survival strength separate from pellet-impact frangibility.

## Priority 7 — Verify current CPSA 2026 scoring wording

**Known:** official CPSA downloads list “CPSA Booklet 1 - Rules 26” dated 27 April 2026 and a 2026 changes document.

**Not yet verified in this record:** the actual 2026 wording governing HIT/LOST, visible fragments, holes/perforations and dust for the disciplines relevant to BangLab.

Next action: inspect the 2026 Booklet 1 primary text and record exact section identifiers with short paraphrase. Compare explicitly with 2023; do not assume unchanged wording.

Official index: https://www.cpsa.co.uk/downloads/booklets/10

## Priority 8 — Re-recover FourTen originals

The FourTen practitioner sources were identified in the earlier recovery but failed to re-fetch during final repository verification.

Targets:

- https://www.fourten.org.uk/steel2.pdf
- https://www.fourten.org.uk/rio.html

Recover stable/archive copies if lawful, identify authors/dates/test conditions, and separate photographed direct observations from narrative interpretation.

## Decision threshold for future modelling

Do not promote beyond GEOMETRIC_CONTACT merely because more sources accumulate.

A candidate empirical break model should require, at minimum:

1. a clearly defined physical/scoring endpoint;
2. primary quantitative trials with known denominators;
3. pellet specification and impact velocity/energy;
4. target specification;
5. enough repetitions to estimate uncertainty;
6. separation of pellet-hit probability from break-given-hit probability;
7. an explicit applicability domain;
8. adversarial validation against contact-without-break observations.

Until those conditions are met, the evidence layer may become richer while the model remains unchanged.
