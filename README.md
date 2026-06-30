# Vortex DSE — Whitepaper

**Deterministic Consensus at the Physical Lower Bound**

Vortex DSE (Deterministic Slot Engine) is a distributed consensus protocol that
reaches finality **without leader election, voting, or gossip**. It operates at
the physical lower bound **&tau;_min = 2&times;RTT** &mdash; confirmed
experimentally across 13 nodes in 13 countries &mdash; and its 14 safety and
liveness invariants are machine-checked in TLA+ (TLC + Apalache, 8M+ states, 0
errors).

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

This repository contains the **whitepaper only**. The engine and the underlying
mathematical derivations remain proprietary. IP registered and timestamped.

Public formal TLA+ specifications:
<https://github.com/vasilisnasopoulos-stack>

## License

&copy; 2026 Vasilis Nasopoulos. Licensed under
**[CC BY-NC-ND 4.0](LICENSE)** &mdash; you may share it with attribution, but
**not** for commercial purposes and **not** in modified form.

Contact: vasilis_nasopoulos@hotmail.com
