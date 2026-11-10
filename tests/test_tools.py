"""Offline tool behavior checks. All installer writes use disposable homes; no desktop notifications."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest(root):
    result = {}
    for path in sorted(root.rglob('*')):
        stat = path.lstat()
        kind = 'link' if path.is_symlink() else 'dir' if path.is_dir() else 'file'
        payload = os.readlink(path) if path.is_symlink() else path.read_bytes() if path.is_file() else None
        result[str(path.relative_to(root))] = (kind, payload, stat.st_mtime_ns, stat.st_ino)
    return result


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='agents-tools-')
        self.addCleanup(self.scratch.cleanup)
        self.tmp = Path(self.scratch.name)
        self.home = self.tmp / 'home with spaces'
        self.home.mkdir()
        (self.home / '.agents').symlink_to(ROOT, target_is_directory=True)
        self.env = dict(os.environ, HOME=str(self.home), PYTHON=sys.executable)

    def run_script(self, name, *args, data='', cwd=ROOT):
        return subprocess.run(['/bin/bash', str(ROOT / name), *args], cwd=cwd, env=self.env,
                              input=data, text=True, capture_output=True)

    def install(self, *args):
        result = self.run_script('scripts/install.sh', *args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def old_layout(self):
        claude = self.home / '.claude'
        claude.mkdir()
        for name in ('commands', 'skills', 'rules', 'statusline.sh'):
            (claude / name).symlink_to(self.home / '.agents' / name)
        return claude

    def test_fresh_home_links_team_skills_and_never_creates_settings(self):
        result = self.install()
        for skill in (ROOT / 'skills').glob('*/SKILL.md'):
            self.assertTrue((self.home / '.claude/skills' / skill.parent.name).samefile(skill.parent))
        for name in ('statusline.sh', 'claude-code-notifier.sh'):
            self.assertTrue((self.home / '.claude' / name).samefile(ROOT / name))
            self.assertTrue((ROOT / name).stat().st_mode & 0o111, 'Existing direct hook links need executable scripts')
        self.assertTrue((self.home / '.codex/AGENTS.md').samefile(ROOT / 'rules/weaverse-team.md'))
        self.assertFalse((self.home / '.claude/settings.json').exists())
        self.assertFalse((self.home / '.config').exists())
        self.assertIn('OpenCode:', result.stdout)
        self.assertIn('Cursor:', result.stdout)

    def test_old_readme_links_migrate_only_our_dangling_commands(self):
        claude = self.old_layout()
        settings = claude / 'settings.json'
        settings.write_text('{"personal":true}\n')
        before = settings.read_bytes()
        self.assertFalse((claude / 'commands').exists())
        self.install()
        self.assertFalse((claude / 'commands').is_symlink())
        self.assertTrue((claude / 'skills').samefile(ROOT / 'skills'))
        self.assertTrue((claude / 'rules').samefile(ROOT / 'rules'))
        self.assertEqual(settings.read_bytes(), before)

    def test_rerun_is_idempotent_including_inode_and_timestamp(self):
        self.install()
        before = manifest(self.home)
        self.install()
        self.assertEqual(manifest(self.home), before)

    def test_dry_run_writes_nothing_in_fresh_and_legacy_homes(self):
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                if legacy:
                    self.old_layout()
                before = manifest(self.home)
                self.install('--dry-run')
                self.assertEqual(manifest(self.home), before)

    def test_existing_personal_files_and_unrelated_links_survive(self):
        claude = self.home / '.claude'
        (claude / 'skills').mkdir(parents=True)
        (claude / 'rules').mkdir()
        personal = claude / 'skills/work'
        personal.write_text('keep personal skill')
        (claude / 'commands').symlink_to('unrelated-missing-directory')
        codex = self.home / '.codex'
        codex.mkdir()
        instructions = codex / 'AGENTS.md'
        instructions.write_text('keep personal instructions')
        self.install()
        self.assertEqual(personal.read_text(), 'keep personal skill')
        self.assertEqual(instructions.read_text(), 'keep personal instructions')
        self.assertEqual(os.readlink(claude / 'commands'), 'unrelated-missing-directory')

    def test_installer_does_not_write_through_config_directory_symlink(self):
        foreign = self.tmp / 'foreign'
        foreign.mkdir()
        (self.home / '.claude').symlink_to(foreign)
        self.install()
        self.assertEqual(list(foreign.iterdir()), [])

    def test_notifier_dry_run_treats_message_as_data(self):
        marker = self.tmp / 'must-not-exist'
        message = f'quotes " ; $(touch "{marker}") `touch "{marker}"`\nsecond line'
        result = self.run_script('claude-code-notifier.sh', '--dry-run',
                                 data=json.dumps(dict(hook_event_name='Notification', message=message)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'Claude Code: ' + message + '\n')
        self.assertFalse(marker.exists())

    def test_notifier_ignores_old_hook_events_and_rejects_bad_json(self):
        for event in ('Stop', 'SessionStart', 'SessionEnd'):
            result = self.run_script('claude-code-notifier.sh', '--dry-run',
                                     data=json.dumps(dict(hook_event_name=event, message='ignored')))
            self.assertEqual((result.returncode, result.stdout), (0, ''))
        result = self.run_script('claude-code-notifier.sh', '--dry-run', data='not-json')
        self.assertNotEqual(result.returncode, 0)

    def test_statusline_shows_context_defaults_and_untracked_dirty_state(self):
        directory = self.tmp / 'repository'
        directory.mkdir()
        subprocess.run(['git', 'init', '-q', '--initial-branch=testing', str(directory)], env=self.env, check=True)
        payload = dict(workspace=dict(current_dir=str(directory)),
                       context_window=dict(used_percentage=57, total_input_tokens=1200),
                       model=dict(display_name='Model\x1b[30m'))
        result = self.run_script('statusline.sh', data=json.dumps(payload))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('57% context', result.stdout)
        self.assertIn('testing (clean)', result.stdout)
        self.assertNotIn('\x1b', result.stdout)
        (directory / 'new-file').write_text('untracked')
        result = self.run_script('statusline.sh', data=json.dumps(payload))
        self.assertIn('testing (dirty)', result.stdout)
        result = self.run_script('statusline.sh', data='{}', cwd=self.tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('0% context', result.stdout)

    def test_validate_sh_rejects_a_bad_skill_in_a_disposable_tree(self):
        copy = self.tmp / 'invalid-copy'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))
        path = copy / 'skills/work/SKILL.md'
        path.write_text(path.read_text().replace('name: work', 'name: INVALID'))
        result = subprocess.run(['/bin/bash', 'scripts/validate.sh'], cwd=copy, env=self.env,
                                text=True, capture_output=True)
        print('Negative validate.sh exit:', result.returncode, result.stderr.strip())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('name must equal folder name', result.stderr)


class ReviewThreadTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module('review_threads', ROOT / 'skills/fix-pr/scripts/fetch-review-threads.py')

    def connection(self, nodes, cursor=None):
        return dict(nodes=nodes, pageInfo=dict(hasNextPage=cursor is not None, endCursor=cursor))

    def comment(self, label):
        return dict(id=label, url='public-comment', body='finding', createdAt='recent',
                    originalCommit=dict(oid='1' * 40), commit=dict(oid='2' * 40))

    def thread(self, label, resolved=False, outdated=False):
        return dict(id=label, isResolved=resolved, isOutdated=outdated, path='source.ts', line=1,
                    comments=self.connection([self.comment(label)]))

    def response(self, connection, head='2' * 40):
        return dict(repository=dict(pullRequest=dict(headRefOid=head, reviewThreads=connection)))

    def transport(self, responses):
        def run(command, **kwargs):
            self.assertEqual(command[:3], ['gh', 'api', 'graphql'])
            self.assertTrue(command[4].startswith('query=\nquery('))
            self.assertNotIn('mutation', command[4])
            self.assertTrue(kwargs['check'])
            result = subprocess.CompletedProcess(command, 0, stdout=json.dumps(responses.pop(0)))
            return result
        return run

    def test_filters_and_both_paginations_preserve_original_commit(self):
        live = self.thread('live')
        live['comments']['pageInfo'] = dict(hasNextPage=True, endCursor='comment-next')
        responses = [
            dict(data=self.response(self.connection([live, self.thread('closed', resolved=True),
                                                     self.thread('stale', outdated=True)], 'thread-next'))),
            dict(data=dict(node=dict(comments=self.connection([self.comment('second-comment')])))),
            dict(data=self.response(self.connection([self.thread('second-thread')]))),
            dict(data=dict(repository=dict(pullRequest=dict(headRefOid='2' * 40)))),
        ]
        with patch.object(self.module.subprocess, 'run', side_effect=self.transport(responses)) as transport:
            result = self.module.collect('Owner', 'Repo', 1)
        self.assertEqual([t['id'] for t in result['threads']], ['live', 'second-thread'])
        self.assertEqual(len(result['threads'][0]['comments']), 2)
        self.assertEqual(result['threads'][0]['comments'][0]['original_commit_id'], '1' * 40)
        self.assertEqual(result['threads'][0]['comments'][0]['commit_id'], '2' * 40)
        self.assertIn('cursor=comment-next', transport.call_args_list[1].args[0])
        self.assertIn('cursor=thread-next', transport.call_args_list[2].args[0])
        self.assertEqual(responses, [])

    def test_head_movement_and_graphql_errors_emit_no_partial_stdout(self):
        scenarios = [
            [dict(data=self.response(self.connection([self.thread('live')]))),
             dict(data=dict(repository=dict(pullRequest=dict(headRefOid='3' * 40))))],
            [dict(errors=[dict(message='denied')], data=None)],
        ]
        for responses in scenarios:
            with self.subTest(responses=len(responses)), \
                    patch.object(self.module.subprocess, 'run', side_effect=self.transport(responses)), \
                    patch.object(sys, 'argv', ['fetch-review-threads.py', 'Owner/Repo', '1']), \
                    contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.module.main(), 1)
                self.assertEqual(output.getvalue(), '')

    def test_repeated_cursor_is_a_failure_not_a_loop(self):
        connection = self.connection([], 'same')
        responses = [dict(data=self.response(connection)), dict(data=self.response(connection))]
        with patch.object(self.module.subprocess, 'run', side_effect=self.transport(responses)):
            with self.assertRaisesRegex(ValueError, 'pagination cursor'):
                self.module.collect('Owner', 'Repo', 1)


class FrontmatterTests(unittest.TestCase):
    def test_portability_limits_cannot_be_accepted_by_upstream_coercion(self):
        module = load_module('skill_validation', ROOT / 'scripts/validate.py')
        cases = [
            ('name: review\ndescription: Use when reviewing\n', 'review', 'collides'),
            ('name: other\ndescription: Use when working\n', 'example', 'equal folder'),
            ('name: example\ndescription: ' + 'x' * 1025 + '\n', 'example', '1024'),
            ('name: example\ndescription: Use when working\nmetadata:\n  value: [tool]\n', 'example', 'metadata'),
            ('name: example\ndescription: Use when working\nmetadata:\n  value: 1\n', 'example', 'metadata'),
            ('name: example\nname: example\ndescription: Use when working\n', 'example', 'unique'),
            ('name: ' + 'x' * 65 + '\ndescription: Use when working\n', 'x' * 65, '1-64'),
            ('name: example\ndescription: Use when working\n', 'example', '500'),
            ('name: work\ndescription: Use when working\n', 'work', 'disable-model-invocation'),
        ]
        with tempfile.TemporaryDirectory(prefix='invalid-skills-') as temporary:
            for frontmatter, name, expected in cases:
                with self.subTest(expected=expected):
                    folder = Path(temporary) / name
                    folder.mkdir(exist_ok=True)
                    path = folder / 'SKILL.md'
                    body = 'body\n' * (501 if expected == '500' else 1)
                    path.write_text('---\n' + frontmatter + '---\n' + body)
                    self.assertIn(expected, '\n'.join(module.check_skill(path, {'review'})))


if __name__ == '__main__':
    unittest.main()
