"""Portable declared-evidence gate. No command execution, network or global writes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import uuid

VERSION = '1.0.0'
MAX_FILE = 16 * 1024 * 1024
MAX_JSON = 1024 * 1024
MAX_RECEIPTS = 500
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', re.ASCII)


class Invalid(ValueError):
    pass


class Unresolved(ValueError):
    pass


def now():
    return datetime.now(timezone.utc)


def timestamp(value):
    if not isinstance(value, str):
        raise Invalid('Timestamp must be timezone-bearing text')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None:
            raise ValueError('timezone missing')
        return result.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise Invalid('Invalid timezone-bearing timestamp') from exc


def digest(data):
    return hashlib.sha256(data).hexdigest()


def text(value):
    return isinstance(value, str) and bool(value.strip())


def identity(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise Invalid('Identity must contain 1-64 letters, digits, underscores or hyphens')
    return value


def relative(value):
    if not text(value) or '\\' in value or ':' in value or any(ord(c) < 32 for c in value):
        raise Invalid('Use a canonical root-relative path with forward slashes')
    p = PurePosixPath(value)
    if not p.parts or p.is_absolute() or any(x in {'.', '..'} for x in p.parts) or p.as_posix() != value:
        raise Invalid('Absolute, traversal and non-canonical paths are refused')
    return p


def load(data):
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=unique,
                          parse_constant=lambda x: (_ for _ in ()).throw(Invalid('Nonfinite JSON value')))
    except Invalid:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise Invalid('Unreadable JSON') from exc


class Workspace:
    def __init__(self, root):
        if sys.version_info < (3,12):
            raise Invalid('Python 3.12+ is required for the supported filesystem checks')
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise Invalid('Project root must be a directory')

    def path(self, name, allow_missing=False):
        parts = relative(name).parts
        p = self.root
        for i, part in enumerate(parts):
            p = p / part
            try:
                info = p.lstat()
            except FileNotFoundError:
                if allow_missing and i == len(parts) - 1:
                    return p
                raise Unresolved('A path parent or required file is missing: ' + name)
            if stat.S_ISLNK(info.st_mode) or (hasattr(p, 'is_junction') and p.is_junction()):
                raise Invalid('Symlink/junction paths are refused: ' + name)
            if i < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
                raise Invalid('Path parent is not a directory: ' + name)
        return p

    def mkdir(self, name):
        p = self.root
        for part in relative(name).parts:
            p = p / part
            if not p.exists():
                p.mkdir(mode=0o700)
            # Recheck every new/existing prefix, including dangling links.
            self.path(p.relative_to(self.root).as_posix())
            if not p.is_dir():
                raise Invalid('Output parent is not a directory')

    def read(self, name, limit=MAX_FILE):
        p = self.path(name)
        before = p.stat()
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise Invalid('Only bounded regular files are supported: ' + name)
        with p.open('rb') as f:
            data = f.read(limit + 1)
        self.path(name)
        after = p.stat()
        key = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if len(data) > limit or key(before) != key(after) or len(data) != after.st_size:
            raise Unresolved('File changed during bounded read: ' + name)
        return data

    def fingerprint(self, name):
        data = self.read(name)
        return {'path': name, 'sha256': digest(data), 'bytes': len(data)}

    def create(self, name, value):
        relative(name)
        parent = PurePosixPath(name).parent.as_posix()
        self.mkdir(parent)
        p = self.path(name, allow_missing=True)
        data = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
        # Exclusive creation never overwrites an older record. Truncated JSON
        # after interruption fails parsing; this is not power-loss durability.
        with p.open('xb') as f:
            f.write(data)
        return name


def location(task):
    return '.principles/tasks/' + identity(task)


def read_task(ws, task):
    data = ws.read(location(task) + '/task.json', MAX_JSON)
    record = load(data)
    if not isinstance(record, dict) or record.get('schema_version') != VERSION or record.get('task_id') != task:
        raise Invalid('Task schema or identity is invalid')
    if record.get('state') not in ['draft', 'ready']:
        raise Invalid('Task state must be draft or ready; ready does not mean accepted')
    for field in ['outcome', 'beneficiary', 'scope', 'authority_reference', 'recovery']:
        value = record.get(field)
        if value is None or value == '':
            raise Unresolved('Resolve task field: ' + field)
        if not text(value):
            raise Invalid('Task field must be nonblank text: ' + field)
    subjects, checks = record.get('subjects'), record.get('checks')
    if not isinstance(subjects, list) or not isinstance(checks, list):
        raise Invalid('Subjects and checks must be arrays')
    if not subjects or not checks:
        raise Unresolved('Declare the selected subjects and acceptance checks')
    if len(subjects) > 128 or len(checks) > 64:
        raise Invalid('Task exceeds bounded subject/check limits')
    paths, ids = [], []
    for item in subjects:
        if not isinstance(item, dict) or item.get('kind') not in ['file', 'absent']:
            raise Invalid('Subject needs file/absent kind')
        paths.append(relative(item.get('path')).as_posix())
    for item in checks:
        if not isinstance(item, dict):
            raise Invalid('Check must be an object')
        ids.append(identity(item.get('id')))
        if item.get('criterion') is None or item.get('criterion') == '':
            raise Unresolved('Resolve acceptance criterion: ' + ids[-1])
        if not text(item.get('criterion')):
            raise Invalid('Criterion must be nonblank text')
        age = item.get('max_age_seconds')
        if age is not None and (type(age) is not int or age < 0):
            raise Invalid('Age limit must be a nonnegative integer or null for no TTL')
    if len(set(paths)) != len(paths) or len(set(ids)) != len(ids):
        raise Invalid('Duplicate subject path or check identity')
    if record['state'] == 'draft':
        raise Unresolved('Task is still draft')
    return record, digest(data)


def snapshot(ws, subjects):
    result = []
    for item in subjects:
        name = item['path']
        if item['kind'] == 'file':
            result.append(dict(ws.fingerprint(name), kind='file'))
        else:
            p = ws.path(name, allow_missing=True)
            if p.exists():
                raise Unresolved('Expected absent path now exists: ' + name)
            result.append({'path': name, 'kind': 'absent'})
    return result


def collector():
    return digest(Path(__file__).read_bytes())


def fingerprint_shape(item):
    if (not isinstance(item, dict) or type(item.get('bytes')) is not int
            or not 0 <= item['bytes'] <= MAX_FILE or not isinstance(item.get('sha256'),str)
            or not re.fullmatch('[0-9a-f]{64}',item['sha256'])):
        raise Invalid('Malformed file fingerprint')
    relative(item.get('path'))


def receipt_body(item):
    # Validate historical bodies too. Do not read old log files or require old
    # subjects to remain current; historical validity and current evidence differ.
    fingerprint_shape(item.get('evidence'))
    if (not text(item.get('method')) or item.get('execution_authenticity')!='unassessed'
            or not isinstance(item.get('collector_sha256'),str)
            or not re.fullmatch('[0-9a-f]{64}',item['collector_sha256'])):
        raise Invalid('Malformed receipt method, collector or authenticity claim')
    subjects=item.get('subjects')
    if not isinstance(subjects,list) or not 1 <= len(subjects) <= 128:
        raise Invalid('Malformed receipt subject set')
    paths=[]
    for subject in subjects:
        if not isinstance(subject,dict) or subject.get('kind') not in ['file','absent']:
            raise Invalid('Malformed receipt subject')
        paths.append(relative(subject.get('path')).as_posix())
        if subject['kind']=='file':fingerprint_shape(subject)
        elif set(subject)!={'kind','path'}:raise Invalid('Absence subject contains unexpected fields')
    if len(paths)!=len(set(paths)):raise Invalid('Duplicate receipt subject')


def initialize(ws, task):
    return ws.create(location(task) + '/task.json', {
        'schema_version': VERSION, 'task_id': task, 'state': 'draft',
        'outcome': None, 'beneficiary': None, 'scope': None,
        'authority_reference': None, 'recovery': None, 'subjects': [],
        'checks': [{'id': 'C-01', 'criterion': None, 'max_age_seconds': None}]})


def receipt(ws, task, check, result, evidence, method, observed=None, clock=None):
    clock = clock or now()
    record, task_hash = read_task(ws, task)
    if check not in {x['id'] for x in record['checks']} or result not in ['pass', 'fail', 'unknown'] or not text(method):
        raise Invalid('Receipt needs a known check, declared result and method')
    if observed is not None and timestamp(observed) > clock:
        raise Unresolved('Declared evidence observation is in the future')
    before = snapshot(ws, record['subjects'])
    log = ws.fingerprint(evidence)
    if before != snapshot(ws, record['subjects']) or read_task(ws, task)[1] != task_hash:
        raise Unresolved('Task or selected subjects changed during capture')
    rid = uuid.uuid4().hex
    value = {'schema_version': VERSION, 'receipt_id': rid, 'task_id': task,
             'task_sha256': task_hash, 'check_id': check, 'declared_result': result,
             'recorded_at': clock.isoformat(), 'evidence_observed_at': observed,
             'collector_sha256': collector(), 'subjects': before, 'evidence': log,
             'method': method, 'execution_authenticity': 'unassessed'}
    return ws.create(location(task) + '/receipts/' + rid + '.json', value)


def inspect(ws, task, clock=None):
    clock = clock or now()
    record, task_hash = read_task(ws, task)
    current = snapshot(ws, record['subjects'])
    bucket = location(task) + '/receipts'
    directory = ws.path(bucket, allow_missing=True)
    paths = [] if not directory.exists() else sorted(directory.iterdir())
    if len(paths) > MAX_RECEIPTS:
        raise Unresolved('Receipt bound exceeded; review and archive history explicitly')
    receipts = []
    for path in paths:
        if path.suffix != '.json':
            continue
        item = load(ws.read(path.relative_to(ws.root).as_posix(), MAX_JSON))
        if (not isinstance(item, dict) or item.get('schema_version') != VERSION
                or item.get('task_id') != task or not text(item.get('task_sha256'))
                or not text(item.get('receipt_id')) or not isinstance(item.get('check_id'),str)
                or not ID.fullmatch(item['check_id'])
                or not re.fullmatch('[0-9a-f]{64}',item['task_sha256'])
                or (item['task_sha256']==task_hash and item['check_id'] not in {c['id'] for c in record['checks']})
                or item.get('declared_result') not in ['pass', 'fail', 'unknown']):
            raise Invalid('Malformed or misbound receipt; old green cannot replace it')
        timestamp(item.get('recorded_at'))
        if item.get('evidence_observed_at') is not None:
            timestamp(item['evidence_observed_at'])
        receipt_body(item)
        receipts.append(item)
    if len({x['receipt_id'] for x in receipts}) != len(receipts):
        raise Invalid('Duplicate receipt identity')
    outcomes = []
    for criterion in record['checks']:
        candidates = [x for x in receipts if x['check_id'] == criterion['id'] and x['task_sha256'] == task_hash]
        status, reason = 'unknown', 'No receipt for this exact current task'
        if candidates:
            times = [timestamp(x['recorded_at']) for x in candidates]
            latest_time = max(times)
            latest = [x for x in candidates if timestamp(x['recorded_at']) == latest_time]
            if latest_time > clock:
                reason = 'Future receipt or backward clock; no fallback'
            elif len(latest) != 1:
                reason = 'Tied newest receipts; no inferred order'
            else:
                item = latest[0]  # Select newest BEFORE validity/result checks.
                if item.get('collector_sha256') != collector() or item.get('subjects') != current:
                    reason = 'Collector or selected subject set/content changed'
                elif not isinstance(item.get('evidence'), dict) or not text(item.get('method')):
                    status, reason = 'fail', 'Malformed newest evidence'
                elif ws.fingerprint(item['evidence'].get('path')) != item['evidence']:
                    status, reason = 'fail', 'Newest log bytes no longer match'
                else:
                    observed = item.get('evidence_observed_at')
                    age = criterion.get('max_age_seconds')
                    if observed is not None and (timestamp(observed) > clock or timestamp(observed) > timestamp(item['recorded_at'])):
                        reason = 'Evidence observed after recording or in the future'
                    elif age is not None and observed is None:
                        reason = 'Evidence observation time is unknown; recording time is not observation time'
                    elif age is not None and (clock - timestamp(observed)).total_seconds() > age:
                        reason = 'Newest evidence is stale; no fallback'
                    else:
                        status = item['declared_result']
                        reason = 'Declared result with matching local integrity; execution unassessed'
        outcomes.append({'check_id': criterion['id'], 'status': status, 'reason': reason})
    if current != snapshot(ws, record['subjects']) or task_hash != read_task(ws, task)[1]:
        raise Unresolved('Task or subjects changed during inspection')
    status = 'fail' if any(x['status'] == 'fail' for x in outcomes) else 'unknown' if any(x['status'] == 'unknown' for x in outcomes) else 'pass'
    return {'status': status, 'task_id': task, 'task_sha256': task_hash,
            'observed_at': clock.isoformat(), 'checks': outcomes,
            'claim': 'Selected declared results and local integrity only',
            'execution_authenticity': 'unassessed', 'authority': 'unassessed',
            'production_readiness': 'unassessed'}


def project_validation(ws, name):
    path = Path(__file__).parent / 'vendor/handbook/harness/validate.py'
    spec = importlib.util.spec_from_file_location('handbook_validator', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = ws.read(name, MAX_JSON)
    result = module.validate(load(data))
    result['input_sha256'] = digest(data)
    result['wrapper_status'] = 'fail' if result['failures'] else 'unknown' if result['unknowns'] else 'pass'
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['init', 'receipt', 'check', 'validate-project']:
        p = sub.add_parser(name)
        p.add_argument('--root', required=True, help='Explicit project root')
        p.add_argument('--task', required=True) if name != 'validate-project' else p.add_argument('--record', required=True)
        if name == 'receipt':
            p.add_argument('--check', required=True)
            p.add_argument('--result', choices=['pass', 'fail', 'unknown'], required=True)
            p.add_argument('--evidence', required=True)
            p.add_argument('--method', required=True)
            p.add_argument('--observed-at', help='Actual declared evidence observation time; never inferred from receipt time')
    args = parser.parse_args(argv)
    try:
        ws = Workspace(args.root)
        if args.command == 'init':
            output = {'status': 'draft-created', 'path': initialize(ws, args.task), 'acceptance': 'unresolved'}
        elif args.command == 'receipt':
            output = {'status': 'declared-receipt-recorded', 'path': receipt(ws, args.task, args.check, args.result, args.evidence, args.method, args.observed_at)}
        elif args.command == 'check':
            output = inspect(ws, args.task)
        else:
            output = project_validation(ws, args.record)
    except Unresolved as exc:
        output = {'status': 'unknown', 'reason': str(exc), 'production_readiness': 'unassessed'}
    except (Invalid, OSError, TypeError, OverflowError, KeyError, UnicodeError, RecursionError) as exc:
        output = {'status': 'fail', 'reason': str(exc), 'production_readiness': 'unassessed'}
    print(json.dumps(output, indent=2, ensure_ascii=True))
    status = output.get('wrapper_status') or output.get('status')
    return 1 if status == 'fail' else 2 if status == 'unknown' else 0


if __name__ == '__main__':
    raise SystemExit(main())
