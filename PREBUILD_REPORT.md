# Final pre-build report

## READY
The architecture, equations, outputs, materiality thresholds, E0–E8 order and claim ceiling are sufficiently specified. DEP Fig B1 timing and p.75–76 load/environment values can be transcribed. Locked-row policy and one-shot E3 semantics are specified. BangLab namespace and replaceable shot-model boundary are documented without changing science.

## BLOCKERS
**B-001: DEP p.82 raw per-round observations are absent from the supplied contract and repository.** F2 requires refs 1–20 paper and 30-inch-circle counts. Aggregates are insufficient and must not be inverted/reconstructed. Therefore `dep_p82.json`, E1, E4 and production implementation are not yet honestly startable.

## NON-BLOCKING UNKNOWNS
Arrival shape, lateral profile family, sigma range law, long/lat coupling magnitude, clay-scale clumping, circle placement, fraction outside main string, personal-load timing, clay presentation, DTL encounter state and POI remain assumptions/variants/inputs/flags.

## CODEX START POINT
After B-001 is cleared: create/verify `dep_p82.json` from the primary p.82 rows, generate fixture SHA-256 sums, then implement `tests/test_fixture_integrity.py` only.

## DO NOT BUILD YET
DEM, CFD, pellet ODE propagation, breakage/scoring models, DTL trajectory model, ShotKam/IMU integration, Unreal, GUI/web app, personal-cartridge longitudinal claims, or experimentally validated 3-D shot-string claims.
