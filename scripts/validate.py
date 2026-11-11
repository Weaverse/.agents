#!/usr/bin/env python3
"""Validate the team contract plus the upstream Agent Skills reference checks."""
import json
from pathlib import Path
import re
import sys
import tempfile

import yaml
from skills_ref import validate

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {'disable-model-invocation', 'argument-hint'}
MANUAL = {'create-task', 'fix-pr', 'ship', 'work'}


class UniqueLoader(yaml.SafeLoader):
    """Safe YAML, additionally rejecting duplicate mapping keys."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError('Mapping keys must be unique strings')
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def check_skill(path, reserved):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    if not match:
        return ['Missing or unclosed YAML frontmatter']
    try:
        data = yaml.load(match.group(1), Loader=UniqueLoader)
    except (yaml.YAMLError, ValueError) as error:
        return [f'Invalid frontmatter: {error}']
    if not isinstance(data, dict):
        return ['Frontmatter must be a mapping']
    errors = []
    name, description = data.get('name'), data.get('description')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        errors.append('name must be 1-64 ASCII lowercase/digit/single-hyphen characters')
    if name != path.parent.name:
        errors.append('name must equal folder name')
    if isinstance(name, str) and name in reserved:
        errors.append('name collides with a Claude Code built-in or bundled command')
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append('description must be a nonempty string of at most 1024 characters')
    elif not re.search(r'\buse when\b', description, re.I):
        errors.append('description must include a Use when trigger')
    metadata = data.get('metadata', {})
    if not isinstance(metadata, dict) or any(not isinstance(v, str) for v in metadata.values()):
        errors.append('metadata must be a string-to-string mapping')
    for key in ('license', 'compatibility', 'allowed-tools', 'argument-hint'):
        if key in data and not isinstance(data[key], str):
            errors.append(f'{key} must be a string')
    if 'disable-model-invocation' in data and not isinstance(data['disable-model-invocation'], bool):
        errors.append('disable-model-invocation must be a boolean')
    if path.parent.name in MANUAL and data.get('disable-model-invocation') is not True:
        errors.append('user-invoked workflow must set disable-model-invocation: true')
    if len(text.splitlines()) > 500:
        errors.append('SKILL.md exceeds 500 lines')
    if not text[match.end():].strip():
        errors.append('Skill body is empty')
    if not errors:
        # The reference rejects documented harness extensions. Validate the unchanged standard fields
        # in an ephemeral normalized skill; check the extension types above, never discard unknown fields.
        with tempfile.TemporaryDirectory(prefix='skill-validation-') as scratch:
            directory = Path(scratch) / name
            directory.mkdir()
            standard = {k: v for k, v in data.items() if k not in EXTENSIONS}
            (directory / 'SKILL.md').write_text('---\n' + yaml.safe_dump(standard) + '---\n' + text[match.end():])
            errors.extend(validate(directory))
    return errors


def main():
    reserved = set(json.loads((ROOT / 'scripts/claude-commands.json').read_text())['commands'])
    allowed = set(re.findall(r'^!/skills/([^/]+)/$', (ROOT / '.gitignore').read_text(), re.M))
    files = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    failures = []
    names = {path.parent.name for path in files}
    if allowed != names:
        failures.append('Skill folders and .gitignore allowlist differ; validate a clean team checkout')
    for path in files:
        errors = check_skill(path, reserved)
        for error in errors:
            failures.append(f'{path.relative_to(ROOT)}: {error}')
    team = (ROOT / 'rules/weaverse-team.md').read_text()
    if len(team.splitlines()) > 60:
        failures.append('Team file exceeds 60 lines')
    if not 20 <= len((ROOT / 'AGENTS.md').read_text().splitlines()) <= 30:
        failures.append('Contributor guide must be 20-30 lines')
    if (ROOT / 'commands').exists():
        failures.append('Retired commands/ directory must not exist')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'Validated {len(files)} skills: strict frontmatter, upstream skills-ref, command collisions and size budgets')
    return 0


if __name__ == '__main__':
    sys.exit(main())
