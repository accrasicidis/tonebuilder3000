---
name: tone3000-preset-builder
description: Build and verify TONE3000 .t3kpreset files from artist guitar tones, songs, or amp/cab/pedal capture requests. Use for TONE3000 rig recreation, capture selection, mono/stereo guitar chains, preamp-only DI/reamp chains, preset inspection, and tone preferences.
---

# TONE3000 Preset Builder

Use `scripts/t3k.py` (Python 3.8+, standard library only) for all deterministic work. Never write binary presets by hand.

What the user says in the current request beats the defaults below and any saved preferences. Paths are relative to this file. The commands below assume this skill's folder is the current directory. You can also call the script by its full path.

## 1. Understand the tone

If you are building for the user's own guitar, read [user-rig.md](references/user-rig.md) first. Use it to read requests like "tighter", "brighter", "less muddy", "more aggressive" or "better for quad tracking". If the file is still blank, ask for the basics.

Run these offline reads:

```text
python scripts/t3k.py presets-dir
python scripts/t3k.py prefs
python scripts/t3k.py rig "artist or song"
```

A missing preset folder does not mean the plugin is missing. Use an explicit `--out` folder if needed.

Read [intake.md](references/intake.md) when the song part, monitoring setup, pickups or voicing change the build. Use what you already know, ask only about gaps that matter, and state your assumptions.

Preferences rank brands and creators in search. You still have to apply amp, drive and cab choices and the monitoring rules yourself. To search for something a saved default would filter out, use `search --no-prefs`. Only save preference changes the user asked for (`prefs set`, `prefs template`, `prefs sync`). Sync needs API access. Preferences are read from `T3K_PREFERENCES_FILE`, then `.t3kpreferences.json` or `preferences.json` in the working folder, then the OS TONE3000 config folder.

## 2. Reuse a bundled preset or build a new one

**Bundled presets.** If one matches, find it with `list --dir "presets/artists"` (or `standard`, `di-reamp`), verify it, and copy only that file. Do not overwrite existing presets. This works offline. Use `install-templates --category ... --out ...` only if the user wants a whole category.

**New presets.** Live catalog access is required, even when rig memory has IDs. Use `whoami` to check the login. If login is needed, the user runs `python scripts/t3k.py login` in their own terminal. See [api.md](references/api.md). Never ask for keys in chat, show credential files, or put keys in recipes, commands, logs or packages.

Use [artist-rig-memory.json](references/artist-rig-memory.json) (through `rig`) and [artist-rig-library.md](references/artist-rig-library.md) as starting points. For new or era specific rigs, follow [gear-research.md](references/gear-research.md) and prefer primary interviews and rundowns. Mark what is documented and what is guessed. Never invent Tone IDs or model names, and never assume an old ID still exists.

Keep three things apart when recreating an artist:

1. The gear the artist really used.
2. The closest captures available on TONE3000 today.
3. Adjustments for the player's own guitar and interface. For example, passive pickups are not the same as active EMGs. Account for output, transient and compression differences without just adding gain.

Keep the artist's character. Do not bend it to fit default preferences.

Search and inspect:

```text
python scripts/t3k.py search "mark iic" --gear amp-cab --n 8
python scripts/t3k.py tone 81803
```

The ID above is only an example. Inspect each tone's models, tags, format and description. Pick the model with a specific regex and not by index. If the gear is not available, explain the gap and do not swap in something unrelated. If you are offline and no bundled preset matches, say the capture lookup could not be done. Do not claim a custom build.

## 3. Design the chain

Read [tone-recipes.md](references/tone-recipes.md) for chain order and starting gear, and [preset-format.md](references/preset-format.md) for the recipe format, stereo routing and gain rules.

Normal order: optional compressor, boost or drive, then amp, then cab if needed, then optional outboard EQ, then a space IR. An `amp-cab` capture already has the cab, so do not add another. An `amp` needs a cab IR for headphones or monitors. Leave out any stage the real rig did not have.

For a real power amp and cab, read [di-reamp-mode.md](references/di-reamp-mode.md). Preamp-only DI needs evidence that the capture has no power amp, cab or mic. A `DI` tag alone is not enough. Leave out cab, mic and space blocks by default.

NAM cannot recreate delay, chorus, phaser, wah or pitch shift. Say which effect is missing. A static capture or a space IR does not recreate movement.

Keep the engine's gain defaults (unity, with cab compensation, and space mix 0.3) unless the target needs a change. For stereo, use different but matching blocks in the right lane. `branchAfter` is a zero based index into the left lane. Leave it out for two independent lanes. Never make up a model or download URL.

## 4. Build and verify

Write the recipe as UTF-8 JSON. Always pass the output folder and voicing flags so saved defaults cannot change the result:

```text
python scripts/t3k.py build "recipe.json" --out "out/my-tone" --mono-only --named
python scripts/t3k.py verify "out/my-tone/My Tone.t3kpreset"
```

Use the real filename the build prints. For stereo, use `--stereo-only` with a recipe that has `stereo.right`. For both, run once with each flag. `--copy-to` makes extra named copies and does not change the main output folder. `--named` can overwrite files with the same name, so use a fresh output folder. Without `--out`, the build writes straight into the real TONE3000 preset folder.

Do not report success until you have at least one file and every delivered file passes `verify`. The check covers file structure, active model and URL presence. It does not prove the download still works or that it sounds right. Fix failures and rebuild.

In your report, give the preset paths, lane order, exact captures and models, sources, and anything approximate. Tell the user to reopen the TONE3000 preset browser and that model weights download on first use.

## Saving research

`rig --add profile.json` adds or replaces a researched rig in this skill's memory. Do it when the user wants the research saved, and record sources and doubts. When testing, use temporary folders and isolated config paths. Never install whole libraries or overwrite the user's preferences just to test.
