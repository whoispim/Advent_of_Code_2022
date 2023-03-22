# implement time as 3rd axis.

import math
import time
import numpy as np
from queue import Queue


def next_minute(layer):
    new_layer = np.zeros(layer.shape, dtype=np.byte)
    for i, row in enumerate(layer):
        for j, point in enumerate(row):
            if point == 16:
                new_layer[i, j] = 16
            # modulo-stuff because we got walls
            if point & 1:  # up
                new_layer[(i - 3) % i_max + 2, j] += 0b0001
            if point & (1 << 1):  # right
                new_layer[i, j % j_max + 1] += 0b0010
            if point & (1 << 2):  # down
                new_layer[(i - 1) % i_max + 2, j] += 0b0100
            if point & (1 << 3):  # left
                new_layer[i, (j - 2) % j_max + 1] += 0b1000
    return new_layer


start_time = time.time()

with open("24/input") as f:
    lines = f.read().strip().split("\n")
# add wall to top
lines.insert(0, "#" * len(lines[0]))

# start with first layer at t0
valley = np.zeros((len(lines), len(lines[0]), 1), dtype=np.byte)
for i, line in enumerate(lines):
    for j, point in enumerate(line):
        if point == "^":
            valley[i, j, 0] = 0b00001
        elif point == ">":
            valley[i, j, 0] = 0b00010
        elif point == "v":
            valley[i, j, 0] = 0b00100
        elif point == "<":
            valley[i, j, 0] = 0b01000
        elif point == "#":
            valley[i, j, 0] = 0b10000

i_max, j_max = valley.shape[0] - 3, valley.shape[1] - 2
# least common multiple will tell us how big our 3D-matrix should be
lcm = math.lcm(i_max, j_max)

# build matrix
for minute in range(lcm - 1):
    valley = np.dstack((valley, next_minute(valley[:, :, -1])))

start = (1, 1)
goal = (valley.shape[0] - 1, valley.shape[1] - 2)

print(
    f"Valley of shape {valley.shape} generated ",
    f"after {time.time()-start_time:.2f} seconds.",
)
print(f"Start: {start}")
print(f"Goal:  {goal}")

queue = Queue()
# row, col, t, steps
queue.put((1, 1, 0, 0))
visited = [(1, 1, 0)]

while not queue.empty():
    i, j, t, s = queue.get()
    t = (t + 1) % lcm
    s += 1
    for a, b in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
        go_here = (i + a, j + b, t, s)
        if go_here[:2] == goal:
            print(
                f"Success on minute {s}! This took ",
                f"{time.time()-start_time:.2f} real time ",
                f"seconds in total.",
            )
            break
        if valley[go_here[:3]] == 0:
            if go_here[:3] not in visited:
                # print(f"Added {go_here} to q")
                visited.append(go_here[:3])
                queue.put(go_here)
    else:
        # will continue if for wasn't broken
        continue
    break
