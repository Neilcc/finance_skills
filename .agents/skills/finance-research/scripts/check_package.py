"""Static package integrity checks only; not a behavioral or investment backtest."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('SKILL.md', 'README.md', 'SOURCES.md', 'agents/openai.yaml',
            'references/evidence.md', 'references/research.md',
            'references/decisions.md', 'references/traders.md',
            'assets/decision-card.md', 'scripts/finance_math.py',
            'scripts/check_package.py', 'tests/test_finance.py', 'tests/acceptance.md')


def check(root: Path = ROOT) -> dict:
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append('missing: ' + name)
    for p in root.rglob('*'):
        if p.is_symlink():
            errors.append('symlink: ' + str(p.relative_to(root)))
    if errors:
        return {'status': 'failed', 'errors': errors}
    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n') or '\nname: finance-research\n' not in skill:
        errors.append('invalid skill front matter')
    if '\ndescription: ' not in skill:
        errors.append('missing skill description')
    for path in re.findall(r'(?:references|assets|scripts)/[A-Za-z0-9_.-]+', skill):
        if not (root / path).is_file():
            errors.append('broken reference: ' + path)
    declared = set(re.findall(r'\| (S\d+) \|', (root / 'SOURCES.md').read_text(encoding='utf-8')))
    for p in root.rglob('*.md'):
        used = set(re.findall(r'\bS\d{2}\b', p.read_text(encoding='utf-8')))
        if used - declared:
            errors.append(f'unknown source in {p.name}: {sorted(used - declared)}')
    try:
        manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
        hashes = manifest['files']
        if not isinstance(hashes, dict) or not hashes:
            raise ValueError('empty or malformed file manifest')
        actual = {str(p.relative_to(root)) for p in root.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
        if set(hashes) != actual:
            errors.append('manifest file set mismatch')
        for name, expected in hashes.items():
            rel = Path(name)
            if rel.is_absolute() or '..' in rel.parts:
                errors.append('unsafe manifest path')
                continue
            p = root / rel
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
                errors.append('hash mismatch: ' + name)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('manifest error: ' + str(exc))
    return {'status': 'passed' if not errors else 'failed', 'errors': errors,
            'scope': 'static_integrity_only_not_authenticity_or_strategy_validation'}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
