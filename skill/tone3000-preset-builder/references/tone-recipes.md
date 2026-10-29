# Tone recipes: chain order, genre defaults and artist gear

The IDs below were checked live in September 2026. **Always run `tone ID` again before building.** Captures get deleted or made private. If one is gone, `search` for the make name and pick the most downloaded A2 capture that has a settings description. Model names here are regexes for the recipe `model` field.

## Chain order (left to right is signal flow)
1. **Compressor / outboard** (optional, for cleans and pop or funk, and it also glues rhythm): Lin76 FET `86750`
   (4:1 medium for rock, 8:1 fast for punk), LA-2A `69103` (cleans, country, worship).
2. **Drive**: boost/OD into an already-driven amp (TS9 `86314`, SD-1 `87914`, Klon `79454`),
   or the dirt itself into a clean amp (DS-1 `89559`, Big Muff `61106`, Rat `78883`,
   Fuzz Face `87219` "Silicon Fuzz Face", Rangemaster `31234`/`45843`).
3. **Amp**: an `amp-cab` capture (done) or an `amp` head plus step 4.
4. **Cab IR** (heads only): Greenback 4x12 `75087` (`0\.50in 0\.0in SA73`), V30 Mesa 4x12 `45023`,
   TJ3 pack `82871` (Marshall/Orange/Vox), Vox blue 2x12 `79866`, Fender 4x10 `61705`.
5. **Console/EQ** (optional studio sheen): Neve 1073LB `79572` "Line 0".
6. **Space**: Lexicon LXP-1 `87851` (room_small1/medium1/large1, room_plate_d, hall_b),
   Lexicon PCM91 `88473` ("Just Plate", "Large Chamber", "Wave NuHall"), Alabs Cetus `88038`
   (Room/Hall/Spring/Plate/Shimmer/Cloud), Sunset Sound plate `84558` ("WetDry").
Reverb mix guide: tight rock 0.12 to 0.18, classic rock 0.22 to 0.3, ballads and cleans 0.3 to 0.4.

## Stereo patterns
- **Dual amp** (most convincing): `branchAfter` is the last pedal and the right lane is a second amp with the same room.
- **Dual cab**: one head chain, branch after the head, and the right lane uses a different cab IR.
- **Dual room**: branch after the amp, and the right lane uses a different reverb IR at a similar mix.
- **Nu-metal and modern metal**: two independent full rigs (no `branchAfter`).

## Genre defaults
| Genre | Chain |
|---|---|
| Classic rock (70s Brit) | Lin76 → Klon/TS9 → Plexi/JCM800 → 1073 → room 0.25 |
| Grunge | DS-1 / Big Muff → Fender or Mesa → room 0.28 |
| Punk / pop-punk | Lin76 8:1 → SD-1 boost → Marshall BJA/JCM800 → small room 0.15 |
| Thrash / modern metal | TS9 D8 → Mark IIC+/Rectifier/5150 → small room 0.12 |
| Indie / Britpop | LA-2A → Klon mid → AC30 → 1073 → plate 0.3 |
| Clean studio / pop / worship | LA-2A → Deluxe/Twin/JC-120 → plate or hall 0.3 to 0.35 |
| Blues | TS9 D5 → Super Reverb / Bassman / Bluesbreaker → spring 0.3 |
| Post-grunge / nu-metal | 5150 or Rectifier full rig → small room 0.15, stereo = second rig |

## Artist gear map (starting points, check each one)
| Artist / song | Chain (left) | Stereo right lane |
|---|---|---|
| GNR - Sweet Child (Slash) | Lin76 4:1 → TS9 D5 → JCM800+V30 `87735` → 1073 → PCM91 plate | after amp: Cetus Plate |
| Nirvana - SLTS (chorus) | DS-1 `89559` CLASSIC (creator tagged "kurt cobain") → Super Reverb `88775` → room | after DS-1: In Utero Twin `65844` "Twin Reverb - STC 4038" |
| Led Zeppelin | Lin76 → Klon mid → JMP-50 '69 plexi `65578` → 1073 → LXP1 room_medium1 | PCM91 Large Chamber |
| Hendrix | Fuzz Face `87219` → '68 Super Lead `72145` → Cetus Spring | LXP1 room_large1 |
| Metallica (Puppets) | TS9 D8 → Mark IIC+ `81803` → 1073 → small room | after TS9: Dual Rec `69206` |
| Pink Floyd (Numb solo) | Big Muff T5 S5 → Hiwatt `53037` "Bright Overdrive - BLEND #1" → PCM91 chamber | Cetus Hall |
| Black Sabbath | Rangemaster `31234` V7_T5 → Laney TI100 `83324` "Iommy 2" → room | Cetus Room |
| Van Halen | "Van halen 1" `89490` → Sunset plate `84558` | Cetus Hall |
| Oasis | LA-2A → Klon mid → '64 AC30 `82521` → 1073 → LXP1 plate | after Klon: Marshall BJA `78832` v2 |
| RHCP (clean) | LA-2A → Deluxe Reverb `65227` → Cetus Spring | LXP1 hall_b |
| Green Day | Lin76 8:1 → SD-1 Boost-I → Marshall 1959BJA `78832` v2 (Billie Joe's settings) → small room | after SD-1: Rectifier RevG `79103` "Orange Crunch" |
| AC/DC | Plexi head `80875` "Driven" → Greenback 4x12 `75087` → small room | after head: TJ3 `82871` "69Mars412" |
| Smashing Pumpkins | Big Muff T7 S7 → Grace Corgan `59102` → room | after Muff: Soldano SLO `46269` "The King - SM57" |
| Pearl Jam | LA-2A → Klon high → Clapton Bassman `84556` → hall | after Klon: Plexi head + Greenback |
| Soundgarden (BHS clean) | JC-120 `10912` "Bright Off - SM57 & Royer" → Cetus Cloud | Cetus Plate |
| Foo Fighters (Everlong) | SD-1 Drive-II → Rectifier RevG "Orange Crunch" → room | after SD-1: '02 AC30 `70408` (Grohl's real pairing) |
| Radiohead (Creep) | LA-2A → '65 Twin `89797` CLEAN → spring | after LA-2A: 1961 AC30/4 `53601` |
| Coldplay | LA-2A → Klon mid → AC30 `70408` → hall | after Klon: Twin WARM |
| U2 (no delay possible!) | LA-2A → AC30 `70408` → Cetus Shimmer 0.4 | after LA-2A: Twin BRIGHT → Cloud |
| Pixies | JC-120 "Bright On, SM57$" → spring | DRRI `51649` "NEW VERSION.*No Room" → room |
| The Killers | SD-1 boost → Orange Rockerverb `88952` Mid → room | after SD-1: JCM800 |
| Jimmy Eat World | Rat `78883` Crunch → Rockerverb High → small room | after Rat: BJA |
| Feeder | SD-1 Drive-II → JCM800 → room | after SD-1: Rockerverb High |
| Creed / Seether / Puddle of Mudd | 5150 `84864` Red → small room | independent: Dual Rec `69206` |
| Limp Bizkit / Papa Roach | Dual Rec `69206` / 5150 Green → small room | independent second rig |
| Eagles (Hotel California) | LA-2A → Klon mid → Twin WARM → PCM91 plate | after Klon: Deluxe Reverb |
| SRV | TS9 D5 → Super Reverb `88775` → spring | after TS9: Twin WARM |
| Clapton (Beano) | Lin76 → JTM45 Bluesbreaker `77706` → room_medium1 | Bassman `84556` |
| Queen / Brian May | Rangemaster `45843` "rangemaster1500" → 1961 AC30/4 `53601` → PCM91 NuHall | after booster: '64 AC30 → Large Chamber |
| Tool | Diezel/Plexi/Bogner blend `88012` "BLEND 2" → room | independent: Diezel VH4 `89509` |
| Dire Straits | LA-2A → DRRI `51649` → Cetus Plate | after LA-2A: Twin CLEAN |
| Modern metal | TS9 D8 → Rectifier RevG "Molten Red" → small room | after TS9: 5150 Red |

## What NAM cannot capture
Delay (U2, Gilmour), chorus (Nirvana clean parts, Cure, Metallica cleans), phaser and flanger (EVH), tremolo, wah and rotary or Leslie (Black Hole Sun). Say so in the report, build the best static rig, and suggest the user add the effect in their DAW after TONE3000.
