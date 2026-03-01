# Overview

## Purpose
Build a safe, noninvasive **species bridge** with sperm whales (odontocetes) by learning a compact symbol set over their click **codas** and **echolocation**. Your human‑legible UI uses **R–T–S**: **Rhythm** on XY, **Tempo** on ZX, **Spectrum** as color.

## Concept
- **Hardware:** A **tri‑segment dorsal tag** (“three C’s”) mounted by soft silicone suction cups. Each segment flexes relative to the next; flexures contain **piezo harvesters**. A low‑profile hydrophone + depth/IMU loggers capture audio and kinematics. The tag pops off on command or timer and floats for recovery.
- **Software:** A disentangled latent space separates **R** (inter‑click intervals) from **T** (local tempo) and **S** (spectral color). Short, safe **glyphs** (synth click phrases) enable limited two‑way prompts in managed settings.
- **Ethics & Safety:** Noninvasive mounts only; short playback at vetted levels; permitted work with partners; session caps and opt‑out behavior.

## MVP Goals
1. **Decode:** Classify sperm‑whale codas into a small **glyph bank** with ≥80% accuracy on held‑out sets; render in R–T–S UI.
2. **EchoGlyphs:** Show that sonar scans of distinct 3D totems fall into separable clusters in latent space.
3. **Energy:** Demonstrate piezo‑flex harvest extending logged mission time by ≥10% relative to no‑harvest baseline.
4. **Hydrodynamics:** Verify low added drag and reliable suction in tank/flume trials; clean auto‑release and recovery.

## Deliverables (v0)
- `Build_Print_EchoGlyph_Tag_v0.md` — mechanical/electrical envelope + BOM classes
- `UI_Spec_RTS_Mapping.md` — algorithms and rendering details
- `Firmware_State_Machine.md` — on‑tag logic
- `Data_Schema.json` — files and message formats
- `Test_Plan.md` — bench → flume → tank → field
- `Ethics_Permit_Checklist.md` — guardrails
