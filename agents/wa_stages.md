# Whale Agent (WA) Lifecycle — Stage Guide (v0)

Each whale gets a persistent agent **WA-<WhaleID>**. Identity is stable (frozen core encoder) with a tiny **per-whale adapter** and an **append-only memory**. Promotion through stages is **metrics-gated** (time alone never promotes).

## Architecture snapshot
- **Core (frozen):** EchoGlyph foundation encoder → R–T–S features (shared across whales).
- **Adapter (per-whale):** small LoRA/adapter fine-tuned on this whale’s data.
- **Ethogram head:** species-native behavior predictor (approach/turn/dive/etc.); **has veto priority** over human-tag meanings.
- **Glyph head:** maps codas to the local glyph bank (6–10 symbols max).
- **Memory:** append-only logs + checkpoints; rollbacks allowed, overwrites prohibited.

## Stages & gates (S0–S6)
| Stage | Name       | Minimum data & coverage                         | Metrics (pass gates)                                                          | Unlocks / Restrictions |
|------:|------------|--------------------------------------------------|-------------------------------------------------------------------------------|------------------------|
| S0    | Seed       | ≥15 min clean codas across ≥2 depth bands       | ID fingerprint stable; click detection ROC-AUC ≥0.9                           | Decode-only; no prompts |
| S1    | Infant     | ≥2 h total codas, ≥3 sessions                   | Glyph clustering silhouette ≥0.50; coda-family accuracy ≥70% (held-out)       | Glyph Bank v1 (3–4); decode-only |
| S2    | Juvenile   | ≥6 h; ≥2 sea states; day & night                | False-alarm ≤5%; arousal ROC-AUC ≥0.80; ECE ≤0.05                             | Managed-care prompts allowed; **no wild playback** |
| S3    | Apprentice | ≥12 h; foraging vs travel contexts              | Ethogram head ≥70% balanced acc; zero injury/agitation; stable confidence     | EchoGlyph object labels (A/B/C) in facility |
| S4    | Adult      | ≥24 h; new sites (short field deployments)      | Coda-family acc ≥80% across sites; glyph-bank churn ≤10% week-to-week         | Sparse, pre-approved request phrases in research sessions |
| S5    | Mentor     | ≥48 h; cross-individual contrast sessions       | Inter-agent confusion ≤3%; acts as calibration anchor                         | Calibrator for younger WAs (never “in charge”) |
| S6    | Steward    | Long-term                                       | Regression tests pass; drift ≤δ; welfare trend non-negative                   | Baseline model, **veto power** when uncertainty/arousal high |

**Definitions**  
- *Silhouette*: cluster separability (−1..1).  
- *ECE*: expected calibration error (confidence calibration).  
- *Churn*: % glyphs added/removed or re-labeled week-to-week.  
- *Arousal*: proxy from click-rate variability/tempo volatility.

## Promotion rules
- All listed gates must pass in **two independent evaluations** (different days).  
- Failing any welfare gate stalls promotion and creates a remediation note.  
- Promotions and rollbacks are recorded in a **stage card** (YAML), hashed and appended to the agent ledger.

## Gating at runtime (always on)
- **Confidence gate:** act only if max posterior ≥ Θ.  
- **Arousal gate:** suspend meanings when arousal high.  
- **Ethogram veto:** if the species-native head predicts avoidance/stress, the system stands down—even if glyph head is confident.

## Identity & reproducibility
- **WhaleID** ↔ cryptographic keypair; every session is signed.  
- **Deterministic seeds**: per-whale adapter seeded by WhaleID; same data → same weights.  
- **Checkpoint ledger**: model hashes + metrics; no in-place edits.

## Change management
- **Drift checks**: embedding centroid shift ≤ δ over a week, else freeze & review.  
- **Glyph-bank governance**: max 10 symbols; additions require justification and two-week stability.

## What not to claim
- WAs do **not** infer beliefs/intent beyond validated ethograms and the agreed glyph set. This is a **translator of patterns**, not a mind reader.

## Files in this folder
- `wa_stage_card.yaml` — template for stage cards (fill per whale).
- (Optional) `WA_<WhaleID>_ledger.jsonl` — append-only history created by your ops scripts.
