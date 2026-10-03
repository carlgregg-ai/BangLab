# AGENTS.md — BangLab scientific coding rules

1. `BUILD_CONTRACT.md` is authoritative for v0.1 science.
2. Do not silently alter any scientific constant, equation, label, tolerance, fixture or gate.
3. Never use 25/35/45 m LOCKED timing rows for fitting. Normal calibration APIs must not expose them before E3.
4. E3 is a one-shot scientific evaluation per immutable model/config version. A FAIL is recordable evidence; never refit, rerun, relax tolerance, or edit fixtures to make it pass.
5. Never weaken a tolerance to make a test pass.
6. Never promote a variant/warning into baseline without a versioned decision in `DECISIONS.md`.
7. Never add a dependency without justification. v0.1 target is Python >=3.11, NumPy, SciPy only.
8. `GEOMETRIC_CONTACT` is not breakage, scoring, or “hit probability”.
9. Never infer physical validation from visual plausibility or implementation agreement.
10. Baseline and variants are deterministic. Randomness belongs only in the E6 oracle and later animation, with PCG64 seed/M recorded.
11. Every generated output requires a receipt.
12. Cube-law, C/gamma, CN, Andert fitting, pellet ODE, DEM and CFD are out of Track E v0.1.
13. If a scientific ambiguity is found, STOP and report it. Do not invent a solution.
14. Keep patches small and coherent; focused tests first, full suite at milestones.
15. Fixtures are evidence. Never change fixture values merely to satisfy tests.
16. `dep_p82.json` must not be fabricated from aggregate statistics. Implementation is blocked until its primary per-round rows are supplied.
17. Package namespace is `banglab`; this naming decision does not alter the contract science.
