"""E5 deterministic baseline field; no oracle, sensitivity or release outputs.

Frame: fixed x/y metre axes normal to fire; direction is counterclockwise
from +x. u=(cos(direction),sin(direction)); u_perp=(-u_y,u_x).
Aim offset e is pattern centre minus clay centre at mid-string. Positive
along-track e dot u is more lead. c(q;e)=v*duration*(q-1/2)*u-e.
Zero offset places the clay centre at the pattern centre at mid-string.

h(q)=1 on [0,1], all 192 pellets in the main string, longitudinal/lateral
factorisation and conditional independence are ASSUMED. Output is an
expectation under those assumptions, not an actual impact or damage count.
"""
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.stats import binom
from ..config import Parameter, validate_fixture
from ..fixtures import load_dev_longitudinal, LOCKED_RANGES_M
from ..units import convert
from .longitudinal import LongitudinalModel
from .lateral import LateralModel, finite
from .geometry import Silhouette, gaussian_mass, quadrature, require_parameter


@dataclass(frozen=True)
class Scenario:
    range: Parameter
    speed: Parameter
    direction: Parameter

    def __post_init__(self):
        if not 20<=require_parameter(self.range,'m')<=50:
            raise ValueError('Domain is 20-50 m.')
        if require_parameter(self.speed,'m/s')<0:
            raise ValueError('Nonnegative crossing speed required.')
        require_parameter(self.direction,'deg')
        if any(p.label!='USER_INPUT' for p in (self.range,self.speed,self.direction)):
            raise ValueError('Scenario parameters must be USER_INPUT.')


@dataclass(frozen=True)
class EncounterResult:
    pi: float
    expected_contacts: float
    count_pmf: tuple
    flags: frozenset
    role: str = 'GEOMETRIC_CONTACT'
    label: str = 'MODEL_PREDICTION'
    assumptions: tuple = ('uniform arrival','all 192 in main string','Gaussian lateral shape',
                          'centred pattern calibration','linear sigma law',
                          'longitudinal/lateral factorisation','conditional independence',
                          'pellet-dilated ellipse approximation')


class EncounterField:
    @classmethod
    def from_repository(cls,root):
        """Consume frozen models and saved PASS receipts; never execute E3.

        At 25/35/45 m use the already recorded predicted duration, not the
        held-out observations. E4 parameters are loaded, not refitted.
        """
        root=Path(root)
        read=lambda name: json.loads((root/name).read_text(encoding='utf-8'))
        e1,e3,e4=read('receipt.json'),read('docs/evidence/e3/receipt.json'),read('docs/evidence/e4/receipt.json')
        ledger=e3['v7_ledger']
        if ledger['status']!='COMPLETE' or ledger['verdict']!='PASS' or ledger['post_hoc_changes']:
            raise ValueError('Unchanged completed E3 PASS required by this field.')
        if [(g['id'],g['verdict']) for g in e4['gates']] != [('E4','PASS')]:
            raise ValueError('E4 PASS required.')
        for source in (e3['model_source_sha256'],e4['implementation_sha256']):
            for name,expected in source.items():
                if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:
                    raise ValueError('Historical implementation changed: '+name)
        for name,expected in e1['hashes'].items():
            if hashlib.sha256((root/'data/fixtures'/f'{name}.json').read_bytes()).hexdigest()!=expected:
                raise ValueError('Canonical fixture changed.')
            if e3['hashes'][name]!=expected or e4['hashes'][name]!=expected:
                raise ValueError('Historical fixture hash disagreement.')
        encoded=json.dumps(ledger['predictions_ms'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()
        if hashlib.sha256(encoded).hexdigest()!=ledger['predictions_sha256']:
            raise ValueError('Saved predictions changed.')
        load=read('data/fixtures/dep_load.json')
        validate_fixture(load)
        self=cls()
        self.longitudinal=LongitudinalModel(load_dev_longitudinal(root/'data/fixtures/dep_b1.json',e1['hashes']['dep_b1']))
        self._locked_duration={int(r):float(convert(row['delta_t'],'ms','s')) for r,row in ledger['predictions_ms'].items()}
        self.pellet_radius=Parameter(float(convert(load['load']['pellet_diameter_mm'],'mm','m')/2),
                                     'm','SOURCE_DERIVED','DEP App. B p.75 diameter / 2')
        count=Parameter(load['load']['pellet_count'],'count','MEASURED_PRIMARY','DEP App. B p.75')
        calibration=e4['calibration']
        self.lateral=LateralModel(tuple(row['range_m'] for row in calibration),
                                  tuple(row['fraction'] for row in calibration),
                                  tuple(Parameter(**row['sigma']) for row in calibration),
                                  Parameter(**e4['radius']),count,
                                  Parameter(**e4['proportional_variant']['k']),e1['hashes']['dep_p82'])
        return self

    def duration(self,range_m):
        r=finite(range_m)
        if not 20<=r<=50:
            raise ValueError('Domain is 20-50 m.')
        if r in LOCKED_RANGES_M:
            return self._locked_duration[r]
        return self.longitudinal.delta_t(r)

    def clay_centre(self,scenario,q,e_x_m,e_y_m):
        if not isinstance(scenario,Scenario):
            raise ValueError('Explicit Scenario required.')
        x,y=finite(e_x_m),finite(e_y_m)
        angle=math.radians(float(scenario.direction.value))
        q=np.asarray(q)
        if q.dtype.kind not in 'iuf' or not np.all(np.isfinite(q)) or np.any((q<0)|(q>1)):
            raise ValueError('Uniform-arrival coordinate q must lie in [0,1].')
        displacement=float(scenario.speed.value)*self.duration(scenario.range.value)*(q-0.5)
        return displacement*math.cos(angle)-x,displacement*math.sin(angle)-y

    def evaluate(self,scenario,silhouette,e_x_m,e_y_m,*,n_q=64,n_x=48,method='auto'):
        """Aim offset in metres; pi is per-pellet geometric contact probability."""
        if not isinstance(silhouette,Silhouette) or silhouette.pellet_radius.value!=self.pellet_radius.value:
            raise ValueError('Silhouette must use the DEP pellet radius.')
        nodes,weights=quadrature(n_q)
        q=(nodes+1)/2
        cx,cy=self.clay_centre(scenario,q,e_x_m,e_y_m)
        scale=self.lateral.scale(scenario.range.value)
        mass=gaussian_mass(silhouette,scale.sigma.value,cx,cy,n_x=n_x,method=method)
        probability=float(np.dot(weights/2,mass))
        if not 0<=probability<=1:
            raise ArithmeticError('Invalid integrated contact probability; no clipping.')
        count=int(self.lateral.pellet_count.value)
        pmf=tuple(float(p) for p in binom.pmf(np.arange(count+1),count,probability))
        return EncounterResult(probability,count*probability,pmf,scale.flags)

    def at_clay_offset(self,scenario,silhouette,clay_x_m,clay_y_m,**settings):
        """Clay centre relative to field at mid-string; equivalent to e=-c."""
        return self.evaluate(scenario,silhouette,-finite(clay_x_m),-finite(clay_y_m),**settings)

    def grid(self,scenario,silhouette,e_x_m,e_y_m):
        """Minimal grid of expected contacts, shape (len(y),len(x)); no plotting."""
        return np.array([[self.evaluate(scenario,silhouette,x,y).expected_contacts
                          for x in e_x_m] for y in e_y_m])
