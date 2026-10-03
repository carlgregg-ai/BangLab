"""E4 DEP_REF Gaussian calibration (contract sections 8.2.3-4 and 8.7).

Gaussian shape, centred circle placement and a linear range law are
ASSUMED. Agreement with both calibration fractions is not validation.
No timing observations, clay geometry or encounter integration are used.
"""
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

from ..config import Parameter, validate_fixture
from ..units import convert, number

LOCATOR = 'DEP 99/953 App. B p.82; authoritative contract 8.2.3-4'


def finite(value):
    if isinstance(value, (np.integer, np.floating)):
        value = value.item()
    result = float(number(value))
    if not math.isfinite(result):
        raise ValueError("Finite machine-representable scalar required.")
    return result


def positive(value):
    value = finite(value)
    if value <= 0:
        raise ValueError('Positive value required.')
    return value


def infer_sigma(fraction, radius_m):
    """Gaussian inversion; fraction dimensionless, radius/sigma in metres."""
    p, radius = finite(fraction), positive(radius_m)
    if not 0 < p < 1:
        raise ValueError('Circle fraction must lie strictly between zero and one.')
    return radius / math.sqrt(-2 * math.log1p(-p))


def circle_fraction(radius_m, sigma_m):
    """Centred Gaussian circle mass, not a clay contact calculation."""
    radius, sigma = finite(radius_m), positive(sigma_m)
    if radius < 0:
        raise ValueError('Nonnegative circle radius required.')
    return -math.expm1(-0.5 * (radius / sigma)**2)


@dataclass(frozen=True)
class LateralScale:
    sigma: Parameter
    flags: frozenset
    law_label: str


@dataclass(frozen=True)
class LateralModel:
    """Scalar SI API. density is probability/m²; pellet_density is pellets/m².

    Both densities are MODEL_PREDICTION. The proportional law is an
    explicitly selected PROPOSED variant; linear is the contract baseline.
    """
    ranges_m: tuple
    fractions: tuple
    calibration_sigmas: tuple
    radius: Parameter
    pellet_count: Parameter
    k: Parameter
    fixture_sha256: str
    shape_label = 'ASSUMED'
    range_law_label = 'ASSUMED'
    circle_placement_label = 'ASSUMED'
    density_label = 'MODEL_PREDICTION'

    @classmethod
    def from_p82(cls, path, expected_sha256):
        raw = Path(path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            raise ValueError('p.82 canonical SHA-256 mismatch.')
        data = json.loads(raw)
        if data.get('fixture') != 'DEP_P82':
            raise ValueError('DEP_P82 evidence required.')
        validate_fixture(data)
        if data['average_pellets_per_cartridge'] != 192:
            raise ValueError('The contract DEP denominator is exactly 192.')
        ranges = tuple(float(convert(r, 'yd', 'm')) for r in (30, 40))
        # 30-inch diameter means 15-inch radius, exactly 0.381 m.
        radius = float(convert(30, 'in', 'm') / 2)
        fractions = tuple(sum(row['circle_30in'] for row in data['rows'] if row['range_yd'] == r)
                          / 10 / data['average_pellets_per_cartridge'] for r in (30, 40))
        sigmas = tuple(infer_sigma(p, radius) for p in fractions)
        # Unweighted least squares in circle-fraction space, NOT sigma space.
        # The two exact single-range k solutions bound the positive optimum:
        # outside this interval both fraction residuals move the same way.
        bounds = sorted(s / r for s, r in zip(sigmas, ranges))
        fit = minimize_scalar(lambda k: sum((circle_fraction(radius, k*r)-p)**2
                              for r, p in zip(ranges, fractions)),
                              bounds=bounds, method='bounded', options={'xatol': 1e-14})
        if not fit.success:
            raise ValueError('Proportional-law numerical solver failed.')
        return cls(ranges, fractions,
                   tuple(Parameter(s, 'm', 'INFERRED', LOCATOR) for s in sigmas),
                   Parameter(radius, 'm', 'SOURCE_DERIVED', LOCATOR),
                   Parameter(192, 'count', 'MEASURED_PRIMARY', LOCATOR),
                   Parameter(float(fit.x), '1', 'INFERRED', LOCATOR), expected_sha256)

    def scale(self, range_m, *, law='linear'):
        r = finite(range_m)
        if not 20 <= r <= 50:
            raise ValueError('Lateral range domain is 20-50 m.')
        if law == 'linear':
            a, b = (p.value for p in self.calibration_sigmas)
            sigma = a + (b-a) * (r-self.ranges_m[0]) / (self.ranges_m[1]-self.ranges_m[0])
            label = 'ASSUMED'
        elif law == 'proportional':
            sigma, label = self.k.value*r, 'PROPOSED'
        else:
            raise ValueError('Unknown sigma law.')
        flags = frozenset({'EXTRAPOLATED_LATERAL'}) if not self.ranges_m[0] <= r <= self.ranges_m[1] else frozenset()
        return LateralScale(Parameter(positive(sigma), 'm', 'MODEL_PREDICTION', LOCATOR), flags, label)

    def density(self, range_m, x_m, y_m, *, law='linear'):
        """Normalized isotropic Gaussian density in m^-2 at a lateral point."""
        sigma = self.scale(range_m, law=law).sigma.value
        x, y = finite(x_m), finite(y_m)
        return math.exp(-0.5*((x/sigma)**2+(y/sigma)**2)) / (2*math.pi*sigma*sigma)

    def pellet_density(self, range_m, x_m, y_m, *, law='linear'):
        return self.pellet_count.value * self.density(range_m, x_m, y_m, law=law)
