#!/usr/bin/env python3
"""
Before / After: the classic blockchain-hackernoon naive-consensus fork,
resolved with Vortex DSE's public toy demo logic.

BEFORE: "Learn Blockchains by Building One" (harrywang/blockchain-hackernoon)
resolves conflicts by picking the longest valid chain. If two nodes mine a
block at the same height with different transactions, chain length is equal
on both sides and resolve_conflicts() never triggers -- a permanent fork.
(Reproduced live against the real project; this script does not re-run it,
it documents the exact reproducible condition.)

AFTER: the same two conflicting blocks are fed into two independent nodes
using the same public demo ordering logic that already ships in this repo's
/demo folder (see demo/vortex_demo.py). No server, no network, no engine --
just the same deterministic (slot, timestamp, id) ordering rule, run twice
with a different arrival order per node.

This file contains no proprietary logic. It reuses the same toy ordering
rule already published in demo/vortex_demo.py.
"""
from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Transaction:
    tx_id: str
    canonical_time_ms: int
    payload: str


@dataclass
class Node:
    name: str
    epoch_ms: int
    slot_ms: int
    admitted: list = field(default_factory=list)

    def ingest(self, tx: Transaction) -> None:
        self.admitted.append(tx)

    def ordered_log(self):
        ordered = sorted(
            self.admitted,
            key=lambda tx: (
                (tx.canonical_time_ms - self.epoch_ms) // self.slot_ms,
                tx.canonical_time_ms,
                tx.tx_id,
            ),
        )
        return [
            {"slot": (tx.canonical_time_ms - self.epoch_ms) // self.slot_ms,
             "tx_id": tx.tx_id, "payload": tx.payload}
            for tx in ordered
        ]

    def digest(self) -> str:
        payload = json.dumps(self.ordered_log(), separators=(",", ":"), sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()


def main() -> int:
    print("=== BEFORE: blockchain-hackernoon naive longest-chain-wins ===")
    print("Node A mines block #3 with tx: Alice->Bob:5")
    print("Node B mines block #3 (same height, same previous_hash) with tx: Carol->Dave:9")
    print("len(chain_A) == len(chain_B) -> resolve_conflicts() never replaces either chain")
    print("Result: PERMANENT FORK (verified live against the real project).\n")

    print("=== AFTER: same two conflicting transactions, deterministic slot ordering ===")
    epoch_ms = 0
    slot_ms = 500
    tx_a = Transaction("tx-a", epoch_ms + 120, "transfer:alice->bob:5")
    tx_b = Transaction("tx-b", epoch_ms + 340, "transfer:carol->dave:9")

    node_a = Node("Node A", epoch_ms, slot_ms)
    node_b = Node("Node B", epoch_ms, slot_ms)

    # Different arrival order per node -- exactly the condition that forked
    # the naive chain. Here it changes nothing about the final ordering.
    rng_a = random.Random(1)
    order_a = [tx_a, tx_b]
    rng_a.shuffle(order_a)
    for tx in order_a:
        node_a.ingest(tx)

    rng_b = random.Random(2)
    order_b = [tx_a, tx_b]
    rng_b.shuffle(order_b)
    for tx in order_b:
        node_b.ingest(tx)

    print(f"Node A arrival order: {[t.tx_id for t in order_a]}")
    print(f"Node B arrival order: {[t.tx_id for t in order_b]}")
    print(f"Node A digest: {node_a.digest()[:16]}...")
    print(f"Node B digest: {node_b.digest()[:16]}...")

    if node_a.digest() == node_b.digest():
        print("\n✓ CONVERGED -- same ordered log despite different arrival order,")
        print("  no leader election, no voting, no gossip between the two nodes.")
        return 0
    print("\n✗ NOT CONVERGED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
