"""Controlled local fixtures; no real project effects or execution attestation."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('principles_under_test', ROOT / 'principles.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
T = datetime(2026, 1, 1, tzinfo=timezone.utc)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='principles project ')
        self.root = Path(self.temp.name)
        self.ws = p.Workspace(self.root)
        self.task = 'T001'
        self.contract = self.root / p.initialize(self.ws, self.task)
        (self.root / 'subject.txt').write_text('first', encoding='utf-8')
        (self.root / 'check.log').write_text('controlled fixture result', encoding='utf-8')
        self.data = json.loads(self.contract.read_text())
        self.data.update(state='ready', outcome='Preserve the chosen fixture',
                         beneficiary='controlled test reader', scope='Disposable local files',
                         authority_reference='this unit-test fixture only', recovery='Recreate disposable fixture',
                         subjects=[{'path': 'subject.txt', 'kind': 'file'}],
                         checks=[{'id': 'C1', 'criterion': 'The selected fixture is inspectable', 'max_age_seconds': None}])
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        self.contract.write_text(json.dumps(self.data), encoding='utf-8')

    def capture(self, result='pass', at=T, observed=None):
        name = p.receipt(self.ws, self.task, 'C1', result, 'check.log',
                         'Controlled unit fixture; no project test execution', observed, at)
        return self.root / name

    def inspect(self, at=T + timedelta(seconds=5)):
        return p.inspect(self.ws, self.task, at)

    def edit_receipt(self, path, **updates):
        data = json.loads(path.read_text()); data.update(updates)
        path.write_text(json.dumps(data), encoding='utf-8')

    def test_initialized_draft_is_unknown(self):
        p.initialize(self.ws, 'DRAFT')
        with self.assertRaises(p.Unresolved):p.inspect(self.ws, 'DRAFT', T)

    def test_init_never_overwrites(self):
        before = self.contract.read_bytes()
        with self.assertRaises(FileExistsError):p.initialize(self.ws, self.task)
        self.assertEqual(before, self.contract.read_bytes())

    def test_missing_evidence_unknown(self):
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_declared_pass_has_unassessed_authenticity(self):
        self.capture(); result = self.inspect()
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['execution_authenticity'], 'unassessed')
        self.assertEqual(result['production_readiness'], 'unassessed')

    def test_same_size_and_mtime_drift_detected(self):
        self.capture(); file = self.root / 'subject.txt'; old = file.stat()
        file.write_text('other', encoding='utf-8');os.utime(file, ns=(old.st_atime_ns, old.st_mtime_ns))
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_changed_log_does_not_reuse_old_green(self):
        self.capture(); (self.root/'check.log').write_text('changed fixture', encoding='utf-8')
        self.assertEqual(self.inspect()['status'], 'fail')

    def test_latest_fail_blocks_old_pass(self):
        self.capture();self.capture('fail', T+timedelta(seconds=1))
        self.assertEqual(self.inspect()['status'], 'fail')

    def test_latest_unknown_blocks_old_pass(self):
        self.capture();self.capture('unknown', T+timedelta(seconds=1))
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_future_receipt_blocks_old_pass(self):
        self.capture();self.capture('pass', T+timedelta(days=1))
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_tied_receipts_are_unknown(self):
        self.capture();self.capture('fail')
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_changed_collector_blocks_old_green(self):
        self.capture(); latest=self.capture(at=T+timedelta(seconds=1))
        self.edit_receipt(latest, collector_sha256='0'*64)
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_changed_contract_needs_new_receipts(self):
        self.capture();self.data['scope'] += '; revised';self.save()
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_retired_check_history_does_not_satisfy_or_block_new_contract(self):
        self.capture();self.data['checks'][0]['id']='C2';self.save()
        self.assertEqual(self.inspect()['status'],'unknown')
        p.receipt(self.ws,self.task,'C2','pass','check.log','Changed controlled contract',clock=T+timedelta(seconds=1))
        self.assertEqual(self.inspect()['status'],'pass')

    def test_omitted_subject_blocks_pass(self):
        self.data['subjects'].append({'path':'check.log','kind':'file'});self.save()
        path=self.capture();data=json.loads(path.read_text())
        self.edit_receipt(path, subjects=data['subjects'][:1])
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_expected_absence_then_creation(self):
        self.data['subjects'].append({'path':'removed.txt','kind':'absent'});self.save()
        self.capture();self.assertEqual(self.inspect()['status'], 'pass')
        (self.root/'removed.txt').write_text('new',encoding='utf-8')
        with self.assertRaises(p.Unresolved):self.inspect()

    def test_missing_parent_is_not_confirmed_absence(self):
        self.data['subjects']=[{'path':'missing/removed.txt','kind':'absent'}];self.save()
        with self.assertRaises(p.Unresolved):self.capture()

    def test_recreated_receipt_does_not_refresh_old_observation(self):
        self.data['checks'][0]['max_age_seconds']=10;self.save()
        self.capture(at=T+timedelta(seconds=100),observed=T.isoformat())
        self.assertEqual(self.inspect(T+timedelta(seconds=101))['status'], 'unknown')

    def test_missing_observation_time_with_ttl_is_unknown(self):
        self.data['checks'][0]['max_age_seconds']=10;self.save();self.capture()
        self.assertEqual(self.inspect()['status'], 'unknown')

    def test_fresh_declared_observation(self):
        self.data['checks'][0]['max_age_seconds']=10;self.save();self.capture(observed=T.isoformat())
        self.assertEqual(self.inspect()['status'], 'pass')

    def test_future_observation_refused_at_capture(self):
        with self.assertRaises(p.Unresolved):self.capture(observed=(T+timedelta(seconds=1)).isoformat())

    def test_future_observation_in_newest_record_blocks(self):
        self.capture(); latest=self.capture(at=T+timedelta(seconds=1))
        self.edit_receipt(latest,evidence_observed_at=(T+timedelta(days=1)).isoformat())
        self.assertEqual(self.inspect()['status'],'unknown')

    def test_observation_after_recording_is_not_a_pass(self):
        path=self.capture()
        self.edit_receipt(path,evidence_observed_at=(T+timedelta(seconds=2)).isoformat())
        self.assertEqual(self.inspect()['status'],'unknown')

    def test_bad_receipt_cannot_be_skipped(self):
        self.capture(); folder=self.contract.parent/'receipts'
        (folder/'bad.json').write_text('{unfinished',encoding='utf-8')
        with self.assertRaises(p.Invalid):self.inspect()

    def test_malformed_older_body_not_skipped_after_newer_green(self):
        path=self.capture();self.capture(at=T+timedelta(seconds=1))
        for field in ['method','subjects','evidence']:
            original=path.read_bytes()
            self.edit_receipt(path,**{field:None})
            with self.assertRaises(p.Invalid):self.inspect()
            path.write_bytes(original)

    def test_boolean_byte_counts_do_not_equal_integer_fingerprints(self):
        (self.root/'subject.txt').write_text('x',encoding='utf-8')
        (self.root/'check.log').write_text('x',encoding='utf-8')
        path=self.capture();data=json.loads(path.read_text())
        data['subjects'][0]['bytes']=True;data['evidence']['bytes']=True
        path.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaises(p.Invalid):self.inspect()

    def test_large_integer_parse_error_has_structured_fail(self):
        self.contract.write_text('{"large":'+('9'*5000)+'}',encoding='utf-8')
        output=io.StringIO()
        with redirect_stdout(output):code=p.main(['check','--root',str(self.root),'--task',self.task])
        self.assertEqual(code,1)
        self.assertEqual(json.loads(output.getvalue())['status'],'fail')

    def test_duplicate_receipt_identity_rejected(self):
        path=self.capture(); other=self.capture(at=T+timedelta(seconds=1))
        self.edit_receipt(other,receipt_id=json.loads(path.read_text())['receipt_id'])
        with self.assertRaises(p.Invalid):self.inspect()

    def test_wrong_task_receipt_rejected(self):
        path=self.capture();self.edit_receipt(path,task_id='OTHER')
        with self.assertRaises(p.Invalid):self.inspect()

    def test_malformed_contract_hash_cannot_hide_as_history(self):
        path=self.capture();self.edit_receipt(path,task_sha256='not-a-sha')
        with self.assertRaises(p.Invalid):self.inspect()

    def test_output_collision_preserves_original_receipt(self):
        path=self.capture();before=path.read_bytes()
        rid=json.loads(before)['receipt_id']
        with patch.object(p.uuid,'uuid4') as mocked:
            mocked.return_value.hex=rid
            with self.assertRaises(FileExistsError):self.capture()
        self.assertEqual(path.read_bytes(),before)

    def test_mutation_during_capture_produces_no_receipt(self):
        original=self.ws.fingerprint
        def mutate(name):
            value=original(name)
            if name=='check.log':(self.root/'subject.txt').write_text('other',encoding='utf-8')
            return value
        with patch.object(self.ws,'fingerprint',side_effect=mutate):
            with self.assertRaises(p.Unresolved):self.capture()
        self.assertFalse((self.contract.parent/'receipts').exists())

    def test_duplicate_json_keys_and_nan_rejected(self):
        for data in ['{"a":1,"a":2}','{"age":NaN}']:
            with self.assertRaises(p.Invalid):p.load(data)

    def test_duplicate_subjects_rejected(self):
        self.data['subjects']*=2;self.save()
        with self.assertRaises(p.Invalid):self.capture()

    def test_invalid_age_not_silently_treated_as_static(self):
        for value in [True,-1,1.5,'10']:
            self.data['checks'][0]['max_age_seconds']=value;self.save()
            with self.assertRaises(p.Invalid):self.capture()

    def test_traversal_absolute_unc_and_stream_paths_refused(self):
        for name in ['.','../x','/x','C:/x','a/../x','a\\x','//server/x','x:stream','a//b']:
            with self.subTest(name=name),self.assertRaises(p.Invalid):self.ws.fingerprint(name)

    def test_symlink_refused_if_host_allows_creation(self):
        try:(self.root/'link').symlink_to(self.root/'subject.txt')
        except OSError as exc:self.skipTest('Host cannot create symlink: '+str(exc))
        with self.assertRaises(p.Invalid):self.ws.fingerprint('link')

    def test_explicit_root_with_spaces_and_non_ascii(self):
        folder=self.root/'projet café 研究';folder.mkdir();workspace=p.Workspace(folder)
        path=folder/p.initialize(workspace,'T2')
        self.assertTrue(path.is_file())

    def test_unsupported_python_is_refused(self):
        with patch.object(p.sys,'version_info',(3,11,0)):
            with self.assertRaises(p.Invalid):p.Workspace(self.root)

    def test_matching_edited_log_is_still_only_declared(self):
        path=self.capture();log=self.root/'check.log';log.write_text('invented fixture statement',encoding='utf-8')
        self.edit_receipt(path,evidence=self.ws.fingerprint('check.log'))
        result=self.inspect()
        self.assertEqual(result['status'],'pass')
        self.assertEqual(result['execution_authenticity'],'unassessed')

    def test_cli_unknown_is_nonzero(self):
        with redirect_stdout(io.StringIO()):code=p.main(['check','--root',str(self.root),'--task',self.task])
        self.assertEqual(code,2)

    def test_vendor_wrapper_unknown_is_nonzero(self):
        fixture=ROOT/'vendor/handbook/starter/project.example.json'
        (self.root/'record.json').write_bytes(fixture.read_bytes())
        with redirect_stdout(io.StringIO()):code=p.main(['validate-project','--root',str(self.root),'--record','record.json'])
        self.assertEqual(code,2)


if __name__=='__main__':unittest.main()
