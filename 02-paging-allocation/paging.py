def init_system():
    try:
        num_frames = int(input("Enter number of frames: "))
        frame_size = int(input("Enter frame size in bytes: "))
        if num_frames <= 0 or frame_size <= 0:
            print("Error: Values must be positive integers.")
            return None, None, None
    except ValueError:
        print("Error: Invalid input.")
        return None, None, None

    frames = [{"used": False, "pid": "-", "page_num": -1} for _ in range(num_frames)]
    processes = {}
    return frames, processes, frame_size


def count_free_frames(frames):
    return sum(1 for f in frames if not f["used"])


def find_free_frame(frames):
    for i, f in enumerate(frames):
        if not f["used"]:
            return i
    return -1


def rq(frames, processes, pid, num_pages):
    if count_free_frames(frames) < num_pages:
        print("Error: Not enough free frames.")
        return

    if pid not in processes:
        processes[pid] = {}

    page_table = processes[pid]
    start_page = len(page_table)

    for i in range(num_pages):
        frame_index = find_free_frame(frames)
        frames[frame_index]["used"] = True
        frames[frame_index]["pid"] = pid
        frames[frame_index]["page_num"] = start_page + i
        page_table[start_page + i] = frame_index

    print(f"Allocated {num_pages} page(s) to process {pid}.")


def rl(frames, processes, pid):
    if pid not in processes:
        print(f"Error: Process {pid} not found.")
        return

    for i, f in enumerate(frames):
        if f["used"] and f["pid"] == pid:
            frames[i]["used"] = False
            frames[i]["pid"] = "-"
            frames[i]["page_num"] = -1

    del processes[pid]
    print(f"Released memory for process {pid}.")


def stat(frames):
    for i, f in enumerate(frames):
        if f["used"]:
            print(f"Frame {i}: Process {f['pid']} - Page {f['page_num']}")
        else:
            print(f"Frame {i}: Free")


def tr(frames, processes, pid, page, offset, frame_size):
    if pid not in processes:
        print("Error: Process not found.")
        return

    page_table = processes[pid]
    if page not in page_table:
        print("Error: Page not allocated.")
        return

    if offset < 0 or offset >= frame_size:
        print(f"Error: Offset out of bounds (0 to {frame_size - 1}).")
        return

    frame_num = page_table[page]
    physical_address = frame_num * frame_size + offset
    print(f"Physical address = {physical_address}")


def main():
    frames, processes, frame_size = init_system()
    if frames is None:
        return

    while True:
        cmd = input("paging> ").strip()
        if not cmd:
            continue

        tokens = cmd.split()
        if tokens[0].upper() == "RQ" and len(tokens) == 3:
            pid = tokens[1]
            try:
                num_pages = int(tokens[2])
                rq(frames, processes, pid, num_pages)
            except ValueError:
                print("Error: num_pages must be an integer.")

        elif tokens[0].upper() == "RL" and len(tokens) == 2:
            rl(frames, processes, tokens[1])

        elif tokens[0].upper() == "STAT":
            stat(frames)

        elif tokens[0].upper() == "TR" and len(tokens) == 4:
            pid = tokens[1]
            try:
                page = int(tokens[2])
                offset = int(tokens[3])
                tr(frames, processes, pid, page, offset, frame_size)
            except ValueError:
                print("Error: page and offset must be integers.")

        elif tokens[0].upper() == "X":
            print("Exiting...")
            break

        else:
            print("Unknown command or wrong format.")


if __name__ == "__main__":
    main()
