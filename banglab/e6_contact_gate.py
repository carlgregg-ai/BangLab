"""One-shot E6 contact verification. Historical F4 runners are never invoked."""
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import traceback

import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.stats import binom

from .config import Parameter
from .encounter.field import EncounterField, Scenario
from .encounter.geometry import Silhouette
from .encounter import oracle_contact as mc
from .encounter import reference_case6 as variant

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'docs/evidence/e6/contact_oracle'
PLAN_SHA256='b9481db993c05f68ce9dd156f0129e45ae2166727d435d6bb7d22afdc84b2b38'


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path,value):
    with path.open('w',encoding='utf-8',newline='\n') as out:
        json.dump(value,out,indent=2,ensure_ascii=False,allow_nan=False)
        out.write('\n')


def verify_preflight(directory):
    plan=read_json(directory/'plan.json')
    if digest(directory/'plan.json')!=PLAN_SHA256:
        raise ValueError('Prospective plan changed.')
    freeze=read_json(directory/'preflight.json')
    if freeze['plan_sha256']!=PLAN_SHA256 or not freeze['software_tests_passed']:
        raise ValueError('Software preflight required.')
    for manifest in (plan['preserved_file_sha256'],freeze['implementation_sha256']):
        for name,expected in manifest.items():
            if digest(ROOT/name)!=expected:
                raise ValueError('Frozen file changed: '+name)
    if digest(ROOT/plan['geometry_path'])!=plan['geometry_sha256']:
        raise ValueError('Frozen geometry changed.')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if head!=plan['head']:
        raise ValueError('Repository checkpoint changed.')
    return plan,freeze


def compare(successes,samples,reference,slack):
    if not 0<=successes<=samples or samples<=0 or not 0<=reference<=1:
        raise ValueError('Invalid probability comparison.')
    p_hat=successes/samples
    se=math.sqrt(p_hat*(1-p_hat)/samples)
    difference=abs(p_hat-reference)
    limit=4*se+slack
    return {'successes':successes,'M':samples,'p_hat':p_hat,'reference':reference,
            'SE':se,'absolute_difference':difference,'limit':limit,'pass':difference<=limit}


def scenario(r,v):
    make=lambda value,unit:Parameter(value,unit,'USER_INPUT','Frozen E6 verification plan')
    return Scenario(make(r,'m'),make(v,'m/s'),make(0,'deg'))


def reference_inputs(field,case):
    """Load shared declared inputs; MC never receives an integrated probability."""
    duration=field.duration(case['range_m'])
    calibration=[]
    if case['case']==6:
        sigma,calibration=variant.calibrate(case['range_m'],field.lateral.ranges_m,
                                           field.lateral.fractions,field.lateral.radius.value)
        kappa,tail=.4,.1
    else:
        sigma=field.lateral.scale(case['range_m']).sigma.value
        kappa,tail=0.,0.
    spec=mc.ContactInputs(**{key:case[key] for key in (
        'a_m','b_m','pellet_radius_m','psi_deg','travel_direction_deg',
        'e_a_m','e_c_m','speed_m_s')},duration_s=duration,sigma_m=sigma,
        kappa=kappa,tail_probability=tail)
    if case['case']==6:
        pi=variant.probability(spec)
        route='ISOLATED_D008_DETERMINISTIC_REFERENCE'
    else:
        param=lambda value,unit:Parameter(value,unit,'USER_INPUT','Frozen D-012/D-013 E6 geometry')
        silhouette=Silhouette(param(case['a_m'],'m'),param(case['b_m'],'m'),
                              param(case['psi_deg'],'deg'),field.pellet_radius)
        if case['travel_direction_deg']!=0:
            raise ValueError('Frozen six-case frame is +x.')
        pi=field.evaluate(scenario(case['range_m'],case['speed_m_s']),silhouette,
                          case['e_a_m'],case['e_c_m'],n_q=64,n_x=48).pi
        route='FROZEN_E5_ENCOUNTER_FIELD'
    return spec,pi,route,calibration


def f4_regression(field,plan):
    """Non-dispersion reviewer regressions only; no historical F4 rerun."""
    rows=[]
    shape=Silhouette.face_on(field.pellet_radius)
    def en(r,v,x):
        return field.evaluate(scenario(r,v),shape,x,0).expected_contacts
    for name,speed in [('static_EN',0),('moving_20m_s_peak_EN',20)]:
        for r,target in plan['F4_regression'][name].items():
            actual=en(float(r),speed,0.)
            tolerance=plan['acceptance']['F4_EN_absolute']
            rows.append({'quantity':name,'range_m':float(r),'speed_m_s':speed,
                         'target':target,'calculated':actual,'tolerance':tolerance,
                         'absolute_difference':abs(actual-target),'pass':abs(actual-target)<=tolerance})
    for item in plan['F4_regression']['FWHM_along_m']:
        r,v=item['range_m'],item['speed_m_s']
        half=en(r,v,0.)/2
        width=2*brentq(lambda x:en(r,v,x)-half,0.,.6,xtol=.0001)
        target=item['target']; tolerance=plan['acceptance']['F4_FWHM_m_absolute']
        rows.append({'quantity':'FWHM_along_m','range_m':r,'speed_m_s':v,
                     'target':target,'calculated':width,'tolerance':tolerance,
                     'absolute_difference':abs(width-target),'pass':abs(width-target)<=tolerance})
    return rows


def run_once(directory=EVIDENCE):
    """Reserve first, persist partial evidence, refuse every second execution."""
    path=directory/'receipt.json'
    # Intentionally outside the try block: an existing record is never replaced.
    with path.open('x',encoding='utf-8',newline='\n') as out:
        record={'record_kind':'FIRST_E6_CONTACT_ORACLE_EVALUATION_NOT_E8',
                'started_utc':now(),'status':'RESERVED','results':[],
                'F4_non_dispersion_regression':[], 'E7_started':False,'E8_started':False,
                'E3_scientific_rerun':False,'F4_v1_v2_scientific_rerun':False}
        json.dump(record,out,indent=2);out.write('\n')
    try:
        plan,freeze=verify_preflight(directory)
        record.update(plan_sha256=PLAN_SHA256,preflight_sha256=digest(directory/'preflight.json'),
                      geometry_sha256=plan['geometry_sha256'],
                      versions={'python':platform.python_version(),'numpy':np.__version__,
                                'scipy':scipy.__version__,'head':plan['head']},
                      claims_allowed=[],interpretation=plan['interpretation'])
        field=EncounterField.from_repository(ROOT)
        for case in plan['cases']:
            number=case['case']
            record.update(status='RUNNING',active_case=number)
            write_json(path,record)
            spec,pi,route,calibration=reference_inputs(field,case)
            # Preserve the deterministic reference before the stochastic draws.
            row={'case':number,'geometry':case,'inputs_SI':asdict(spec),
                 'deterministic_route':route,'pi':pi,'variant_calibration':calibration,
                 'status':'REFERENCE_RECORDED_BEFORE_MC'}
            record['results'].append(row)
            write_json(path,record)
            sampled=mc.simulate(spec,seed=plan['seeds'][str(number)],
                                single_pellets=plan['single_pellets_per_case'],
                                rounds=plan['rounds_per_case'],pellets_per_round=plan['pellets_per_round'],
                                single_block=plan['draw_order']['single_block_pellets'],
                                round_block=plan['draw_order']['round_block_rounds'])
            row['sampling']=sampled
            row['single']=compare(sampled['single_contacts'],sampled['single_pellets'],pi,0.)
            row['round_tails']={str(k):compare(sum(sampled['round_count_histogram'][k:]),
                                              sampled['rounds'],float(binom.sf(k-1,192,pi)),.001)
                                for k in plan['k']}
            passed=row['single']['pass'] and all(value['pass'] for value in row['round_tails'].values())
            row['status']='PASS' if passed else 'FAIL'
            write_json(path,record)
            print('E6 case',number,row['status'],flush=True)
            if not passed:
                record.update(status='SCIENTIFIC_FAIL',verdict='FAIL',completed_utc=now())
                write_json(path,record)
                return record
        record['F4_non_dispersion_regression']=f4_regression(field,plan)
        passed=all(row['pass'] for row in record['F4_non_dispersion_regression'])
        record.update(status='COMPLETE' if passed else 'SCIENTIFIC_FAIL',
                      verdict='PASS' if passed else 'FAIL',completed_utc=now())
        if passed:
            record['claims_allowed']=[plan['claim_ceiling']]
        record['historical_F4_note']='D-009/D-010 FAIL/FAIL immutable; D-011/F4-v2 preserved; neither rerun.'
        write_json(path,record)
    except Exception as error:
        record.update(status='IMPLEMENTATION_FAILURE',verdict='STOP',completed_utc=now(),
                      error_type=type(error).__name__,error=str(error),traceback=traceback.format_exc())
        write_json(path,record)
    return record


if __name__=='__main__':
    result=run_once()
    print(result['status'],result.get('verdict'),flush=True)
    raise SystemExit(0 if result.get('verdict')=='PASS' else 1)
