This repo is a set of Claude skills for building TONE3000 presets.
## Quickstart/
1. Clone the repo, then open Claude in the terminal. You should see the new skills immediately:
- `/tone-hunt <artist> - <song or album> [part]` is the main entry point. It lives in `.claude/skills/tone-hunt/`. Use it for any request like "get me Slash's tone on Appetite".
- `skill/tone3000-preset-builder/` is the engine skill. Read its `SKILL.md` before building anything.

## Engine

`skill/tone3000-preset-builder/scripts/t3k.py` does all the deterministic work. It is Python 3.8+ with no dependencies. Run it from the repo root:

```bash
python skill/tone3000-preset-builder/scripts/t3k.py <command>
```

Common commands: `presets-dir`, `prefs`, `rig "<artist>"`, `search "<term>" --gear <type>`, `tone <id>`, `build <recipe> --out <dir> --mono-only`, `verify <file>`, `list --dir <dir>`.

## Predefined rules

- What the user says in chat beats `user-rig.md`, which beats saved prefs, which beats skill defaults.
- Treat stored rigs and Tone IDs as leads. Check them live before building. Never invent IDs or model names.
- Do not swap in unrelated gear without asking. Say so when a capture is missing.
- Tell the user about effects NAM cannot capture (delay, chorus, phaser, wah, pitch).
- Verify every preset before reporting success. Report the file paths, the captures used and anything approximated.
- `login` is interactive and handles secrets. The user runs it in their own terminal. Never ask for, print or store API keys or tokens.
- Do not overwrite files in the user's TONE3000 preset folder. Bump the version instead.
- Do not bulk install presets or change preferences as a test. Use temporary folders.
- `out/` is scratch space for builds and is git ignored. Do not commit unless asked.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests are offline. No login needed.
