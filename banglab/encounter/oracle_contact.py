"""Independent direct E6 sampling, separate from historical F4 oracles.

All inputs are explicit SI scalars supplied from the frozen verification plan.
Gaussian shape and conditional independence are assumptions, not validations.
This module imports no deterministic geometry, quadrature or encounter field.
"""
from dataclasses import dataclass, fields
import math
import numpy as np


@dataclass(frozen=True)
class ContactInputs:
    a_m: float
    b_m: float
    pellet_radius_m: float
    psi_deg: float
    travel_direction_deg: float
    e_a_m: float
    e_c_m: float
    speed_m_s: float
    duration_s: float
    sigma_m: float
    kappa: float
    tail_probability: float

    def __post_init__(self):
        for field in fields(self):
            value=getattr(self,field.name)
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
                raise ValueError('Finite explicit SI scalar required: '+field.name)
        if min(self.a_m,self.b_m,self.pellet_radius_m,self.duration_s,self.sigma_m)<=0:
            raise ValueError('Positive dimensions, duration and spread required.')
        if self.speed_m_s<0 or not 0<=self.tail_probability<1 or not 0<=self.kappa<2:
            raise ValueError('Invalid speed, tail fraction or coupling.')


def arrival(u,tail_probability):
    """Inverse CDF; tail probability is fixed by the declared model."""
    if tail_probability==0:
        return u
    return np.where(u<1-tail_probability,u/(1-tail_probability),
                    1+(u-(1-tail_probability))/tail_probability)


def direct_contacts(spec,q,xy):
    """Brute-force pellet centres in the moving, rotated, dilated ellipse."""
    direction=math.radians(spec.travel_direction_deg)
    ux,uy=math.cos(direction),math.sin(direction)
    ex=spec.e_a_m*ux-spec.e_c_m*uy
    ey=spec.e_a_m*uy+spec.e_c_m*ux
    movement=spec.speed_m_s*spec.duration_s*(q-.5)
    x=xy[:,0]-(movement*ux-ex)
    y=xy[:,1]-(movement*uy-ey)
    psi=math.radians(spec.psi_deg)
    local_x=math.cos(psi)*x+math.sin(psi)*y
    local_y=-math.sin(psi)*x+math.cos(psi)*y
    return ((local_x/(spec.a_m+spec.pellet_radius_m))**2+
            (local_y/(spec.b_m+spec.pellet_radius_m))**2)<=1+1e-12


def draw_contacts(spec,rng,n):
    q=arrival(rng.random(n),spec.tail_probability)
    scale=spec.sigma_m*(1+spec.kappa*(q-.5))
    points=rng.standard_normal((n,2))*scale[:,None]
    return direct_contacts(spec,q,points)


def simulate(spec,*,seed,single_pellets,rounds,pellets_per_round,single_block,round_block):
    """Disjoint pellet and round experiments; preserve integer sufficient counts.

    Round probabilities come from grouping direct pellet contacts, never from
    drawing a Binomial with the deterministic reference probability.
    """
    if not isinstance(spec,ContactInputs):
        raise ValueError('Explicit ContactInputs required.')
    for name,value in [('seed',seed),('single_pellets',single_pellets),('rounds',rounds),
                        ('pellets_per_round',pellets_per_round),('single_block',single_block),
                        ('round_block',round_block)]:
        if type(value) is not int or value<(0 if name=='seed' else 1):
            raise ValueError('Invalid integer '+name)
    rng=np.random.Generator(np.random.PCG64(seed))
    initial_state=rng.bit_generator.state
    hits=0
    for start in range(0,single_pellets,single_block):
        hits+=int(np.count_nonzero(draw_contacts(spec,rng,min(single_block,single_pellets-start))))
    histogram=np.zeros(pellets_per_round+1,dtype=np.int64)
    for start in range(0,rounds,round_block):
        n=min(round_block,rounds-start)
        contacts=draw_contacts(spec,rng,n*pellets_per_round)
        counts=contacts.reshape(n,pellets_per_round).sum(axis=1)
        histogram+=np.bincount(counts,minlength=pellets_per_round+1)
    return {'seed':seed,'generator':'PCG64','single_pellets':single_pellets,
            'rounds':rounds,'pellets_per_round':pellets_per_round,
            'single_contacts':hits,'round_count_histogram':histogram.tolist(),
            'initial_rng_state':initial_state,'final_rng_state':rng.bit_generator.state}
