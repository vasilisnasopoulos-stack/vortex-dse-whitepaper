# Before / After: fixing a real, well-known consensus bug

This is a small, self-contained illustration of the idea behind Vortex DSE,
applied to a real, widely-used open-source project.

## The "before": a real, reproducible bug

[`blockchain-hackernoon`](https://github.com/harrywang/blockchain-hackernoon)
is the code behind the popular tutorial *"Learn Blockchains by Building
One."* Its consensus rule (`resolve_conflicts()`) is simple: whenever nodes
disagree, the **longest valid chain wins**.

That rule has a gap. If two nodes each mine a block at the same height, at
the same time, with **different transactions**, both resulting chains have
**equal length**. The longest-chain rule has nothing to compare — it never
triggers a replacement on either side. The two nodes disagree forever. This
is not a hypothetical: we reproduced it live by running the project
unmodified and simulating exactly this condition.

## The "after": deterministic ordering, no coordination

[`before_after_demo.py`](before_after_demo.py) takes the same two
conflicting transactions and feeds them into two independent nodes using
the same public ordering rule already shown in
[`../vortex_demo.py`](../vortex_demo.py): each transaction is assigned to a
canonical time slot, and within a slot, ordering falls back to timestamp
and then transaction id. Each node sees the transactions in a **different
arrival order** — the same condition that broke the naive chain — and
still produces an **identical ordered log and hash**, with zero messages
exchanged between the two nodes.

Run it:

```bash
python3 demo/before_after/before_after_demo.py
```

Expected output: both nodes report the same digest and `✓ CONVERGED`.

## What this is, and isn't

This script demonstrates the **shape of the idea** — deterministic,
coordination-free convergence — using the same simplified, illustrative
ordering rule as the rest of `/demo`. It is not the production engine.

It does not implement, and does not attempt to reproduce:

- the real tie-breaking rule used when two transactions land in the exact
  same slot with no timestamp separation (that rule is proprietary),
- the `τ_min = 2×RTT` physical-lower-bound measurement described in the
  whitepaper,
- Byzantine-fault handling, replay protection, or the signature-free
  security layer (receipts, rotor auditors, proof of cadence / location)
  described in the whitepaper,
- real network communication of any kind — everything here runs in a
  single local process for illustration.

In short: this shows *that* the naive bug in a real project has a
deterministic-ordering fix, not *how* the production system achieves it
under adversarial, real-network conditions. See the
[whitepaper](../../vortex_dse_whitepaper_en.md) for the actual claims and
their scope.
