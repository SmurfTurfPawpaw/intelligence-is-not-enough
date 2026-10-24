"""Required project-work gate over the unchanged declared-evidence collector.

No project command execution, networking, AI calls or global configuration writes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import principles as core

VERSION = '2.0.0'
PILLARS = tuple('P%02d' % i for i in range(1, 11))
RISKS = ('behavior', 'shared_contract', 'data_or_access', 'external_effect',
         'dependency_or_migration', 'recovery')
ALWAYS = {'P01', 'P05', 'P10'}


def collector():
    return core.digest(Path(__file__).read_bytes())


def names(task):
    folder = core.location(task)
    return folder + '/begin.json', folder + '/review.json'


def begin(ws, task, plan=None, small_reason=None):
    if bool(plan) == bool(small_reason):
        raise core.Invalid('Choose an existing material plan OR a concrete small-change reason')
    start, review = names(task)
    task_path = core.location(task) + '/task.json'
    plan_value = ws.fingerprint(plan) if plan else None
    # Create parents without overwriting any previous or interrupted start.
    ws.mkdir(core.location(task))
    for name in (start, review, task_path):
        if ws.path(name, allow_missing=True).exists():
            raise core.Invalid('Task/start already exists; preserve it and resume or use a new ID')
    stamp = core.now().isoformat()
    ws.create(start, {'workflow_version': VERSION, 'task_id': task,
                     'recorded_at': stamp, 'profile': 'material' if plan else 'small',
                     'small_reason': small_reason, 'plan': plan_value,
                     'workflow_sha256': collector(), 'core_sha256': core.collector()})
    ws.create(review, {'workflow_version': VERSION, 'task_id': task,
                      'reviewer': None, 'summary': None,
                      'no_impact': {key: None for key in RISKS},
                      'scope_checks': [],
                      'principles': [{'id': key, 'status': 'unknown',
                                      'reason': None, 'checks': []} for key in PILLARS]})
    subjects = [{'path': start, 'kind': 'file'}, {'path': review, 'kind': 'file'}]
    if plan:
        subjects.append({'path': plan, 'kind': 'file'})
    ws.create(task_path, {'schema_version': core.VERSION, 'task_id': task,
                         'state': 'draft', 'outcome': None, 'beneficiary': None,
                         'scope': None, 'authority_reference': None, 'recovery': None,
                         'subjects': subjects,
                         'checks': [{'id': 'C-01', 'criterion': None,
                                     'max_age_seconds': None}]})
    return {'status': 'created', 'task_id': task, 'profile': 'material' if plan else 'small',
            'task': task_path, 'begin': start, 'review': review,
            'claim': 'Draft records created; no acceptance or permission granted'}


def required_text(value, label):
    if not core.text(value):
        raise core.Unresolved('Resolve ' + label)
    if value.strip().casefold() in {'todo', 'tbd', 'unresolved', 'unknown', 'checked', 'n/a', 'na'}:
        raise core.Unresolved('Replace placeholder with a concrete ' + label)


def check_ids(value, known, label, required=False):
    if (not isinstance(value, list) or len(value) > 64
            or any(not isinstance(x, str) for x in value)
            or len(set(value)) != len(value)):
        raise core.Invalid('Expected unique bounded check IDs for ' + label)
    if any(not isinstance(x, str) or x not in known for x in value):
        raise core.Invalid('Unknown check reference for ' + label)
    if required and not value:
        raise core.Unresolved('Cite actual task evidence checks for ' + label)
    return value


def check(ws, task, clock=None):
    clock = clock or core.now()
    record, task_hash = core.read_task(ws, task)
    start_path, review_path = names(task)
    selected = {x['path'] for x in record['subjects'] if x['kind'] == 'file'}
    if not {start_path, review_path} <= selected:
        raise core.Invalid('Begin and review MUST remain selected file subjects')
    initial = core.snapshot(ws, record['subjects'])
    start = core.load(ws.read(start_path, core.MAX_JSON))
    review = core.load(ws.read(review_path, core.MAX_JSON))
    for obj in (start, review):
        if (not isinstance(obj, dict) or obj.get('workflow_version') != VERSION
                or obj.get('task_id') != task):
            raise core.Invalid('Missing or misbound workflow records')
    if core.timestamp(start.get('recorded_at')) > clock:
        raise core.Unresolved('Begin is future-dated or clock moved backward')
    if start.get('workflow_sha256') != collector() or start.get('core_sha256') != core.collector():
        raise core.Unresolved('Workflow/core changed since begin; preserve records and reassess')
    profile = start.get('profile')
    if profile == 'material':
        plan = start.get('plan')
        core.fingerprint_shape(plan)
        if plan['path'] not in selected:
            raise core.Invalid('Material plan MUST remain a selected file subject')
        if ws.fingerprint(plan['path']) != plan:
            raise core.Unresolved('Material plan changed after begin; admit a new task')
    elif profile == 'small':
        required_text(start.get('small_reason'), 'small-change scope reason')
        risks = review.get('no_impact')
        if not isinstance(risks, dict) or set(risks) != set(RISKS):
            raise core.Invalid('Small review needs all six impact classifications')
        if any(type(v) is not bool for v in risks.values()):
            raise core.Unresolved('Resolve every small-change impact classification')
        if not all(risks.values()):
            raise core.Unresolved('Consequential impact requires a material plan and new task')
    else:
        raise core.Invalid('Unknown work profile')
    required_text(review.get('reviewer'), 'attributed reviewer; disclose self-review')
    required_text(review.get('summary'), 'review summary and limits')
    known = {x['id'] for x in record['checks']}
    scope_checks = check_ids(review.get('scope_checks'), known, 'scope', profile == 'small')
    rows = review.get('principles')
    if (not isinstance(rows, list) or len(rows) != 10
            or any(not isinstance(x, dict) or not isinstance(x.get('id'), str) for x in rows)
            or {x['id'] for x in rows} != set(PILLARS)):
        raise core.Invalid('Review MUST resolve each P01-P10 exactly once')
    judgments = []
    for row in rows:
        key, state = row['id'], row.get('status')
        if state in ('unknown', 'fail'):
            judgments.append({'id': key, 'status': state})
            continue
        if state == 'unchanged' and profile == 'small':
            judgments.append({'id': key, 'status': state, 'checks': scope_checks})
            continue
        if state not in ('supported', 'not_applicable'):
            raise core.Invalid('Unsupported principle disposition: ' + key)
        if state == 'not_applicable' and key in ALWAYS:
            raise core.Invalid('Outcome, durable knowledge and accountability apply to every task')
        required_text(row.get('reason'), key + ' scoped judgment/reason')
        ids = check_ids(row.get('checks'), known, key, state == 'supported')
        judgments.append({'id': key, 'status': state, 'checks': ids})
    result = core.inspect(ws, task, clock)
    if any(x['status'] == 'fail' for x in judgments):
        result['status'] = 'fail'
    elif any(x['status'] == 'unknown' for x in judgments) and result['status'] != 'fail':
        result['status'] = 'unknown'
    if initial != core.snapshot(ws, record['subjects']) or task_hash != core.read_task(ws, task)[1]:
        raise core.Unresolved('Selected subjects or contract changed during workflow check')
    result.update(workflow_version=VERSION, profile=profile, principle_dispositions=judgments,
                  claim='Required workflow records, declared judgments and current selected evidence bindings',
                  semantic_adequacy='unassessed by the deterministic checker',
                  boundary='This command does not intercept other tools or grant approval')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('begin', 'check'):
        p = sub.add_parser(command)
        p.add_argument('--root', required=True)
        p.add_argument('--task', required=True)
        if command == 'begin':
            group = p.add_mutually_exclusive_group(required=True)
            group.add_argument('--plan')
            group.add_argument('--small-reason')
    args = parser.parse_args(argv)
    try:
        ws = core.Workspace(args.root)
        result = (begin(ws, args.task, args.plan, args.small_reason)
                  if args.command == 'begin' else check(ws, args.task))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
        return 1 if result['status'] == 'fail' else 2 if result['status'] == 'unknown' else 0
    except core.Unresolved as exc:
        print(json.dumps({'status': 'unknown', 'reason': str(exc)})); return 2
    except (core.Invalid, OSError, ValueError, RecursionError) as exc:
        print(json.dumps({'status': 'fail', 'reason': str(exc)})); return 1


if __name__ == '__main__':
    raise SystemExit(main())
