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

# ── ANSI colour helpers ──────────────────────────────────────────────────────

_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_DIM    = "\033[2m"
_RED    = "\033[91m"
_GREEN  = "\033[92m"
_YELLOW = "\033[93m"
_CYAN   = "\033[96m"
_WHITE  = "\033[97m"
_GREY   = "\033[90m"

import re as _re

_ANSI_RE = _re.compile(r"\033\[[0-9;]*m")

def _c(text: str, *codes: str) -> str:
    return "".join(codes) + text + _RESET

def _visible_len(text: str) -> int:
    return len(_ANSI_RE.sub("", text))

def _header(title: str, *, width: int = 62, colour: str = _CYAN) -> str:
    inner = width - 2
    top    = colour + "╔" + "═" * inner + "╗" + _RESET
    bottom = colour + "╚" + "═" * inner + "╝" + _RESET
    pad_total = max(0, inner - _visible_len(title))
    left  = " " * (pad_total // 2)
    right = " " * (pad_total - pad_total // 2)
    mid_row = colour + "║" + _RESET + _c(left + title + right, _BOLD + _WHITE) + colour + "║" + _RESET
    return "\n".join([top, mid_row, bottom])


def _box(title: str, lines: list[str], *, width: int = 62, colour: str = _CYAN) -> str:
    inner = width - 2
    top    = colour + "╔" + "═" * inner + "╗" + _RESET
    mid    = colour + "╠" + "═" * inner + "╣" + _RESET
    bottom = colour + "╚" + "═" * inner + "╝" + _RESET

    def row(text: str = "", bold: bool = False) -> str:
        style = (_BOLD if bold else "") + _WHITE
        pad = " " * max(0, inner - _visible_len(text))
        return colour + "║" + _RESET + _c(text, style) + _c(pad, style) + colour + "║" + _RESET

    parts = [top, row(f"  {title}", bold=True), mid]
    for line in lines:
        parts.append(row(f"  {line}"))
    parts.append(bottom)
    return "\n".join(parts)


# ── Data model ───────────────────────────────────────────────────────────────

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


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    # ── header ──────────────────────────────────────────────────────────────
    print()
    print(_header("VORTEX DSE  ·  Before / After Demo"))
    print()

    # ── BEFORE ──────────────────────────────────────────────────────────────
    before_lines = [
        _c("Project : ", _DIM + _WHITE) + "blockchain-hackernoon (harrywang)",
        _c("Rule    : ", _DIM + _WHITE) + "longest valid chain wins",
        "",
        _c("Node A  ", _YELLOW) + "mines block #3  →  tx: Alice → Bob   : 5",
        _c("Node B  ", _YELLOW) + "mines block #3  →  tx: Carol → Dave  : 9",
        _c("        ", _WHITE)  + "(same height, same previous_hash)",
        "",
        _c("len(chain_A) == len(chain_B)", _DIM + _WHITE),
        _c("→ resolve_conflicts() never triggers on either side", _DIM + _WHITE),
        "",
        _c("✗  PERMANENT FORK", _RED + _BOLD) + _c("  (verified live against the real project)", _DIM),
    ]
    print(_box("BEFORE  ·  naive longest-chain-wins", before_lines, colour=_RED))
    print()

    # ── AFTER ────────────────────────────────────────────────────────────────
    epoch_ms = 0
    slot_ms  = 500
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

    arrival_a = " → ".join(t.tx_id for t in order_a)
    arrival_b = " → ".join(t.tx_id for t in order_b)
    digest_a  = node_a.digest()
    digest_b  = node_b.digest()
    converged = digest_a == digest_b

    log_a = node_a.ordered_log()
    log_b = node_b.ordered_log()

    after_lines = [
        _c("Rule    : ", _DIM + _WHITE) + "deterministic (slot, timestamp, tx_id) ordering",
        "",
        _c("Node A  ", _YELLOW) + f"arrival order : {arrival_a}",
        _c("Node B  ", _YELLOW) + f"arrival order : {arrival_b}",
        "",
        _c("Node A  ", _YELLOW) + "ordered log :",
    ]
    for entry in log_a:
        after_lines.append(
            _c("        ", _WHITE) +
            _c(f"slot {entry['slot']}", _CYAN) +
            f"  {entry['tx_id']}  {entry['payload']}"
        )
    after_lines += [
        "",
        _c("Node B  ", _YELLOW) + "ordered log :",
    ]
    for entry in log_b:
        after_lines.append(
            _c("        ", _WHITE) +
            _c(f"slot {entry['slot']}", _CYAN) +
            f"  {entry['tx_id']}  {entry['payload']}"
        )
    after_lines += [
        "",
        _c("Node A digest : ", _DIM + _WHITE) + _c(digest_a[:24] + "…", _GREY),
        _c("Node B digest : ", _DIM + _WHITE) + _c(digest_b[:24] + "…", _GREY),
        "",
    ]

    if converged:
        after_lines += [
            _c("✓  CONVERGED", _GREEN + _BOLD),
            _c("   same ordered log despite different arrival order", _DIM),
            _c("   no leader election · no voting · no gossip", _DIM),
        ]
    else:
        after_lines.append(_c("✗  NOT CONVERGED", _RED + _BOLD))

    print(_box("AFTER  ·  Vortex DSE deterministic slot ordering", after_lines, colour=_GREEN))
    print()

    return 0 if converged else 1


if __name__ == "__main__":
    raise SystemExit(main())
