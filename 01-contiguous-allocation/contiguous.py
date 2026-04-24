def create_block(start: int, size: int, process: str | None = None) -> dict:
    # Create a memory block dictionary, can be either allocated block of free !.
    return {"start": start, "size": size, "end": start + size - 1, "process": process}

def show_status(blocks: list[dict]) -> None:
    # Prints the current status of my simmulated memory to the sceen.
    # a loop to go through all blocks list, if a block has a process it prints it as used, ow. prints it as unused.
    for b in blocks:
        if b["process"]:
            print(f"Addresses [{b['start']}:{b['end']}] Process {b['process']}")
        else:
            print(f"Addresses [{b['start']}:{b['end']}] Unused")

def compact_memory_and_collapse_holes(blocks: list[dict]) -> list[dict]:
    # Puts all allocated memory blocks in the front and puts all the holes at the end after merging them .
    used = [b for b in blocks if b['process']]
    free_sz = sum(b['size'] for b in blocks if not b['process'])
    pos = 0
    for b in used:
        b['start'] = pos
        b['end'] = b['start'] + b['size'] - 1
        pos += b['size']
    if free_sz:
        used.append(create_block(pos, free_sz))
    return used

def request_memory(blocks: list[dict], process: str, size: int, strat: str) -> list[dict]:
    # Request memory allocation for a process with a given strategy: F (First Fit), B (Best Fit), W (Worst Fit).
    # Find all the holes (free blocks) that are big enough to fit the request.
    holes = []
    for i in range(len(blocks)):
        block = blocks[i]
        if block['process'] is None and block['size'] >= size:
            holes.append((i, block))  # store the index and the block itself.

    if not holes:
        print(f"error: can't alloc mem for {process}")
        return blocks

    # Choose the appropriate hole based on the strategy
    if strat == 'F':
        idx, hole = holes[0]  # First Fit: just take the first suitable one.
    elif strat == 'B':
        # Best Fit: smallest hole that fits.
        min_size = 9999999999999999999
        for i, h in holes:
            if h['size'] < min_size:
                min_size = h['size']
                idx, hole = i, h
    elif strat == 'W':
        # Worst Fit: largest hole that fits.
        max_size = -1
        for i, h in holes:
            if h['size'] > max_size:
                max_size = h['size']
                idx, hole = i, h
    else:
        print("bad strategy")
        return blocks

    # Allocate memory from the chosen hole.
    del blocks[idx]  # remove the old hole.
    blocks.insert(idx, create_block(hole['start'], size, process))  # insert the new allocated block.

    # If there is leftover space, insert it as a new free block.
    if hole['size'] > size:
        blocks.insert(idx + 1, create_block(hole['start'] + size, hole['size'] - size))

    return blocks


def release_memory(blocks: list[dict], process: str) -> list[dict]:
    # Frees memory used by a specific process and merges adjacent holes.
    # Loops through all blocks.
    # When it finds the process, it sets its process field to None.
    # After releasing, it calls merge_blocks() to clean up.
    found = False
    for b in blocks:
        if b['process'] == process:
            b['process'] = None
            found = True
    if not found:
        print(f"process {process} not found")
    return merge_blocks(blocks)

def merge_blocks(blocks: list[dict]) -> list[dict]:
    # Merge adjacent free memory blocks into one big block to avoid fragmentation.
    res = []
    i = 0
    while i < len(blocks):
        if blocks[i]['process'] is None:
            st = blocks[i]['start']
            sz = blocks[i]['size']
            j = i + 1
            while j < len(blocks) and blocks[j]['process'] is None:
                sz += blocks[j]['size']
                j += 1
            res.append(create_block(st, sz))
            i = j
        else:
            res.append(blocks[i])
            i += 1
    return res

def main() -> None:
    # Main function to run the allocator prompt loop
    try:
        total = int(input("Enter total memory size: "))
    except:
        print("bad mem size")
        return

    mem = [create_block(0, total)]

    while True:
        try:
            cmd_input = input("allocator>").strip()
            if cmd_input == 'X':
                break
            elif cmd_input == 'STAT':
                show_status(mem)
            elif cmd_input == 'C':
                mem = compact_memory_and_collapse_holes(mem)
            elif cmd_input.startswith('RQ'):
                parts = cmd_input.split()
                mem = request_memory(mem, parts[1], int(parts[2]), parts[3])
            elif cmd_input.startswith('RL'):
                parts = cmd_input.split()
                mem = release_memory(mem, parts[1])
            else:
                print("unknown command")
        except Exception as e:
            print("error:", e)

if __name__ == '__main__':
    main()
