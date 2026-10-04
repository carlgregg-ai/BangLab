"""E7-JF-01 Lowry source-regression utilities.

This module implements ONLY the recovered 1979 Lowry worked-example arithmetic.
It does not apply Lowry to BangLab outputs and does not modify E6.

Important compatibility note:
The recovered primary-source worked example evaluates the factor numerically as
    80 * 70 / 700 = 8
where L80 is reported as 80 inches and both velocities are ft/s.
We preserve that published numerical convention verbatim for regression.
We do not silently convert 80 inches to feet, because that would no longer
reproduce the source calculation.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LowryWorkedCase:
    range_yd: float = 40.0
    l80_in: float = 80.0
    stationary_pattern_pct: float = 75.0
    pellet_velocity_ft_s: float = 700.0
    target_velocity_ft_s: float = 70.0
    crossing_angle_deg: float = 90.0


# Only the primary-source anchor needed for the authorised regression is encoded.
# This is not a reconstruction of Lowry Table B.
_PUBLISHED_LOSS_ANCHOR_PP = {(8.0, 75.0): 4.8}


def published_factor(l80_numeric: float, target_velocity: float, pellet_velocity: float) -> float:
    """Reproduce Lowry's published numerical factor convention exactly."""
    if pellet_velocity <= 0:
        raise ValueError("pellet_velocity must be positive")
    if l80_numeric < 0 or target_velocity < 0:
        raise ValueError("l80_numeric and target_velocity must be non-negative")
    return l80_numeric * target_velocity / pellet_velocity


def published_loss_anchor_pp(factor: float, stationary_pattern_pct: float) -> float:
    """Return only the explicitly recovered Table-B anchor for E7-JF-01."""
    key = (float(factor), float(stationary_pattern_pct))
    try:
        return _PUBLISHED_LOSS_ANCHOR_PP[key]
    except KeyError as exc:
        raise ValueError(
            "No recovered Lowry Table-B anchor is authorised for these inputs; "
            "do not interpolate or invent a value."
        ) from exc


def reproduce_worked_case(case: LowryWorkedCase = LowryWorkedCase()) -> dict[str, float]:
    factor = published_factor(case.l80_in, case.target_velocity_ft_s, case.pellet_velocity_ft_s)
    loss_pp = published_loss_anchor_pp(factor, case.stationary_pattern_pct)
    moving_pattern_pct = case.stationary_pattern_pct - loss_pp
    return {
        "factor": factor,
        "loss_pp": loss_pp,
        "moving_pattern_pct": moving_pattern_pct,
    }
