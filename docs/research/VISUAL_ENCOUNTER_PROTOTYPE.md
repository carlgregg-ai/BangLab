# BangLab visual encounter prototype

**Purpose:** make the current BangLab encounter model visible and usable without pretending unresolved physics have been solved.

## What it shows

The prototype animates a declared clay silhouette moving through the existing lateral probability field over the current main-string duration.

It displays:
- 1σ / 2σ / 3σ lateral-field rings;
- the user-input clay path in the encounter plane;
- instantaneous Gaussian probability mass inside the clay silhouette;
- model pellet density at the clay centre;
- the existing integrated GEOMETRIC_CONTACT outputs.

## What it deliberately does not show

It does not invent:
- pellet identities;
- pellet trajectories;
- a physically validated 3-D shot string;
- a validated DTL clay trajectory;
- breakage;
- scoring;
- Carl's cartridge.

Those omissions are visible in the UI rather than buried in documentation.

## Default demonstration scenario

Defaults are illustrative USER_INPUT / ASSUMED values:
- range: 35 m
- clay speed: 20 m/s
- direction: 90°
- zero aim offset
- face-on clay silhouette

These are not claimed to represent a particular DTL target.

## Run

```bash
python -m banglab.visual_encounter --root . --out docs/evidence/visual_encounter/prototype.html
```

Open the generated HTML in a browser. It is self-contained and requires no web server.

A JSON receipt with the same scenario, assumptions, per-frame values and integrated result is written beside the HTML.

## Honesty rule

The interface must always retain:

**MODEL_PREDICTION — GEOMETRIC_CONTACT ≠ BREAKAGE**

A more visually impressive representation is not allowed to imply stronger evidence than the underlying model.
