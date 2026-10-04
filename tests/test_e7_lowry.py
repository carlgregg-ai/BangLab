import math
import pytest

from banglab.e7_lowry import (
    LowryWorkedCase,
    published_factor,
    published_loss_anchor_pp,
    reproduce_worked_case,
)


def test_lowry_primary_worked_example_regression():
    result = reproduce_worked_case()
    assert math.isclose(result["factor"], 8.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(result["loss_pp"], 4.8, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(result["moving_pattern_pct"], 70.2, rel_tol=0.0, abs_tol=1e-12)


def test_preserve_published_numeric_convention_not_unit_corrected_reinterpretation():
    # The source worked example explicitly uses 80 * 70 / 700 = 8.
    assert published_factor(80.0, 70.0, 700.0) == 8.0


def test_no_unrecovered_table_interpolation():
    with pytest.raises(ValueError):
        published_loss_anchor_pp(7.5, 75.0)


def test_invalid_velocity_rejected():
    with pytest.raises(ValueError):
        published_factor(80.0, 70.0, 0.0)
