"""Bounded mandatory-workflow fixtures; declared judgments are not truth proofs."""
from contextlib import redirect_stdout
from datetime import timedelta
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import workflow as w
p = w.core


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='mandatory principles ')
        self.root = Path(self.tmp.name)
        self.ws = p.Workspace(self.root)
        (self.root/'plan.md').write_text('Controlled plan fixture: outcome, scope, checks, recovery.', encoding='utf-8')
        (self.root/'subject.txt').write_text('selected source', encoding='utf-8')
        (self.root/'actual.log').write_text('controlled retained output; no customer outcome', encoding='utf-8')
        self.task = 'T001'

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, name, value):
        (self.root/name).write_text(json.dumps(value), encoding='utf-8')

    def prepare(self, small=False):
        w.begin(self.ws, self.task, small_reason='Spelling-only correction, meaning preserved' if small else None,
                plan=None if small else 'plan.md')
        self.contract = p.location(self.task)+'/task.json'
        self.review_path = w.names(self.task)[1]
        self.data = p.load(self.ws.read(self.contract))
        self.data.update(state='ready', outcome='Fixture acceptance', beneficiary='Fixture reviewer',
                         scope='Disposable local files', authority_reference='Controlled unit test', recovery='Discard temp files')
        self.data['subjects'].append({'path':'subject.txt','kind':'file'})
        self.data['checks']=[{'id':'C1','criterion':'Controlled source/output and review check','max_age_seconds':None}]
        self.save(self.contract,self.data)
        self.review = p.load(self.ws.read(self.review_path))
        self.review.update(reviewer='Fixture author, self-review disclosed',
                           summary='Controlled test review; no real customer, host or independent approval.',
                           scope_checks=['C1'],no_impact={key:True for key in w.RISKS})
        for row in self.review['principles']:
            row.update(status='unchanged' if small else 'supported',
                       reason='Controlled scoped assessment, referenced by C1', checks=['C1'])
        self.save(self.review_path,self.review)

    def receipt(self,result='pass'):
        return p.receipt(self.ws,self.task,'C1',result,'actual.log','Controlled fixture declaration')

    def result(self):
        return w.check(self.ws,self.task)

    def test_begin_material_creates_unresolved_review_and_draft(self):
        r=w.begin(self.ws,self.task,plan='plan.md')
        self.assertEqual(r['status'],'created')
        review=p.load(self.ws.read(r['review']))
        self.assertTrue(all(x['status']=='unknown' for x in review['principles']))
        with self.assertRaises(p.Unresolved):self.result()

    def test_begin_never_overwrites(self):
        self.prepare(); before=self.ws.read(self.contract)
        with self.assertRaises(p.Invalid):w.begin(self.ws,self.task,plan='plan.md')
        self.assertEqual(before,self.ws.read(self.contract))

    def test_partial_start_is_preserved(self):
        self.ws.mkdir(p.location(self.task))
        self.ws.create(w.names(self.task)[0],{'interrupted':True})
        with self.assertRaises(p.Invalid):w.begin(self.ws,self.task,plan='plan.md')

    def test_begin_requires_one_mode(self):
        for kwargs in ({},{'plan':'plan.md','small_reason':'typo'}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(p.Invalid):w.begin(self.ws,self.task,**kwargs)

    def test_material_pass_has_explicit_semantic_limit(self):
        self.prepare();self.receipt();r=self.result()
        self.assertEqual(r['status'],'pass')
        self.assertEqual(r['semantic_adequacy'],'unassessed by the deterministic checker')
        self.assertEqual(len(r['principle_dispositions']),10)

    def test_missing_receipt_is_unknown(self):
        self.prepare();self.assertEqual(self.result()['status'],'unknown')

    def test_review_changes_invalidate_prior_evidence(self):
        self.prepare();self.receipt();self.review['summary']+=' revised'
        self.save(self.review_path,self.review)
        self.assertEqual(self.result()['status'],'unknown')

    def test_subject_changes_invalidate_prior_evidence(self):
        self.prepare();self.receipt();(self.root/'subject.txt').write_text('changed',encoding='utf-8')
        self.assertEqual(self.result()['status'],'unknown')

    def test_material_plan_is_frozen_at_begin(self):
        self.prepare();(self.root/'plan.md').write_text('new scope',encoding='utf-8');self.receipt()
        with self.assertRaises(p.Unresolved):self.result()

    def test_workflow_changed_since_begin_is_unknown(self):
        self.prepare();self.receipt()
        with patch.object(w,'collector',return_value='0'*64):
            with self.assertRaises(p.Unresolved):self.result()

    def test_future_begin_is_unknown(self):
        self.prepare();self.receipt()
        with self.assertRaises(p.Unresolved):w.check(self.ws,self.task,p.now()-timedelta(days=1))

    def test_cannot_omit_selected_review(self):
        self.prepare();self.data['subjects']=[x for x in self.data['subjects'] if x['path']!=self.review_path]
        self.save(self.contract,self.data);self.receipt()
        with self.assertRaises(p.Invalid):self.result()

    def test_all_ten_unique_ids_required(self):
        self.prepare();self.review['principles'][-1]['id']='P01';self.save(self.review_path,self.review)
        with self.assertRaises(p.Invalid):self.result()

    def test_supported_needs_real_known_check_reference(self):
        self.prepare();self.review['principles'][0]['checks']=[];self.save(self.review_path,self.review)
        with self.assertRaises(p.Unresolved):self.result()

    def test_unknown_reference_and_unhashable_input_fail(self):
        self.prepare()
        for value in (['missing'],[{}],['C1','C1']):
            self.review['scope_checks']=value;self.save(self.review_path,self.review)
            with self.subTest(value=value):
                with self.assertRaises(p.Invalid):self.result()

    def test_na_requires_reason_and_cannot_evade_accountability(self):
        self.prepare();row=self.review['principles'][1]
        row.update(status='not_applicable',reason='',checks=[]);self.save(self.review_path,self.review)
        with self.assertRaises(p.Unresolved):self.result()
        row.update(reason='No changed shared interface in this fixture')
        self.review['principles'][0].update(status='not_applicable',reason='No evidence')
        self.save(self.review_path,self.review)
        with self.assertRaises(p.Invalid):self.result()

    def test_scoped_na_can_pass(self):
        self.prepare();self.review['principles'][2].update(status='not_applicable',reason='Fixture has no changing shared state or external consumers',checks=[])
        self.save(self.review_path,self.review);self.receipt()
        self.assertEqual(self.result()['status'],'pass')

    def test_unknown_and_failed_judgments_block_completion(self):
        self.prepare()
        for state in ('unknown','fail'):
            self.review['principles'][1]['status']=state;self.save(self.review_path,self.review);self.receipt()
            self.assertEqual(self.result()['status'],state)

    def test_small_shared_reason_and_check_can_pass(self):
        self.prepare(small=True);self.receipt();r=self.result()
        self.assertEqual(r['status'],'pass');self.assertEqual(r['profile'],'small')

    def test_small_unknown_or_real_impact_blocks(self):
        self.prepare(small=True)
        for value in (None,False,0):
            self.review['no_impact']['behavior']=value;self.save(self.review_path,self.review)
            with self.subTest(value=value):
                with self.assertRaises(p.Unresolved):self.result()

    def test_material_cannot_claim_unchanged_shortcut(self):
        self.prepare();self.review['principles'][0]['status']='unchanged';self.save(self.review_path,self.review)
        with self.assertRaises(p.Invalid):self.result()

    def test_placeholder_reviewer_is_unresolved(self):
        self.prepare();self.review['reviewer']='TODO';self.save(self.review_path,self.review)
        with self.assertRaises(p.Unresolved):self.result()

    def test_cli_preserves_pass_unknown_and_fail(self):
        self.prepare()
        for expected,result in ((2,None),(0,'pass'),(1,'fail')):
            if result:self.receipt(result)
            out=io.StringIO()
            with redirect_stdout(out): code=w.main(['check','--root',str(self.root),'--task',self.task])
            self.assertEqual(code,expected);self.assertIn('status',json.loads(out.getvalue()))


if __name__=='__main__':unittest.main()
