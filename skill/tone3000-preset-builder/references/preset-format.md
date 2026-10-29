# Recipe format and the .t3kpreset file

## Recipe (the input to `t3k.py build`)

```json
{
  "name": "Artist - Song (part)",
  "chain": [ { "tone": 86314, "model": "D5-T6", "mix": 1.0, "outGain": 0.5, "inGain": 0.5, "enabled": true, "slimSize": 0.5 } ],
  "stereo": { "branchAfter": 1, "right": [ { "tone": 88038, "model": "Plate", "mix": 0.3 } ] },
  "params": { "toneTreble": 6.0 }
}
```

- `tone` (required) is the TONE3000 tone ID.
- `model` is a case-insensitive regex matched against model names. The first match wins. Leave it out to use the first model. Escape regex characters (`0\\.50in`, `Boost-I$`).
- `mix` runs from 0 to 1. The default is 1.0 and spaces use 0.3.
- `outGain` and `inGain` run from 0 to 1. **0.5 is 0 dB and each 0.1 is 4.8 dB** (range is plus or minus 24 dB). Defaults are unity. Cab IRs use 0.66 (+7.7 dB) to offset the plugin's -18 dB pad on short IRs.
- `slimSize` runs from 0 to 1 and picks the NAM A2 size tier. 0.5 is full size and 0 is the lite version for weak CPUs.
- `stereo.branchAfter` is a zero based index into `chain`. The right lane is fed by the output of that left block. Leave it out for an independent right chain where both lanes get the input. `right` blocks use the same fields.
- `params` overrides the faceplate in the plugin's own units:
  - `outputLevel` and `inputLevel`: 0 to 1 (0.5 is 0 dB)
  - `toneBass`, `toneMid`, `toneTreble`: 0 to 10 (5 is flat)
  - `toneEqEnabled`, `gateEnabled`: 0 or 1
  - `gateThreshold`: dB
  - `chainPanLeft`, `chainPanRight`: 0 to 1
  - `spreadEnabled` (mono widener) and `alignEnabled`
- A file can hold one recipe or a list of them. `build` writes `name` for mono and `name [Stereo]` when `stereo` is present.

## How each gear type behaves

| Gear | Platform | Type | Notes |
| --- | --- | --- | --- |
| amp-cab | nam | nam | Complete. Do not add a cab. |
| amp | nam | nam | Head only. Needs a `cab` IR after it for FRFR or monitors. |
| cab | ir | ir | The plugin applies a -18 dB pad. The script adds +7.7 dB. |
| pedal, outboard | nam | nam | Unity gain, mix 1.0. |
| space | ir | ir | Reverb and room IRs. The plugin defaults long IRs to 50%. The script uses 30%. |

## The file on disk (why you never write it by hand)

A `.t3kpreset` starts with the magic bytes `T3KB`, followed by a JUCE `ValueTree::writeToStream` binary tree. The layout was checked against the plugin source (`PresetManager.cpp`) and JUCE (`juce_ValueTree.cpp`, `juce_Variant.cpp`).

```text
T3KPreset {schemaVersion:int=1, name:string}
  ChainSnapshot {stereoEnabled:bool, branchSide:"left", branchAfterBlockId:string}
    ChainBlocks       [ChainBlock...]        (left lane)
    RightChainBlocks  [ChainBlock...]        (right lane)
  Params [Param {id, value:double}...]       (optional, defaults apply if missing)
ChainBlock {id:32-hex uuid, type:"nam"|"ir"|"insert", enabled, normalize, slimSize, inputGain,
            outputGain, mix, toneId:int, toneJson:string, activeModelId:int}
  [Eq]  (optional, flat if absent)  [ModelCache] (optional embedded bytes, downloaded if missing)
```

Strings are UTF-8 with a trailing NUL. `var` values are `compressedInt(len)`, then a marker byte, then the payload. Markers: int=1 (int32 little endian), boolTrue=2, boolFalse=3, double=4 (f64 little endian), string=5, int64=6, binary=8. A `compressedInt` is one size byte (bit 7 means negative) followed by that many little endian bytes.

Use `t3k.py verify FILE` to parse any preset, including your own.
