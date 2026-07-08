# Public demo

This folder contains a small public demo of the deterministic slot-ordering
idea described in the Vortex DSE whitepaper.

## What it demonstrates

- one producer broadcasting transactions to multiple independent nodes,
- deterministic canonical-slot assignment,
- duplicate rejection,
- future-dated rejection beyond a fixed admission horizon,
- identical ordered logs and identical final hashes across nodes.

## What it does not claim

- it is not the proprietary Vortex DSE engine,
- it does not implement the full runtime invariant set,
- it is an educational proof-of-concept only.

## Run

```bash
python3 vortex_demo.py
```

Optional flags:

```bash
python3 vortex_demo.py --nodes 5 --slot-ms 500 --seed 7
```
