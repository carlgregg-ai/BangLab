"""Generate an honest, self-contained visual encounter prototype.

This is a visualisation of the existing Eulerian encounter/intensity model.
It does NOT invent pellet identities, pellet trajectories, clay breakage, scoring,
or a validated DTL flight path.

The animation shows a declared clay centre moving through the lateral model field
over the modelled main-string duration q in [0,1]. The displayed instantaneous
mass is the Gaussian probability mass inside the pellet-dilated clay silhouette
at that q. The integrated result is the existing EncounterField GEOMETRIC_CONTACT
model prediction.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import numpy as np

from .config import Parameter
from .encounter.field import EncounterField, Scenario
from .encounter.geometry import Silhouette, gaussian_mass


def _p(value: float, unit: str, label: str, locator: str) -> Parameter:
    return Parameter(value, unit, label, locator)


def build_payload(
    root: Path,
    *,
    range_m: float = 35.0,
    clay_speed_m_s: float = 20.0,
    direction_deg: float = 90.0,
    aim_x_m: float = 0.0,
    aim_y_m: float = 0.0,
    frames: int = 81,
) -> dict:
    if frames < 3:
        raise ValueError("frames must be >= 3")
    field = EncounterField.from_repository(root)
    scenario = Scenario(
        _p(range_m, "m", "USER_INPUT", "visual prototype CLI"),
        _p(clay_speed_m_s, "m/s", "USER_INPUT", "visual prototype CLI"),
        _p(direction_deg, "deg", "USER_INPUT", "visual prototype CLI"),
    )
    silhouette = Silhouette.face_on(field.pellet_radius)
    result = field.evaluate(scenario, silhouette, aim_x_m, aim_y_m)
    duration_s = field.duration(range_m)
    sigma_m = field.lateral.scale(range_m).sigma.value

    q = np.linspace(0.0, 1.0, frames)
    cx, cy = field.clay_centre(scenario, q, aim_x_m, aim_y_m)
    inst_mass = gaussian_mass(silhouette, sigma_m, cx, cy, method="auto")
    inst_density = np.array([
        field.lateral.pellet_density(range_m, float(x), float(y))
        for x, y in zip(cx, cy)
    ])

    pmf = result.count_pmf
    p_ge_1 = 1.0 - pmf[0]
    p_ge_2 = 1.0 - sum(pmf[:2])
    p_ge_3 = 1.0 - sum(pmf[:3])

    return {
        "meta": {
            "title": "BangLab visual encounter prototype",
            "role": result.role,
            "label": result.label,
            "claim_ceiling": (
                "MODEL PREDICTION of GEOMETRIC CONTACT under declared assumptions. "
                "Not breakage, scoring, a validated DTL trajectory, Carl's cartridge, "
                "or an actual fired pellet cloud."
            ),
        },
        "scenario": {
            "range_m": range_m,
            "clay_speed_m_s": clay_speed_m_s,
            "direction_deg": direction_deg,
            "aim_x_m": aim_x_m,
            "aim_y_m": aim_y_m,
            "clay_presentation": "face-on circular silhouette",
            "clay_presentation_status": "ASSUMED",
            "trajectory_status": "USER_INPUT straight transverse path in encounter plane",
        },
        "model": {
            "main_string_duration_ms": duration_s * 1000.0,
            "sigma_m": sigma_m,
            "pellet_count": int(field.lateral.pellet_count.value),
            "pellet_radius_mm": field.pellet_radius.value * 1000.0,
            "arrival_shape": "uniform over q in [0,1]",
            "arrival_shape_status": "ASSUMED",
            "lateral_shape": "isotropic Gaussian",
            "lateral_shape_status": "ASSUMED after DEP calibration",
            "longitudinal_lateral_coupling": "factorised / independent",
            "coupling_status": "ASSUMED",
        },
        "integrated_result": {
            "per_pellet_geometric_contact_probability": result.pi,
            "expected_geometric_contacts": result.expected_contacts,
            "p_ge_1_geometric_contacts": p_ge_1,
            "p_ge_2_geometric_contacts": p_ge_2,
            "p_ge_3_geometric_contacts": p_ge_3,
            "flags": sorted(result.flags),
        },
        "frames": [
            {
                "q": float(qi),
                "time_ms_from_string_start": float(qi * duration_s * 1000.0),
                "clay_x_m": float(x),
                "clay_y_m": float(y),
                "instantaneous_per_pellet_mass": float(m),
                "pellet_density_per_m2_at_clay_centre": float(d),
            }
            for qi, x, y, m, d in zip(q, cx, cy, inst_mass, inst_density)
        ],
    }


def render_html(payload: dict) -> str:
    data = json.dumps(payload, separators=(",", ":"), allow_nan=False)
    meta = payload["meta"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(meta["title"])}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{font-family:system-ui,Arial,sans-serif;margin:0;background:#111;color:#eee}}
main{{display:grid;grid-template-columns:minmax(560px,2fr) minmax(320px,1fr);gap:16px;padding:16px}}
.card{{background:#1b1b1b;border:1px solid #444;border-radius:10px;padding:14px}}
h1,h2{{margin:.2em 0 .6em}}
.badge{{display:inline-block;border:1px solid #888;border-radius:999px;padding:3px 8px;margin:2px;font-size:.82rem}}
.warn{{background:#332600;border-color:#ad8b00}}
.good{{background:#16301c;border-color:#4e9b5b}}
svg{{width:100%;height:auto;background:#0d0d0d;border:1px solid #333}}
.grid{{stroke:#333;stroke-width:1}}
.sigma{{fill:none;stroke:#777;stroke-width:1.5}}
.path{{stroke:#aaa;stroke-width:2;stroke-dasharray:6 5}}
.clay{{fill:none;stroke:#fff;stroke-width:3}}
.cross{{stroke:#aaa;stroke-width:1}}
label{{display:block;margin-top:10px}}
input[type=range]{{width:100%}}
table{{border-collapse:collapse;width:100%}}
td{{padding:5px;border-bottom:1px solid #333;vertical-align:top}}
td:first-child{{color:#bbb;width:48%}}
.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.small{{font-size:.9rem;color:#bbb}}
</style>
</head>
<body>
<main>
<section class="card">
<h1>BangLab visual encounter</h1>
<div><span class="badge good">MODEL_PREDICTION</span><span class="badge warn">GEOMETRIC_CONTACT ≠ BREAKAGE</span></div>
<p id="ceiling" class="small"></p>
<svg id="view" viewBox="-300 -300 600 600" aria-label="Encounter plane">
  <g id="grid"></g>
  <circle class="sigma" r="0" id="s1"/>
  <circle class="sigma" r="0" id="s2"/>
  <circle class="sigma" r="0" id="s3"/>
  <line class="path" id="path"/>
  <line class="cross" x1="-8" y1="0" x2="8" y2="0"/>
  <line class="cross" x1="0" y1="-8" x2="0" y2="8"/>
  <circle class="clay" id="clay" r="10"/>
</svg>
<label>String time: <span id="qtxt" class="mono"></span>
<input id="slider" type="range" min="0" max="80" step="1" value="0"></label>
<button id="play">Play</button>
<div id="instant" class="mono"></div>
</section>

<section class="card">
<h2>Integrated encounter result</h2>
<table id="result"></table>
<h2>Scenario</h2>
<table id="scenario"></table>
<h2>What is assumed?</h2>
<table id="assumptions"></table>
<p class="small">The moving circle is the declared pellet-dilated clay silhouette in the plane normal to fire. The grey rings are 1σ/2σ/3σ of the assumed Gaussian lateral field. No individual pellet trajectories are shown because this model does not contain them.</p>
</section>
</main>
<script>
const D={data};
const frames=D.frames;
const svg=document.getElementById('view');
const clay=document.getElementById('clay');
const slider=document.getElementById('slider');
slider.max=frames.length-1;
document.getElementById('ceiling').textContent=D.meta.claim_ceiling;

const PX=1000; // metres -> SVG pixels
const sigma=D.model.sigma_m*PX;
for (const [id,k] of [['s1',1],['s2',2],['s3',3]]) document.getElementById(id).setAttribute('r',sigma*k);
const p0=frames[0], p1=frames[frames.length-1];
const path=document.getElementById('path');
path.setAttribute('x1',p0.clay_x_m*PX); path.setAttribute('y1',-p0.clay_y_m*PX);
path.setAttribute('x2',p1.clay_x_m*PX); path.setAttribute('y2',-p1.clay_y_m*PX);
clay.setAttribute('r',0.055*PX);

function rows(obj, map={{}}){{
  return Object.entries(obj).map(([k,v])=>'<tr><td>'+ (map[k]||k) +'</td><td class="mono">'+
    (typeof v==='number'? (Math.abs(v)<0.01?v.toPrecision(4):v.toFixed(4)) : String(v))+'</td></tr>').join('');
}}
document.getElementById('result').innerHTML=rows(D.integrated_result,{{
  per_pellet_geometric_contact_probability:'P(contact), one pellet',
  expected_geometric_contacts:'Expected contacts E[N]',
  p_ge_1_geometric_contacts:'P(N≥1 geometric contacts)',
  p_ge_2_geometric_contacts:'P(N≥2 geometric contacts)',
  p_ge_3_geometric_contacts:'P(N≥3 geometric contacts)',
  flags:'Model flags'
}});
document.getElementById('scenario').innerHTML=rows(D.scenario);
document.getElementById('assumptions').innerHTML=rows({{
  main_string_duration_ms:D.model.main_string_duration_ms,
  sigma_m:D.model.sigma_m,
  arrival_shape:D.model.arrival_shape+' — '+D.model.arrival_shape_status,
  lateral_shape:D.model.lateral_shape+' — '+D.model.lateral_shape_status,
  coupling:D.model.longitudinal_lateral_coupling+' — '+D.model.coupling_status
}});

function show(i){{
  const f=frames[i];
  clay.setAttribute('cx',f.clay_x_m*PX); clay.setAttribute('cy',-f.clay_y_m*PX);
  document.getElementById('qtxt').textContent='q='+f.q.toFixed(3)+' / '+f.time_ms_from_string_start.toFixed(3)+' ms';
  document.getElementById('instant').textContent=
    'instantaneous per-pellet silhouette mass = '+f.instantaneous_per_pellet_mass.toFixed(6)+
    ' | model pellet density at clay centre = '+f.pellet_density_per_m2_at_clay_centre.toFixed(1)+' /m²';
}}
slider.addEventListener('input',()=>show(Number(slider.value)));
let timer=null;
document.getElementById('play').onclick=()=>{{
  if(timer){{clearInterval(timer);timer=null;return;}}
  timer=setInterval(()=>{{
    let i=(Number(slider.value)+1)%frames.length; slider.value=i; show(i);
  }},50);
}};
show(0);
</script>
</body></html>"""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--out", type=Path, default=Path("docs/evidence/visual_encounter/prototype.html"))
    p.add_argument("--range-m", type=float, default=35.0)
    p.add_argument("--speed-m-s", type=float, default=20.0)
    p.add_argument("--direction-deg", type=float, default=90.0)
    p.add_argument("--aim-x-m", type=float, default=0.0)
    p.add_argument("--aim-y-m", type=float, default=0.0)
    p.add_argument("--frames", type=int, default=81)
    args = p.parse_args()
    payload = build_payload(
        args.root,
        range_m=args.range_m,
        clay_speed_m_s=args.speed_m_s,
        direction_deg=args.direction_deg,
        aim_x_m=args.aim_x_m,
        aim_y_m=args.aim_y_m,
        frames=args.frames,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_html(payload), encoding="utf-8")
    receipt = args.out.with_suffix(".json")
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.out)
    print(receipt)


if __name__ == "__main__":
    main()
