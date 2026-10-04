"""Synthetic checks for the E6 F4 prerequisite; no target-driven fitting."""
import unittest
import numpy as np
from banglab.encounter.oracle import sample_dispersion,bootstrap_dispersion


class DispersionTests(unittest.TestCase):
    def test_sample_variance_convention_on_synthetic_counts(self):
        self.assertAlmostEqual(sample_dispersion(list(range(1,11))),5/3,places=14)
        self.assertEqual(sample_dispersion([7]*10),0)

    def test_seeded_resampling_and_percentiles_against_explicit_order_statistics(self):
        counts=np.arange(1,11)
        actual=bootstrap_dispersion(counts,seed=123,replicates=100)
        again=bootstrap_dispersion(counts,seed=123,replicates=100)
        self.assertEqual(actual,again)
        rng=np.random.Generator(np.random.PCG64(123))
        samples=counts[rng.integers(0,10,size=(100,10))]
        statistics=[]
        for row in samples:
            mean=sum(int(x) for x in row)/10
            variance=sum((int(x)-mean)**2 for x in row)/9
            statistics.append(variance/mean)
        statistics.sort()
        expected=[]
        for p in (0.025,0.975):
            position=99*p; lo=int(position); weight=position-lo
            expected.append(statistics[lo]*(1-weight)+statistics[lo+1]*weight)
        np.testing.assert_allclose(actual['ci_95'],expected,rtol=0,atol=1e-14)

    def test_invalid_counts_and_rng_settings(self):
        for counts in ([1]*9,[1]*11,[0]*10,[-1]*10,[True]*10,[1.5]*10):
            with self.assertRaises(ValueError):
                sample_dispersion(counts)
        for seed,b in ((True,100),(-1,100),(1,0),(1,1),(1,True)):
            with self.assertRaises(ValueError):
                bootstrap_dispersion([1]*10,seed=seed,replicates=b)


if __name__=='__main__':
    unittest.main()
