# Gear research: check the real rig before designing a chain

`tone-recipes.md` is a starting map. For anything not in it, or when the user wants a specific era or album, research the real gear first. Do not invent a chain from memory.

## Search

Use whatever web search you have to find artist interviews and primary rig rundowns. If Equipboard blocks automated access, use indexed search results to find sources you can open. Do not try to get around the block. Treat snippets as leads and open the primary source when you can. If you cannot check a source, say it is unverified. Do not assume a specific tool or browser is installed. If you are offline, use the stored memory and say the data is historical.

Run 2 to 4 targeted searches, one per gear category:

```text
<artist name> equipboard pedals
<artist name> equipboard amplifier
<artist name> pedalboard rig <song or album>
<artist name> guitar rig <song or album> interview
```

Look for exact model names, which album, tour or song they belong to, and any quote from the player about why they chose it. A Rat instead of a Tube Screamer changes the chain, not just one block. Rig rundowns often disagree. Say so, and follow the best supported account. That is usually the one several independent sources repeat, or the one tied to the song in question.

## Turn real gear into a TONE3000 search

Model names rarely match capture titles. Try the shortest distinctive part first, then widen.

| Real gear | Try first | Then |
| --- | --- | --- |
| ProCo Rat or Rat 2 | `rat` with `--gear pedal` | `proco rat` |
| Ibanez Tube Screamer TS-9 or TS808 | `ts9` or `ts808` with `--gear pedal` | `tube screamer` |
| Marshall JMP 2203 or 1959 SLP | `jmp` or `super lead` with `--gear amp-cab` | `marshall plexi` |
| Mesa Boogie Mark IIC+ | `mark iic` with `--gear amp-cab` | `mesa boogie iic` |
| Diezel VH4 | `vh4` with `--gear amp-cab` | `diezel` |
| MXR Phase 100 or Distortion+ | the model number with `--gear pedal` | brand plus short name |
| Boss NS-2 or TU-3 (gate, tuner) | Skip. These do not shape tone. The plugin's own gate covers the NS-2. | |

Always run `python scripts/t3k.py tone ID` before using a result. A matching title is not proof. Read the description and tags to confirm the exact amp, cab or pedal.

## How research changes the chain

A rig rundown can show that the static map guessed wrong.

- **Amp only, no pedal.** Some eras have no drive pedal at all. Hetfield after 1985 is an example: the gain comes from the preamp. Do not force a drive block in.
- **Modulation and pitch gear.** Whammy, Phase 100 and chorus cannot be captured by NAM. Name them as a limit in the report, the same way `tone-recipes.md` does for delay and chorus.
- **Two amps blended.** Diezel plus Plexi plus Bogner, or any dual amp rig, maps to two chains. That is what the stereo branch in `preset-format.md` is for.

## Worked example

James Hetfield:

- Ride the Lightning era: Ibanez TS-9 into a Marshall JMP-50 (`72145`, "SL68 I Drive").
- Kill 'Em All era: ProCo Rat (`78883`) into a modded Marshall plexi.
- Master of Puppets era: Mesa Mark IIC+ (`81803`), no pedal.
- Later Diezel era: Diezel VH4 (`89509`), no pedal.

All four IDs were already in `tone-recipes.md` and `examples/library.json`. Research confirmed the picks. That is the point of this step. It turns a plausible guess into a checked one, and sometimes it disagrees with the guess.

## Report the evidence briefly

Keep updates short. In the final report, cite the sources behind the gear choice (for example "per rig rundowns from the Ride the Lightning era"). Only include the detail where it is interesting or where you had to choose between conflicting accounts.
