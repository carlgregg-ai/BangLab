# Decisions

## D-001 — v0.1 architecture
Use the deterministic Eulerian encounter/intensity field from the build contract. Do not implement pellet ODE, DEM or CFD for v0.1.

## D-002 — replaceable shot model
Preserve the conceptual boundary `FireEvent -> ShotModel -> evaluable ShotState/encounter field -> consumers`. Track E is the first implementation, not the permanent definition of a shot.

## D-003 — BangLab namespace
Repository/package namespace is `banglab`. The contract calls its package `claypath`; this is a non-scientific naming difference. Equations, fixtures, gates, tolerances and claim scope do not change.

## D-004 — Deng boundary
Deng supports plausibility of an evolving 3-D pellet swarm and radial-dispersion modelling. It does not independently validate BangLab longitudinal shot-string behaviour. DEM/CFD reproduction is future work.

## D-005 — locked rows
25/35/45 m may not be exposed to calibration/interpolation construction before E3. Access must be mediated by a one-shot gate capability; ordinary model code sees DEV rows only. E3 failure is a scientific result, not a coding defect.

## D-006 — missing p.82 raw rows
The supplied contract specifies 20 per-round p.82 observations but does not reproduce those observations. Do not reconstruct them from aggregates. `dep_p82.json` remains BLOCKED until primary rows are supplied/recovered.
