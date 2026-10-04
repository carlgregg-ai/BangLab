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
The supplied contract specifies 20 per-round p.82 observations but does not reproduce those observations. Do not reconstruct them from aggregates. Resolved: primary refs 1–20 are supplied in committed `data/fixtures/dep_p82.json`; the DEP Appendix B receipt records independent reproduction of published summaries. The source-data blocker is cleared. The prohibition on reconstructing observations from aggregates remains in force; E1 fixture integrity verification is still required.

## D-007 — E5 symmetry verification clarification (2026-10-04)
Human-authorised clarification before E5 implementation/results, against checkpoint `cf8d95923c35bacae3446b9bdeabba13bcbdf751`. The E5 STOP was legitimate: no failed scientific evaluation occurred, no E5 implementation existed at clarification, and no numerical result motivated this decision.

This clarifies the verification invariant in contract section 8.7; it does not change the physical/model specification in section 8.2.6. Under the isotropic baseline field and uniform arrival, arbitrary ellipse orientations require joint inversion: pi(e_a,e_c,psi) = pi(-e_a,-e_c,psi). Separate e_a and e_c reflections are required only when the target has those symmetries relative to the travel axes (principal axes aligned, including relative psi=0 or pi/2 modulo pi). Circular geometry is orientation-independent; rotational comparisons rotate the travel direction and offsets together for a moving target. General rotated non-circular ellipses must not be forced to satisfy separate reflections, nor may geometry/orientation be changed to satisfy a test. Use the existing numerical tolerances; no scientific tolerance changes.

Historical E0-E4 receipts remain unchanged. E6, E7 and E8 are not authorised by this clarification.
