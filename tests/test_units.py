"""E0 only: required metadata, fixture structure, and exact unit conversions."""
import copy
import json
from decimal import Decimal
from pathlib import Path
import unittest

from banglab.config import Parameter, validate_fixture
from banglab.units import convert

ROOT = Path(__file__).resolve().parents[1]


class UnitsTests(unittest.TestCase):
    def test_exact_contract_converters(self):
        for value, source, target, expected in [
            (1, 'yd', 'm', '0.9144'), (30, 'yd', 'm', '27.432'),
            (40, 'yd', 'm', '36.576'), (1, 'in', 'm', '0.0254'),
            (30, 'in', 'm', '0.762'), (60.8, 'ms', 's', '0.0608'),
            (187, 'mg', 'kg', '0.000187'), (3.15, 'mm', 'm', '0.00315'),
        ]:
            with self.subTest(source=source, value=value):
                self.assertEqual(convert(value, source, target), Decimal(expected))

    def test_dimension_and_unknown_unit_rejected(self):
        for source, target in [('m', 's'), ('yards', 'm'), ('ms', 'kg')]:
            with self.assertRaises(ValueError):
                convert(1, source, target)

    def test_invalid_numbers_rejected(self):
        for value in [True, None, '1', float('nan'), float('inf')]:
            with self.assertRaises(ValueError):
                convert(value, 'ms', 's')


class SchemaTests(unittest.TestCase):
    def test_parameter_requires_all_metadata_and_is_frozen(self):
        p = Parameter(20, 'm', 'USER_INPUT', 'contract §8.3')
        self.assertEqual(p.si('m'), Decimal(20))
        with self.assertRaises(AttributeError):
            p.value = 30
        for field in ['value', 'unit', 'label', 'locator']:
            fields = dict(value=20, unit='m', label='USER_INPUT', locator='§8.3')
            del fields[field]
            with self.assertRaises(TypeError):
                Parameter(**fields)

    def test_invalid_parameter_metadata_rejected(self):
        for fields in [
            (None, 'm', 'USER_INPUT', '§8.3'),
            (20, 'm', 'MEASURED', '§8.3'),
            (20, 'unknown', 'USER_INPUT', '§8.3'),
            (20, 'm', 'USER_INPUT', ''),
            (float('nan'), 'm', 'USER_INPUT', '§8.3'),
        ]:
            with self.assertRaises(ValueError):
                Parameter(*fields)

    def test_current_fixtures_have_valid_structure(self):
        for path in (ROOT / 'data/fixtures').glob('*.json'):
            with self.subTest(fixture=path.name):
                validate_fixture(json.loads(path.read_text(encoding='utf-8')))

    def test_each_existing_required_field_is_required(self):
        # Deleting each scalar/container exercises nested required-field checks.
        for path in (ROOT / 'data/fixtures').glob('*.json'):
            fixture = json.loads(path.read_text(encoding='utf-8'))
            def walk(node, route=()):
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key == 'notes':
                            continue
                        altered = copy.deepcopy(fixture)
                        parent = altered
                        for step in route:
                            parent = parent[step]
                        del parent[key]
                        with self.subTest(fixture=path.name, field=route + (key,)):
                            with self.assertRaises(ValueError):
                                validate_fixture(altered)
                        walk(value, route + (key,))
                elif isinstance(node, list):
                    for i, value in enumerate(node):
                        walk(value, route + (i,))
            walk(fixture)

    def test_invalid_rows_and_semantics_rejected(self):
        b1 = json.loads((ROOT / 'data/fixtures/dep_b1.json').read_text())
        p82 = json.loads((ROOT / 'data/fixtures/dep_p82.json').read_text())
        cases = []
        for field, value in [('t2_ms', -1), ('t3_ms', 1), ('vL_m_s', True),
                             ('split', 'TRAIN'), ('range_m', float('nan'))]:
            x = copy.deepcopy(b1); x['rows'][0][field] = value; cases.append(x)
        x = copy.deepcopy(b1); x['column_labels']['EL_J'] = 'MEASURED_PRIMARY'; cases.append(x)
        x = copy.deepcopy(b1); x['rows'].pop(); cases.append(x)
        for field, value in [('ref', 1), ('circle_30in', 999), ('paper_5ft', 2.5),
                             ('source_percent', -1), ('range_yd', 31)]:
            x = copy.deepcopy(p82); x['rows'][1][field] = value; cases.append(x)
        for x in cases:
            with self.assertRaises(ValueError):
                validate_fixture(x)


if __name__ == '__main__':
    unittest.main()
