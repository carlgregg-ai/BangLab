# Final pre-build report

## READY
The architecture, equations, outputs, materiality thresholds, E0–E8 order and claim ceiling are sufficiently specified. DEP Fig B1 timing and p.75–76 load/environment values can be transcribed. Locked-row policy and one-shot E3 semantics are specified. BangLab namespace and replaceable shot-model boundary are documented without changing science.

## BLOCKERS
**B-002: primary PDF binary storage only.** The p.82 scientific-data blocker is CLEARED: refs 1–20 are transcribed from primary printed p.82 and independently reproduce the published summary. The exact reviewed PDF is pinned by SHA-256 `5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7`. This chat's GitHub writer cannot commit binary PDF bytes, so a binary-capable Git/Codex step must add the PDF under `docs/evidence/` and verify that hash before release.

## NON-BLOCKING UNKNOWNS
Arrival shape, lateral profile family, sigma range law, long/lat coupling magnitude, clay-scale clumping, circle placement, fraction outside main string, personal-load timing, clay presentation, DTL encounter state and POI remain assumptions/variants/inputs/flags.

## CODEX START POINT
First add `03_DEP_99_953_Appendix_B_PRIMARY_UNALTERED.pdf` to `docs/evidence/` and verify its SHA-256 against the pinned receipt. Then implement `tests/test_fixture_integrity.py`: validate schema, reproduce p.82 published summaries, verify B1/load values and freeze fixture SHA-256 values. Only after that proceed to units/longitudinal code.

## DO NOT BUILD YET
DEM, CFD, pellet ODE propagation, breakage/scoring models, DTL trajectory model, ShotKam/IMU integration, Unreal, GUI/web app, personal-cartridge longitudinal claims, or experimentally validated 3-D shot-string claims.
