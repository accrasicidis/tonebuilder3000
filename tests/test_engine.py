"""Offline engine tests. They never read the user's auth or preference files."""
import contextlib
import copy
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
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skill' / 'tone3000-preset-builder'
SCRIPT = SKILL / 'scripts' / 't3k.py'
spec = importlib.util.spec_from_file_location('t3k', SCRIPT)
t3k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t3k)


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='tone3000 engine test ')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        env = {k: v for k, v in os.environ.items() if not k.startswith('T3K_')}
        env.update(T3K_AUTH_FILE=str(self.work / 'auth.json'),
                   T3K_PREFERENCES_FILE=str(self.work / 'preferences.json'),
                   APPDATA=str(self.work / 'config'),
                   XDG_CONFIG_HOME=str(self.work / 'config'), PYTHONUTF8='1')
        self.env = env
        patcher = mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        guard = mock.patch.object(t3k.urllib.request, 'urlopen',
                                  side_effect=AssertionError('Network forbidden in offline tests'))
        guard.start()
        self.addCleanup(guard.stop)

    def cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                cwd=self.work, env=self.env, capture_output=True,
                                text=True, encoding='utf-8', timeout=30)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def main(self, *args):
        with mock.patch.object(sys, 'argv', [str(SCRIPT), *map(str, args)]), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            t3k.main()
        return output.getvalue()

    def fixture_recipe(self, stereo=False):
        # Reuse actual embedded catalog metadata from a bundled preset, without API calls.
        preset = next((SKILL / 'presets' / 'standard').glob('*.t3kpreset'))
        tree = t3k.Reader(preset.read_bytes()[4:]).node()
        snap = next(c for c in tree['children'] if c['type'] == 'ChainSnapshot')
        chain, cache = [], {}
        for block in snap['children'][0]['children']:
            p = block['props']
            tone = json.loads(p['toneJson'])
            model = next(m for m in tone['models'] if m['id'] == p['activeModelId'])
            chain.append({'tone': tone['id'], 'model': '^' + t3k.re.escape(model['name']) + '$'})
            cache[tone['id']] = (tone, tone['models'])
        recipe = {'name': 'Test fixture', 'chain': chain}
        if stereo:
            recipe['stereo'] = {'branchAfter': 0, 'right': [chain[-1]]}
        path = self.work / 'recipe.json'
        path.write_text(json.dumps(recipe), encoding='utf-8')
        return path, cache

    def test_help_and_offline_reads(self):
        self.assertIn('package-skill', self.cli('--help').stdout)
        self.assertIn('--include-presets', self.cli('package-skill', '--help').stdout)
        rigs = json.loads(self.cli('rig', 'list', '--json').stdout)
        self.assertGreaterEqual(len(rigs), 80)
        self.assertTrue(json.loads(self.cli('rig', 'Metallica', '--json').stdout))
        self.assertIn('profiles', json.loads(self.cli('prefs', '--json').stdout))
        self.cli('presets-dir')
        self.cli('list', '--dir', SKILL / 'presets' / 'di-reamp')
        self.assertFalse((self.work / 'auth.json').exists())
        self.assertFalse((self.work / 'preferences.json').exists())

    def test_all_bundled_presets(self):
        presets = list((SKILL / 'presets').rglob('*.t3kpreset'))
        self.assertEqual(len(presets), 272)
        for preset in presets:
            with self.subTest(preset=preset.name):
                name, blocks, problems = t3k.verify(preset, quiet=True)
                self.assertTrue(name)
                self.assertGreater(blocks, 0)
                self.assertEqual(problems, [])
        self.assertIn('OK', self.cli('verify', presets[0]).stdout)

    def test_verifier_failure_exit_status(self):
        path = self.work / 'empty.t3kpreset'
        path.write_bytes(t3k.preset_bytes('Empty', [], [], False, None, None))
        self.assertIn('FAILED', self.cli('verify', path, success=False).stdout)
        path.write_bytes(b'not a preset')
        self.cli('verify', path, success=False)

    def test_default_stereo_preference_builds_mono_recipe(self):
        recipe, cache = self.fixture_recipe()
        with mock.patch.dict(t3k._cache, cache, clear=True):
            output = self.main('build', recipe, '--out', self.work / 'output', '--named')
        self.assertIn('1 preset file(s)', output)
        preset = next((self.work / 'output').glob('*.t3kpreset'))
        self.assertEqual(t3k.verify(preset, quiet=True)[2], [])
        tree = t3k.Reader(preset.read_bytes()[4:]).node()
        self.assertFalse(tree['children'][0]['props']['stereoEnabled'])

    def test_explicit_mono_and_stereo_preserve_routing(self):
        recipe, cache = self.fixture_recipe(stereo=True)
        with mock.patch.dict(t3k._cache, cache, clear=True):
            for flag in ('--mono-only', '--stereo-only'):
                self.main('build', recipe, '--out', self.work / 'output', flag)
        files = list((self.work / 'output').glob('*.t3kpreset'))
        self.assertEqual(len(files), 2)
        snaps = [t3k.Reader(p.read_bytes()[4:]).node()['children'][0] for p in files]
        stereo = next(s for s in snaps if s['props']['stereoEnabled'])
        self.assertEqual(stereo['props']['branchAfterBlockId'],
                         stereo['children'][0]['children'][0]['props']['id'])
        self.assertTrue(stereo['children'][1]['children'])

    def test_impossible_or_empty_build_fails_before_network(self):
        recipe, _ = self.fixture_recipe()
        self.cli('build', recipe, '--stereo-only', success=False)
        self.cli('build', recipe, '--mono-only', '--stereo-only', success=False)
        recipe.write_text('[]', encoding='utf-8')
        self.cli('build', recipe, success=False)

    def test_build_verification_failure_exit_status(self):
        recipe, cache = self.fixture_recipe()
        with mock.patch.dict(t3k._cache, cache, clear=True), \
                mock.patch.object(t3k, 'verify', return_value=('Broken', 1, ['missing model'])):
            with self.assertRaises(SystemExit) as error:
                self.main('build', recipe, '--out', self.work / 'output', '--mono-only')
        self.assertEqual(error.exception.code, 1)

    def test_package_relative_path_and_full_contents(self):
        # The parent containing "presets" used to cause the whole archive to be empty.
        isolated = self.work / 'presets development' / 'tone3000-preset-builder'
        shutil.copytree(SKILL, isolated, ignore=shutil.ignore_patterns('__pycache__'))
        (isolated / 'auth.json').write_text('{}', encoding='utf-8')
        (isolated / 'preferences.json').write_text('{}', encoding='utf-8')
        script = isolated / 'scripts' / 't3k.py'
        for full in (False, True):
            args = ['package-skill', '--out', 'package.zip']
            if full:
                args.append('--include-presets')
            result = subprocess.run([sys.executable, str(script), *args], cwd=self.work,
                                    env=self.env, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(self.work / 'package.zip') as archive:
                names = archive.namelist()
                for name in ('SKILL.md', 'scripts/t3k.py',
                             'references/artist-rig-library.md', 'LICENSE'):
                    self.assertIn(name, names)
                    self.assertEqual(archive.read(name), (isolated / name).read_bytes())
                self.assertNotIn('auth.json', names)
                self.assertNotIn('preferences.json', names)
                self.assertEqual(sum(n.endswith('.t3kpreset') for n in names), 272 if full else 0)
                self.assertIsNone(archive.testzip())

    def test_templates_copy_to_isolated_directory(self):
        with contextlib.redirect_stdout(io.StringIO()):
            written = t3k.install_templates('di-reamp', str(self.work / 'presets'))
        self.assertEqual(len(written), 8)
        for path in written:
            self.assertEqual(t3k.verify(path, quiet=True)[2], [])
            self.assertEqual(Path(path).read_bytes(),
                             (SKILL / 'presets' / 'di-reamp' / Path(path).name).read_bytes())

    def test_preferences_write_only_to_isolated_config(self):
        self.cli('prefs', 'set', '--monitoring', 'di-reamp', '--voicing', 'mono')
        prefs = json.loads(self.cli('prefs', '--json').stdout)
        defaults = prefs['profiles'][prefs['active_profile']]['defaults']
        self.assertEqual(defaults['monitoring'], 'di-reamp')
        self.assertEqual(defaults['voicing'], 'mono')
        self.assertTrue((self.work / 'preferences.json').exists())
        self.assertFalse((self.work / 'auth.json').exists())


if __name__ == '__main__':
    unittest.main()
