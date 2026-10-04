"""D-011 count-dispersion null test, independent of the contact oracle.

New prospective methodology, not recovery of the historical CI method.
No historical target or interval participates in the decision.
"""
import numpy as np


def dispersion_rows(counts):
    """Ten integer counts per row; never discard an undefined experiment."""
    x = np.asarray(counts)
    if (x.ndim != 2 or x.shape[1] != 10 or len(x) == 0
            or x.dtype.kind not in 'iu' or np.any(x < 0) or np.any(x > 192)):
        raise ValueError('Rows of ten integer counts in [0,192] required.')
    means = np.mean(x, axis=1)
    denominators = means * (1-means/192)
    if np.any(denominators <= 0):
        raise ValueError('Undefined binomial denominator: STOP; no exclusion or redraw.')
    return np.var(x, axis=1, ddof=1) / denominators


def observed_statistic(counts):
    x = np.asarray(counts)
    if x.shape != (10,):
        raise ValueError('Exactly ten physical pattern counts required.')
    d = float(dispersion_rows(x[None,:])[0])
    mean = float(np.mean(x))
    return {'mean':mean, 'p_hat':mean/192,
            'sample_variance':float(np.var(x,ddof=1)),
            'binomial_variance':mean*(1-mean/192), 'D':d}


def summarize_null(observed_d, simulated_d):
    """Upper-tail +1 p-value and a descriptive NULL REFERENCE INTERVAL."""
    values = np.asarray(simulated_d)
    if (values.ndim != 1 or len(values) < 2 or not np.all(np.isfinite(values))
            or np.any(values < 0) or not np.isfinite(observed_d) or observed_d < 0):
        raise ValueError('Finite nonnegative statistics required.')
    count = int(np.count_nonzero(values >= observed_d))
    p = (1+count)/(len(values)+1)
    bounds = np.percentile(values, [2.5,97.5], method='linear')
    return {'B':len(values), 'upper_tail_count':count, 'p_MC':p,
            'alpha':0.05, 'evidence_of_overdispersion':p < 0.05,
            'null_reference_interval_95':[float(v) for v in bounds],
            'percentile_method':'linear'}


def null_test(counts, *, seed, experiments):
    """Draw once at fixed observed p; refit the denominator per experiment."""
    if (type(seed) is not int or seed < 0 or type(experiments) is not int
            or experiments < 2):
        raise ValueError('Explicit integer seed >=0 and experiments >=2 required.')
    observed = observed_statistic(counts)
    rng = np.random.Generator(np.random.PCG64(seed))
    samples = rng.binomial(192, observed['p_hat'], size=(experiments,10))
    simulated_d = dispersion_rows(samples)
    return {**observed, **summarize_null(observed['D'], simulated_d), 'seed':seed}
