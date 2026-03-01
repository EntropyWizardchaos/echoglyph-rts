# Build Print — EchoGlyph Tag v0 (Tri‑Segment Dorsal Suction)

> **Intent:** Low‑profile, flexible, recoverable tag for sperm‑whale acoustic logging and motion capture. No sharp edges; all radii ≥ 4 mm.

## 1) Envelope (initial targets — tune in flume)
- **Overall planform:** 630 × 140 mm (L × W) in flow direction, split into **three 200 × 140 mm segments** plus **two 15 mm flex couplers**.
- **Profile height:** ≤ 25–30 mm over skin.
- **Mass in air:** ≤ 2.2 kg; **net buoyancy in seawater:** +100 to +200 g (floats upon release).
- **Operating depth rating:** electronics potting and seals **≥ 10 bar** for v0 (tank trials). *Note:* blue‑water field hardware will require ≥ 100 bar; defer until partners confirm scope.

```
Top view (not to scale)
 ┌───────────────┬───────────────┬───────────────┐  flow →
 │   Segment C1  │  Segment C2   │   Segment C3  │
 │    (cups)     │   (cups)      │    (cups)     │
 └─────~~────────┴─────~~────────┴─────~~────────┘
        ^  flex coupler (piezo)    ^  flex coupler (piezo)

Side profile (centerline)
   rounded LE →  ▃▃▃▃▃      ▃▃▃▃▃      ▃▃▃▃▃   ← rounded TE   (max 25–30 mm)
```

## 2) Body interface
- **Suction cups:** 3–4 per segment; **Ø 90–120 mm**, Shore‑00 soft silicone lip; shallow dish; gentle vacuum channel with check valve.
- **Backer:** compliant silicone pad (3–5 mm), tapering edges; textured to reduce slip without abrasion.
- **Release:** 
  - **Timed burn‑wire** (nichrome) or motorized pin to admit water under cups.
  - **Remote acoustic command** (failsafe) from chase boat.
  - **Failsafe**: loss‑of‑suction trigger.

## 3) Segment structure
- **Shell:** glass‑filled **PEEK** or Delrin (acetal) fairings; teardrop cross‑section.
- **Flex couplers:** elastomer hinges with embedded **piezo stacks/films** on neutral axis carriers; strain‑limited to avoid drift.
- **Fasteners:** captive; no metal protrusions; all external surfaces matte.

## 4) Sensing & electronics
- **Hydrophone:** wideband (2–40 kHz useful band), low‑noise preamp, 24‑bit ADC.
- **Depth/Temp:** 0–10 bar transducer (v0); thermistor.
- **IMU:** 6‑axis @ 100–200 Hz (tail‑beat and orientation inference).
- **MCU/Storage:** low‑power MCU + ≥ 128 GB flash.
- **Clock:** TCXO for timestamp stability.
- **Power:** primary lithium cells (e.g., Li‑SOCl₂) sized for **12–48 h**; **piezo harvester** bridge + supercap for trickle; optional thin‑film TEG.
- **Recovery:** VHF beacon + strobe; GPS when surfaced.

## 5) Acoustics (playback, optional in managed care only)
- **Underwater speaker** (external, not on tag) with calibrated SPL; short phrases, strict duty cycle.
- **On‑tag playback omitted** in v0 to reduce drag and complexity.

## 6) BOM classes (source‑agnostic)
- Soft silicone suction cups (Ø 90–120 mm), compliant pads, PEEK/Delrin shells, elastomer flexures, piezo stacks/films, hydrophone + preamp, pressure transducer, IMU, MCU board, flash, Li‑SOCl₂ cell pack, VHF pinger, strobe, burn‑wire release, epoxy potting, gasket set.

## 7) Acceptance tests (shop)
- **Hydro:** tow tank drag < 10 N @ 1.5 m/s; suction retention > 30 min @ 1.0 m/s; clean release.
- **Electronics:** audio self‑noise floor; timing drift < 5 ppm; IMU saturation margin.
- **Power:** logging runtime ≥ 12 h at duty profile; harvest adds ≥ 10% life in shaker test.
- **Recovery:** pop‑off to float in < 5 s; beacon audible at 1 km line‑of‑sight.
