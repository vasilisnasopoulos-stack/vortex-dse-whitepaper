#!/usr/bin/env python3
"""Public toy demo of deterministic slot ordering across independent nodes."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich import box

console = Console()


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
    admission_horizon_ms: int
    seen_ids: set[str] = field(default_factory=set)
    admitted: list[Transaction] = field(default_factory=list)
    rejected_duplicates: int = 0
    rejected_future: int = 0

    def ingest(self, tx: Transaction) -> None:
        if tx.tx_id in self.seen_ids:
            self.rejected_duplicates += 1
            return

        if tx.canonical_time_ms > self.admission_horizon_ms:
            self.rejected_future += 1
            return

        self.seen_ids.add(tx.tx_id)
        self.admitted.append(tx)

    def ordered_log(self) -> list[dict[str, object]]:
        ordered = sorted(
            self.admitted,
            key=lambda tx: (
                (tx.canonical_time_ms - self.epoch_ms) // self.slot_ms,
                tx.canonical_time_ms,
                tx.tx_id,
            ),
        )
        return [
            {
                "slot": (tx.canonical_time_ms - self.epoch_ms) // self.slot_ms,
                "tx_id": tx.tx_id,
                "canonical_time_ms": tx.canonical_time_ms,
                "payload": tx.payload,
            }
            for tx in ordered
        ]

    def digest(self) -> str:
        payload = json.dumps(self.ordered_log(), separators=(",", ":"), sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_transactions(epoch_ms: int, slot_ms: int) -> tuple[list[Transaction], Transaction]:
    valid = [
        Transaction("tx-001", epoch_ms + 40, "create-account:alice"),
        Transaction("tx-002", epoch_ms + 120, "credit:alice:+50"),
        Transaction("tx-003", epoch_ms + 510, "create-account:bob"),
        Transaction("tx-004", epoch_ms + 710, "transfer:alice->bob:15"),
        Transaction("tx-005", epoch_ms + 1060, "credit:bob:+20"),
        Transaction("tx-006", epoch_ms + 1340, "transfer:bob->alice:5"),
    ]
    future = Transaction("tx-999", epoch_ms + (4 * slot_ms) + 250, "future-dated:reject-me")
    return valid, future


def build_arrival_stream(
    txs: list[Transaction], future: Transaction, rng: random.Random
) -> list[Transaction]:
    stream = list(txs)
    stream.append(txs[1])
    stream.append(txs[3])
    stream.append(future)
    rng.shuffle(stream)
    return stream


def run_demo(node_count: int, slot_ms: int, seed: int) -> int:
    epoch_ms = 0
    valid_txs, future_tx = build_transactions(epoch_ms, slot_ms)
    admission_horizon_ms = max(tx.canonical_time_ms for tx in valid_txs)

    nodes = [
        Node(
            name=f"node-{index + 1}",
            epoch_ms=epoch_ms,
            slot_ms=slot_ms,
            admission_horizon_ms=admission_horizon_ms,
        )
        for index in range(node_count)
    ]

    for index, node in enumerate(nodes):
        rng = random.Random(seed + index)
        for tx in build_arrival_stream(valid_txs, future_tx, rng):
            node.ingest(tx)

    digests = {node.digest() for node in nodes}
    converged = len(digests) == 1

    console.print(
        Panel(
            f"[bold cyan]nodes[/bold cyan]={node_count}  "
            f"[bold cyan]slot_ms[/bold cyan]={slot_ms}  "
            f"[bold cyan]seed[/bold cyan]={seed}  "
            f"[bold cyan]admission_horizon_ms[/bold cyan]={admission_horizon_ms}",
            title="[bold white]Vortex DSE — public demo[/bold white]",
            border_style="bright_blue",
        )
    )

    table = Table(box=box.ROUNDED, border_style="bright_blue", show_header=True)
    table.add_column("Node", style="bold white")
    table.add_column("Admitted", justify="right", style="green")
    table.add_column("Dup rejects", justify="right", style="yellow")
    table.add_column("Future rejects", justify="right", style="yellow")
    table.add_column("Digest (first 16)", style="dim cyan")

    for node in nodes:
        table.add_row(
            node.name,
            str(len(node.admitted)),
            str(node.rejected_duplicates),
            str(node.rejected_future),
            node.digest()[:16],
        )

    console.print(table)
    console.print()

    if converged:
        console.print(
            Panel(
                f"[bold green]✓ CONVERGED[/bold green]\n"
                f"[dim]shared digest:[/dim] [cyan]{nodes[0].digest()}[/cyan]",
                border_style="green",
            )
        )
        console.print()
        log_json = json.dumps(nodes[0].ordered_log(), indent=2)
        console.print(Panel(
            Syntax(log_json, "json", theme="monokai"),
            title="[bold white]Ordered log[/bold white]",
            border_style="bright_blue",
        ))
        return 0

    console.print(
        Panel("[bold red]✗ NOT CONVERGED[/bold red]", border_style="red")
    )
    for node in nodes:
        log_json = json.dumps(node.ordered_log(), indent=2)
        console.print(Panel(
            Syntax(log_json, "json", theme="monokai"),
            title=f"[bold white]{node.name} log[/bold white]",
            border_style="red",
        ))
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=int, default=3, help="number of independent nodes")
    parser.add_argument("--slot-ms", type=int, default=500, help="canonical slot period in ms")
    parser.add_argument("--seed", type=int, default=42, help="shuffle seed for per-node arrival order")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_demo(node_count=args.nodes, slot_ms=args.slot_ms, seed=args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
