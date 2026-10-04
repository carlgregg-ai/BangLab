"""E6 F4 dispersion prerequisite only, D-009/D-010.

This is a bootstrap of physical pattern counts, not the independent
pellet-contact Monte Carlo oracle. No encounter oracle is implemented here.
"""
import numpy as np


def sample_dispersion(counts):
    """Return sample variance / mean; preserve the prospective ddof=1 rule."""
    x=np.asarray(counts)
    if x.shape!=(10,) or x.dtype.kind not in 'iu' or np.any(x<0) or x.mean()<=0:
        raise ValueError('Ten nonnegative integer shot counts with positive mean required.')
    return float(np.var(x,ddof=1)/np.mean(x))


def bootstrap_dispersion(counts,*,seed,replicates):
    """D-010 ordinary bootstrap, explicit seed/B, linear percentile interval.

    Returns full-precision descriptive results; target decisions are made
    separately against the predeclared plan, never inside the estimator.
    """
    estimate=sample_dispersion(counts)
    if type(seed) is not int or seed<0 or type(replicates) is not int or replicates<2:
        raise ValueError('Explicit nonnegative integer seed and replicate count >=2 required.')
    x=np.asarray(counts)
    rng=np.random.Generator(np.random.PCG64(seed))
    samples=x[rng.integers(0,10,size=(replicates,10))]
    means=np.mean(samples,axis=1)
    if np.any(means==0):
        raise ValueError('Zero-mean bootstrap replicate: D undefined; no silent exclusion.')
    values=np.var(samples,axis=1,ddof=1)/means
    bounds=np.quantile(values,[0.025,0.975],method='linear')
    return {'mean':float(np.mean(x)),'sample_variance':float(np.var(x,ddof=1)),
            'D':estimate,'ci_95':[float(v) for v in bounds]}
