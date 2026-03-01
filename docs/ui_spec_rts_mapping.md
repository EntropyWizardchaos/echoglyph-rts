# UI Spec — R–T–S Mapping & Rendering

## Inputs
Per‑click features extracted from on‑tag audio:
- **ICI** (inter‑click interval), **tempo** (local inverse ICI), **centroid** (Hz), **bandwidth** (Hz), **SNR/amplitude**.

## Axes
- **XY (Rhythm):** Y = normalized ICI deviation. X = click index (or time).
- **ZX (Tempo):** Z = normalized local tempo (moving average inverse ICI).
- **Color (Spectrum):** hue = spectral centroid; saturation = bandwidth; value = amplitude/SNR.

## Rendering
- Draw a **3D ribbon**; XY panel shows rhythmic motif; ZX panel shows breathing of tempo.
- **Stroke width:** classifier confidence.
- **Halo/blur:** arousal proxy (click‑rate variance).
- **Legend:** glyph ID, confidence, depth, arousal, session time.

## Decoder (whale → us) — steps
1. Segment clicks; compute features.
2. Project to disentangled latent (β‑TCVAE + triplet loss).
3. Classify into **glyph bank** (6–10 IDs) with posterior/confidence.
4. Render R–T–S panels; suppress rendering if confidence < threshold or arousal high.

## Encoder (us → whale) — safe playback in managed care only
1. Select glyph template (R/T/S).
2. Synthesize click phrase: set ICIs from R, time‑warp from T, filter each click by S.
3. Enforce SPL, duration, cooldown; vet oversight required.

## Glyph bank (example layout)
- G1: Approach/Scan
- G2: Hold/Stay
- G3: Object‑A (EchoGlyph A)
- G4: Object‑B
- G5: Food/School (context cue)
- G6: End/Done

## Confidence & guardrails
- Act only if **max posterior > Θ** and **arousal < gate**.
- Never infer “meaning” beyond ethogram labels; keep a species‑native behavior head separate from human tags.

---
## Spiral Mode (2D default)

Some users think in 2D. **Spiral Mode** renders R–T–S without a Z axis.

**Mapping**
- Coordinates: polar \((r,\theta)\).  
  - \(\theta_i = i \cdot \Delta\theta\) (click index in radians; choose \(\Delta\theta \in [\pi/6, \pi/3]\)).  
  - Base radius: \(r^\*_{i} = a + b\,\theta_i/(2\pi)\) (slow outward growth per revolution).  
  - **Rhythm (R)**: \(r_i = r^\*_i + k_R\,R_i\) (radius wiggles with normalized ICI).
- **Tempo (T)** (2D encodings): pick one (or combine):
  1) **Stroke width** \(w_i = w_0 + k_T\,\tilde T_i\) (faster tempo → thicker line).  
  2) **Dash frequency** (faster tempo → shorter dash, tighter cadence).  
  3) **Radial slope** (advanced): modulate \(b\) locally by \(\tilde T_i\) to make the spiral open faster/slower.
- **Spectrum (S)**: hue = spectral centroid, saturation = bandwidth, value = amplitude/SNR.
- **Confidence** → opacity; **Arousal** → glow/halo.

**Defaults**
- \(a=1.0\), \(b=0.25\), \(k_R=0.25\), \(\Delta\theta=\pi/5\).  
- Colorblind‑safe palette fallback when hues cluster.

**Toggle**
- UI exposes a **Spiral ↔ Ribbon** toggle. Both views use the same R–T–S features and glyph IDs.

**Export**
- Square PNG/SVG at 2048×2048 for social pins; include legend with glyph ID, confidence, depth band, and session time.

*Added: 2025-11-12*
