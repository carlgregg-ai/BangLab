"""E4 tests: calibration and mathematics, not physical validation."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
from scipy.integrate import quad

from banglab.encounter.lateral import LateralModel, circle_fraction, infer_sigma

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/fixtures/dep_p82.json'
SHA = '37de300cd68184cc2315b6fffaf4fa04dbe07127a30514e982b538238359dc09'


class LateralTests(unittest.TestCase):
    def setUp(self):
        self.model = LateralModel.from_p82(PATH, SHA)

    def test_evidence_hash_and_raw_count_fractions(self):
        self.assertEqual(hashlib.sha256(PATH.read_bytes()).hexdigest(), SHA)
        self.assertEqual(self.model.fractions, (180.5 / 192, 145.3 / 192))
        self.assertEqual(self.model.pellet_count.value, 192)
        self.assertEqual(self.model.pellet_count.label, 'MEASURED_PRIMARY')

    def test_exact_units_and_parameter_labels(self):
        self.assertEqual(self.model.ranges_m, (27.432, 36.576))
        self.assertEqual(self.model.radius.value, 0.381)
        self.assertEqual(self.model.radius.unit, 'm')
        for sigma in self.model.calibration_sigmas:
            self.assertEqual(sigma.unit, 'm')
            self.assertEqual(sigma.label, 'INFERRED')
            self.assertTrue(sigma.locator)
        self.assertEqual(self.model.shape_label, 'ASSUMED')
        self.assertEqual(self.model.range_law_label, 'ASSUMED')
        self.assertEqual(self.model.k.unit, '1')
        self.assertEqual(self.model.k.label, 'INFERRED')

    def test_contract_sigma_targets_and_fraction_reproduction(self):
        for r, p, target in zip(self.model.ranges_m, self.model.fractions, (0.1606, 0.2266)):
            sigma = self.model.scale(r).sigma.value
            self.assertLessEqual(abs(sigma - target), 1e-4)
            self.assertLessEqual(abs(circle_fraction(0.381, sigma) - p), 1e-9)

    def test_gaussian_inversion_independent_analytic_case(self):
        self.assertAlmostEqual(infer_sigma(1 - np.exp(-0.5), 2), 2, places=14)
        self.assertAlmostEqual(circle_fraction(2, 2), 1 - np.exp(-0.5), places=14)
        self.assertEqual(circle_fraction(0, 2), 0)

    def test_linear_law_including_extrapolation(self):
        a, b = [p.value for p in self.model.calibration_sigmas]
        for r in (20, 27.432, 30, 36.576, 40, 50):
            expected = a + (b - a) * (r - 27.432) / (36.576 - 27.432)
            self.assertEqual(self.model.scale(r).sigma.value, expected)
        self.assertAlmostEqual(self.model.scale(32.004).sigma.value, (a + b) / 2)

    def test_flags_and_positive_sigma_on_domain(self):
        for r in np.linspace(20, 50, 301):
            scale = self.model.scale(float(r))
            self.assertGreater(scale.sigma.value, 0)
            self.assertEqual(scale.flags, frozenset({'EXTRAPOLATED_LATERAL'})
                             if r < 27.432 or r > 36.576 else frozenset())
        for r in self.model.ranges_m:
            self.assertEqual(self.model.scale(r).flags, frozenset())

    def test_proportional_k_contract_target_and_fraction_least_squares(self):
        k = self.model.k.value
        self.assertLessEqual(abs(k - 0.00611), 1e-5)
        # Independently check the derivative of the fraction-space objective.
        gradient = 0.0
        def objective(value):
            return sum((circle_fraction(0.381, value*r)-p)**2
                       for r, p in zip(self.model.ranges_m, self.model.fractions))
        for r, p in zip(self.model.ranges_m, self.model.fractions):
            exponential = np.exp(-0.381**2 / (2*k*k*r*r))
            derivative = -exponential * 0.381**2 / (k**3*r*r)
            gradient += 2 * (1-exponential-p) * derivative
        self.assertLess(abs(gradient), 1e-5)  # Numerical optimisation check, not an evidence tolerance.
        self.assertLess(objective(k), objective(k-1e-5))
        self.assertLess(objective(k), objective(k+1e-5))
        self.assertEqual(self.model.scale(30, law='proportional').sigma.value, k*30)
        self.assertEqual(self.model.scale(30, law='proportional').law_label, 'PROPOSED')

    def test_density_normalization_and_circle_integral(self):
        for r in (20, 27.432, 36.576, 50):
            integral = quad(lambda x: 2*np.pi*x*self.model.density(r, x, 0), 0, np.inf)[0]
            self.assertAlmostEqual(integral, 1, places=10)
        for r, p in zip(self.model.ranges_m, self.model.fractions):
            integral = quad(lambda x: 2*np.pi*x*self.model.density(r, x, 0), 0, 0.381)[0]
            self.assertLessEqual(abs(integral-p), 1e-9)

    def test_radial_symmetry_and_expected_pellet_density(self):
        for r in (20, 30, 50):
            value = self.model.density(r, 0.3, 0.4)
            self.assertAlmostEqual(value, self.model.density(r, 0.5, 0), places=14)
            self.assertEqual(value, self.model.density(r, -0.3, -0.4))
            self.assertEqual(self.model.pellet_density(r, 0.3, 0.4), 192*value)

    def test_determinism(self):
        other = LateralModel.from_p82(PATH, SHA)
        self.assertEqual(self.model, other)
        self.assertEqual(self.model.density(30, 0.1, 0.2), other.density(30, 0.1, 0.2))

    def test_invalid_inputs_rejected(self):
        for bad in (19.9, 50.1, float('nan'), float('inf'), True, '30', None, [30]):
            with self.assertRaises(ValueError):
                self.model.scale(bad)
        for p in (0, 1, -0.1, 1.1, True, float('nan')):
            with self.assertRaises(ValueError):
                infer_sigma(p, 0.381)
        for sigma in (0, -1, float('inf'), True):
            with self.assertRaises(ValueError):
                circle_fraction(0.381, sigma)
        with self.assertRaises(ValueError):
            circle_fraction(-1, 1)
        with self.assertRaises(ValueError):
            self.model.scale(30, law='unknown')
        with self.assertRaises(ValueError):
            self.model.density(30, float('nan'), 0)

    def test_hash_guard_precedes_parsing_and_only_p82_is_read(self):
        with patch('banglab.encounter.lateral.json.loads', side_effect=AssertionError('No parsing')):
            with self.assertRaises(ValueError):
                LateralModel.from_p82(PATH, '0'*64)
        raw = PATH.read_bytes()
        with patch.object(Path, 'read_bytes', return_value=raw) as read:
            LateralModel.from_p82(PATH, SHA)
            self.assertEqual(read.call_count, 1)

    def test_invalid_evidence_denominator_rejected(self):
        data = json.loads(PATH.read_bytes())
        data['average_pellets_per_cartridge'] = 191
        raw = json.dumps(data).encode()
        with patch.object(Path, 'read_bytes', return_value=raw):
            with self.assertRaises(ValueError):
                LateralModel.from_p82(PATH, hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    unittest.main()
