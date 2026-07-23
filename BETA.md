# Vortex DSE — Beta

**A deterministic "who-wins" arbitration primitive for exclusive-action
coordination between AI agents.**

## The problem

Multi-agent AI systems increasingly need to coordinate on *exclusive*
actions — two agents trying to claim the same resource, execute the same
tool-call with a side effect, or make the same booking/payment. Unlike
collaborative editing (where CRDTs let concurrent writes both survive),
exclusive actions need a single, unambiguous winner. Two agents both
"succeeding" at the same exclusive action is a bug, not a merge.

## What the beta gives you

An endpoint that resolves exactly this: submit a claim, get back a
deterministic, ordered decision — which claim wins, at which slot, with a
receipt — typically in well under a second, across continents, with:

- **No leader election, no voting, no gossip** — resolution is
  deterministic by construction.
- **Physical lower bound latency** (τ_min = 2×RTT) — not an artificial
  round count.
- **Formally verified core** — TLA+/TLC/Apalache/TLAPS, and now Lean4 for
  the agreement-extension layer. See the [whitepaper](vortex_dse_whitepaper_en.md)
  and [proof repos](https://github.com/vasilisnasopoulos-stack).

## Scope of this beta

This is an early, open beta of the **coordination/ordering primitive**
only — not a hosted database, not a full agent framework. You send a
claim, you get back a canonical decision. What you build on top (locking
semantics, retries, application logic) is up to you.

The service is offered as a **black box**: you interact with the public
HTTP interface only — submit a claim, receive a decision and receipt.
The underlying engine, its internal ordering rule, and the security
mechanisms behind it remain proprietary and are not exposed by this beta.

## Requesting access

Access is token-gated (entry-cost admission — see the whitepaper's
Sybil-resistance discussion). To request a token:

1. Open an issue in this repository using the **Beta Access Request**
   template, or
2. Email vasilis_nasopoulos@hotmail.com with a short description of what
   you're building.

Tokens are currently issued manually while the beta is small. Expect a
short delay, not instant automated signup.

## Status

Early beta. Endpoints and token format may change without notice. Not
recommended for production traffic yet — this is for evaluation and
integration testing.
