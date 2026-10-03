"""E0 metadata and fixture validation; never loads data for model calibration."""
from dataclasses import dataclass
from .units import UNITS, convert, number

LABELS = frozenset({'MEASURED_PRIMARY', 'SOURCE_DERIVED', 'INFERRED',
                    'ASSUMED', 'PROPOSED', 'USER_INPUT', 'MODEL_PREDICTION',
                    'UNKNOWN', 'UNSUPPORTED'})


@dataclass(frozen=True)
class Parameter:
    value: object
    unit: str
    label: str
    locator: str

    def __post_init__(self):
        number(self.value)
        if not isinstance(self.unit, str) or self.unit not in UNITS:
            raise ValueError('Explicit supported unit required.')
        if not isinstance(self.label, str) or self.label not in LABELS:
            raise ValueError('Allowed epistemic label required.')
        if not isinstance(self.locator, str) or not self.locator.strip():
            raise ValueError('Nonempty source/contract locator required.')

    def si(self, target_unit):
        return convert(self.value, self.unit, target_unit)


def text(x):
    return isinstance(x, str) and bool(x.strip())


def positive(x):
    return number(x) > 0


def nonnegative(x):
    return number(x) >= 0


def count(x):
    return type(x) is int and x >= 0


def percent(x):
    return 0 <= number(x) <= 100


def check(data, schema, path='fixture'):
    if isinstance(schema, dict):
        if not isinstance(data, dict) or set(data) != set(schema):
            raise ValueError(f'{path}: missing or unexpected fields')
        for key, rule in schema.items():
            check(data[key], rule, f'{path}.{key}')
    elif isinstance(schema, list):
        if not isinstance(data, list) or not data:
            raise ValueError(f'{path}: nonempty list required')
        for i, item in enumerate(data):
            check(item, schema[0], f'{path}[{i}]')
    elif callable(schema):
        try:
            valid = schema(data)
        except (TypeError, ValueError):
            valid = False
        if not valid:
            raise ValueError(f'{path}: invalid value')
    elif data != schema:
        raise ValueError(f'{path}: invalid declared metadata')


B1_LABELS = {k: ('MEASURED_PRIMARY' if k in ('range_m', 't2_ms', 't3_ms')
                 else 'SOURCE_DERIVED') for k in
             ('range_m', 't2_ms', 't3_ms', 'vL_m_s', 'vT_m_s', 'EL_J', 'ET_J', 'L_m')}
B1_ROW = {k: positive for k in B1_LABELS}
B1_ROW['split'] = lambda x: x in ('DEV', 'LOCKED')
P82_ROW = {'ref': count, 'range_yd': positive, 'paper_5ft': count,
           'circle_30in': count, 'source_percent': lambda x: count(x) and x <= 100}
SUMMARY = {k: nonnegative for k in ('paper_mean', 'paper_sd_population',
           'circle_mean', 'circle_sd_population', 'percent_mean',
           'percent_sd_population', 'paper_sig_avg_percent',
           'circle_sig_avg_percent', 'percent_sig_avg_percent')}
LOAD = {
    'fixture': 'DEP_LOAD', 'locators': [text],
    'load': {'mass_g': positive, 'pellet_count': count, 'pellet_mass_mg': positive,
             'pellet_diameter_mm': positive, 'velocity_at_2_5m_m_s': positive},
    'gun': {'proof_barrel_in': positive, 'bore_mm': positive, 'choke_in': nonnegative},
    'environment': {'temperature_C': lambda x: number(x).is_finite(),
                    'pressure_mb': positive, 'relative_humidity_percent': percent,
                    'wind_m_s': nonnegative, 'wind_from_deg': lambda x: 0 <= number(x) < 360},
    'design': {'ranges_m': [positive], 'rounds_per_range': count},
    'labels': {'source_values': 'MEASURED_PRIMARY'},
}


def validate_fixture(data):
    """Validate evidence structure in place; returns no model/calibration view."""
    if not isinstance(data, dict):
        raise ValueError('Fixture object required.')
    kind = data.get('fixture')
    if kind == 'DEP_B1':
        check(data, {'fixture': kind, 'locator': text, 'notes': [text],
                     'column_labels': B1_LABELS, 'rows': [B1_ROW]})
        rows = data['rows']
        if [r['range_m'] for r in rows] != [20, 25, 30, 35, 40, 45, 50]:
            raise ValueError('Seven ordered B1 ranges required.')
        for row in rows:
            expected = 'DEV' if row['range_m'] in (20, 30, 40, 50) else 'LOCKED'
            if row['split'] != expected or row['t3_ms'] <= row['t2_ms']:
                raise ValueError('Invalid B1 split or timing order.')
    elif kind == 'DEP_P82':
        check({k: v for k, v in data.items() if k != 'rows'},
              {'fixture': kind, 'source': text, 'locator': text,
               'average_pellets_per_cartridge': lambda x: count(x) and x > 0,
               'epistemic_status': 'MEASURED_PRIMARY', 'notes': [text],
               'published_summary': {'30yd': SUMMARY, '40yd': SUMMARY}})
        rows = data.get('rows')
        if not isinstance(rows, list) or len(rows) != 20:
            raise ValueError('Twenty p.82 rows required.')
        for ref, row in enumerate(rows, 1):
            schema = dict(P82_ROW)
            if ref == 2:
                schema['source_note'] = 'overstrike, read 192, confirmed by mean'
            check(row, schema)
            if row['ref'] != ref or row['range_yd'] != (30 if ref <= 10 else 40):
                raise ValueError('Invalid p.82 ref/range allocation.')
            if row['circle_30in'] > row['paper_5ft']:
                raise ValueError('Circle count exceeds paper count.')
    elif kind == 'DEP_LOAD':
        check(data, LOAD)
        if data['load']['pellet_count'] <= 0 or data['design']['rounds_per_range'] <= 0:
            raise ValueError('Positive count required.')
        if data['design']['ranges_m'] != [20, 25, 30, 35, 40, 45, 50]:
            raise ValueError('Invalid source range design.')
    else:
        raise ValueError('Unknown or missing fixture identifier.')
