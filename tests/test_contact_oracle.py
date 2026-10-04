"""Synthetic software checks only; never execute the six-case E6 experiment."""
import ast
from contextlib import contextmanager
from dataclasses import replace
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
from scipy.integrate import quad
from scipy.stats import ncx2

from banglab.encounter import oracle_contact as mc
from banglab.encounter import reference_case6 as reference
from banglab import e6_contact_gate as gate

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def scratch_directory():
    """Real test files, with inherited sandbox ACLs on Windows.

    Python's TemporaryDirectory uses mkdir(0700), which installs a protected
    Windows ACL excluding the parent's sandbox grants. Do not alter global
    tempfile behaviour or weaken permissions on existing evidence directories.
    """
    parent=gate.EVIDENCE.resolve()
    directory=parent/('test-'+uuid4().hex)
    directory.mkdir(mode=0o777 if os.name=='nt' else 0o700)
    try:
        yield directory
    finally:
        if directory.resolve().parent!=parent:
            raise RuntimeError('Test cleanup escaped its declared parent.')
        shutil.rmtree(directory)


def toy():
    return mc.ContactInputs(a_m=0.4, b_m=0.2, pellet_radius_m=0.01,
                            psi_deg=90., travel_direction_deg=0.,
                            e_a_m=0.3, e_c_m=-0.2, speed_m_s=2.,
                            duration_s=0.5, sigma_m=0.7,
                            kappa=0., tail_probability=0.)


class DirectOracleTests(unittest.TestCase):
    def test_offset_sign_rotation_and_closed_boundary(self):
        spec = toy()
        q = np.array([0.5, 0.5, 0.5, 0.5, 1.])
        # At mid-string clay centre=(-.3,.2), major axis vertical.
        xy = np.array([[-.3,.2], [-.3,.61], [-.3,.610001],
                       [-.089999,.2], [.2,.2]])
        np.testing.assert_array_equal(mc.direct_contacts(spec,q,xy),
                                      [True,True,False,False,True])

    def test_travel_frame_rotation(self):
        s = replace(toy(), travel_direction_deg=90., psi_deg=180.)
        self.assertTrue(mc.direct_contacts(s,np.array([.5]),np.array([[-.2,-.3]]))[0])

    def test_inverse_tail_and_conditional_scale(self):
        u = np.array([0., .45, .9, .95])
        np.testing.assert_allclose(mc.arrival(u,.1),[0.,.5,1.,1.5],atol=1e-15)
        np.testing.assert_array_equal(mc.arrival(u,0.),u)
        spec = replace(toy(), kappa=.4, tail_probability=.1)
        class Draws:
            def random(self,n):
                self.n=n
                return u
            def standard_normal(self,shape):
                self.shape=shape
                return np.ones(shape)
        rng=Draws()
        with patch.object(mc,'direct_contacts',return_value=np.ones(4,dtype=bool)) as contact:
            mc.draw_contacts(spec,rng,4)
        self.assertEqual(rng.shape,(4,2))
        np.testing.assert_allclose(contact.call_args.args[1],[0.,.5,1.,1.5])
        np.testing.assert_allclose(contact.call_args.args[2],
                                  np.repeat((.7*np.array([.8,1.,1.2,1.4]))[:,None],2,axis=1))

    def test_seeded_direct_round_grouping_and_stream_continuation(self):
        spec=toy()
        actual=mc.simulate(spec,seed=123,single_pellets=17,rounds=5,
                           pellets_per_round=3,single_block=7,round_block=2)
        rng=np.random.Generator(np.random.PCG64(123))
        def manual(n):
            q=rng.random(n); points=rng.standard_normal((n,2))*.7
            contacts=[]
            for t,(x,y) in zip(q,points):
                cx=2*.5*(t-.5)-.3; cy=.2
                # psi=90: local x=y-cy, local y=-(x-cx).
                contacts.append(((y-cy)/.41)**2+((x-cx)/.21)**2<=1+1e-12)
            return contacts
        hits=sum(sum(manual(n)) for n in (7,7,3))
        counts=[]
        for n in (2,2,1):
            draws=manual(n*3)
            counts.extend(sum(draws[i:i+3]) for i in range(0,len(draws),3))
        self.assertEqual(actual['single_contacts'],hits)
        self.assertEqual(actual['round_count_histogram'],np.bincount(counts,minlength=4).tolist())
        self.assertEqual(actual,mc.simulate(spec,seed=123,single_pellets=17,rounds=5,
                         pellets_per_round=3,single_block=7,round_block=2))

    def test_invalid_inputs_and_counts_rejected(self):
        for name,value in [('sigma_m',0),('duration_s',-1),('a_m',float('nan')),
                           ('kappa',2),('tail_probability',1),('psi_deg',True)]:
            with self.assertRaises(ValueError):
                replace(toy(),**{name:value})
        for name,value in [('seed',-1),('single_pellets',0),('rounds',True)]:
            kwargs=dict(seed=1,single_pellets=10,rounds=10,pellets_per_round=3,
                        single_block=5,round_block=5)
            kwargs[name]=value
            with self.assertRaises(ValueError):
                mc.simulate(toy(),**kwargs)

    def test_no_deterministic_dependency_in_mc(self):
        tree=ast.parse(Path(mc.__file__).read_text())
        imported=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import): imported.extend(n.name for n in node.names)
            if isinstance(node,ast.ImportFrom): imported.append(node.module)
        self.assertEqual(set(imported),{'dataclasses','math','numpy'})


class IsolatedReferenceTests(unittest.TestCase):
    def test_quadrature_measure_and_conditional_circle_against_adaptive_integral(self):
        q,w=reference.tail_nodes()
        self.assertAlmostEqual(sum(w),1.,places=14)
        self.assertAlmostEqual(float(w@q),.6,places=14)
        fraction=reference.marginal_fraction(.8,.3)
        f=lambda q: -math.expm1(-.5*(.3/(.8*(1+.4*(q-.5))))**2)
        expected=.9*quad(f,0,1)[0]+.1*quad(f,1,2)[0]
        self.assertAlmostEqual(fraction,expected,places=14)
        sigma=reference.fit_anchor(fraction,.3)
        self.assertAlmostEqual(sigma,.8,places=12)

    def test_variant_mass_against_separate_synthetic_adaptive_reference(self):
        spec=replace(toy(),a_m=.2,b_m=.2,kappa=.4,tail_probability=.1)
        actual=reference.probability(spec)
        def f(q):
            sigma=.7*(1+.4*(q-.5))
            cx=2*.5*(q-.5)-.3
            return ncx2.cdf((.21/sigma)**2,2,(cx*cx+.2**2)/sigma**2)
        expected=.9*quad(f,0,1,epsabs=1e-12)[0]+.1*quad(f,1,2,epsabs=1e-12)[0]
        self.assertAlmostEqual(actual,expected,places=13)
        with self.assertRaises(ValueError):
            reference.probability(toy())


class GateSoftwareTests(unittest.TestCase):
    def test_acceptance_exact_counts_SE_and_failure(self):
        actual=gate.compare(25,100,.25,0.)
        self.assertEqual(actual['SE'],math.sqrt(.25*.75/100))
        self.assertTrue(actual['pass'])
        self.assertFalse(gate.compare(0,100,.001,0.)['pass'])
        self.assertTrue(gate.compare(0,100,.001,.001)['pass'])
        self.assertFalse(gate.compare(0,100,.00100001,.001)['pass'])

    def test_second_execution_refused_before_model_or_sampling(self):
        # Use a historical directory with an existing receipt: exclusive open fails.
        with patch.object(gate,'verify_preflight',side_effect=AssertionError('no model reads')):
            with self.assertRaises(FileExistsError):
                gate.run_once(ROOT/'docs/evidence/e6')

    def test_plan_and_historical_preservation(self):
        plan=gate.read_json(gate.EVIDENCE/'plan.json')
        self.assertEqual(gate.digest(gate.EVIDENCE/'plan.json'),gate.PLAN_SHA256)
        self.assertEqual(plan['seeds'],{str(i):60000+i for i in range(1,7)})
        self.assertEqual((plan['single_pellets_per_case'],plan['rounds_per_case']),(1000000,20000))
        self.assertEqual(gate.digest(ROOT/plan['geometry_path']),plan['geometry_sha256'])
        for name,value in plan['preserved_file_sha256'].items():
            self.assertEqual(gate.digest(ROOT/name),value,name)

    def test_injected_implementation_failure_persisted_and_retry_refused(self):
        # Fault injection in a disposable directory, not an E6 evaluation.
        with scratch_directory() as tmp:
            directory=Path(tmp)
            with patch.object(gate,'verify_preflight',side_effect=ValueError('synthetic fault')):
                result=gate.run_once(directory)
                self.assertEqual(result['status'],'IMPLEMENTATION_FAILURE')
                self.assertEqual(result['results'],[])
                self.assertEqual(gate.read_json(directory/'receipt.json'),result)
                with self.assertRaises(FileExistsError):
                    gate.run_once(directory)

    def test_injected_failed_comparison_stops_before_next_case(self):
        plan=gate.read_json(gate.EVIDENCE/'plan.json')
        fake={'single_pellets':100,'single_contacts':0,'rounds':100,
              'round_count_histogram':[100]+[0]*192}
        with scratch_directory() as tmp:
            directory=Path(tmp)
            (directory/'preflight.json').write_text('{}')
            with patch.object(gate,'verify_preflight',return_value=(plan,{})), \
                 patch.object(gate.EncounterField,'from_repository'), \
                 patch.object(gate,'reference_inputs',return_value=(toy(),.2,'synthetic',[])), \
                 patch.object(mc,'simulate',return_value=fake) as sampler:
                result=gate.run_once(directory)
            self.assertEqual(result['status'],'SCIENTIFIC_FAIL')
            self.assertEqual(len(result['results']),1)
            self.assertEqual(sampler.call_count,1)
            self.assertEqual(result['F4_non_dispersion_regression'],[])
            self.assertEqual(gate.read_json(directory/'receipt.json'),result)

    def test_saved_first_result_arithmetic_without_scientific_rerun(self):
        path=gate.EVIDENCE/'receipt.json'
        if not path.exists():
            # Before execution only the prospective plan exists; no skipped test.
            self.assertTrue((gate.EVIDENCE/'plan.json').exists())
            return
        result=gate.read_json(path)
        self.assertEqual(result['plan_sha256'],gate.PLAN_SHA256)
        self.assertEqual(result['preflight_sha256'],gate.digest(gate.EVIDENCE/'preflight.json'))
        freeze=gate.read_json(gate.EVIDENCE/'preflight.json')
        self.assertLess(freeze['timestamp_utc'],result['started_utc'])
        for name,value in freeze['implementation_sha256'].items():
            self.assertEqual(gate.digest(ROOT/name),value,name)
        for row in result['results']:
            if 'sampling' not in row:
                continue  # An implementation STOP may leave a recorded reference.
            sample=row['sampling']
            self.assertEqual(sample['seed'],60000+row['case'])
            self.assertEqual(sample['single_pellets'],1000000)
            self.assertEqual(sample['rounds'],20000)
            self.assertEqual(sum(sample['round_count_histogram']),20000)
            self.assertEqual(row['single'],gate.compare(sample['single_contacts'],1000000,row['pi'],0.))
            for k,check in row['round_tails'].items():
                self.assertEqual(check,gate.compare(sum(sample['round_count_histogram'][int(k):]),
                                                    20000,check['reference'],.001))
            passed=row['single']['pass'] and all(c['pass'] for c in row['round_tails'].values())
            self.assertEqual(row['status'],'PASS' if passed else 'FAIL')
        if result.get('verdict')=='PASS':
            self.assertEqual([r['case'] for r in result['results']],list(range(1,7)))
            self.assertTrue(all(r['status']=='PASS' for r in result['results']))
            self.assertEqual(len(result['F4_non_dispersion_regression']),8)
            for row in result['F4_non_dispersion_regression']:
                self.assertLessEqual(abs(row['calculated']-row['target']),row['tolerance'])


if __name__=='__main__':
    unittest.main()
