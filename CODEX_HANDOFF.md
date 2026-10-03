# CODEX IMPLEMENTATION PROMPT — BANGLAB v0.1

**Do not begin production implementation while STATE.md contains a BLOCKED fixture/E1 status.**

When the blocker is cleared:

1. Read AGENTS.md, the authoritative build contract, STATE.md, CLAIMS.md, DECISIONS.md and docs/GATES.md.
2. Run pre-build/fixture verification first. If it fails, stop and report the exact failure.
3. Implement one bounded slice at a time:
   fixture integrity -> units -> longitudinal interpolation -> E3 locked gate -> lateral calibration -> geometry -> field quadrature -> landscape -> variants -> oracle -> determinism -> claim lint -> integrated E0–E8 -> outputs -> figures after E8 only.
4. Write tests before or with each slice. Focused tests first; full suite at milestones.
5. Never reinterpret science. Stop on ambiguity with file/contract locator.
6. Never modify fixtures or tolerances to satisfy tests.
7. Never expose/read LOCKED 25/35/45 m rows to calibration before E3.
8. E3 is one-shot per immutable model/config version. A FAIL narrows applicability and is not repaired.
9. Produce only required landscape.npz, summary.json and receipt.json after gates permit.
10. Report exact PASS / STOP / FAIL-RECORD outcomes.
11. No UI, DEM, CFD, pellet ODE, DTL trajectory, ShotKam, Unreal or speculative features.
12. Inspect before editing; batch related reads; make small coherent patches; avoid rereading unchanged large files.

## Test-first slices
1. tests/test_fixture_integrity.py
2. tests/test_units.py
3. tests/test_longitudinal.py
4. tests/test_locked_rows.py
5. tests/test_lateral.py
6. tests/test_geometry.py
7. tests/test_field.py
8. tests/test_landscape.py
9. tests/test_variants.py
10. tests/test_oracle.py
11. tests/test_determinism.py
12. tests/test_claims.py
13. tests/test_gates.py

Update STATE.md only from test evidence. Implementation correctness is not physical validation.
