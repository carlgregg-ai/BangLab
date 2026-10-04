import math
from banglab.jones import corrected, legacy

def test_recovered_hit_probability_regression():
    assert math.isclose(legacy.k_or_more_probability(4.7, 1), 0.990904936636, rel_tol=0, abs_tol=5e-12)
    assert math.isclose(legacy.k_or_more_probability(4.7, 2), 0.948157711353, rel_tol=0, abs_tol=5e-12)
    assert math.isclose(legacy.k_or_more_probability(4.7, 3), 0.847700941107, rel_tol=0, abs_tol=5e-12)

def test_recovered_point_density_regression():
    assert math.isclose(legacy.point_density(5.0, 10.0), 0.001404537443, rel_tol=0, abs_tol=5e-12)

def test_recovered_combined_skill_regression():
    one = legacy.combined_hit_probability(pellet_count=400, target_area=10.0, pattern_sigma=10.0, skill_sigma=8.0, poi_offset=0.0, k=1)
    two = legacy.combined_hit_probability(pellet_count=400, target_area=10.0, pattern_sigma=10.0, skill_sigma=8.0, poi_offset=0.0, k=2)
    assert math.isclose(one, 96.989396826147, rel_tol=0, abs_tol=5e-6)
    assert math.isclose(two, 90.894715424582, rel_tol=0, abs_tol=5e-6)

def test_direct_poisson_is_not_legacy_binomial():
    assert corrected.poisson_k_or_more(4.7, 1) != legacy.k_or_more_probability(4.7, 1)

def test_corrected_skill_weight_changes_combined_result():
    case = legacy.JonesInputs(400, 10.0, legacy.D75_RAYLEIGH_RADIUS * 20.0, legacy.D95_RAYLEIGH_RADIUS * 16.0)
    old = legacy.evaluate(case)
    new = corrected.evaluate(case, correct_skill_weight=True, direct_poisson=False, exact_angles=False)
    assert abs(new - old) > 1e-6
