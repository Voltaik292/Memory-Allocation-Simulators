# Test Cases — Paging Memory Allocation

Three progressive test cases demonstrating paging behavior: basic allocation,
address translation, error handling, and non-contiguous frame reuse after release.

> Adapted from Slides 6–8 of `Paging-Memory-Allocation-Simulator.pptx`.

---

## How to Run

```bash
python paging.py
```

Then enter the commands below one at a time when prompted.

---

## Initial Setup (used for all test cases)

```
Enter number of frames: 8
Enter frame size in bytes: 256
```

> Number of frames should be a power of 2; frame size a positive integer.

---

## Test Case 1 — Basic Allocation & Translation

Verifies frame allocation and the `TR` command.

| Step | Command | What It Tests |
|------|---------|----------------|
| 1 | `RQ P0 3` | P0 takes frames 0, 1, 2 |
| 2 | `RQ P1 2` | P1 takes frames 3, 4 |
| 3 | `RQ P0 1` | P0 grows — takes frame 5 |
| 4 | `STAT` | Verify frame map |
| 5 | `TR P0 0 10` | Translate P0 page 0 + offset 10 → physical = `0*256 + 10 = 10` |
| 6 | `TR P1 1 100` | Translate P1 page 1 + offset 100 → physical = `4*256 + 100 = 1124` |
| 7 | `X` | Exit |

---

## Test Case 2 — Release & Error Handling

Verifies `RL` and robustness against invalid input.

| Step | Command | What It Tests |
|------|---------|----------------|
| 1 | `RQ P0 3` | Allocate P0 |
| 2 | `RQ P1 2` | Allocate P1 |
| 3 | `STAT` | Verify initial layout |
| 4 | `RL P1` | Release P1 — frames 3, 4 become free |
| 5 | `STAT` | Verify P1's frames are marked free |
| 6 | `RL P99` | **Invalid:** process not found → error message |
| 7 | `RQ P0` | **Invalid:** missing `num_pages` → error message |
| 8 | `TR P0 99 10` | **Invalid:** page not allocated → error message |
| 9 | `TR P0 0 9999` | **Invalid:** offset out of bounds → error message |
| 10 | `HELLO` | **Invalid:** unknown command → error message |
| 11 | `X` | Exit |

---

## Test Case 3 — Non-Contiguous Frame Reuse

Demonstrates paging's advantage: allocating a process into frames previously
held by a different process, even if they aren't contiguous.

| Step | Command | What It Tests |
|------|---------|----------------|
| 1 | `RQ P0 2` | P0 takes frames 0, 1 |
| 2 | `RQ P1 3` | P1 takes frames 2, 3, 4 |
| 3 | `STAT` | Verify initial layout |
| 4 | `RL P1` | Release P1 — frames 2, 3, 4 become free |
| 5 | `RQ P0 3` | P0 grows into the freed frames (non-contiguous reuse) |
| 6 | `STAT` | Verify P0 now owns frames 0, 1, 2, 3, 4 — pages stored non-contiguously by time of allocation |
| 7 | `TR P0 4 200` | Translate P0 page 4 + offset 200 → physical = `frame_index * 256 + 200` |
| 8 | `X` | Exit |

---

## Key Concepts Verified

- **Allocation:** `RQ` assigns free frames and updates the page table
- **Release:** `RL` frees all frames of a process and removes its page table
- **Address translation:** `TR` computes `physical = frame_index * frame_size + offset`
- **Non-contiguous placement:** paging allows a process's pages to sit in any free frames
- **Error handling:** invalid processes, missing arguments, out-of-bounds offsets, and unknown commands all produce clear error messages instead of crashing
