"""E5 pellet-dilated silhouette and Gaussian mass, contract 8.2.6-7/A10.

Coordinates are metres in the plane normal to fire. psi is counterclockwise
from +x to the a principal axis, in degrees. This is a declared simplified
silhouette, not fracture geometry. Dilation (a+rp,b+rp) is the contract's
approximation to the offset ellipse; it is exact for a circle.
"""
from dataclasses import dataclass
from functools import lru_cache
import math
import numpy as np
from scipy.special import ndtr
from scipy.stats import ncx2
from ..config import Parameter
from .lateral import finite, positive


def require_parameter(p,unit):
    if not isinstance(p,Parameter) or p.unit!=unit:
        raise ValueError('Explicit Parameter with unit '+unit+' required.')
    return finite(p.value)


@lru_cache(maxsize=16)
def quadrature(n):
    if type(n) is not int or n<=0:
        raise ValueError('Positive integer node count required.')
    x,w=np.polynomial.legendre.leggauss(n)
    x.setflags(write=False)
    w.setflags(write=False)
    return x,w


@dataclass(frozen=True)
class Silhouette:
    a: Parameter
    b: Parameter
    psi: Parameter
    pellet_radius: Parameter

    def __post_init__(self):
        for p in (self.a,self.b,self.pellet_radius):
            positive(require_parameter(p,'m'))
        require_parameter(self.psi,'deg')
        if self.a.label not in ('USER_INPUT','ASSUMED') or self.b.label not in ('USER_INPUT','ASSUMED'):
            raise ValueError('Declared or assumed silhouette required.')

    @classmethod
    def face_on(cls,pellet_radius):
        locator='Contract 8.2.6 face-on default (ASSUMED)'
        return cls(Parameter(0.055,'m','ASSUMED',locator),
                   Parameter(0.055,'m','ASSUMED',locator),
                   Parameter(0,'deg','ASSUMED',locator),pellet_radius)

    @property
    def A(self):
        return float(self.a.value)+float(self.pellet_radius.value)

    @property
    def B(self):
        return float(self.b.value)+float(self.pellet_radius.value)

    @property
    def area(self):
        return math.pi*self.A*self.B

    def local(self,x,y):
        angle=math.radians(float(self.psi.value))
        c,s=math.cos(angle),math.sin(angle)
        return c*x+s*y,-s*x+c*y

    def contains(self,x_m,y_m):
        """Pellet centre relative to clay centre; closed set, A10 tolerance."""
        x,y=self.local(finite(x_m),finite(y_m))
        return (x/self.A)**2+(y/self.B)**2 <= 1+1e-12


def gaussian_mass(silhouette,sigma_m,cx_m,cy_m,*,n_x=48,method='auto'):
    """Probability mass in translated silhouette. Scalar or broadcast centres.

    cx/cy describe clay centre relative to Gaussian centre. Circle uses ncx2;
    method='ellipse' forces the independent 48-node Gaussian/CDF quadrature.
    """
    if not isinstance(silhouette,Silhouette):
        raise ValueError('Declared Silhouette required.')
    sigma=positive(sigma_m)
    nodes,weights=quadrature(n_x)
    x,y=np.asarray(cx_m),np.asarray(cy_m)
    if any(v.dtype.kind not in 'iuf' or not np.all(np.isfinite(v)) for v in (x,y)):
        raise ValueError('Finite numerical metre offsets required.')
    x,y=np.broadcast_arrays(x,y)
    A,B=silhouette.A,silhouette.B
    if method not in ('auto','circle','ellipse'):
        raise ValueError('Unknown integration method.')
    if method=='circle' and A!=B:
        raise ValueError('Circle reference requires equal axes.')
    if method=='circle' or (method=='auto' and A==B):
        value=ncx2.cdf((A/sigma)**2,2,(x*x+y*y)/(sigma*sigma))
    else:
        cx,cy=silhouette.local(x,y)
        theta=nodes*math.pi/2
        xx=A*np.sin(theta)
        half_y=B*np.cos(theta)
        upper=(cy[...,None]+half_y)/sigma
        lower=(cy[...,None]-half_y)/sigma
        # Reflect positive-tail CDF differences to avoid cancellation near 1.
        interval=np.where(lower>0,ndtr(-lower)-ndtr(-upper),ndtr(upper)-ndtr(lower))
        density_x=np.exp(-0.5*((cx[...,None]+xx)/sigma)**2)/(sigma*math.sqrt(2*math.pi))
        value=np.sum(weights*(math.pi/2)*A*np.cos(theta)*density_x*interval,axis=-1)
    return float(value) if np.ndim(value)==0 else value
