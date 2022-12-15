import numpy as np
from queue import PriorityQueue

height_map = []
start = (-1, -1)
goal = (-1, -1)
with open("input", "r") as f:
    for i, line in enumerate(f.read().strip().split("\n")):
        if line.find("S") >= 0:
            start = (i + 1, line.find("S") + 1)
            line = line.replace("S", "a")
        if line.find("E") >= 0:
            goal = (i + 1, line.find("E") + 1)
            line = line.replace("E", "z")
        height_map.append([ord(letter) - 97 for letter in line])

height_map = np.array(height_map)
height_map = np.pad(
    height_map, ((1, 1), (1, 1)), "constant", constant_values=30
)
path_queue = PriorityQueue()
path_queue.put((0, start))

known_distances = {start: 0}
known_paths = {}

while not path_queue.empty():
    energy, coords = path_queue.get()
    # print(f"Now looking at {coords} with energy {energy}")
    if coords == goal:
        break
    energy += 1
    for x, y in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
        new_coords = (coords[0] + x, coords[1] + y)
        # print(f"New Neighbor: {new_coords}")
        if height_map[new_coords] <= height_map[coords] + 1 and (
            new_coords not in known_distances
            or known_distances[new_coords] > energy
        ):
            # print(f"Good neighbor!")
            known_distances[new_coords] = energy
            known_paths[new_coords] = coords
            path_queue.put((energy, new_coords))

print(f"Shortest path to goal takes {known_distances[goal]} steps.")

plot_map = np.zeros(height_map.shape)
coords = goal
while coords != start:
    plot_map[coords] = 1
    coords = known_paths[coords]
for row in range(plot_map.shape[0]):
    for col in range(plot_map.shape[1]):
        if plot_map[row, col] == 1:
            print("#", end="")
        else:
            print(".", end="")
    print("")
