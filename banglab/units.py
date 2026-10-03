"""Exact decimal unit factors; no scientific defaults or model constants."""
from decimal import Decimal

# Decimal factors preserve exact contract-defined conversions.
UNITS = {
    'm': ('length', '1'), 'yd': ('length', '0.9144'),
    'in': ('length', '0.0254'), 'mm': ('length', '0.001'),
    's': ('time', '1'), 'ms': ('time', '0.001'),
    'kg': ('mass', '1'), 'g': ('mass', '0.001'), 'mg': ('mass', '0.000001'),
    'm/s': ('speed', '1'), 'J': ('energy', '1'),
    'deg': ('angle', '1'), 'C': ('temperature_C', '1'),
    'mb': ('pressure_mb', '1'), '%': ('ratio', '0.01'),
    '1': ('ratio', '1'), 'count': ('count', '1'),
}


def number(value):
    if type(value) not in (int, float, Decimal):
        raise ValueError('A finite number is required (booleans are not numbers).')
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError('A finite number is required.')
    return result


def convert(value, source, target):
    """Convert only compatible explicit units, returning a Decimal."""
    if source not in UNITS or target not in UNITS:
        raise ValueError('Unknown unit.')
    dimension, factor = UNITS[source]
    other_dimension, other_factor = UNITS[target]
    if dimension != other_dimension:
        raise ValueError('Incompatible dimensions.')
    return number(value) * Decimal(factor) / Decimal(other_factor)
