"""E1 evidence regression only; no fitting, interpolation, or E3 evaluation."""
import hashlib
import json
from pathlib import Path
from statistics import mean, pstdev
import unittest

from banglab.config import validate_fixture

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'data/fixtures'
# Independently calculated canonical-byte candidates; receipt freeze follows PASS.
EXPECTED_HASHES = {
    'dep_b1': '9ac268e4d96b145b3ef9f82fda71193c43339a103cec4632203f68e3c0ce1e79',
    'dep_p82': '37de300cd68184cc2315b6fffaf4fa04dbe07127a30514e982b538238359dc09',
    'dep_load': '7ddde731928ec2df4f8d4d256a75842181fc5ee54b885fb393b92f1a462c3b1b',
}
CONTRACT = 'ClayPath — Final Review to Build Contract (v1.1 amendments + v0.1 Python contract)(1).md'
SOURCE_HASHES = {
    CONTRACT: '9647717afa835afe1c5e79c86d1b01e93bb6c8804d8d8b2b81b5a00b4015085f',
    '03_DEP_99_953_Appendix_B_PRIMARY_UNALTERED.pdf':
    '5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7',
}


def load(name):
    return json.loads((FIXTURES / (name + '.json')).read_text(encoding='utf-8'))


class FixtureIntegrityTests(unittest.TestCase):
    def test_canonical_byte_hashes_and_schema(self):
        for name, expected in EXPECTED_HASHES.items():
            with self.subTest(fixture=name):
                data = (FIXTURES / (name + '.json')).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
                validate_fixture(json.loads(data))

    def test_authority_hashes_and_pinned_contract(self):
        for filename, expected in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256((ROOT / 'docs/evidence' / filename).read_bytes()).hexdigest(), expected)
        self.assertIn(SOURCE_HASHES[CONTRACT], (ROOT / 'BUILD_CONTRACT.md').read_text())

    def test_b1_cell_for_cell_primary_p77_and_contract_section2(self):
        expected = [
            (20,60.8,68.4,293,250,8.0,5.9,1.9,'DEV'),
            (25,78.7,89.2,265,230,6.6,4.9,2.5,'LOCKED'),
            (30,98.4,111.8,242,213,5.5,4.2,2.9,'DEV'),
            (35,120.0,136.2,223,198,4.6,3.7,3.3,'LOCKED'),
            (40,143.3,162.4,206,185,4.0,3.2,3.6,'DEV'),
            (45,168.4,190.3,192,173,3.4,2.8,3.9,'LOCKED'),
            (50,195.3,220.0,180,163,3.0,2.5,4.1,'DEV'),
        ]
        keys = ('range_m','t2_ms','t3_ms','vL_m_s','vT_m_s','EL_J','ET_J','L_m','split')
        self.assertEqual([tuple(row[k] for k in keys) for row in load('dep_b1')['rows']], expected)
        self.assertEqual(load('dep_b1')['rows'][0]['vL_m_s'], 293)

    def test_all14_energy_cells_share_allowed_pellet_mass(self):
        # Primary p.77 prints velocities to 1 m/s and energies to 0.1 J.
        # Check overlap of their rounding intervals with the §8.7 mass
        # interval. These are source print precisions, not gate tolerances.
        low, high = 186.5e-6, 187.5e-6  # §8.7: mg converted to kg
        for row in load('dep_b1')['rows']:
            for velocity, energy in [('vL_m_s','EL_J'), ('vT_m_s','ET_J')]:
                v, e = row[velocity], row[energy]
                low = max(low, 2 * (e - 0.05) / (v + 0.5)**2)
                high = min(high, 2 * (e + 0.05) / (v - 0.5)**2)
        self.assertLess(low, high, 'No common mass reproduces all printed energies')

    def test_load_reference_primary_p75_p76(self):
        data = load('dep_load')
        self.assertEqual(data['load'], dict(mass_g=35.8,pellet_count=192,pellet_mass_mg=187,
                          pellet_diameter_mm=3.15,velocity_at_2_5m_m_s=363))
        self.assertEqual(data['gun'], dict(proof_barrel_in=29,bore_mm=18.4,choke_in=0.030))
        self.assertEqual(data['environment'], dict(temperature_C=23,pressure_mb=1006,
                          relative_humidity_percent=56.5,wind_m_s=1,wind_from_deg=225))
        self.assertEqual(data['design'], dict(ranges_m=[20,25,30,35,40,45,50],rounds_per_range=10))
        self.assertEqual(data['labels'], {'source_values':'MEASURED_PRIMARY'})

    def test_p82_all20_raw_observations_primary_p82(self):
        expected = [
            (184,176,92),(192,184,96),(192,189,98),(187,181,94),(190,184,96),
            (189,181,94),(192,178,93),(186,178,93),(185,180,94),(180,174,91),
            (195,147,77),(189,149,78),(197,136,71),(191,160,83),(196,138,72),
            (189,153,80),(194,142,74),(186,134,70),(192,151,79),(182,143,74),
        ]
        rows = load('dep_p82')['rows']
        self.assertEqual([r['ref'] for r in rows], list(range(1,21)))
        self.assertEqual([r['range_yd'] for r in rows], [30]*10+[40]*10)
        self.assertEqual([(r['paper_5ft'],r['circle_30in'],r['source_percent']) for r in rows], expected)
        self.assertEqual(rows[1]['source_note'], 'overstrike, read 192, confirmed by mean')

    def test_p82_every_printed_summary_and_percentage(self):
        data = load('dep_p82')
        self.assertEqual(data['average_pellets_per_cartridge'], 192)
        expected = {
            '30yd': (187.7,3.8,180.5,4.2,94,2.2,2.0,2.3,2.3),
            '40yd': (191.1,4.5,145.3,7.8,76,4.1,2.3,5.4,5.4),
        }
        keys = ('paper_mean','paper_sd_population','circle_mean','circle_sd_population',
                'percent_mean','percent_sd_population','paper_sig_avg_percent',
                'circle_sig_avg_percent','percent_sig_avg_percent')
        for group, values in expected.items():
            self.assertEqual(tuple(data['published_summary'][group][k] for k in keys), values)
            rows = [r for r in data['rows'] if str(r['range_yd'])+'yd' == group]
            summary = data['published_summary'][group]
            for field, prefix in [('paper_5ft','paper'),('circle_30in','circle'),('source_percent','percent')]:
                # A15: percentages are count/192; individual printed % cells
                # are rounded separately. Do not calculate SD from rounded cells.
                observations = ([100*r['circle_30in']/192 for r in rows]
                                if prefix == 'percent' else [r[field] for r in rows])
                avg, sd = mean(observations), pstdev(observations)
                self.assertEqual(round(avg, 0 if prefix=='percent' else 1), summary[prefix+'_mean'])
                self.assertEqual(round(sd,1), summary[prefix+'_sd_population'])
                self.assertEqual(round(100*sd/avg,1), summary[prefix+'_sig_avg_percent'])
        for row in data['rows']:
            self.assertEqual(round(100*row['circle_30in']/192), row['source_percent'])
        self.assertEqual(sum(r['paper_5ft'] for r in data['rows'][:10]),1877)

    def test_accepted_hash_freeze_receipt(self):
        receipt = json.loads((ROOT / 'receipt.json').read_text(encoding='utf-8'))
        self.assertEqual(receipt['hashes'], EXPECTED_HASHES)
        self.assertEqual(receipt['hash_algorithm'], 'SHA-256 over exact file bytes (not Git blob SHA)')
        self.assertEqual([(g['id'], g['verdict']) for g in receipt['gates']],
                         [('E0', 'PASS'), ('E1', 'PASS')])
        self.assertEqual(receipt['outputs'], [])
        for name, digest in receipt['hashes'].items():
            self.assertEqual(hashlib.sha256((FIXTURES / (name+'.json')).read_bytes()).hexdigest(), digest)

    def test_column_semantics_not_promoted_to_measurements(self):
        labels = load('dep_b1')['column_labels']
        self.assertEqual({k for k,v in labels.items() if v=='MEASURED_PRIMARY'},
                         {'range_m','t2_ms','t3_ms'})
        self.assertEqual({k for k,v in labels.items() if v=='SOURCE_DERIVED'},
                         {'vL_m_s','vT_m_s','EL_J','ET_J','L_m'})
        self.assertEqual(load('dep_p82')['epistemic_status'], 'MEASURED_PRIMARY')


if __name__ == '__main__':
    unittest.main()
