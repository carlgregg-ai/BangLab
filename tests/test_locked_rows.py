"""Verify the saved E3 experiment, never repeat its predictions/evaluation.

The explicit two-phase gate is in banglab.gates. Test discovery has no
capability to create a receipt or open the LOCKED envelope.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from banglab import gates


class LockedGateTests(unittest.TestCase):
    def test_existing_reservation_refuses_another_prediction_run(self):
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(gates, 'verify_frozen') as verify:
                with self.assertRaisesRegex(RuntimeError, 'already exists'):
                    gates.freeze_predictions()
                verify.assert_not_called()

    def test_opened_gate_refuses_before_source_read_or_model_evaluation(self):
        saved = {'v7_ledger': {'status': 'COMPLETE'}}
        with patch.object(gates, 'verify_frozen', return_value={}):
            with patch.object(Path, 'read_text', return_value=json.dumps(saved)):
                with patch.object(Path, 'read_bytes', side_effect=AssertionError('No source read')):
                    with patch.object(gates, 'LongitudinalModel', side_effect=AssertionError('No model rerun')):
                        with self.assertRaisesRegex(RuntimeError, 'no second evaluation'):
                            gates.open_once('unused')


@unittest.skipUnless(gates.RECEIPT.exists(), 'E3 has not been executed; no automatic opening')
class SavedE3Tests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(gates.RECEIPT.read_text(encoding='utf-8'))
        self.ledger = self.record['v7_ledger']

    def test_provenance_and_prediction_freeze(self):
        record, ledger = self.record, self.ledger
        self.assertEqual(ledger['status'], 'COMPLETE')
        self.assertEqual(ledger['code_sha'], gates.FROZEN_SHA)
        self.assertEqual(record['config'], gates.CONFIG)
        self.assertEqual(record['hashes'], {**gates.HASHES, 'config': gates.digest(gates.canonical(gates.CONFIG))})
        for name, expected in record['model_source_sha256'].items():
            self.assertEqual(gates.digest((gates.ROOT / name).read_bytes()), expected)
        self.assertEqual(record['runner_sha256'], gates.digest(Path(gates.__file__).read_bytes()))
        frozen_hash = gates.digest(gates.canonical(ledger['predictions_ms']))
        self.assertEqual(ledger['predictions_sha256'], frozen_hash)
        marker = json.loads(gates.RECEIPT.with_name('opened.json').read_text())
        self.assertEqual(marker['predictions_sha256'], frozen_hash)
        self.assertEqual(marker['code_sha'], gates.FROZEN_SHA)
        self.assertEqual(marker['fixture_sha256'], gates.HASHES)
        self.assertEqual(marker['config_sha256'], record['hashes']['config'])
        self.assertEqual(marker['opened_utc'], ledger['opened_utc'])
        self.assertLess(ledger['predictions_recorded_utc'], ledger['opened_utc'])
        self.assertLess(ledger['opened_utc'], ledger['completed_utc'])
        self.assertTrue(ledger['run_once'])
        self.assertTrue(ledger['no_refitting_or_tuning'])
        self.assertTrue(ledger['first_and_only_E3_evaluation'])
        self.assertEqual(ledger['post_hoc_changes'], [])

    def test_saved_residuals_and_individual_decisions(self):
        ledger = self.ledger
        self.assertEqual(ledger['tolerance_ms'], 1.0)
        self.assertEqual(set(ledger['predictions_ms']), {'25', '35', '45'})
        verdicts = []
        for r in ('25', '35', '45'):
            for k in ('t2', 't3', 'delta_t'):
                # Arithmetic audit of saved evidence, not a new model evaluation.
                error = ledger['predictions_ms'][r][k] - ledger['observations_ms'][r][k]
                self.assertEqual(ledger['residuals_ms'][r][k], error)
                self.assertEqual(ledger['absolute_errors_ms'][r][k], abs(error))
                decision = 'PASS' if abs(error) <= 1.0 else 'FAIL'
                self.assertEqual(ledger['decisions'][r][k], decision)
                verdicts.append(decision)
        expected = 'PASS' if all(v == 'PASS' for v in verdicts) else 'FAIL'
        self.assertEqual(ledger['verdict'], expected)
        self.assertEqual(self.record['gates'], [{'id': 'E3', 'verdict': 'PASS' if expected == 'PASS' else 'FAIL-RECORD'}])

    def test_scientific_E3_verdict_is_explicit(self):
        self.assertEqual(self.ledger['verdict'], 'PASS',
                         'Scientific E3 FAIL-RECORD: preserve failure; never refit or rerun.')


if __name__ == '__main__':
    unittest.main()
