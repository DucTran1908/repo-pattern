"""SPEC-001/AC-8: report reviewed instruction drift; never update the baseline."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def fingerprint(path):
    data = path.read_bytes().replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    return hashlib.sha256(data).hexdigest()


def check(root, manifest):
    errors = []
    if manifest.get('version') != 1 or not isinstance(manifest.get('pairs'), list) or not manifest['pairs']:
        return ['Invalid or empty compatibility manifest.']
    ids = set()
    for pair in manifest['pairs']:
        name = pair.get('id', '<missing>')
        if name in ids or name == '<missing>':
            errors.append('Missing/duplicate mapping id: ' + name)
        ids.add(name)
        if not pair.get('differences'):
            errors.append(name + ': review notes are missing')
        for side in ('source', 'target'):
            try:
                path = (root / pair[side]).resolve()
                path.relative_to(root.resolve())
                actual = fingerprint(path)
            except (KeyError, OSError, ValueError):
                errors.append('{}: missing or invalid {} file'.format(name, side))
                continue
            if actual != pair.get(side + '_sha256'):
                errors.append('{}: unreviewed {} drift in {}'.format(name, side, pair[side]))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--fingerprint', type=Path, help='Print one file digest for manual baseline review; does not write.')
    args = parser.parse_args()
    try:
        if args.fingerprint:
            print(fingerprint(args.root / args.fingerprint))
            return 0
        manifest = json.loads((args.root / '.codex/compatibility.json').read_text(encoding='utf-8'))
        errors = check(args.root, manifest)
    except (OSError, ValueError, TypeError) as exc:
        print('Compatibility check unavailable: {}'.format(exc), file=sys.stderr)
        return 1
    if errors:
        print('\n'.join(errors))
        print('Review behavior and intentional differences before manually updating hashes; no files were changed.')
        return 1
    print('Compatibility baseline matches ({} mappings). Semantic review is still required for new changes.'.format(len(manifest['pairs'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
