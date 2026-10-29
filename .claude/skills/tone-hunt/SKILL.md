---
name: tone-hunt
description: Hunt down a specific artist's guitar tone for a song or album, build it as a verified TONE3000 preset adapted to the guitarist's own guitar and interface, load it for audition, and run a review loop until the player approves it. Use when the user names an artist plus a song, album or era and wants that tone ("get me the Master of Puppets rhythm", "Slash on Appetite", "Gilmour's Comfortably Numb solo").
argument-hint: "<artist> - <song or album> [part: rhythm|lead|solo|clean] [notes]"
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, Bash(python skill/tone3000-preset-builder/scripts/t3k.py *)
---

# Tone hunt

Request: **$ARGUMENTS**

The goal is one tone the player can use on their own rig today. It should match what the artist really used, then get refined by the player's ears.

Work from the repo root. This skill runs the existing engine skill and does not replace it.

- Engine: `skill/tone3000-preset-builder/scripts/t3k.py`. Always run it as `python skill/tone3000-preset-builder/scripts/t3k.py ...` through the Bash tool.
- Rules: `skill/tone3000-preset-builder/SKILL.md` and its `references/`. Read that SKILL.md once at the start. Never write or patch `.t3kpreset` bytes by hand.

Order of authority: what the player says in chat, then `references/user-rig.md`, then saved `prefs`, then skill defaults.

## 1. Pin down the target

Find the **artist**, the **song or album** and, if given, the **part** (rhythm, lead, solo, clean, intro), the **era** (studio or live, year) and the use (solo track or quad tracked rhythm).

- If the artist or song is missing, ask before anything else.
- If only an album is given, build the album's main rhythm sound and say so.
- If the song uses very different rigs for different parts and no part was given, ask once with the parts as options. Put the signature part first and mark it "(Recommended)". If the rig is the same all the way through, do not ask.
- Do not ask about anything you can infer. State your assumption instead.

## 2. Load the player's gear

Run these offline checks together:

```text
python skill/tone3000-preset-builder/scripts/t3k.py presets-dir
python skill/tone3000-preset-builder/scripts/t3k.py prefs
python skill/tone3000-preset-builder/scripts/t3k.py rig "<artist>"
python skill/tone3000-preset-builder/scripts/t3k.py rig "<song or album>"
```

Read `skill/tone3000-preset-builder/references/user-rig.md`. It should describe the guitar, pickups, tuning, interface, DAW, monitoring and taste.

If it is still the blank template, ask once for the guitar, the pickups and how they monitor. Offer to save the answers to that file.

Monitoring sets the shape of the chain (see `references/intake.md`). Headphones or monitors need a cab. A real power amp and cab means DI mode (see `references/di-reamp-mode.md`).

Read prefs but never change them unless the player asks.

## 3. Research the original rig

Follow `references/gear-research.md`. Treat `rig` results as a lead and not as proof.

Run 2 to 4 targeted web searches for the exact song, album and era. Open primary sources where you can, such as interviews, studio rundowns and engineer accounts.

Collect:

- Guitar and pickups, tuning (and capo or half step), pedals in order, amp, mods, channel, cab and speakers, mic, studio processing and time based effects.
- A label for each item: **Documented** (with a source), **Reported** (forums or secondary sources) or **Inferred**.
- Any conflicts between sources and which one you followed.

Keep chat updates short. The findings go in the tone sheet (step 7).

## 4. Check catalog access

Run `python skill/tone3000-preset-builder/scripts/t3k.py whoami`.

- Logged in: go to step 5.
- Not logged in: do not invent Tone IDs. Look for a bundled preset with `list --dir "skill/tone3000-preset-builder/presets/artists"` (also `standard` and `di-reamp`) and offer a match as a stopgap. Tell the player to run `python skill/tone3000-preset-builder/scripts/t3k.py login` in their own terminal, then say "go on". Never ask for keys in chat. Stop until they do.

## 5. Hunt the captures

For each stage (drive, amp, cab, outboard, space), turn the gear into search terms using the table in `gear-research.md`. Then run `search "<term>" --gear <type> --n 8`. Widen the terms if nothing comes back. Inspect the best 2 or 3 candidates per stage with `tone <id>`.

Choose in this order:

1. Same gear, mod, channel and era as the research. Read the description and tags, not just the title. An `amp-cab` already has a cab. An `amp` needs a cab IR unless you are in DI mode.
2. A model whose settings match the record.
3. Fit for the player's gear. Use preferred brands and creators from prefs only as a tie breaker. Downloads and recency break any tie that is left.

If the documented gear has no capture, show the closest options and ask before building something quite different. Never swap gear silently.

**Adapting to the player's rig.** Keep the artist's character, then adjust.

- Passive pickups against an artist's active pickups (EMG and similar): pick a capture variant or add the documented boost. Do not just pile on gain. Watch transient and compression differences.
- Single coils into high gain: use a hotter variant or a boost. Humbuckers into vintage amps: use a lower gain variant.
- The player's taste in `user-rig.md` helps choose between faithful candidates. It does not change the target.
- Quad tracked rhythm: less gain than a solo tone, tight lows, mono, little or no reverb.
- Tuning: if the song's tuning differs from the player's usual, tell them to retune. NAM cannot shift pitch.

## 6. Build, verify and load for audition

Make a slug: lowercase `artist-song-part` in ASCII with hyphens. Keep every attempt in its own folder so the player can compare: `out/tone-hunt/<slug>/v1/`, `v2/` and so on. Name presets `<Artist> - <Song or Album> (<part>) v<N>`.

1. Write `out/tone-hunt/<slug>/v<N>/recipe.json` using `references/preset-format.md`. Take model regexes from the `tone` output you inspected. Keep unity gains and the engine's IR defaults unless you have a reason.
2. Build mono every time. Build stereo too if prefs voicing is `stereo` or `both`, or if the player asked, unless it is a quad tracked rhythm. Stereo needs a `stereo.right` lane built from the real rig (dual amp or dual cab).

   ```text
   python skill/tone3000-preset-builder/scripts/t3k.py build "out/tone-hunt/<slug>/v<N>/recipe.json" --out "out/tone-hunt/<slug>/v<N>" --mono-only --named
   python skill/tone3000-preset-builder/scripts/t3k.py build "out/tone-hunt/<slug>/v<N>/recipe.json" --out "out/tone-hunt/<slug>/v<N>" --stereo-only --named
   ```

3. Run `verify` on every file. You need at least one file, blocks above zero and no problems. If it fails, fix the recipe and rebuild. Use the filenames the build printed.
4. Copy each verified file into the folder from `presets-dir`. Never overwrite. If the same name exists, bump the version and rebuild. Verify the copies. If the folder does not exist, skip the copy and give the `out/` path.

## 7. Write the tone sheet and ask for review

Write `out/tone-hunt/<slug>/v<N>/TONE-SHEET.md` using [tone-sheet-template.md](tone-sheet-template.md).

Then reply in chat with a short version. Start with the result.

- The preset names to pick in the TONE3000 browser. Tell them to reopen the browser. The first load downloads model weights, so they need to be online.
- The chain, one line per block: gear, Tone ID, capture title, model, creator.
- What you adapted for their guitar and interface, and what is approximate.
- How to set up: pickup and position, tuning, interface gain with headroom, and any DAW effects for things NAM cannot do (delay, chorus, phaser, wah, pitch). Suggest a stock plugin if you know their DAW.
- The path to the tone sheet.

Then ask for a review with these options:

| Option | What happens |
| --- | --- |
| Nailed it | Approved. Go to step 9. |
| Close, needs tweaks | They describe it. Go to step 8. |
| Wrong character | Swap a capture. Go back to step 5 for the stage they name. |
| Haven't played it yet | Stop. They will come back with feedback. |

## 8. Revise

Turn the feedback into one or two changes that are easy to hear. Build them as the next version and keep the old one for comparison. Verify, copy, and go back to step 7. Say exactly what changed.

| They say | Try first |
| --- | --- |
| tighter or chuggier | A documented TS style boost in front, a tighter capture variant, less bass |
| less muddy | `toneBass` or `toneMid` down a notch, a brighter cab or mic model, less gain |
| brighter or more cut | `toneTreble` up, an SM57 style or brighter mic or cab model |
| less gain or less fizz | A lower gain model variant, `inGain` 0.45 to 0.4 (about -2.4 to -4.8 dB) |
| more aggressive | More mids and presence, a boost pedal, not more saturation |
| fuller or thicker | A bigger capture with less gain, `toneBass` up a little, dual cab stereo |
| too quiet or too loud | `outputLevel`, or `outGain` on the last block (0.5 is 0 dB, each 0.1 is 4.8 dB) |
| better for quad tracking | Less gain, tighter lows, mono, drop the space block |

Tone params run from 0 to 10 with 5 as flat. If the feedback is about the target (wrong part or wrong era), go back to step 1 or 3 instead of tweaking.

## 9. Wrap up

When they approve, give the final preset name and path. Then offer these, and do none of them unless asked:

- **Save the rig research** to memory. Write a profile JSON in the shape of the entries in `references/artist-rig-memory.json` (id, artist, song, year, genres, guitars, pedals, amp, cab, outboard, reverb, notes with sources and doubts, `t3k_chain`, stereo_strategy), then run `rig --add <file>`.
- **Remove old versions** from the TONE3000 preset folder. List the exact files first. The `out/` history stays.
- **Save a preference** they mentioned, using `prefs set`. Save only what they said.

Do not commit anything to git unless asked.
