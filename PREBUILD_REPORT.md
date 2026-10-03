# Final pre-build report

## READY
The architecture, equations, outputs, materiality thresholds, E0–E8 order and claim ceiling are sufficiently specified. DEP Fig B1 timing and p.75–76 load/environment values can be transcribed. Locked-row policy and one-shot E3 semantics are specified. BangLab namespace and replaceable shot-model boundary are documented without changing science.

## BLOCKERS
**Contract commit pending.** The full authoritative contract is physically present under `docs/evidence/` and its independently calculated SHA-256 matches the reviewed artifact (`9647717afa835afe1c5e79c86d1b01e93bb6c8804d8d8b2b81b5a00b4015085f`). It must be committed before implementation, as required by `BUILD_CONTRACT.md`.

**B-002 CLEARED.** The primary PDF is committed under `docs/evidence/`; independent working-tree and HEAD verification matches SHA-256 `5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7` (see the evidence receipt). The p.82 scientific-data blocker is also CLEARED: committed refs 1–20 are transcribed from primary printed p.82, with independent summary reproduction recorded in the receipt. E0/E1 verification remains unrun.

## NON-BLOCKING UNKNOWNS
Arrival shape, lateral profile family, sigma range law, long/lat coupling magnitude, clay-scale clumping, circle placement, fraction outside main string, personal-load timing, clay presentation, DTL encounter state and POI remain assumptions/variants/inputs/flags.

## CODEX START POINT
After the verified authoritative contract artifact is committed and implementation is authorized, implement `tests/test_fixture_integrity.py`: validate schema, reproduce p.82 published summaries, verify B1/load values and freeze fixture SHA-256 values. Only after that proceed to units/longitudinal code.

## DO NOT BUILD YET
DEM, CFD, pellet ODE propagation, breakage/scoring models, DTL trajectory model, ShotKam/IMU integration, Unreal, GUI/web app, personal-cartridge longitudinal claims, or experimentally validated 3-D shot-string claims.
