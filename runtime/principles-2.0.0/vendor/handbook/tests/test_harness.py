import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('handbook_validator', ROOT/'harness/validate.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NOW = datetime(2026, 10, 23, 10, 15, tzinfo=timezone.utc)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'starter/project.example.json').read_text(encoding='utf-8'))

    def result(self):
        return mod.validate(self.data, NOW)

    def active_policy(self, mode, proposer='fixture proposer', approver='fixture approver'):
        self.data['policy'] = {
            'status': 'active', 'approval_mode': mode,
            'proposed_by': proposer, 'approved_by': approver,
            'approval_reference': 'fictional decision record',
            'authority_reference': 'fictional project adoption policy',
            'adoption_reason': 'Exercise the declared-record contract only',
            'review_condition': 'Reconsider when the fictional scope changes',
        }

    def test_valid_records_leave_real_world_readiness_unassessed(self):
        r = self.result()
        self.assertEqual(r['structural_status'], 'pass')
        self.assertEqual(r['validator_version'], '0.2.0')
        self.assertEqual(r['production_readiness'], 'unassessed')
        self.assertEqual(r['unknowns'], 4)

    def test_legacy_record_needs_explicit_contract_migration(self):
        self.data['schema_version'] = '1.0.0'
        self.assertTrue(any(x['check'] == 'CORE-01' and x['status'] == 'fail' for x in self.result()['checks']))

    def test_wrong_root_shape_fails_without_exception(self):
        self.assertEqual(mod.validate([], NOW)['structural_status'], 'fail')

    def test_duplicate_component_identity_fails(self):
        self.data['components'].append(copy.deepcopy(self.data['components'][0]))
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_broken_dependency_fails(self):
        self.data['links'][0]['to'] = 'missing-component'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_stale_green_is_unknown(self):
        self.data['observations'][0]['observed_at'] = '2026-10-22T10:00:00Z'
        r=self.result()
        self.assertEqual(r['structural_status'], 'pass')
        self.assertTrue(any(x['check']=='OBS-04' and x['status']=='unknown' for x in r['checks']))

    def test_revision_change_invalidates_old_observation(self):
        self.data['components'][0]['revision'] = 'example-r4'
        self.assertTrue(any(x['check']=='OBS-04' and x['status']=='unknown' for x in self.result()['checks']))

    def test_future_observation_fails(self):
        self.data['observations'][0]['observed_at'] = '2026-10-24T10:00:00Z'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_observation_without_timezone_fails(self):
        self.data['observations'][0]['observed_at'] = '2026-10-23T10:00:00'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_failed_observation_is_not_old_green(self):
        self.data['observations'][0]['result'] = 'fail'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_missing_observation_is_unknown(self):
        self.data['observations'] = []
        self.assertTrue(any(x['check']=='OBS-05' and x['status']=='unknown' for x in self.result()['checks']))

    def test_percentage_requires_denominator(self):
        del self.data['components'][0]['maintenance']['denominator']
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_negative_cost_range_fails(self):
        self.data['components'][0]['maintenance']['low'] = -1
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_boolean_is_not_cost_number(self):
        self.data['components'][0]['maintenance']['low'] = False
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_infinite_cost_is_not_a_bounded_estimate(self):
        self.data['components'][0]['maintenance'].update({'unit':'hours','high':float('inf')})
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_infinite_freshness_window_does_not_revalidate_old_green(self):
        self.data['observations'][0].update({'observed_at':'2020-01-01T00:00:00Z','max_age_seconds':float('inf')})
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_timestamp_normalization_overflow_is_invalid(self):
        self.data['observations'][0]['observed_at']='0001-01-01T00:00:00+01:00'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_non_ascii_semver_digit_is_invalid(self):
        self.data['project']['version']='1\u0661.0.0'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_large_finite_integer_cost_does_not_overflow(self):
        self.data['components'][0]['maintenance'].update({'unit':'illustrative-units','high':10**400})
        self.assertEqual(self.result()['structural_status'], 'pass')
        self.assertEqual(self.result()['production_readiness'], 'unassessed')

    def test_large_finite_integer_age_budget_is_structurally_valid(self):
        self.data['observations'][0]['max_age_seconds']=10**400
        self.assertEqual(self.result()['structural_status'], 'pass')

    def test_pushed_updates_need_reconciliation(self):
        self.data['synchronization'] = {'enabled':True,'authority':'notes'}
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_null_verification_member_fails(self):
        self.data['change']['verification'] = [None]
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_blank_verification_member_fails(self):
        self.data['change']['verification'] = [' \t']
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_object_verification_member_fails(self):
        self.data['change']['verification'] = [{'claim': 'not a statement'}]
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_empty_verification_list_fails(self):
        self.data['change']['verification'] = []
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_owner_can_adopt_own_proposal(self):
        owner = self.data['project']['owner']
        self.active_policy('owner-adoption', proposer=owner, approver=owner)
        r = self.result()
        self.assertEqual(r['structural_status'], 'pass')
        self.assertEqual(r['production_readiness'], 'unassessed')

    def test_owner_can_adopt_an_agent_proposal(self):
        self.active_policy('owner-adoption', proposer='fixture worker', approver=self.data['project']['owner'])
        self.assertEqual(self.result()['structural_status'], 'pass')

    def test_agent_cannot_self_promote_as_non_owner(self):
        self.active_policy('owner-adoption', proposer='fixture worker', approver='fixture worker')
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_independent_review_accepts_distinct_declared_actors(self):
        self.active_policy('independent-review')
        r = self.result()
        self.assertEqual(r['structural_status'], 'pass')
        self.assertEqual(r['production_readiness'], 'unassessed')

    def test_independent_review_rejects_same_actor(self):
        self.active_policy('independent-review', proposer='fixture reviewer', approver='fixture reviewer')
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_active_policy_needs_a_resolved_mode(self):
        for mode in [None, '', 'unspecified', {'not': 'a mode'}]:
            with self.subTest(mode=mode):
                self.active_policy(mode)
                if mode is None:
                    del self.data['policy']['approval_mode']
                self.assertEqual(self.result()['structural_status'], 'fail')

    def test_active_policy_needs_each_decision_field(self):
        for field in ['proposed_by', 'approved_by', 'approval_reference', 'authority_reference',
                      'adoption_reason', 'review_condition']:
            with self.subTest(field=field):
                self.active_policy('independent-review')
                del self.data['policy'][field]
                self.assertEqual(self.result()['structural_status'], 'fail')

    def test_proposed_policy_does_not_become_an_active_declaration(self):
        self.data['policy'] = {'status': 'proposed', 'proposed_by': 'fixture worker'}
        r = self.result()
        self.assertEqual(r['structural_status'], 'pass')
        self.assertFalse(any(x['check'] == 'GOV-01' for x in r['checks']))
        self.assertEqual(r['production_readiness'], 'unassessed')

    def test_consequential_change_needs_authority_and_recovery(self):
        self.data['change']['risk'] = 'external-effect'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_semver_rejects_numeric_prerelease_leading_zero(self):
        self.data['project']['version'] = '1.0.0-01'
        self.assertEqual(self.result()['structural_status'], 'fail')

    def test_semver_accepts_text_prerelease_with_leading_digit(self):
        self.data['project']['version'] = '1.0.0-01alpha+build.02'
        self.assertEqual(self.result()['structural_status'], 'pass')

    def test_human_review_is_a_declaration_not_attestation(self):
        for key in ['research_scope','customer_outcome','permissions','recovery_applicability']:
            self.data['human_review'][key]={'status':'reviewed','by':'fixture reviewer','reason':'illustrative','reference':'demo'}
        r=self.result()
        self.assertEqual(r['unknowns'],0)
        self.assertEqual(r['production_readiness'],'unassessed')

    def test_not_applicable_human_review_needs_a_named_reason_and_reference(self):
        self.data['human_review']['permissions'] = {
            'status': 'not-applicable', 'by': 'fixture reviewer',
            'reason': 'The fictional scope has no external collection or effect',
            'reference': 'fictional scope decision',
        }
        r = self.result()
        entry = next(x for x in r['checks'] if x['check'] == 'HUMAN-01' and x['subject'] == 'permissions')
        self.assertEqual(entry['status'], 'declared')
        self.assertEqual(r['unknowns'], 3)
        self.assertEqual(r['production_readiness'], 'unassessed')

    def test_incomplete_human_declaration_remains_unknown(self):
        self.data['human_review']['permissions'] = {'status': 'not-applicable', 'by': 'fixture reviewer'}
        entry = next(x for x in self.result()['checks'] if x['check'] == 'HUMAN-01' and x['subject'] == 'permissions')
        self.assertEqual(entry['status'], 'unknown')


if __name__ == '__main__':
    unittest.main()
