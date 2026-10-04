"""Recovered A. C. Jones / Shotgun-Insight compatibility model.

This module intentionally reproduces recovered executable behaviour, including
known quirks. It is a compatibility target, not a statement of physical truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, pi, hypot

D75_RAYLEIGH_RADIUS = 1.66512
D95_RAYLEIGH_RADIUS = 2.4477468
BINOMIAL_P = 1.0 / 100000.0
SKILL_TRUNCATION_SIGMA = 4.0

def sigma_from_d75(d75: float) -> float:
    if d75 <= 0:
        raise ValueError("d75 must be positive")
    return d75 / (2.0 * D75_RAYLEIGH_RADIUS)

def skill_sigma_from_d95(d95: float) -> float:
    if d95 <= 0:
        raise ValueError("d95 must be positive")
    return d95 / (2.0 * D95_RAYLEIGH_RADIUS)

def point_density(r: float, sigma: float) -> float:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    return exp(-(r * r) / (2.0 * sigma * sigma)) / (2.0 * pi * sigma * sigma)

def radial_rayleigh_pdf(r: float, sigma: float) -> float:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if r < 0:
        return 0.0
    return (r / (sigma * sigma)) * exp(-(r * r) / (2.0 * sigma * sigma))

def expected_strikes(r: float, pattern_sigma: float, pellet_count: int, target_area: float) -> float:
    if pellet_count < 0:
        raise ValueError("pellet_count must be non-negative")
    if target_area < 0:
        raise ValueError("target_area must be non-negative")
    return point_density(r, pattern_sigma) * pellet_count * target_area

def k_or_more_probability(lam: float, k: int) -> float:
    """Recovered large-n/small-p binomial approximation."""
    if lam < 0:
        raise ValueError("lam must be non-negative")
    if k < 1:
        return 1.0
    k = min(k, 10)
    n = int(round(100000.0 * lam))
    if n == 0:
        return 0.0
    p = BINOMIAL_P
    q = 1.0 - p
    pj = exp(n * __import__("math").log1p(-p))
    cumulative = pj
    for j in range(1, k):
        if j > n:
            break
        pj *= ((n - j + 1) / j) * (p / q)
        cumulative += pj
    return max(0.0, min(1.0, 1.0 - cumulative))

def _legacy_skill_weight(r: float, skill_sigma: float) -> float:
    return point_density(r, skill_sigma)

def _angular_mean_local_hit(shooter_r: float, poi_offset: float, pattern_sigma: float, pellet_count: int, target_area: float, k: int) -> float:
    if poi_offset == 0.0:
        lam = expected_strikes(shooter_r, pattern_sigma, pellet_count, target_area)
        return k_or_more_probability(lam, k)
    values = []
    for i in range(4):
        theta = i * pi / 4.0
        c = __import__("math").cos(theta)
        s = __import__("math").sin(theta)
        for sign in (1.0, -1.0):
            x = sign * shooter_r * c
            y = sign * shooter_r * s
            rr = hypot(x - poi_offset, y)
            lam = expected_strikes(rr, pattern_sigma, pellet_count, target_area)
            values.append(k_or_more_probability(lam, k))
    return sum(values) / len(values)

def _legacy_integrate(func, a: float, b: float, *, rel_tol: float = 1e-5, max_levels: int = 20) -> float:
    """Recovered trapezoid refinement with Simpson/Richardson extrapolation."""
    def trap(n: int) -> float:
        h = (b - a) / n
        total = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            total += func(a + i * h)
        return total * h
    previous_t = trap(1)
    previous_s = None
    for level in range(1, max_levels + 1):
        current_t = trap(2 ** level)
        current_s = (4.0 * current_t - previous_t) / 3.0
        if previous_s is not None:
            scale = max(abs(previous_s), 1e-30)
            if abs(current_s - previous_s) <= rel_tol * scale:
                return current_s
        previous_t = current_t
        previous_s = current_s
    return float(previous_s)

def combined_hit_probability(*, pellet_count: int, target_area: float, pattern_sigma: float, skill_sigma: float, poi_offset: float = 0.0, k: int = 1) -> float:
    """Recovered default SKILL_RAYLEIGH combined probability, percent."""
    if skill_sigma <= 0:
        raise ValueError("skill_sigma must be positive")
    upper = SKILL_TRUNCATION_SIGMA * skill_sigma
    norm = _legacy_integrate(lambda r: _legacy_skill_weight(r, skill_sigma), 0.0, upper)
    num = _legacy_integrate(
        lambda r: _legacy_skill_weight(r, skill_sigma) * _angular_mean_local_hit(r, poi_offset, pattern_sigma, pellet_count, target_area, k),
        0.0, upper,
    )
    return 100.0 * num / norm

@dataclass(frozen=True)
class JonesInputs:
    pellet_count: int
    target_area: float
    d75: float
    skill_d95: float
    poi_offset: float = 0.0
    k: int = 1

def evaluate(inputs: JonesInputs) -> float:
    return combined_hit_probability(
        pellet_count=inputs.pellet_count,
        target_area=inputs.target_area,
        pattern_sigma=sigma_from_d75(inputs.d75),
        skill_sigma=skill_sigma_from_d95(inputs.skill_d95),
        poi_offset=inputs.poi_offset,
        k=inputs.k,
    )
