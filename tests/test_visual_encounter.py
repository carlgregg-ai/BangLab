from pathlib import Path

from banglab.visual_encounter import build_payload, render_html


ROOT = Path(__file__).resolve().parents[1]


def test_visual_payload_is_honest_and_runnable():
    p = build_payload(ROOT, frames=5)
    assert p["meta"]["role"] == "GEOMETRIC_CONTACT"
    assert p["meta"]["label"] == "MODEL_PREDICTION"
    assert "Not breakage" in p["meta"]["claim_ceiling"]
    assert p["scenario"]["trajectory_status"].startswith("USER_INPUT")
    assert p["model"]["arrival_shape_status"] == "ASSUMED"
    assert p["model"]["lateral_shape_status"].startswith("ASSUMED")
    assert len(p["frames"]) == 5
    assert 0 <= p["integrated_result"]["per_pellet_geometric_contact_probability"] <= 1


def test_visual_html_contains_required_claim_labels():
    h = render_html(build_payload(ROOT, frames=5))
    assert "GEOMETRIC_CONTACT ≠ BREAKAGE" in h
    assert "No individual pellet trajectories are shown" in h
    assert "MODEL_PREDICTION" in h
