# E0–E8 gate specification

Authoritative numerical detail remains in the build contract §8.7.

| Gate | Purpose | Pass | Failure |
|---|---|---|---|
| E0 | labelled schema/units/locators | valid schema + exact converters | STOP |
| E1 | immutable primary fixtures + derived consistency | hashes; 293 m/s; energies; p.82 summaries | STOP |
| E2 | PCHIP from DEV 20/30/40/50 only | exact dev rows; monotone; domain/lock guards | STOP |
| E3 | one-shot LOCKED 25/35/45 evaluation | abs error <=1.0 ms for t2,t3,Δt; ledger | FAIL-RECORD; restrict to DEV; never tune/rerun |
| E4 | p.82 lateral calibration | contract sigma/k/fraction tolerances | STOP |
| E5 | geometry/quadrature correctness | contract tolerances | STOP |
| E6 | independent Monte Carlo oracle | six frozen cases + F4 regression | STOP |
| E7 | declared sensitivity matrix | all variants; materiality flags/bands | FAIL-RECORD; band |
| E8 | labels/claims/receipt | claim lint/schema pass | STOP; display nothing |

## Locked-data rule
Calibration receives a DEV-only view containing 20/30/40/50 m. LOCKED rows are accessible only to the E3 runner through a separate capability. Any locked access from calibration/model code before E3 is a STOP. E3 writes a ledger keyed by code/config/fixture hashes and refuses a second evaluation for the same immutable version.

## Scientific-test semantics
E3 and E7 are experiments, not “make green” unit tests. Their recordable FAIL verdicts must not be tuned away.
