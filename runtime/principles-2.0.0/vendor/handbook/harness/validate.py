"""Local companion validator. Checks supplied records; performs no external actions."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re


SEMVER = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$', re.ASCII)
PROFILES = {'private-tool', 'shared-service', 'research', 'authorized-investigation'}
SCHEMA_VERSION = '2.0.0'
VALIDATOR_VERSION = '0.2.0'


def timestamp(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.astimezone(timezone.utc) if parsed.tzinfo else None
    except (ValueError, OverflowError):
        return None


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def finite_number(value):
    # Python integers are finite; converting a large one to float can overflow.
    return type(value) is int or (type(value) is float and math.isfinite(value))


def validate(record, now=None):
    """Treat all assertions as supplied evidence, not trusted provider attestation."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('The evaluation clock must include a timezone')
    checks = []

    def check(identity, passed, message, subject='project', status=None):
        checks.append({'check': identity, 'status': status or ('pass' if passed else 'fail'),
                       'subject': subject, 'message': message})

    if not isinstance(record, dict):
        check('CORE-01', False, 'Project input must be a JSON object')
        return report(checks, now)
    check('CORE-01', record.get('schema_version') == SCHEMA_VERSION, 'Recognized record schema '+SCHEMA_VERSION)
    project = record.get('project')
    if not isinstance(project, dict):
        check('CORE-02', False, 'Project brief is missing or invalid')
        return report(checks, now)
    check('CORE-02', all(nonempty(project.get(k)) for k in ['id', 'purpose', 'owner', 'scope']),
          'Purpose, accountable owner, identity and scope are explicit')
    people = project.get('beneficiaries')
    check('CORE-03', isinstance(people, list) and bool(people) and all(nonempty(x) for x in people),
          'Intended beneficiaries are identified')
    check('CORE-04', project.get('profile') in PROFILES, 'A supported contextual profile is selected')
    version = project.get('version')
    check('CORE-05', isinstance(version, str) and bool(SEMVER.fullmatch(version)),
          'The declared interface version has valid SemVer syntax; compatibility is not inferred')

    components = record.get('components')
    if not isinstance(components, list) or not components:
        check('CORE-06', False, 'At least one accountable component is needed')
        components = []
    ids = [c.get('id') for c in components if isinstance(c, dict)]
    valid_ids = [x for x in ids if nonempty(x)]
    check('CORE-06', len(valid_ids) == len(components) and len(set(valid_ids)) == len(valid_ids),
          'Component identifiers are present and unique')
    by_id = {c['id']: c for c in components if isinstance(c, dict) and nonempty(c.get('id'))}

    for index, component in enumerate(components):
        if not isinstance(component, dict):
            check('CORE-07', False, 'Component must be an object', str(index))
            continue
        cid = component.get('id', str(index))
        check('CORE-07', all(nonempty(component.get(k)) for k in ['purpose', 'owner', 'canonical_record', 'revision']),
              'Component purpose, ownership, authoritative record and revision are declared', cid)
        cost = component.get('maintenance', {})
        numeric = isinstance(cost, dict) and all(finite_number(cost.get(k)) for k in ['low', 'high'])
        valid_cost = (numeric and 0 <= cost['low'] <= cost['high'] and nonempty(cost.get('basis'))
                      and nonempty(cost.get('unit')) and nonempty(cost.get('review_trigger'))
                      and cost.get('kind') in ['estimate', 'measurement'])
        if isinstance(cost, dict) and cost.get('unit') == 'weekly_ai_allocation_percent':
            valid_cost = valid_cost and nonempty(cost.get('denominator')) and cost.get('high', 101) <= 100
        check('CORE-08', valid_cost, 'Maintenance has a bounded estimate or measurement with basis and review trigger', cid)
        check('CORE-09', nonempty(component.get('reconsider_when')), 'A useful reassessment trigger is recorded', cid)

    links = record.get('links', [])
    if not isinstance(links, list):
        check('CORE-10', False, 'Dependencies must be an explicit list')
        links = []
    for index, link in enumerate(links):
        check('CORE-10', isinstance(link, dict) and link.get('from') in by_id and link.get('to') in by_id
              and nonempty(link.get('reason')), 'Dependency endpoints and reason are known', str(index))

    decisions = record.get('decisions')
    check('CORE-11', isinstance(decisions, list) and bool(decisions), 'At least the selected approach is recorded')
    if isinstance(decisions, list):
        for index, decision in enumerate(decisions):
            valid = isinstance(decision, dict) and all(nonempty(decision.get(k)) for k in ['id', 'reason', 'status', 'revisit_when'])
            check('CORE-11', valid, 'Decision retains reason, status and review condition', str(index))

    changes = record.get('change', {})
    affected = changes.get('affected_components', []) if isinstance(changes, dict) else []
    check('CORE-12', isinstance(affected, list) and bool(affected) and all(x in by_id for x in affected)
          and nonempty(changes.get('outcome')) and isinstance(changes.get('verification'), list)
          and bool(changes['verification']) and all(nonempty(x) for x in changes['verification']),
          'Change declares outcome, affected components and nonempty verification statements')
    if isinstance(changes, dict) and changes.get('risk') in ['external-effect', 'difficult-to-reverse']:
        check('RISK-01', nonempty(changes.get('recovery')) and nonempty(changes.get('authority_reference')),
              'Consequential change declares recovery and current authority reference; authority authenticity remains unassessed')

    evidence = record.get('observations', [])
    if not isinstance(evidence, list):
        check('OBS-01', False, 'Observations must be a list')
        evidence = []
    evidence_ids = [x.get('id') for x in evidence if isinstance(x, dict)]
    check('OBS-01', len(evidence_ids) == len(evidence) and all(nonempty(x) for x in evidence_ids)
          and len(set(evidence_ids)) == len(evidence_ids), 'Observation identities are present and unique')
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            check('OBS-02', False, 'Observation must be an object', str(index))
            continue
        eid = item.get('id', str(index))
        target = by_id.get(item.get('component'))
        check('OBS-02', target is not None and nonempty(item.get('collector')),
              'Observation is bound to a known component and collector', eid)
        observed = timestamp(item.get('observed_at'))
        max_age = item.get('max_age_seconds')
        well_timed = observed is not None and finite_number(max_age) and max_age >= 0
        if not well_timed:
            check('OBS-03', False, 'Observation time or freshness budget is invalid', eid)
            continue
        if observed > now:
            check('OBS-03', False, 'Observation lies in the future relative to this evaluation clock', eid)
            continue
        if not target or item.get('subject_revision') != target.get('revision'):
            check('OBS-04', False, 'Observation does not describe the current declared revision', eid, status='unknown')
        elif (now-observed).total_seconds() > max_age:
            check('OBS-04', False, 'Observation is stale; a historical pass is not current coverage', eid, status='unknown')
        else:
            state = item.get('result')
            check('OBS-04', state == 'pass', 'Current scoped observation result: '+str(state), eid,
                  status=state if state in ['pass', 'fail', 'unknown'] else 'fail')

    for cid, component in by_id.items():
        if component.get('needs_current_observation') is True:
            found = [x for x in evidence if isinstance(x, dict) and x.get('component') == cid]
            check('OBS-05', bool(found), 'Required current-observation coverage is present' if found else 'Observation coverage is missing',
                  cid, status=None if found else 'unknown')

    sync = record.get('synchronization', {})
    if isinstance(sync, dict) and sync.get('enabled') is True:
        check('SYNC-01', all(nonempty(sync.get(k)) for k in ['authority', 'identity', 'ordering', 'deduplication', 'reconciliation', 'disconnection']),
              'Push synchronization has identity, order, deduplication and missed-update recovery contracts')
        if sync.get('delivery_claim') == 'universal-exactly-once':
            check('SYNC-02', False, 'A universal exactly-once delivery claim is unsupported by this specification')

    policy = record.get('policy', {})
    if isinstance(policy, dict) and policy.get('status') == 'active':
        proposer = policy.get('proposed_by')
        approver = policy.get('approved_by')
        mode = policy.get('approval_mode')
        declared = all(nonempty(policy.get(k)) for k in [
            'proposed_by', 'approved_by', 'approval_reference', 'authority_reference',
            'adoption_reason', 'review_condition'])
        if mode == 'owner-adoption':
            valid = declared and approver == project.get('owner')
        elif mode == 'independent-review':
            valid = declared and proposer != approver
        else:
            valid = False
        check('GOV-01', valid,
              'Active policy resolves its declared adoption mode, actors, authority and decision records; actual authority, authenticity and runtime activation remain unassessed')

    required = ['research_scope', 'customer_outcome', 'permissions', 'recovery_applicability']
    reviews = record.get('human_review', {})
    for identity in required:
        entry = reviews.get(identity) if isinstance(reviews, dict) else None
        valid = isinstance(entry, dict) and entry.get('status') in ['reviewed', 'not-applicable']
        if valid:
            valid = all(nonempty(entry.get(k)) for k in ['by', 'reason', 'reference'])
        check('HUMAN-01', valid, 'Human judgement supplied for '+identity if valid else 'Human judgement remains needed for '+identity,
              identity, status='declared' if valid else 'unknown')
    return report(checks, now)


def report(checks, now):
    failures = sum(x['status'] == 'fail' for x in checks)
    unknown = sum(x['status'] == 'unknown' for x in checks)
    return {
        'validator_version': VALIDATOR_VERSION, 'evaluated_at': now.isoformat(),
        'scope': 'Supplied local records only; no provider, deployed system or real-world approval attestation',
        'structural_status': 'fail' if failures else 'pass',
        'evidence_status': 'incomplete' if unknown else 'bounded-records-present',
        'production_readiness': 'unassessed', 'failures': failures, 'unknowns': unknown,
        'checks': checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--at', help='Explicit timezone-bearing evaluation time for reproducible fixtures')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    at = timestamp(args.at) if args.at else datetime.now(timezone.utc)
    if at is None:
        parser.error('--at requires a timezone-bearing ISO timestamp')
    try:
        raw = args.project.read_bytes()
        data = json.loads(raw)
        result = validate(data, at)
        result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    except (OSError, ValueError, TypeError) as exc:
        result = {'structural_status': 'fail', 'production_readiness': 'unassessed',
                  'error': f'{type(exc).__name__}: {exc}', 'evaluated_at': at.isoformat()}
    output = json.dumps(result, indent=2, ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding='utf-8')
    print(output)
    return 1 if result['structural_status'] == 'fail' else 0


if __name__ == '__main__':
    raise SystemExit(main())
