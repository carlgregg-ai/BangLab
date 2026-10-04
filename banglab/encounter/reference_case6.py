"""D-008 isolated deterministic reference, never an E5 baseline change.

Only the kappa=.4 / 10% tail verification variant is supported. The two
sigma_bar anchors preserve p.82 marginal circle fractions; their straight
line inherits the contract range law. These assumptions are not measurements.
No Monte Carlo calculation calls this module.
"""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.stats import ncx2


def tail_nodes():
    x,w=np.polynomial.legendre.leggauss(64)
    q=(x+1)/2
    return np.concatenate((q,q+1)),np.concatenate((.9*w/2,.1*w/2))


def marginal_fraction(sigma_bar,radius_m):
    q,w=tail_nodes()
    sigma=sigma_bar*(1+.4*(q-.5))
    return float(w@(-np.expm1(-.5*(radius_m/sigma)**2)))


def fit_anchor(fraction,radius_m):
    if not 0<fraction<1 or not radius_m>0:
        raise ValueError('Positive radius and interior circle fraction required.')
    uncoupled=radius_m/math.sqrt(-2*math.log1p(-fraction))
    # For q in [0,2], the conditional multiplier spans [.8,1.6].
    # Monotonicity supplies the bracket, independent of any oracle outcome.
    return float(brentq(lambda s:marginal_fraction(s,radius_m)-fraction,
                        uncoupled/1.6,uncoupled/.8,xtol=1e-14,rtol=1e-14))


def calibrate(range_m,ranges_m,fractions,radius_m):
    if len(ranges_m)!=2 or len(fractions)!=2 or ranges_m[1]<=ranges_m[0]:
        raise ValueError('Two ordered calibration anchors required.')
    anchors=[fit_anchor(p,radius_m) for p in fractions]
    sigma=anchors[0]+(anchors[1]-anchors[0])*(range_m-ranges_m[0])/(ranges_m[1]-ranges_m[0])
    if sigma<=0:
        raise ValueError('Nonpositive interpolated variant scale.')
    return float(sigma),[{'range_m':r,'fraction':p,'sigma_bar_m':s,
                         'reproduced_fraction':marginal_fraction(s,radius_m)}
                        for r,p,s in zip(ranges_m,fractions,anchors)]


def probability(spec):
    if spec.a_m!=spec.b_m or spec.kappa!=.4 or spec.tail_probability!=.1:
        raise ValueError('Only the isolated D-008 circular coupled/tail variant is supported.')
    q,w=tail_nodes()
    sigma=spec.sigma_m*(1+.4*(q-.5))
    # Isotropy permits travel-frame coordinates for a circle.
    along=spec.speed_m_s*spec.duration_s*(q-.5)-spec.e_a_m
    cross=-spec.e_c_m
    radius=spec.a_m+spec.pellet_radius_m
    mass=ncx2.cdf((radius/sigma)**2,2,(along*along+cross*cross)/sigma**2)
    value=float(w@mass)
    if not 0<=value<=1:
        raise ArithmeticError('Invalid variant probability; no clipping.')
    return value
