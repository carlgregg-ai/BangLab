"""E2: independent DEV-only PCHIP timing; E3 remains sealed."""
import numpy as np
from scipy.interpolate import PchipInterpolator

from ..fixtures import DEV_RANGES_M, LOCKED_RANGES_M, DevTimingView, LockedDataError


class LongitudinalModel:
    """Empirical main-string timing in seconds, contract §8.2.1.

    Public predictions at held-out range IDs remain blocked until a later
    separately authorised E3 capability exists. No extrapolation or fitting
    to held-out observations is available.
    """
    unit = 's'
    label = 'MODEL_PREDICTION'
    locator = 'Authoritative contract §8.2.1; DEP Appendix B p.77 Fig B1 DEV timings'

    def __init__(self, dev):
        if not isinstance(dev, DevTimingView):
            raise TypeError('A DEV-only timing view is required, not a raw fixture.')
        ranges = np.asarray(DEV_RANGES_M, dtype=float)
        lead = np.asarray([dev[r].lead.value for r in DEV_RANGES_M], dtype=float)
        trail = np.asarray([dev[r].trail.value for r in DEV_RANGES_M], dtype=float)
        if not (np.all(np.diff(lead) > 0) and np.all(np.diff(trail) > 0)):
            raise ValueError('DEV lead and trail times must be strictly increasing.')
        self._lead = PchipInterpolator(ranges, lead, extrapolate=False)
        self._trail = PchipInterpolator(ranges, trail, extrapolate=False)

    @staticmethod
    def _ranges(range_m):
        ranges = np.asarray(range_m)
        if ranges.dtype.kind not in 'iuf' or ranges.ndim > 1 or ranges.size == 0:
            raise ValueError('Finite scalar or one-dimensional numeric ranges in metres required.')
        if not np.all(np.isfinite(ranges)):
            raise ValueError('Finite ranges required.')
        if np.any((ranges < DEV_RANGES_M[0]) | (ranges > DEV_RANGES_M[-1])):
            raise ValueError('Timing domain is 20–50 m; extrapolation is forbidden.')
        if np.any(np.isin(ranges, LOCKED_RANGES_M)):
            raise LockedDataError('Held-out range predictions are sealed until E3.')
        return ranges

    @staticmethod
    def _result(values):
        return float(values) if values.ndim == 0 else values

    def t2(self, range_m):
        """Leading-edge flight time from muzzle, seconds."""
        return self._result(self._lead(self._ranges(range_m)))

    def t3(self, range_m):
        """Trailing-edge flight time from muzzle, seconds."""
        return self._result(self._trail(self._ranges(range_m)))

    def delta_t(self, range_m):
        """Main-string duration t3 - t2, seconds."""
        ranges = self._ranges(range_m)
        return self._result(self._trail(ranges) - self._lead(ranges))
