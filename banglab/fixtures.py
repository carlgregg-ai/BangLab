"""Trusted E2 data boundary: expose only hash-verified DEV timing fields."""
from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from types import MappingProxyType

from .config import Parameter
from .units import convert

# Contract §2 / A17: range IDs only, never held-out timing observations.
DEV_RANGES_M = (20, 30, 40, 50)
LOCKED_RANGES_M = (25, 35, 45)


class LockedDataError(ValueError):
    """Access requires a separately authorised E3 capability (not implemented)."""


@dataclass(frozen=True)
class DevTiming:
    range: Parameter
    lead: Parameter
    trail: Parameter


class DevTimingView(Mapping):
    """Immutable DEV-only calibration view; sealed range lookup always raises."""
    def __init__(self, observations):
        rows = {}
        for row in observations:
            if not isinstance(row, DevTiming):
                raise TypeError('DEV timing observations required.')
            range_m = row.range.value
            if range_m in LOCKED_RANGES_M:
                raise LockedDataError('LOCKED observations cannot enter a DEV view.')
            if range_m not in DEV_RANGES_M or range_m in rows:
                raise ValueError('Invalid or duplicate DEV range.')
            for parameter, unit in ((row.range, 'm'), (row.lead, 's'), (row.trail, 's')):
                if parameter.unit != unit or parameter.label != 'MEASURED_PRIMARY':
                    raise ValueError('Explicit primary-observation metadata required.')
                if parameter.value <= 0:
                    raise ValueError('Positive source observations required.')
            if row.trail.value <= row.lead.value:
                raise ValueError('Invalid DEV timing order.')
            rows[range_m] = row
        if tuple(sorted(rows)) != DEV_RANGES_M:
            raise ValueError('Exactly the four contract DEV ranges are required.')
        self._rows = MappingProxyType({range_m: rows[range_m] for range_m in DEV_RANGES_M})

    def __getitem__(self, range_m):
        if range_m in LOCKED_RANGES_M:
            raise LockedDataError('LOCKED observations are sealed until E3.')
        return self._rows[range_m]

    def __iter__(self):
        return iter(self._rows)

    def __len__(self):
        return len(self._rows)


def _discard_locked(obj):
    # The JSON parser handles file structure inside this trusted boundary.
    # Drop sealed row objects before any observation fields are accessed
    # or returned; the model never receives the full parsed fixture.
    if obj.get('split') == 'LOCKED':
        return None
    return obj


def load_dev_longitudinal(path, expected_sha256):
    """Project the canonical B1 bytes into four labelled SI observations.

    Caller supplies the frozen file-byte digest. No default path, digest,
    scientific value, or E3 bypass is supplied. Derived columns are unused.
    """
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError('B1 canonical file-byte SHA-256 mismatch.')
    data = json.loads(raw, object_hook=_discard_locked)
    if data.get('fixture') != 'DEP_B1':
        raise ValueError('DEP_B1 fixture required.')
    try:
        locator, labels, rows = data['locator'], data['column_labels'], data['rows']
        for field in ('range_m', 't2_ms', 't3_ms'):
            if labels[field] != 'MEASURED_PRIMARY':
                raise ValueError('Primary timing metadata required.')
        observations = []
        for row in rows:
            if row is None:
                continue
            if row.get('split') != 'DEV':
                raise ValueError('Unknown source split.')
            range_m = row['range_m']
            if range_m in LOCKED_RANGES_M:
                raise LockedDataError('Sealed range incorrectly marked DEV.')
            if range_m not in DEV_RANGES_M:
                raise ValueError('Unsupported DEV range.')
            observations.append(DevTiming(
                Parameter(range_m, 'm', labels['range_m'], locator),
                Parameter(float(convert(row['t2_ms'], 'ms', 's')),
                          's', labels['t2_ms'], locator),
                Parameter(float(convert(row['t3_ms'], 'ms', 's')),
                          's', labels['t3_ms'], locator)))
    except (KeyError, TypeError) as error:
        raise ValueError('Missing or invalid DEV fixture fields.') from error
    return DevTimingView(observations)
