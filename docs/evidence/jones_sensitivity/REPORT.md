# Jones legacy vs corrected sensitivity report

Cases: **324**

This is an implementation-sensitivity exercise, not physical validation.
The E6 baseline is untouched. Jones compatibility and BangLab adoption remain separate.

| Variant | Mean abs Δ (pp) | Max abs Δ (pp) | Signed Δ at max (pp) | Max-case inputs |
|---|---:|---:|---:|---|
| skill_only | 7.647316 | 25.469913 | -25.469913 | `{"d75": 30.0, "k": 3, "pellet_count": 600, "poi_offset": 0.0, "skill_d95": 60.0, "target_area": 6.0}` |
| poisson_only | 0.000084 | 0.000234 | -0.000234 | `{"d75": 50.0, "k": 1, "pellet_count": 300, "poi_offset": 0.0, "skill_d95": 40.0, "target_area": 6.0}` |
| angles_only | 0.000431 | 0.009977 | -0.009977 | `{"d75": 30.0, "k": 3, "pellet_count": 600, "poi_offset": 10.0, "skill_d95": 60.0, "target_area": 6.0}` |
| corrected_all | 7.647562 | 25.469933 | -25.469933 | `{"d75": 30.0, "k": 3, "pellet_count": 600, "poi_offset": 0.0, "skill_d95": 60.0, "target_area": 6.0}` |

## Interpretation rule

A large delta identifies a legacy implementation choice that can materially alter the model output. It does not establish which alternative is physically correct. Any adoption into BangLab requires independent evidence and an E7 decision.
