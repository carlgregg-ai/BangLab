"""Controlled alternatives to the recovered Jones compatibility model."""
from __future__ import annotations

from math import cos, hypot, pi, sin
from numpy.polynomial.legendre import leggauss
from . import legacy

_GL_X, _GL_W = leggauss(32)

def poisson_k_or_more(lam: float, k: int) -> float:
    if lam < 0:
        raise ValueError("lam must be non-negative")
    if k < 1:
        return 1.0
    p = __import__("math").exp(-lam)
    cumulative = p
    for j in range(1, k):
        p *= lam / j
        cumulative += p
    return max(0.0, min(1.0, 1.0 - cumulative))

def _local_hit(r: float, pattern_sigma: float, pellet_count: int, target_area: float, k: int, *, direct_poisson: bool) -> float:
    lam = legacy.expected_strikes(r, pattern_sigma, pellet_count, target_area)
    return poisson_k_or_more(lam, k) if direct_poisson else legacy.k_or_more_probability(lam, k)

def _angular_mean_dense(shooter_r: float, poi_offset: float, pattern_sigma: float, pellet_count: int, target_area: float, k: int, *, direct_poisson: bool, nodes: int = 32) -> float:
    if poi_offset == 0.0:
        return _local_hit(shooter_r, pattern_sigma, pellet_count, target_area, k, direct_poisson=direct_poisson)
    xs, ws = (_GL_X, _GL_W) if nodes == 32 else leggauss(nodes)
    total = 0.0
    for x, w in zip(xs, ws):
        theta = pi * (float(x) + 1.0)
        rr = hypot(shooter_r * cos(theta) - poi_offset, shooter_r * sin(theta))
        total += float(w) * _local_hit(rr, pattern_sigma, pellet_count, target_area, k, direct_poisson=direct_poisson)
    return 0.5 * total

def combined_hit_probability(*, pellet_count: int, target_area: float, pattern_sigma: float, skill_sigma: float, poi_offset: float = 0.0, k: int = 1, correct_skill_weight: bool = True, direct_poisson: bool = True, exact_angles: bool = True) -> float:
    """Evaluate a controlled corrected variant, returning percent."""
    upper = legacy.SKILL_TRUNCATION_SIGMA * skill_sigma
    weight = legacy.radial_rayleigh_pdf if correct_skill_weight else legacy._legacy_skill_weight
    rx, rw = _GL_X, _GL_W

    def local(r: float) -> float:
        if exact_angles:
            return _angular_mean_dense(r, poi_offset, pattern_sigma, pellet_count, target_area, k, direct_poisson=direct_poisson)
        if not direct_poisson:
            return legacy._angular_mean_local_hit(r, poi_offset, pattern_sigma, pellet_count, target_area, k)
        if poi_offset == 0.0:
            return _local_hit(r, pattern_sigma, pellet_count, target_area, k, direct_poisson=True)
        vals = []
        for i in range(4):
            theta = i * pi / 4.0
            for sign in (1.0, -1.0):
                rr = hypot(sign * r * cos(theta) - poi_offset, sign * r * sin(theta))
                vals.append(_local_hit(rr, pattern_sigma, pellet_count, target_area, k, direct_poisson=True))
        return sum(vals) / 8.0

    norm = 0.0
    num = 0.0
    for x, w in zip(rx, rw):
        r = 0.5 * upper * (float(x) + 1.0)
        ww = 0.5 * upper * float(w)
        wr = weight(r, skill_sigma)
        norm += ww * wr
        num += ww * wr * local(r)
    return 100.0 * num / norm

def evaluate(inputs: legacy.JonesInputs, **kwargs: bool) -> float:
    return combined_hit_probability(
        pellet_count=inputs.pellet_count,
        target_area=inputs.target_area,
        pattern_sigma=legacy.sigma_from_d75(inputs.d75),
        skill_sigma=legacy.skill_sigma_from_d95(inputs.skill_d95),
        poi_offset=inputs.poi_offset,
        k=inputs.k,
        **kwargs,
    )
