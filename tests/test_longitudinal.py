"""E2 only: DEV reproduction and structural correctness; no E3 evaluation."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
from scipy.interpolate import PchipInterpolator

from banglab.fixtures import (DEV_RANGES_M, LOCKED_RANGES_M, DevTimingView,
                              LockedDataError, load_dev_longitudinal)
from banglab.encounter.longitudinal import LongitudinalModel

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'data/fixtures/dep_b1.json'
B1_SHA256 = '9ac268e4d96b145b3ef9f82fda71193c43339a103cec4632203f68e3c0ce1e79'
LEAD_S = np.array([0.0608, 0.0984, 0.1433, 0.1953])
TRAIL_S = np.array([0.0684, 0.1118, 0.1624, 0.2200])


def view():
    return load_dev_longitudinal(FIXTURE, B1_SHA256)


def permitted_grid():
    grid = np.linspace(20.0, 50.0, 3001)
    return grid[~np.isin(grid, LOCKED_RANGES_M)]


class DevBoundaryTests(unittest.TestCase):
    def test_dev_only_metadata_and_single_si_conversion(self):
        data = view()
        self.assertEqual(tuple(data), DEV_RANGES_M)
        for i, range_m in enumerate(DEV_RANGES_M):
            row = data[range_m]
            self.assertEqual(row.range.unit, 'm')
            self.assertEqual(row.lead.unit, 's')
            self.assertEqual(row.trail.unit, 's')
            self.assertEqual(row.lead.value, LEAD_S[i])
            self.assertEqual(row.trail.value, TRAIL_S[i])
            for parameter in (row.range, row.lead, row.trail):
                self.assertEqual(parameter.label, 'MEASURED_PRIMARY')
                self.assertTrue(parameter.locator)
        with self.assertRaises(TypeError):
            data[20] = data[20]

    def test_locked_observation_access_raises(self):
        data = view()
        for range_m in LOCKED_RANGES_M:
            with self.assertRaises(LockedDataError):
                data[range_m]
        with self.assertRaises(KeyError):
            data[19]

    def test_hash_mismatch_stops_before_json_parsing(self):
        with patch('banglab.fixtures.json.loads', side_effect=AssertionError('Must not parse')):
            with self.assertRaises(ValueError):
                load_dev_longitudinal(FIXTURE, '0' * 64)

    def test_locked_fields_not_accessed_by_projection(self):
        from banglab.fixtures import _discard_locked
        class SealedRow(dict):
            def get(self, key, default=None):
                if key == 'split':
                    return 'LOCKED'
                raise AssertionError('Sealed observation field accessed')
            def __getitem__(self, key):
                raise AssertionError('Sealed observation field accessed')
        self.assertIsNone(_discard_locked(SealedRow()))

    def test_missing_dev_rows_and_invalid_metadata_rejected(self):
        data = view()
        with self.assertRaises(ValueError):
            DevTimingView(tuple(data.values())[:-1])
        # Synthetic DEV-only invalid input; no held-out observations used.
        source = {'fixture': 'DEP_B1', 'locator': 'synthetic schema rejection',
                  'column_labels': {'range_m':'MEASURED_PRIMARY',
                                    't2_ms':'SOURCE_DERIVED', 't3_ms':'MEASURED_PRIMARY'},
                  'rows': [{'range_m':20,'t2_ms':1,'t3_ms':2,'split':'DEV'}]}
        raw = json.dumps(source).encode()
        with patch('banglab.fixtures.Path.read_bytes', return_value=raw):
            with self.assertRaises(ValueError):
                load_dev_longitudinal('synthetic.json', hashlib.sha256(raw).hexdigest())


class LongitudinalTests(unittest.TestCase):
    def setUp(self):
        self.model = LongitudinalModel(view())

    def test_two_independent_pchip_constructions_dev_only(self):
        with patch('banglab.encounter.longitudinal.PchipInterpolator',
                   wraps=PchipInterpolator) as constructor:
            LongitudinalModel(view())
        self.assertEqual(constructor.call_count, 2)
        for call, expected in zip(constructor.call_args_list, (LEAD_S, TRAIL_S)):
            np.testing.assert_array_equal(call.args[0], DEV_RANGES_M)
            np.testing.assert_array_equal(call.args[1], expected)
            self.assertFalse(call.kwargs['extrapolate'])

    def test_dev_knots_reproduced_below_contract_1e_minus9_s(self):
        for function, expected in [(self.model.t2, LEAD_S), (self.model.t3, TRAIL_S)]:
            errors = np.abs(function(DEV_RANGES_M) - expected)
            self.assertTrue(np.all(errors < 1e-9))

    def test_monotone_and_positive_duration_on_permitted_domain(self):
        ranges = permitted_grid()
        lead, trail = self.model.t2(ranges), self.model.t3(ranges)
        self.assertTrue(np.all(np.diff(lead) > 0))
        self.assertTrue(np.all(np.diff(trail) > 0))
        self.assertTrue(np.all(trail > lead))
        np.testing.assert_array_equal(self.model.delta_t(ranges), trail - lead)
        self.assertTrue(np.all(self.model.delta_t(ranges) > 0))

    def test_piecewise_polynomials_certify_domain_structure(self):
        # Algebra on DEV-built coefficients certifies the whole interval;
        # no held-out observations or timing predictions at locked IDs.
        lead = PchipInterpolator(DEV_RANGES_M, LEAD_S, extrapolate=False)
        trail = PchipInterpolator(DEV_RANGES_M, TRAIL_S, extrapolate=False)
        for j, width in enumerate(np.diff(lead.x)):
            for polynomial in (lead.c[:, j], trail.c[:, j]):
                slope = np.polyder(polynomial)
                candidates = [0.0, width]
                for root in np.roots(np.polyder(slope)):
                    if np.isreal(root) and 0 < root.real < width:
                        candidates.append(float(root.real))
                self.assertTrue(all(np.polyval(slope, x) > 0 for x in candidates))
            gap = trail.c[:, j] - lead.c[:, j]
            candidates = [0.0, width]
            for root in np.roots(np.polyder(gap)):
                if np.isreal(root) and 0 < root.real < width:
                    candidates.append(float(root.real))
            self.assertTrue(all(np.polyval(gap, x) > 0 for x in candidates))

    def test_locked_predictions_raise_before_pchip_evaluation(self):
        with patch.object(self.model, '_lead', side_effect=AssertionError('Must not evaluate')):
            for function in (self.model.t2, self.model.t3, self.model.delta_t):
                for range_m in LOCKED_RANGES_M:
                    with self.assertRaises(LockedDataError):
                        function(range_m)
                with self.assertRaises(LockedDataError):
                    function([20, LOCKED_RANGES_M[0]])

    def test_domain_and_invalid_inputs_rejected(self):
        invalid = [19.99, 50.01, float('nan'), float('inf'), True, '30', None,
                   [20, 51], [True, False], [], [[20,30]]]
        for function in (self.model.t2, self.model.t3, self.model.delta_t):
            for value in invalid:
                with self.subTest(function=function.__name__, input_type=type(value).__name__):
                    with self.assertRaises(ValueError):
                        function(value)

    def test_scalar_vector_units_and_prediction_metadata(self):
        self.assertIsInstance(self.model.t2(20), float)
        self.assertEqual(self.model.unit, 's')
        self.assertEqual(self.model.label, 'MODEL_PREDICTION')
        self.assertTrue(self.model.locator)
        np.testing.assert_array_equal(self.model.t2([20,30]), LEAD_S[:2])
        self.assertEqual(self.model.delta_t(20), self.model.t3(20)-self.model.t2(20))

    def test_repeatability_and_raw_fixture_rejected(self):
        ranges = permitted_grid()
        other = LongitudinalModel(view())
        for name in ('t2','t3','delta_t'):
            a = getattr(self.model, name)(ranges)
            b = getattr(other, name)(ranges)
            self.assertEqual(a.tobytes(), b.tobytes())
            self.assertEqual(a.tobytes(), getattr(self.model, name)(ranges).tobytes())
        with self.assertRaises(TypeError):
            LongitudinalModel({'rows': []})


if __name__ == '__main__':
    unittest.main()
