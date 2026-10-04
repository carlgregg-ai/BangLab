"""E5 field tests; E3 is consumed from its saved predictions, not rerun."""
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
from banglab.config import Parameter
from banglab.encounter.field import EncounterField, Scenario
from banglab.encounter.geometry import gaussian_mass
from test_geometry import shape

ROOT=Path(__file__).resolve().parents[1]

def scenario(r=30,v=20,direction=0):
    return Scenario(Parameter(r,'m','USER_INPUT','E5 scenario'),
                    Parameter(v,'m/s','USER_INPUT','E5 scenario'),
                    Parameter(direction,'deg','USER_INPUT','E5 scenario'))


class FieldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.field=EncounterField.from_repository(ROOT)

    def test_static_equals_mass_and_binomial_normalization(self):
        for r in (20,30,40,50):
            for s in (shape(),shape(b=0.0125,psi=37)):
                result=self.field.evaluate(scenario(r,0),s,0.1,-0.05)
                g=gaussian_mass(s,self.field.lateral.scale(r).sigma.value,-0.1,0.05)
                self.assertAlmostEqual(result.pi,g,places=14)
                self.assertEqual(result.expected_contacts,192*result.pi)
                self.assertLessEqual(abs(sum(result.count_pmf)-1),1e-12)
                self.assertEqual(result.role,'GEOMETRIC_CONTACT')
                self.assertEqual(result.label,'MODEL_PREDICTION')

    def test_clarified_general_joint_inversion(self):
        for psi in (17,37,75):
            for direction in (0,29):
                s=shape(b=0.0125,psi=psi)
                sc=scenario(direction=direction)
                a=self.field.evaluate(sc,s,0.12,0.08).pi
                b=self.field.evaluate(sc,s,-0.12,-0.08).pi
                self.assertLessEqual(abs(a/b-1),1e-6)

    def test_separate_reflections_only_compatible_orientations(self):
        for s in (shape(),shape(b=0.0125,psi=0),shape(b=0.0125,psi=90)):
            a=self.field.evaluate(scenario(),s,0.12,0.08).pi
            for x,y in ((-0.12,0.08),(0.12,-0.08)):
                b=self.field.evaluate(scenario(),s,x,y).pi
                self.assertLessEqual(abs(a/b-1),1e-6)

    def test_rotated_non_circle_is_not_forced_to_separate_reflections(self):
        s=shape(b=0.0125,psi=45)
        a=self.field.evaluate(scenario(v=0),s,0.1,0.1).pi
        b=self.field.evaluate(scenario(v=0),s,-0.1,0.1).pi
        self.assertGreater(abs(a-b),1e-8)

    def test_full_rotation_covariance(self):
        a=self.field.evaluate(scenario(),shape(b=0.02,psi=15),0.13,-0.04).pi
        theta=np.deg2rad(40)
        x,y=np.cos(theta)*0.13-np.sin(theta)*(-0.04),np.sin(theta)*0.13+np.cos(theta)*(-0.04)
        b=self.field.evaluate(scenario(direction=40),shape(b=0.02,psi=55),x,y).pi
        self.assertAlmostEqual(a,b,places=14)

    def test_node_doubling(self):
        for r in (20,30,40,50):
            for v in (0,10,20):
                for s in (shape(),shape(b=0.0125,psi=37)):
                    for x,y in ((0,0),(0.1,-0.05),(0.6,0.6)):
                        a=self.field.evaluate(scenario(r,v),s,x,y,n_q=64,n_x=48,method='ellipse').pi
                        b=self.field.evaluate(scenario(r,v),s,x,y,n_q=128,n_x=96,method='ellipse').pi
                        self.assertLess(abs(a/b-1),1e-6)

    def test_si_duration_coordinate_sign_and_static_offset_api(self):
        self.assertAlmostEqual(self.field.duration(30),0.0134,places=15)
        sc=scenario()
        np.testing.assert_allclose(self.field.clay_centre(sc,0.5,0.1,-0.2),(-0.1,0.2))
        np.testing.assert_allclose(self.field.clay_centre(sc,0,0,0),(-0.134,0),atol=1e-15)
        self.assertEqual(self.field.at_clay_offset(sc,shape(),0.1,-0.2),
                         self.field.evaluate(sc,shape(),-0.1,0.2))

    def test_saved_locked_predictions_consumed_without_new_evaluation(self):
        with patch.object(self.field.longitudinal,'_lead',side_effect=AssertionError('No E3 rerun')):
            with patch.object(self.field.longitudinal,'_trail',side_effect=AssertionError('No E3 rerun')):
                for r in (25,35,45):
                    result=self.field.evaluate(scenario(r),shape(),0,0)
                    self.assertGreater(result.expected_contacts,0)

    def test_determinism_grid_and_far_offset(self):
        sc=scenario()
        a=self.field.grid(sc,shape(),[0,0.1],[0,0.1])
        b=self.field.grid(sc,shape(),[0,0.1],[0,0.1])
        self.assertEqual(a.tobytes(),b.tobytes())
        self.assertGreater(a[0,0],a[1,1])
        self.assertLess(self.field.evaluate(sc,shape(),3,3).expected_contacts,1e-40)
        self.assertIn('EXTRAPOLATED_LATERAL',self.field.evaluate(scenario(20),shape(),0,0).flags)

    def test_invalid_scenarios_and_nodes(self):
        for q in (-0.1,1.1,float('nan'),True):
            with self.assertRaises(ValueError):
                self.field.clay_centre(scenario(),q,0,0)
        for r in (19,51,True,float('nan')):
            with self.assertRaises(ValueError):
                scenario(r)
        with self.assertRaises(ValueError):
            scenario(v=-1)
        with self.assertRaises(ValueError):
            self.field.evaluate(scenario(),shape(),float('inf'),0)
        with self.assertRaises(ValueError):
            self.field.evaluate(scenario(),shape(),0,0,n_q=0)


if __name__=='__main__':
    unittest.main()
