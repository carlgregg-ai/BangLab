"""Bounded Jones legacy-vs-corrected sensitivity harness."""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from itertools import product
from pathlib import Path
from statistics import mean
from . import corrected, legacy

DEFAULT_GRID = {
    "pellet_count": [300, 450, 600],
    "target_area": [6.0, 10.0, 14.0],
    "d75": [30.0, 40.0, 50.0],
    "skill_d95": [20.0, 40.0, 60.0],
    "poi_offset": [0.0, 10.0],
    "k": [1, 3],
}

VARIANTS = {
    "legacy": dict(correct_skill_weight=False, direct_poisson=False, exact_angles=False),
    "skill_only": dict(correct_skill_weight=True, direct_poisson=False, exact_angles=False),
    "poisson_only": dict(correct_skill_weight=False, direct_poisson=True, exact_angles=False),
    "angles_only": dict(correct_skill_weight=False, direct_poisson=False, exact_angles=True),
    "corrected_all": dict(correct_skill_weight=True, direct_poisson=True, exact_angles=True),
}

def _cases(grid: dict[str, list[float]]) -> list[legacy.JonesInputs]:
    keys = ["pellet_count", "target_area", "d75", "skill_d95", "poi_offset", "k"]
    return [legacy.JonesInputs(**dict(zip(keys, vals))) for vals in product(*(grid[k] for k in keys))]

def run(grid: dict[str, list[float]] | None = None) -> dict:
    grid = grid or DEFAULT_GRID
    rows = []
    for case in _cases(grid):
        legacy_value = legacy.evaluate(case)
        rec = {"inputs": asdict(case), "legacy": legacy_value}
        for name, opts in VARIANTS.items():
            if name == "legacy":
                continue
            value = corrected.evaluate(case, **opts)
            rec[name] = value
            rec[f"delta_{name}_pp"] = value - legacy_value
        rows.append(rec)
    summary = {}
    for name in VARIANTS:
        if name == "legacy":
            continue
        ds = [r[f"delta_{name}_pp"] for r in rows]
        worst = max(rows, key=lambda r: abs(r[f"delta_{name}_pp"]))
        summary[name] = {
            "mean_abs_delta_pp": mean(abs(x) for x in ds),
            "max_abs_delta_pp": abs(worst[f"delta_{name}_pp"]),
            "max_case": worst["inputs"],
            "legacy_at_max": worst["legacy"],
            "variant_at_max": worst[name],
            "signed_delta_pp_at_max": worst[f"delta_{name}_pp"],
        }
    return {"grid": grid, "case_count": len(rows), "summary": summary, "rows": rows}

def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "comparison.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fields = ["pellet_count", "target_area", "d75", "skill_d95", "poi_offset", "k", "legacy"]
    for name in VARIANTS:
        if name != "legacy":
            fields.extend([name, f"delta_{name}_pp"])
    with (out_dir / "comparison.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in result["rows"]:
            flat = {**r["inputs"], **{k: v for k, v in r.items() if k != "inputs"}}
            w.writerow({k: flat[k] for k in fields})
    lines = [
        "# Jones legacy vs corrected sensitivity report","",f"Cases: **{result['case_count']}**","",
        "This is an implementation-sensitivity exercise, not physical validation.",
        "The E6 baseline is untouched. Jones compatibility and BangLab adoption remain separate.","",
        "| Variant | Mean abs Δ (pp) | Max abs Δ (pp) | Signed Δ at max (pp) | Max-case inputs |",
        "|---|---:|---:|---:|---|",
    ]
    for name, s in result["summary"].items():
        lines.append(f"| {name} | {s['mean_abs_delta_pp']:.6f} | {s['max_abs_delta_pp']:.6f} | {s['signed_delta_pp_at_max']:.6f} | `{json.dumps(s['max_case'], sort_keys=True)}` |")
    lines += ["","## Interpretation rule","",
        "A large delta identifies a legacy implementation choice that can materially alter the model output. It does not establish which alternative is physically correct. Any adoption into BangLab requires independent evidence and an E7 decision."]
    (out_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("docs/evidence/jones_sensitivity"))
    args = p.parse_args()
    result = run()
    write_outputs(result, args.out)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
