"""E3 only: durable two-phase evaluation of the immutable E2 predictor.

Ordinary tests inspect the receipt; they never call either evaluation phase.
The private PCHIP objects are used only by this separately authorised gate.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

import numpy as np
import scipy

from .encounter.longitudinal import LongitudinalModel
from .fixtures import DEV_RANGES_M, LOCKED_RANGES_M, load_dev_longitudinal

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'docs/evidence/e3/receipt.json'
FROZEN_SHA = '9c98d3d9be0b2837652153fbc7cad650a5598dc0'
HASHES = {
    'dep_b1': '9ac268e4d96b145b3ef9f82fda71193c43339a103cec4632203f68e3c0ce1e79',
    'dep_p82': '37de300cd68184cc2315b6fffaf4fa04dbe07127a30514e982b538238359dc09',
    'dep_load': '7ddde731928ec2df4f8d4d256a75842181fc5ee54b885fb393b92f1a462c3b1b',
}
CONFIG = {'dev_m': list(DEV_RANGES_M), 'locked_m': list(LOCKED_RANGES_M),
          'method': 'separate frozen E2 PCHIP objects; extrapolate=False',
          'internal_unit': 's', 'comparison_unit': 'ms',
          'comparisons': ['t2', 't3', 'delta_t'], 'tolerance_ms': 1.0}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def persist(file, record):
    file.seek(0)
    file.write(json.dumps(record, indent=2, allow_nan=False) + '\n')
    file.truncate()
    file.flush()
    os.fsync(file.fileno())


def verify_frozen():
    """Check bytes without exposing held-out observations."""
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    if head != FROZEN_SHA:
        raise RuntimeError('STOP: HEAD is not the authorised frozen checkpoint.')
    files = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', FROZEN_SHA, 'banglab'], cwd=ROOT
    ).decode().splitlines()
    code_hashes = {}
    for name in files:
        actual = (ROOT / name).read_bytes()
        committed = subprocess.check_output(['git', 'show', FROZEN_SHA + ':' + name], cwd=ROOT)
        # Git may check out CRLF; require exact logical source and record file bytes.
        if actual.replace(b'\r\n', b'\n') != committed.replace(b'\r\n', b'\n'):
            raise RuntimeError('STOP: frozen source changed: ' + name)
        code_hashes[name] = digest(actual)
    for name, expected in HASHES.items():
        if digest((ROOT / 'data/fixtures' / (name + '.json')).read_bytes()) != expected:
            raise RuntimeError('STOP: canonical fixture changed: ' + name)
    return code_hashes


def freeze_predictions():
    """Reserve the one-shot receipt and persist predictions before opening."""
    if RECEIPT.exists():
        raise RuntimeError('E3 receipt already exists; refusing another evaluation.')
    code_hashes = verify_frozen()
    record = {
        'receipt_kind': 'E3_ONE_SHOT_LOCKED_TIMING',
        'scope': 'E3 only; not the future E8 model-run receipt.',
        'timestamp_utc': timestamp(), 'versions': {'code': FROZEN_SHA, 'spec': 'v1.1', 'contract': 'v0.1'},
        'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__},
        'hashes': {**HASHES, 'config': digest(canonical(CONFIG))},
        'model_source_sha256': code_hashes,
        'runner_sha256': digest(Path(__file__).read_bytes()),
        'config': CONFIG,
        'pre_open': {'clean_working_tree_confirmed_before_E3_machinery': True,
                     'existing_E0_E1_E2_tests': '30 tests PASS',
                     'prior_E3_result_found': False,
                     'integrity_only_access': 'E0/E1 source-integrity checks previously read fixture cells; no locked prediction evaluation.'},
        'split': {'dev_m': list(DEV_RANGES_M), 'locked_m': list(LOCKED_RANGES_M),
                  'locked_read_before_E3': False},
        'prediction_method': 'Construct LongitudinalModel(load_dev_longitudinal(...)) using the frozen DEV-only loader; evaluate its existing _lead and _trail PCHIP objects at 25/35/45 m through this E3-only capability. No alternative predictor, monkeypatch, refit, or E2 edit. Subtract in SI seconds, then multiply by 1000 for ms.',
        'v7_ledger': {'run_once': True, 'code_sha': FROZEN_SHA, 'tolerance_ms': 1.0,
                      'status': 'RESERVED', 'verdict': None, 'residuals_ms': {}, 'post_hoc_changes': []},
        'outputs': [],
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation is the durable reservation. An incomplete run is not retried.
    with RECEIPT.open('x+', encoding='utf-8', newline='\n') as file:
        persist(file, record)
        model = LongitudinalModel(load_dev_longitudinal(
            ROOT / 'data/fixtures/dep_b1.json', HASHES['dep_b1']))
        predictions = {}
        for r in LOCKED_RANGES_M:
            lead, trail = float(model._lead(r)), float(model._trail(r))
            predictions[str(r)] = {'t2': lead * 1000, 't3': trail * 1000,
                                   'delta_t': (trail - lead) * 1000}
        ledger = record['v7_ledger']
        ledger.update(status='PREDICTIONS_FROZEN', predictions_ms=predictions,
                      predictions_sha256=digest(canonical(predictions)),
                      predictions_recorded_utc=timestamp())
        persist(file, record)
    return record


def open_once(predictions_sha256):
    """Open only an intact prediction record; mark RUN before retrieving cells."""
    code_hashes = verify_frozen()
    # A separate exclusive marker prevents concurrent/repeated opens, including
    # interruption after exposure. It remains as an immutable gate record.
    marker = RECEIPT.with_name('opened.json')
    record = json.loads(RECEIPT.read_text(encoding='utf-8'))
    ledger = record['v7_ledger']
    if ledger['status'] != 'PREDICTIONS_FROZEN' or marker.exists():
        raise RuntimeError('E3 already opened or incomplete; no second evaluation.')
    if (digest(canonical(ledger['predictions_ms'])) != predictions_sha256
            or ledger['predictions_sha256'] != predictions_sha256
            or record['model_source_sha256'] != code_hashes
            or record['hashes'] != {**HASHES, 'config': digest(canonical(CONFIG))}
            or record['runner_sha256'] != digest(Path(__file__).read_bytes())):
        raise RuntimeError('STOP: frozen record changed.')
    with marker.open('x', encoding='utf-8', newline='\n') as file:
        json.dump({'opened_utc': timestamp(), 'code_sha': FROZEN_SHA,
                   'config_sha256': record['hashes']['config'],
                   'fixture_sha256': HASHES, 'predictions_sha256': predictions_sha256}, file, indent=2)
        file.write('\n')
        file.flush()
        os.fsync(file.fileno())
    with RECEIPT.open('r+', encoding='utf-8', newline='\n') as file:
        ledger.update(status='RUN', opened_utc=json.loads(marker.read_text())['opened_utc'])
        persist(file, record)
        # First retrieval of LOCKED numerical observations for E3: predictions
        # are already durable and this immutable version is irreversibly RUN.
        rows = json.loads((ROOT / 'data/fixtures/dep_b1.json').read_bytes())['rows']
        locked = [row for row in rows if row['split'] == 'LOCKED']
        if sorted(row['range_m'] for row in locked) != list(LOCKED_RANGES_M):
            raise RuntimeError('Opened source has an invalid LOCKED split; do not retry.')
        observations = {}
        for row in locked:
            lead, trail = row['t2_ms'], row['t3_ms']
            observations[str(row['range_m'])] = {'t2': lead, 't3': trail, 'delta_t': trail - lead}
        ledger['observations_ms'] = observations
        persist(file, record)
        absolute, decisions = {}, {}
        for r, observed in observations.items():
            errors = {k: ledger['predictions_ms'][r][k] - observed[k] for k in CONFIG['comparisons']}
            ledger['residuals_ms'][r] = errors
            absolute[r] = {k: abs(v) for k, v in errors.items()}
            decisions[r] = {k: 'PASS' if abs(v) <= 1.0 else 'FAIL' for k, v in errors.items()}
        verdict = 'PASS' if all(v == 'PASS' for row in decisions.values() for v in row.values()) else 'FAIL'
        ledger.update(status='COMPLETE', absolute_errors_ms=absolute, decisions=decisions,
                      verdict=verdict, completed_utc=timestamp(), no_refitting_or_tuning=True,
                      first_and_only_E3_evaluation=True)
        record['gates'] = [{'id': 'E3', 'verdict': 'PASS' if verdict == 'PASS' else 'FAIL-RECORD'}]
        record['claims_allowed'] = [
            'Main-string timing matched the locked DEP rows within 1.0 ms.' if verdict == 'PASS'
            else 'Timing failed the locked check; outputs limited to 20/30/40/50 m.']
        record['applicability'] = {'timing_ranges_m': [20, 50] if verdict == 'PASS' else list(DEV_RANGES_M),
                                   'between_row_output_allowed': verdict == 'PASS'}
        persist(file, record)
    return record
