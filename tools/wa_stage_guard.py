#!/usr/bin/env python3
"""
wa_stage_guard.py — Validate Whale Agent stage cards and compute a content hash.

Usage:
  python wa_stage_guard.py check path/to/WA_<WhaleID>_stage_<S#>_<YYYYMMDD>.yaml
  python wa_stage_guard.py hash  path/to/WA_<WhaleID>_stage_<S#>_<YYYYMMDD>.yaml

- Ensures required gates/metrics are above thresholds for promotion to the declared stage.
- Computes a deterministic SHA-256 over the normalized JSON of the card (excluding 'signatures.card_hash').
"""

import sys, json, hashlib, pathlib, copy
from typing import Dict, Any
try:
    import yaml
except Exception as e:
    print("YAML support missing. Please 'pip install pyyaml' if running outside the packaged environment.")
    sys.exit(1)

# Thresholds for promotion TO each stage (same as spec; conservative defaults)
THRESHOLDS = {
    "S0": {  # seed: basic detection quality
        "click_detection_auc": (">=", 0.90),
    },
    "S1": {  # infant
        "glyph_clustering_silhouette": (">=", 0.50),
        "coda_family_accuracy": (">=", 0.70),
    },
    "S2": {  # juvenile
        "false_alarm_rate": ("<=", 0.05),
        "arousal_auc": (">=", 0.80),
        "ece": ("<=", 0.05),
    },
    "S3": {  # apprentice
        "ethogram_balanced_accuracy": (">=", 0.70),
    },
    "S4": {  # adult
        "coda_family_accuracy": (">=", 0.80),
        "glyph_churn": ("<=", 0.10),
    },
    "S5": {  # mentor
        "inter_agent_confusion": ("<=", 0.03),
    },
    "S6": {  # steward
        "drift_delta": ("<=", 0.02),  # example δ; adjust in policy
    }
}

# Gate booleans that must be true in all promoted stages
BOOLEAN_GATES = ["confidence_calibrated", "welfare_ok", "separability_ok"]

def cmp(op, a, b):
    if op == ">=":
        return a >= b
    if op == "<=":
        return a <= b
    raise ValueError(op)

def normalize_json(d: Dict[str, Any]) -> str:
    """Return deterministic JSON string (sorted keys, no whitespace)."""
    return json.dumps(d, sort_keys=True, separators=(",", ":"))

def compute_hash(card: Dict[str, Any]) -> str:
    card_copy = copy.deepcopy(card)
    # Remove any existing hash to avoid circularity
    try:
        del card_copy["signatures"]["card_hash"]
    except Exception:
        pass
    s = normalize_json(card_copy).encode("utf-8")
    return hashlib.sha256(s).hexdigest()

def check_stage(card: Dict[str, Any]) -> int:
    stage = card.get("stage", {}).get("current")
    if stage not in THRESHOLDS:
        print(f"[WARN] Unknown stage '{stage}'. Skipping metric thresholds.")
        return 0
    thresh = THRESHOLDS[stage]
    met = True

    metrics = card.get("metrics", {})
    # Derived metrics
    derived = {}
    # glyph churn and inter-agent confusion might be absent unless set by ops
    metrics_full = {**metrics, **derived}

    # Evaluate numeric thresholds
    for k, (op, v) in thresh.items():
        val = metrics_full.get(k)
        if val is None:
            print(f"[FAIL] Missing metric '{k}' required for stage {stage}.")
            met = False
            continue
        if not cmp(op, float(val), float(v)):
            print(f"[FAIL] {k}={val:.3f} does not meet {op} {v:.3f} for stage {stage}.")
            met = False
        else:
            print(f"[OK]   {k}={val:.3f} meets {op} {v:.3f}.")

    # Evaluate boolean gates
    gates = card.get("gates_passed", {})
    for g in BOOLEAN_GATES:
        if not gates.get(g, False):
            print(f"[FAIL] Gate '{g}' is not true.")
            met = False
        else:
            print(f"[OK]   Gate '{g}' = true.")

    if met:
        print(f"[PASS] Card meets stage {stage} thresholds.")
        return 0
    else:
        print(f"[BLOCK] Card does not meet stage {stage} thresholds.")
        return 2

def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("check","hash"):
        print(__doc__)
        sys.exit(1)
    cmd, path = sys.argv[1], pathlib.Path(sys.argv[2])
    data = yaml.safe_load(path.read_text())

    if cmd == "hash":
        h = compute_hash(data)
        print(h)
        sys.exit(0)

    if cmd == "check":
        rc = check_stage(data)
        # Always print a suggested hash for audit trail
        h = compute_hash(data)
        print(f"[INFO] Suggested card_hash: {h}")
        sys.exit(rc)

if __name__ == "__main__":
    main()
