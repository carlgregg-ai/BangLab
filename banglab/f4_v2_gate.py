"""Explicit one-shot D-011 runner. Import/test discovery never evaluates it."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform

import numpy as np
from .encounter import oracle_f4_v2

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/evidence/f4_v2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def verify_preflight(directory):
    plan_path = directory/'plan.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    freeze = json.loads((directory/'preflight.json').read_text(encoding='utf-8'))
    if digest(plan_path) != freeze['plan_sha256']:
        raise ValueError('Predeclared plan changed.')
    for name, expected in freeze['implementation_sha256'].items():
        if digest(ROOT/name) != expected:
            raise ValueError(f'Preflight implementation changed: {name}')
    for name, expected in plan['preserved_file_sha256'].items():
        if name not in plan['allowed_existing_file_changes'] and digest(ROOT/name) != expected:
            raise ValueError(f'Historical file changed: {name}')
    if (plan['B'],plan['n'],plan['pellets'],plan['variance_ddof'],plan['alpha']) != (1000000,10,192,1,0.05):
        raise ValueError('D-011 constants changed.')
    expected_groups = [dict(range_yd=30,refs=list(range(1,11)),seed=30192),
                       dict(range_yd=40,refs=list(range(11,21)),seed=40192)]
    if plan['groups'] != expected_groups:
        raise ValueError('D-011 groups changed.')
    return plan,freeze


def run_once(directory=EVIDENCE):
    """Exclusive receipt reservation precedes source reads and all arithmetic.

    A partial/failed receipt also blocks rerun. Each completed range is persisted
    immediately; an exception leaves a STOP receipt with prior results intact.
    """
    directory = Path(directory)
    receipt_path = directory/'receipt.json'
    # Exclusive creation also rejects a previous incomplete attempt.
    with receipt_path.open('x', encoding='utf-8', newline='\n') as handle:
        record = {'record_kind':'D-011_F4-v2_FIRST_NULL_TEST_NOT_E8',
                  'status':'RUNNING', 'started_utc':now(), 'results':[],
                  'historical_E6_verdict':'FAIL_UNCHANGED',
                  'method_status':'NEW_PROSPECTIVE_NOT_RECOVERED_HISTORICAL',
                  'remaining_E6_contact_oracle_run':False, 'E7_started':False,
                  'E8_started':False, 'historical_CI_acceptance':False}

        def persist():
            handle.seek(0)
            json.dump(record,handle,indent=2,allow_nan=False)
            handle.write('\n')
            handle.truncate()
            handle.flush()
            os.fsync(handle.fileno())

        persist()
        try:
            plan,freeze = verify_preflight(directory)
            record.update(plan_sha256=digest(directory/'plan.json'),
                          preflight_sha256=digest(directory/'preflight.json'),
                          starting_commit=plan['starting_commit'],
                          environment={'python':platform.python_version(),'numpy':np.__version__},
                          implementation_sha256=freeze['implementation_sha256'],
                          input_fixture_sha256=digest(ROOT/'data/fixtures/dep_p82.json'),
                          interval_label='NULL REFERENCE INTERVAL; not a CI for physical D')
            fixture = json.loads((ROOT/'data/fixtures/dep_p82.json').read_text(encoding='utf-8'))
            if fixture['average_pellets_per_cartridge'] != 192:
                raise ValueError('Nominal count mismatch.')
            persist()
            for group in plan['groups']:
                rows = [r for r in fixture['rows'] if r['range_yd']==group['range_yd']]
                if [r['ref'] for r in rows] != group['refs']:
                    raise ValueError('Canonical reference allocation mismatch.')
                counts = [r['circle_30in'] for r in rows]
                result = oracle_f4_v2.null_test(counts,seed=group['seed'],experiments=plan['B'])
                record['results'].append({**result,'range_yd':group['range_yd'],
                                          'refs':group['refs'],'raw_counts':counts,'saved_utc':now()})
                persist()
            record.update(status='COMPLETE',completed_utc=now(),first_result_preserved=True)
            persist()
        except Exception as error:
            record.update(status='STOP',error=f'{type(error).__name__}: {error}',stopped_utc=now())
            persist()
            raise
    return record


if __name__ == '__main__':
    print(json.dumps(run_once(),indent=2))
