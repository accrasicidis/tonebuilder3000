# DI and reamp mode

For players with their own power amp and real cabs. They do not want TONE3000 to do the cab or mic. They want the preamp character digitally, then they reamp it into their hardware.

Switch to this mode when the user mentions real speaker cabinets, a separate power amp, or something like "I use a real rig". Treat it as its own rig type in `intake.md`, not as a version of "real guitar amp".

## What to ask

- Which real cab or speaker will each chain feed? This does not change the search, but it confirms DI mode. Put it in the preset name so they can tell chains apart later.
- Any preference among boutique makers, or "surprise me" within a budget.
- Genre and feel. This still decides the pedals.

## Default chain: no cab, no mic

For a preamp-only DI chain, leave out `cab` and `space` (room mic) blocks. The chain ends at the amp's preamp stage. The real power amp and cab handle everything after that. A cab IR or reverb here would double the signal path and defeat the purpose.

If the user asks for a different routing, follow it and describe any departure from this default.

## Finding true DI or preamp-only captures

`amp-cab` captures already include a mic'd cab, so they are the wrong type here. Search `gear=amp` (head or preamp only) and look for these markers in the title, tags and description.

| Marker | Meaning |
| --- | --- |
| `DI`, `BAL DI`, `DI-ready` | Direct out. No cab in the signal at all. |
| `preamp`, `preamp-only`, `preamp capture` | Preamp stage only. It may still assume a power amp and cab after it, so read the description. |
| `reamp-ready`, `no ir included`, `no cab` | An explicit statement. Highest confidence. |
| No mention of cab or mic anywhere (no "SM57", "Royer", "MD421", "cab") | A weak hint. Check with `tone ID` and read the description for reamp intent. |

Reject anything that names a mic (SM57, MD421, Royer, U87) or a cab spec (4x12, V30, Greenback). That means a cab is baked in.

Past direct capture candidates (inspect again before use):

- **Two-Rock SSS Clean BAL DI** (`4658`)
- **Diezel VH4** (`53749`, tagged `di-ready`, `reamp-ready` and `poweramp-capture`)

Both are `gear=amp` with no mic or cab, according to earlier notes. A direct capture can still include the power amp. A `poweramp-capture` tag does not prove it is preamp only, so check which stages the capture covers before using it with a real power amp.

Treat these as patterns to match and not as a fixed list. Boutique brands come and go on TONE3000 (Two-Rock, Bad Cat, Friedman, Wizard, Revv, Diezel, Category 5, Komet, Carr, Cornell). Search the brand the user names first.

## Genre notes

These players care about touch and dynamics and the feel of a real amp. Use fewer, better chosen pedals.

- **Hendrix:** Fuzz Face (`1531`, verified) into a clean to edge of breakup boutique DI amp, low mix.
- **Stoner, doom, fuzz:** Pro Co RAT 2 (`45294`, tagged stoner and doom) or a Big Muff into a higher gain boutique DI (Diezel, Friedman). Skip the noise gate unless asked. This style wants the amp's own sag.
- **Boutique clean platform:** No pedals. LA-2A (`69103`) into the DI capture is often the whole request. These players are the pedal.

## Recipe shape

A `chain` with no `space` or `cab` entries. The recipe format needs nothing special.

```json
{"name": "Hendrix Boutique DI - Fuzz into Two-Rock (feeds real 1x12 Greenback)",
 "chain": [{"tone": 1531}, {"tone": 4658}]}
```

Name each preset after the real cab it feeds when the user has more than one. The plugin does not know a physical cab exists, so the name is the only way to tell them apart.
