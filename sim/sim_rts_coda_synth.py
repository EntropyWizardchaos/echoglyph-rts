#!/usr/bin/env python3
import os, json, numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Config
OUT = Path(__file__).parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)
np.random.seed(7)

# Define 5 glyph templates (R rhythm deltas, T tempo factor, S spectrum centroid/bandwidth ranges)
GLYPHS = {
    "G1_approach_scan": {"ici_seq":[0.12,0.12,0.24,0.12,0.12], "tempo":1.0, "centroid":6000, "bw":1200},
    "G2_hold":          {"ici_seq":[0.20,0.20,0.20,0.20,0.20], "tempo":0.8, "centroid":5500, "bw":900},
    "G3_object_A":      {"ici_seq":[0.10,0.18,0.10,0.18,0.10], "tempo":1.2, "centroid":6500, "bw":1000},
    "G4_object_B":      {"ici_seq":[0.14,0.14,0.14,0.28,0.14], "tempo":1.1, "centroid":7000, "bw":1400},
    "G5_end":           {"ici_seq":[0.08,0.30,0.30,0.08],      "tempo":0.9, "centroid":5200, "bw":800},
}

def synth_coda(ici_seq, tempo, centroid, bw, jitter_t=0.008, jitter_amp=0.15, n_reps=1):
    """Return click times t, per-click spectral centroid/bw with noise, and an RTS feature vector for classification."""
    ici = np.array(ici_seq) / max(tempo, 1e-3)
    # Repeat pattern
    t = [0.0]
    for _ in range(n_reps):
        for dt in ici:
            t.append(t[-1] + dt + np.random.randn()*jitter_t)
    t = np.array(t[1:])
    # Spectral color per click with noise
    fc = np.full_like(t, centroid, dtype=float) + np.random.randn(t.size)*bw*0.05
    bwv = np.full_like(t, bw, dtype=float) + np.random.randn(t.size)*bw*0.05
    amp = np.clip(1.0 + np.random.randn(t.size)*jitter_amp, 0.2, 2.0)

    # Features for classification (summary stats)
    ici_inst = np.diff(np.concatenate([[0], t]))
    R = (ici_inst - ici_inst.mean()) / (ici_inst.std() + 1e-6)
    T = (ici_inst.mean() / (ici_inst + 1e-6))
    # Aggregate features: mean/std of R and T, mean fc, mean bw, amp var
    feat = np.array([R.mean(), R.std(), T.mean(), T.std(), fc.mean(), bwv.mean(), amp.var()])
    return t, fc, bwv, amp, feat, R, T

def render_spiral(name, t, R, T, fc, bw):
    """Render coda as 2D polar spiral — radius modulated by rhythm, color by spectrum."""
    n = len(R)
    delta_theta = np.pi / 5
    a, b, k_R = 1.0, 0.25, 0.25
    theta = np.arange(n) * delta_theta
    r_base = a + b * theta / (2 * np.pi)
    r = r_base + k_R * R

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    # Normalize fc for colormap
    fc_norm = (fc - fc.min()) / (fc.max() - fc.min() + 1e-6)
    cmap = plt.cm.viridis
    for i in range(n - 1):
        ax.plot([theta[i], theta[i+1]], [r[i], r[i+1]],
                color=cmap(fc_norm[i]), linewidth=1.5 + T[i] * 0.3)
    ax.set_title(f"{name} — Spiral (R–T–S)", pad=20)
    plt.tight_layout()
    plt.savefig(OUT / f"{name}_Spiral.png", dpi=150)
    plt.close()

def render_rts(name, t, R, T, fc, bw):
    # XY: Rhythm (Y=R vs X=click index)
    idx = np.arange(len(R))
    plt.figure()
    plt.plot(idx, R)
    plt.xlabel("Click index"); plt.ylabel("Rhythm (normalized ICI)")
    plt.title(f"{name} — XY Rhythm")
    plt.tight_layout(); plt.savefig(OUT / f"{name}_XY.png"); plt.close()

    # ZX: Tempo (Z=T vs X=click index) — render as 2D since depth can't be shown; label as tempo trace
    plt.figure()
    plt.plot(idx, (T - T.mean())/(T.std()+1e-6))
    plt.xlabel("Click index"); plt.ylabel("Tempo (normalized)")
    plt.title(f"{name} — ZX Tempo")
    plt.tight_layout(); plt.savefig(OUT / f"{name}_ZX.png"); plt.close()

    # Spectrum as color bar vs index (centroid hue proxy)
    plt.figure()
    plt.scatter(idx, np.zeros_like(idx), c=fc, cmap="viridis")
    plt.xlabel("Click index"); plt.yticks([])
    plt.title(f"{name} — Spectrum (color ~ centroid)")
    plt.tight_layout(); plt.savefig(OUT / f"{name}_Spec.png"); plt.close()

def main():
    # Generate dataset
    feats = []
    labels = []
    examples = {}
    for gi, (gname, g) in enumerate(GLYPHS.items()):
        for k in range(60):
            t, fc, bw, amp, feat, R, T = synth_coda(g["ici_seq"], g["tempo"], g["centroid"], g["bw"],
                                                    jitter_t=0.006, jitter_amp=0.12, n_reps=np.random.randint(1,3))
            feats.append(feat); labels.append(gi)
            if k==0:
                examples[gname] = (t, fc, bw, amp, R, T)

    feats = np.vstack(feats); labels = np.array(labels)

    # Train a nearest-centroid classifier
    centroids = []
    for gi in range(len(GLYPHS)):
        centroids.append(feats[labels==gi].mean(axis=0))
    centroids = np.vstack(centroids)

    # Simple test accuracy (hold-out every 5th sample)
    test_idx = np.arange(len(labels)) % 5 == 0
    train_idx = ~test_idx
    C_tr = []
    for gi in range(len(GLYPHS)):
        C_tr.append(feats[train_idx][labels[train_idx]==gi].mean(axis=0))
    C_tr = np.vstack(C_tr)
    pred = np.argmin(((feats[test_idx,None,:]-C_tr[None,:,:])**2).sum(axis=2), axis=1)
    acc = (pred == labels[test_idx]).mean()

    with open(OUT / "sim_metrics.json", "w") as f:
        json.dump({"holdout_accuracy": float(acc), "n_samples": int(len(labels))}, f, indent=2)

    # Render one example per glyph (ribbon panels + spiral)
    for gname, (t, fc, bw, amp, R, T) in examples.items():
        render_rts(gname, t, R, T, fc, bw)
        render_spiral(gname, t, R, T, fc, bw)

if __name__ == "__main__":
    main()
