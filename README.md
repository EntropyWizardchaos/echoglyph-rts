# EchoGlyph R–T–S

A geometric visualization layer for sperm whale coda analysis. Decomposes click sequences into three orthogonal axes — **Rhythm**, **Tempo**, **Spectrum** — and renders them as navigable 2D spirals or 3D ribbons.

Designed to sit on top of existing bio-logger data (including [Project CETI](https://www.projectceti.org/) open-source tags). No new hardware required.

## Why geometry instead of transcription?

Current coda analysis represents clicks as discrete symbols — timing patterns, phonetic alphabets, letter transcriptions. This works, but it **flattens continuous structure**. A coda isn't a sequence of letters. It's a shape moving through frequency space over time.

R–T–S preserves what transcription drops:

| Axis | Source feature | Encoding |
|------|---------------|----------|
| **R** (Rhythm) | Normalized inter-click interval deviation | Y position (ribbon) or radial displacement (spiral) |
| **T** (Tempo) | Local tempo (moving average inverse ICI) | Z position (ribbon) or stroke width / dash frequency (spiral) |
| **S** (Spectrum) | Spectral centroid, bandwidth, amplitude | Color (hue = centroid, saturation = bandwidth, value = SNR) |

The result: each coda becomes a **visible shape** whose geometric properties (symmetry, torque, periodicity) correspond to acoustic properties that symbolic transcription compresses away.

## What's here

```
echoglyph-rts/
├── README.md
├── LICENSE
├── docs/
│   ├── overview.md              # Full system concept
│   ├── ui_spec_rts_mapping.md   # Axis definitions, rendering math, spiral mode
│   ├── tag_build_print.md       # Hardware envelope (tri-segment suction tag)
│   ├── firmware_state_machine.md
│   ├── data_schema.json         # Per-click feature format + UI packet spec
│   ├── test_plan.md             # Bench → flume → tank → field
│   └── ethics_permits.md
├── sim/
│   ├── sim_rts_coda_synth.py    # Synthetic coda generator + R–T–S renderer
│   └── outputs/                 # Example renders (auto-generated)
├── agents/
│   ├── wa_stages.md             # Per-whale agent lifecycle (S0–S6)
│   └── wa_stage_card.yaml       # Template stage card
├── tools/
│   ├── wa_stage_guard.py        # Stage card validator + SHA-256 hash
│   └── glyph_bank.json          # Starter glyph templates (5 symbols)
└── examples/
    ├── spiral_example.png
    └── ribbon_example.png
```

## Quick start

```bash
# Generate synthetic codas and R–T–S renders
cd sim
python sim_rts_coda_synth.py
# Outputs: sim/outputs/*.png + sim_metrics.json
```

Requires: `numpy`, `matplotlib`. No GPU. No special dependencies.

## How it connects to existing work

R–T–S is a **visualization and analysis layer**, not a competing pipeline. It takes the same per-click features that existing tools extract — ICI, spectral centroid, bandwidth, SNR — and maps them to geometric axes.

If you have bio-logger data with click timestamps and spectral features, you can render R–T–S views today. The `data_schema.json` specifies the expected input format.

### Integration with CETI bio-logger data

The CETI open-source bio-logger outputs multi-channel audio + behavioral data. R–T–S expects per-click features extracted from that audio. The pipeline:

1. **Your existing click detector** → timestamps + spectral features
2. **R–T–S renderer** → spiral or ribbon visualization
3. **Optional: glyph classifier** → nearest-centroid or learned clustering on R–T–S feature vectors

## The whale agent model

Each whale gets a persistent agent (`WA-<WhaleID>`) with:

- **Frozen core encoder** (shared R–T–S feature extraction)
- **Per-whale adapter** (small, fine-tuned on individual data)
- **Ethogram head** with veto priority over glyph labels
- **Append-only memory** (no overwrites, rollbacks allowed)
- **Metrics-gated promotion** through stages S0–S6

The ethogram head always wins. If the behavioral model predicts avoidance or stress, the system stands down — even if the glyph classifier is confident. See `agents/wa_stages.md` for full stage definitions and gate thresholds.

## Rendering modes

**Ribbon (3D):** Click index on X, rhythm deviation on Y, tempo on Z, spectrum as color. A coda traces a path through R–T–S space.

**Spiral (2D):** Polar coordinates. Angle = click index, radius = base growth + rhythm modulation, tempo encoded as stroke width or dash frequency, spectrum as color. Useful for print, social sharing, and quick pattern recognition.

Both views use identical features. Toggle in the UI.

## Design principles

- **Noninvasive only.** Suction-cup tags. No implants.
- **Cite or abstain.** Glyph classifications carry confidence scores. Below threshold = no label.
- **Ethogram veto.** Species-native behavior prediction overrides human-assigned meanings.
- **Append-only.** No overwriting whale agent memory. Drift is checked, not erased.
- **Translator, not mind reader.** R–T–S maps patterns. It does not infer beliefs or intent.

## License

CC BY 4.0 — Harley Robinson

## Citation

If you use R–T–S in your work:

```
Robinson, H. (2025). EchoGlyph R–T–S: Geometric visualization of sperm whale
coda structure. https://github.com/EntropyWizardchaos/echoglyph-rts
```
