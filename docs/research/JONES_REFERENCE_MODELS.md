# Jones 2005 compatibility and corrected reference models

**Status:** bounded research implementation. Not E7 adoption. E6 remains frozen and untouched.

This package turns the recovered A. C. Jones / Shotgun-Insight executable specification into two deliberately separate model families:

- `legacy`: reproduce recovered executable behaviour, including known quirks;
- `corrected`: change specific implementation choices one at a time so their materiality can be measured.

The implementation is an adversarial benchmark for BangLab, not independent physical validation.

## Frozen recovered anchors

- `HitProbability(4.7,1) = 0.990904936636`
- `HitProbability(4.7,2) = 0.948157711353`
- `HitProbability(4.7,3) = 0.847700941107`
- point density at `r=5 cm, sigma=10 cm = 0.001404537443 cm^-2`
- combined default skill model, 400 pellets, target area 10 cm², pattern sigma 10 cm, skill sigma 8 cm, zero offset:
  - 1+ = `96.989396826147%`
  - 2+ = `90.894715424582%`

## Controlled corrections

1. true Rayleigh radial skill weighting;
2. direct Poisson strike probability;
3. dense 32-node Gauss-Legendre POI angular integration.

Single-change variants are primary diagnostic evidence. `corrected_all` is secondary.

## Deliberate non-changes

- radial skill integration remains truncated at 4 sigma and normalised there;
- Jones's scalar target-area approximation remains;
- no clay fracture model is introduced;
- no E6/E7 constants or fixtures are changed.

## Run

```bash
python -m banglab.jones.compare --out docs/evidence/jones_sensitivity
pytest -q tests/test_jones_reference.py
```

Generated output is implementation-sensitivity evidence only. Any BangLab adoption still requires an explicit E7 decision.
