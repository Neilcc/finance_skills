"""Static package integrity checks only; not a behavioral or investment backtest."""
from __future__ import annotations
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('SKILL.md', 'README.md', 'SOURCES.md', 'agents/openai.yaml',
            'references/evidence.md', 'references/research.md',
            'references/decisions.md', 'references/traders.md',
            'references/serenity.md', 'assets/decision-card.md',
            'scripts/finance_math.py', 'scripts/check_package.py',
            'tests/test_finance.py', 'tests/acceptance.md')


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
    if 'version: "0.3.0"' not in skill:
        errors.append('unexpected skill version')
    for path in re.findall(r'(?:references|assets|scripts)/[A-Za-z0-9_.-]+', skill):
        if not (root / path).is_file():
            errors.append('broken reference: ' + path)
    declared = set(re.findall(r'\| (S\d+) \|', (root / 'SOURCES.md').read_text(encoding='utf-8')))
    for p in root.rglob('*.md'):
        used = set(re.findall(r'\bS\d{2}\b', p.read_text(encoding='utf-8')))
        if used - declared:
            errors.append(f'unknown source in {p.name}: {sorted(used - declared)}')
    try:
        meta = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
        if meta.get('version') != '0.3.0':
            errors.append('manifest version mismatch')
    except (OSError, ValueError, TypeError) as exc:
        errors.append('manifest error: ' + str(exc))
    return {'status': 'passed' if not errors else 'failed', 'errors': errors,
            'scope': 'static_structure_only_not_authenticity_behavior_or_strategy_validation'}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
