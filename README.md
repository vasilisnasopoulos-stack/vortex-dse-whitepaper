# Vortex DSE — Whitepaper

**Deterministic Consensus at the Physical Lower Bound**

Vortex DSE (Deterministic Slot Engine) is a distributed consensus protocol that
reaches finality **without leader election, voting, or gossip**. It operates at
the physical lower bound **&tau;_min = 2&times;RTT** &mdash; confirmed
experimentally across 13 nodes in 13 countries &mdash; and its 14 safety and
liveness invariants are machine-checked in TLA+ (TLC + Apalache, 8M+ states, 0
errors).

## Try it in 30 seconds

```bash
git clone https://github.com/vasilisnasopoulos-stack/vortex-dse-whitepaper.git
cd vortex-dse-whitepaper
pip install -r demo/requirements.txt
python demo/vortex_demo.py
```

Independent nodes admit the same transactions in a different arrival order
each and still converge on an identical ordered log and hash &mdash; no
node-to-node communication. Details: [`/demo`](demo/README.md).

## Read the whitepaper

**[vortex_dse_whitepaper.pdf](vortex_dse_whitepaper.pdf)** &mdash; full paper
(cover, figures, references).

Markdown version: [vortex_dse_whitepaper_en.md](vortex_dse_whitepaper_en.md).

## Key results

- **&tau;_min = 2&times;RTT** &mdash; the physical floor on global consensus,
  reached with zero coordination.
- 13 nodes / 13 countries converge on an identical state hash.
- Formally verified: 14 invariants, machine-checked (TLA+ / Apalache / TLAPS).

## Scope

This repository contains the **whitepaper** and a small **public demo** of the
deterministic slot-ordering idea described in the paper. The engine and the
underlying mathematical derivations remain proprietary. IP registered and
timestamped.

## Public demo

The repository includes a toy educational demo in
[`/demo/vortex_demo.py`](demo/vortex_demo.py). It shows a producer broadcasting
transactions to independent nodes that:

- assign the same canonical slot,
- reject duplicates,
- reject future-dated entries beyond a fixed horizon,
- produce the same ordered log and hash with no node-to-node communication.

Prerequisite: Python 3.11 or newer.

Run it locally with:

```bash
pip install -r demo/requirements.txt   # one-time install
python demo/vortex_demo.py
```

A CI workflow can also run the demo on demand
(see [`.github/workflows/demo.yml`](.github/workflows/demo.yml), manual trigger).

This demo is **not** the proprietary engine and does not claim to reproduce the
full implementation or all runtime invariants.

Public formal TLA+ specifications:
<https://github.com/vasilisnasopoulos-stack>

## License

&copy; 2026 Vasilis Nasopoulos. Licensed under
**[CC BY-NC-ND 4.0](LICENSE)** &mdash; you may share it with attribution, but
**not** for commercial purposes and **not** in modified form.

Contact: vasilis_nasopoulos@hotmail.com
