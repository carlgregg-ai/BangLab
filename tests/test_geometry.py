"""E5 deterministic geometry tests; no physical-validation claim."""
import unittest
import numpy as np
from banglab.config import Parameter
from banglab.encounter.geometry import Silhouette, gaussian_mass


def shape(a=0.055, b=0.055, psi=0):
    return Silhouette(Parameter(a,'m','USER_INPUT','E5 declared test silhouette'),
                      Parameter(b,'m','USER_INPUT','E5 declared test silhouette'),
                      Parameter(psi,'deg','USER_INPUT','E5 declared test orientation'),
                      Parameter(0.001575,'m','SOURCE_DERIVED','DEP p.75 diameter / 2'))


class GeometryTests(unittest.TestCase):
    def test_dilation_defaults_units_and_boundary(self):
        s=Silhouette.face_on(shape().pellet_radius)
        self.assertEqual(s.a.label,'ASSUMED')
        self.assertEqual(s.A,0.056575)
        self.assertTrue(s.contains(s.A,0))
        self.assertTrue(s.contains(s.A*(1+2e-13),0))
        self.assertFalse(s.contains(s.A*(1+1e-8),0))
        self.assertEqual(s.area,np.pi*s.A*s.B)

    def test_ellipse_vs_ncx2_contract_tolerance(self):
        for sigma in (0.1,0.16,0.23,0.33):
            for radius in (0.0125,0.055):
                s=shape(radius,radius)
                for x,y in ((0,0),(0.05,0.1),(0.3,-0.2),(0.6,0.6)):
                    reference=gaussian_mass(s,sigma,x,y,method='circle')
                    numerical=gaussian_mass(s,sigma,x,y,method='ellipse')
                    if reference>1e-8:
                        self.assertLessEqual(abs(numerical/reference-1),1e-6)

    def test_area_density_small_target_limit(self):
        for s in (shape(),shape(b=0.0125,psi=30)):
            sigma=100*s.a.value
            g=gaussian_mass(s,sigma,0,0,method='ellipse')
            approximation=s.area/(2*np.pi*sigma*sigma)
            self.assertLessEqual(abs(g/approximation-1),1e-3)

    def test_rotation_covariance_and_joint_inversion(self):
        s=shape(b=0.0125,psi=37)
        angle=np.deg2rad(37)
        x,y=0.13,-0.09
        local=(np.cos(angle)*x+np.sin(angle)*y,-np.sin(angle)*x+np.cos(angle)*y)
        g=gaussian_mass(s,0.2,x,y)
        self.assertAlmostEqual(g,gaussian_mass(shape(b=0.0125),0.2,*local),places=14)
        self.assertAlmostEqual(g,gaussian_mass(s,0.2,-x,-y),places=14)

    def test_circle_orientation_independence(self):
        self.assertEqual(gaussian_mass(shape(),0.2,0.1,0.2),
                         gaussian_mass(shape(psi=71),0.2,0.1,0.2))

    def test_centred_monotonic_and_far_offset(self):
        values=[gaussian_mass(shape(),0.2,x,0) for x in (0,0.1,0.3,1,3)]
        self.assertTrue(all(a>b for a,b in zip(values,values[1:])))
        self.assertLess(values[-1],1e-40)

    def test_ellipse_node_doubling(self):
        for s in (shape(),shape(b=0.0125,psi=30),shape(b=0.03,psi=90)):
            for x,y in ((0,0),(0.2,0.1),(0.6,-0.6)):
                a=gaussian_mass(s,0.11,x,y,n_x=48,method='ellipse')
                b=gaussian_mass(s,0.11,x,y,n_x=96,method='ellipse')
                self.assertLess(abs(a/b-1),1e-6)

    def test_invalid_inputs_and_units(self):
        with self.assertRaises(ValueError):
            shape(a=0)
        with self.assertRaises(ValueError):
            Silhouette(Parameter(55,'mm','USER_INPUT','test'),shape().b,shape().psi,shape().pellet_radius)
        for bad in (0,-1,float('nan'),True):
            with self.assertRaises(ValueError):
                gaussian_mass(shape(),bad,0,0)
        with self.assertRaises(ValueError):
            gaussian_mass(shape(b=0.01),0.2,0,0,method='circle')
        with self.assertRaises(ValueError):
            gaussian_mass(shape(),0.2,0,0,n_x=True)


if __name__=='__main__':
    unittest.main()
