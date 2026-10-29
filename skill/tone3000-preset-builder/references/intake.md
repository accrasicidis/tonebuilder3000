# Intake: what to ask and what each answer changes

User instructions and saved preferences beat the defaults below. Only ask about things that change the build.

## 1. Target sound

| Ask | Why it matters |
| --- | --- |
| Artist, song, or a description ("thick 70s fuzz into a cranked Marshall") | Drives the whole gear choice |
| Which part of the track? (intro, verse, chorus, solo) | Many songs use two rigs. Creed "Higher" has a clean intro and a chorus wall. Everlong has a clean verse and a Mesa chorus. Comfortably Numb has a rhythm tone and a Big Muff solo. |
| Era, live or studio? | Slash's 1987 Appetite rig is not his later Jubilee rig. Metallica on Puppets (Mark IIC+) is not the Black Album (Rectifier style). |
| Their own tweaks ("more mids", "less fizz") | Pick another model variant or add an outboard EQ |

If they only name an artist, build the artist's most iconic rig and say which part you built.

## 2. Output format

- Mono, stereo or both. Use the saved voicing unless they ask for something else. Stereo needs a right lane and costs more CPU.
- Name. The default is `Artist - Song (part)`. Stereo adds ` [Stereo]`.

## 3. Their rig (this changes the chain shape)

| Setup | Chain rule |
| --- | --- |
| Interface to DAW or standalone, then studio monitors, headphones or FRFR | The chain must end in a cab. Use an `amp-cab` capture, or an `amp` head plus a `cab` IR. |
| A real guitar amp and cab, or the plugin used only for pedals or preamp in front of it | No cab in the chain. Amp-cab captures sound boxy here. Use `amp` heads or pedal only chains and skip room IRs. |
| A real power amp and real cab, and they only want the preamp digitally (they name cabs or speakers, or say "reamp") | DI mode. Read `di-reamp-mode.md`. No cab, no mic and no reverb. Find true DI or preamp only captures. Ask which real cab each chain feeds and put it in the preset name. |
| Bass | Search for bass captures (put `bass` in the query). Pedals and outboard gear are fine. |
| Recording a DI to reamp later, with no real cab yet | Pedal and preamp only. Tell them to add a cab later. |

You can detect some of this yourself. `python scripts/t3k.py presets-dir` shows the expected preset folder for the OS and whether it exists. It does not prove the plugin is installed, so do not ask about that. You do have to ask about interface, monitors and cabs, unless the rig is already known.

"No cab, add one later" and "no cab, ever, I have real hardware" are different. If they mention any real speaker, cab or power amp, that is DI mode and not just "no cab".

## 4. Guitar and pickups (optional)

- Single coils (Strat, Tele) into high gain: pick the amp's hotter variant or add a boost pedal.
- Humbuckers into vintage Marshall or Vox: pick the lower gain variant. The capture was probably made with humbuckers.
- 7 string or downtuned: prefer tight amps (5150, Rectifier, Diezel) and a TS style boost.

## Defaults when the user says "just make it"

Use the saved voicing and monitoring. If nothing is saved, assume FRFR (cab included), stereo, the song's signature part, unity levels and one room or plate reverb at about 30%. State every assumption in one line.
