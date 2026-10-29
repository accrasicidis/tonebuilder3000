"""Offline checks that the /tone-hunt skill points at files and commands that exist."""
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / '.claude' / 'skills' / 'tone-hunt'
SKILL_MD = SKILL_DIR / 'SKILL.md'
ENGINE = 'skill/tone3000-preset-builder/scripts/t3k.py'


def frontmatter(text):
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise AssertionError('missing YAML frontmatter')
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(':')
        fields[key.strip()] = value.strip().strip('"')
    return fields


class ClaudeSkillTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL_MD.read_text(encoding='utf-8')

    def test_frontmatter(self):
        fields = frontmatter(self.text)
        self.assertEqual(fields['name'], SKILL_DIR.name)
        self.assertTrue(fields['description'])
        self.assertLessEqual(len(fields['description']), 1024)
        self.assertIn('$ARGUMENTS', self.text)
        self.assertIn(f'Bash(python {ENGINE} *)', fields['allowed-tools'])

    def test_referenced_paths_exist(self):
        docs = self.text + (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
        paths = set(re.findall(r'skill/tone3000-preset-builder/[\w./-]+[\w]', docs))
        self.assertIn(ENGINE, paths)
        for path in sorted(paths):
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).exists(), path)
        for name in re.findall(r'`references/([\w.-]+)`', self.text):
            with self.subTest(reference=name):
                self.assertTrue((ROOT / 'skill/tone3000-preset-builder/references' / name).exists())
        for link in re.findall(r'\]\(([\w.-]+\.md)\)', self.text):
            with self.subTest(link=link):
                self.assertTrue((SKILL_DIR / link).exists())

    def test_engine_commands_exist(self):
        help_text = subprocess.run([sys.executable, str(ROOT / ENGINE), '--help'],
                                   capture_output=True, text=True, encoding='utf-8',
                                   timeout=30, check=True).stdout
        # Every engine subcommand the workflow relies on must still exist.
        for command in ('presets-dir', 'prefs', 'rig', 'whoami', 'login', 'list',
                        'search', 'tone', 'build', 'verify'):
            with self.subTest(command=command):
                self.assertRegex(self.text, rf'\b{command}\b')
                self.assertRegex(help_text, rf'(?m)^\s+{command}\b')

    def test_claude_md_mentions_skill(self):
        claude = (ROOT / 'CLAUDE.md').read_text(encoding='utf-8')
        self.assertIn('/tone-hunt', claude)


if __name__ == '__main__':
    unittest.main()
