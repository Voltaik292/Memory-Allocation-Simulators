# Test Cases — Contiguous Memory Allocation

A comprehensive command sequence demonstrating all simulator features:
First-Fit / Best-Fit / Worst-Fit allocation, release with hole merging,
compaction, and graceful error handling.

> Adapted from Slide 5 of `Contiguous-Memory-Allocation-Simulator.pptx`.

---

## How to Run

```bash
python contiguous.py
```

Then enter the commands below one at a time when prompted.

---

## Initial Setup

```
Enter total memory size: 1000000
```

---

## Command Sequence

| Step | Command | What It Tests |
|------|---------|----------------|
| 1 | `RQ P1 200000 F` | First-Fit allocation from empty memory |
| 2 | `RQ P2 300000 B` | Best-Fit allocation after P1 |
| 3 | `RQ P4 250000 B` | Best-Fit — should pick the tightest hole |
| 4 | `RQ P3 100000 W` | Worst-Fit — should pick the largest hole |
| 5 | `STAT` | Verify layout after initial allocations |
| 6 | `RQ P5 100000 F` | Allocate into remaining free space |
| 7 | `RL P1` | Release a process, leaving a hole at the start |
| 8 | `RQ P6 50000 W` | Worst-Fit into the new hole |
| 9 | `RL P3` | Release another process (test hole merging) |
| 10 | `STAT` | Verify holes and merging |
| 11 | `C` | Compact memory — consolidate all holes |
| 12 | `STAT` | Verify compaction moved used blocks to front |
| 13 | `RQ P7 700000 F` | Large allocation into the consolidated free space |
| 14 | `RQ P8 50000 B` | Best-Fit small allocation |
| 15 | `STAT` | Verify final layout |
| 16 | `RQ P9 100000 W` | **Expected to fail** — not enough free memory |
| 17 | `X` | Exit |

---

## Edge Cases Verified

- **Allocation strategies:** First-Fit, Best-Fit, Worst-Fit all exercised
- **Hole reuse:** freed blocks are successfully reused by later requests
- **Adjacent hole merging:** releasing neighboring blocks produces one big hole
- **Compaction:** `C` moves all used blocks forward and consolidates free space
- **Error handling:** requesting more memory than available prints an error instead of crashing
- **`STAT` reporting:** correctly shows address ranges and process names at every step
