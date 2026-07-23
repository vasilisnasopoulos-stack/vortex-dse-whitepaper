# Vortex DSE — Whitepaper

**Deterministic Consensus at the Physical Lower Bound**

Vortex DSE (Deterministic Slot Engine) is a distributed consensus protocol that reaches finality **without leader election, voting, or gossip**. It operates at the physical lower bound **τ_min = 2×RTT** — confirmed experimentally across 13 nodes in 13 countries — and its 14 safety and liveness invariants are machine-checked in TLA+ (TLC + Apalache, 8M+ states, 0 errors).

---

## 🚀 Try it in 30 seconds

No setup. No dependencies (except Python 3.11+). Just clone and run:

```bash
git clone https://github.com/vasilisnasopoulos-stack/vortex-dse-whitepaper.git
cd vortex-dse-whitepaper
pip install -r demo/requirements.txt
python demo/vortex_demo.py
```

### What you'll see

**Three independent nodes broadcast the same transactions in different arrival orders** — yet converge on an identical ordered log and cryptographic hash with **zero node-to-node communication**.

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Vortex DSE — public demo                                      ┃
┃ nodes=3  slot_ms=500  seed=42  admission_horizon_ms=1340    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Node   ┃ Admit  ┃ Dup Rj.  ┃ Fut. Rj.   ┃ Digest (first 16) ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ node-1 │ 6      │ 2        │ 1          │ a7f2c8e91d34... │
│ node-2 │ 6      │ 2        │ 1          │ a7f2c8e91d34... │
│ node-3 │ 6      │ 2        │ 1          │ a7f2c8e91d34... │
└────────┴────────┴──────────┴────────────┴─────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ✓ CONVERGED                                             ┃
┃ shared digest: a7f2c8e91d34f5a8c6b2e9f7d1c3a4b9 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

Try with different parameters:

```bash
# 5 nodes, 500ms slots
python demo/vortex_demo.py --nodes 5 --slot-ms 500

# 7 nodes, 1000ms slots, different shuffle seed
python demo/vortex_demo.py --nodes 7 --slot-ms 1000 --seed 99
```

**Details:** [`/demo`](demo/README.md)

---

## 🧪 Beta: agent coordination endpoint

A "who-wins" arbitration primitive for exclusive-action coordination
between AI agents — deterministic resolution, no leader election, no
voting, no gossip, formally verified core. Open beta, token-gated.

**[Request access / read the details →](BETA.md)**

---

## 📖 Read the Whitepaper

**[vortex_dse_whitepaper.pdf](vortex_dse_whitepaper.pdf)** — full paper with figures, proofs, and experimental validation.

Markdown version: [vortex_dse_whitepaper_en.md](vortex_dse_whitepaper_en.md)

---

## 🎯 Key Results

| Result | Value |
|--------|-------|
| **Latency bound** | τ_min = 2×RTT (physical floor, no coordination) |
| **Validation** | 13 nodes across 13 countries converge to identical state hash |
| **Safety proofs** | 14 invariants, machine-checked in TLA+ (Apalache + TLAPS, 8M+ states) |

---

## 📋 Scope

This repository contains:

- ✅ **The whitepaper** — full technical specification and proofs
- ✅ **A public demo** — educational, runnable proof-of-concept showing deterministic slot ordering
- ✅ **Before/After case study** — fixing a real consensus bug in an open-source blockchain tutorial

**Not included** (proprietary):

- The production engine implementation
- The exact tie-breaking rule for same-slot transactions
- The full runtime invariant set
- Byzantine-fault-handling extensions

---

## 🔬 The Demo Explained

The toy demo in [`/demo/vortex_demo.py`](demo/vortex_demo.py) illustrates the core idea:

### What it does:

1. **Simulates a producer** broadcasting transactions to N independent nodes
2. **Each node independently assigns** transactions to canonical time slots
3. **Duplicate rejection** — identical tx_ids are ignored (seen_ids set)
4. **Admission horizon** — future-dated transactions are rejected
5. **Deterministic ordering** — within each slot, transactions are ordered by:
   - canonical_time_ms (timestamp)
   - tx_id (unique identifier)
6. **Convergence check** — all nodes compute the same SHA256 digest over their ordered log

### What it doesn't claim:

- This is **not** the proprietary engine
- It does not reproduce the full runtime invariant set
- **Zero network communication** in this demo; the real system handles Byzantine adversaries
- It is an **educational proof-of-concept only**

---

## 🔄 Before / After: A Real Consensus Bug

The repository includes [`/demo/before_after`](demo/before_after/) — a case study showing:

1. **The bug**: A real, well-known open-source project (`blockchain-hackernoon`) uses a "longest-chain-wins" rule that **fails when two nodes mine conflicting blocks at the same height**. No tie-breaker exists; the nodes fork permanently.

2. **The fix**: The same transactions, fed to two independent nodes using the **Vortex DSE ordering rule**, converge deterministically with identical logs and digests — **with zero messages** between the nodes.

Run it:

```bash
python demo/before_after/before_after_demo.py
```

---

## 🔗 Formal Specifications

Public TLA+ formal specifications (machine-checked, no errors):

- [vortex-dse-cslot-spec](https://github.com/vasilisnasopoulos-stack/vortex-dse-cslot-spec) — TLA+ spec + reference implementation
- [vortex-dse-cslot-proofs](https://github.com/vasilisnasopoulos-stack/vortex-dse-cslot-proofs) — TLAPS machine-checked safety proofs
- [vortex-merkle-agreement](https://github.com/vasilisnasopoulos-stack/vortex-merkle-agreement) — per-slot Merkle agreement spec

---

## 🛠️ System Requirements

- **Python 3.11+** (for the demo)
- **Git** (to clone the repository)

That's it. The demo uses only the Python standard library plus `rich` for colored output.

---

## 📜 License

© 2026 Vasilis Nasopoulos. Licensed under **[CC BY-NC-ND 4.0](LICENSE)** — you may share it with attribution, but **not** for commercial purposes and **not** in modified form.

---

## 📧 Contact

Questions, feedback, or collaboration inquiries:

**vasilis_nasopoulos@hotmail.com**

---

## 🤝 Contributing

This is a research artifact. If you find the work interesting:

- ⭐ Star this repository
- 📢 Share it in your networks (HN, Reddit, academic communities)
- 💬 Open an issue with questions or feedback
- 🔬 If you're a researcher, consider citing the whitepaper

---
