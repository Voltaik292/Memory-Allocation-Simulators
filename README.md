# Memory Allocation Simulators

**Project 2 — ENCS3390 (Operating Systems), Birzeit University**

Two Python CLI simulators demonstrating core memory-management techniques
from Chapter 9 of the Silberschatz Operating Systems textbook:

1. **Contiguous Memory Allocation** — First-Fit, Best-Fit, Worst-Fit, with compaction
2. **Paging** — frames, page tables, and virtual-to-physical address translation

---

## Authors

| # | Name | Student ID | Part Implemented |
|---|------|------------|------------------|
| 1 | **Abdulrahman Sawalmeh** | 1221574 | `01-contiguous-allocation` |
| 2 | **Saleh Shawer**          | 1220217 | `02-paging-allocation` |

---

## Repository Index

| # | Folder | Description |
|---|--------|-------------|
| 01 | [`01-contiguous-allocation/`](01-contiguous-allocation/) | Contiguous allocator with First/Best/Worst-Fit + compaction |
| 02 | [`02-paging-allocation/`](02-paging-allocation/) | Paging simulator with frame allocation + address translation |

Each folder contains:
- The Python source file
- A `test_cases.md` file with ready-to-run command sequences
- The `.pptx` presentation documenting design, data structures, and results

---

## Requirements

- **Python 3.10 or newer** (the contiguous script uses the `str | None` type-hint syntax introduced in PEP 604)
- No external dependencies — standard library only

---

## Part 1 — Contiguous Memory Allocation

**Run:**

```bash
cd 01-contiguous-allocation
python contiguous.py
```

The program first asks for the total memory size, then enters a command loop.

### Commands

| Command | Description |
|---|---|
| `RQ <process> <size> <F\|B\|W>` | Request memory using First-Fit (`F`), Best-Fit (`B`), or Worst-Fit (`W`) |
| `RL <process>` | Release memory held by a process (adjacent free blocks are merged) |
| `C` | Compact memory — move all used blocks to the front, consolidate free space |
| `STAT` | Print current memory map (used vs. unused blocks with address ranges) |
| `X` | Exit |

### Example

```
Enter total memory size: 1000000
allocator>RQ P1 200000 F
allocator>RQ P2 300000 B
allocator>STAT
Addresses [0:199999] Process P1
Addresses [200000:499999] Process P2
Addresses [500000:999999] Unused
allocator>X
```

See [`01-contiguous-allocation/test_cases.md`](01-contiguous-allocation/test_cases.md) for a full test sequence.

---

## Part 2 — Paging

**Run:**

```bash
cd 02-paging-allocation
python paging.py
```

The program asks for the number of frames and the frame size, then enters a command loop.

### Commands

| Command | Description |
|---|---|
| `RQ <process> <num_pages>` | Allocate N pages to a process (assigns free frames, updates page table) |
| `RL <process>` | Release all frames held by a process |
| `TR <process> <page> <offset>` | Translate a virtual address `(page, offset)` to a physical address |
| `STAT` | Print current frame map (which process and page each frame holds) |
| `X` | Exit |

### Example

```
Enter number of frames: 8
Enter frame size in bytes: 256
paging> RQ P0 3
Allocated 3 page(s) to process P0.
paging> TR P0 1 50
Physical address = 306
paging> STAT
Frame 0: Process P0 - Page 0
Frame 1: Process P0 - Page 1
Frame 2: Process P0 - Page 2
Frame 3: Free
...
paging> X
```

See [`02-paging-allocation/test_cases.md`](02-paging-allocation/test_cases.md) for a full test sequence.

---

## Documentation

Each part includes a PowerPoint deck with detailed explanations, data
structures, and annotated output screenshots:

- [`01-contiguous-allocation/Contiguous-Memory-Allocation-Simulator.pptx`](01-contiguous-allocation/Contiguous-Memory-Allocation-Simulator.pptx)
- [`02-paging-allocation/Paging-Memory-Allocation-Simulator.pptx`](02-paging-allocation/Paging-Memory-Allocation-Simulator.pptx)
