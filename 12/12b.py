import numpy as np
from queue import PriorityQueue

height_map = []
goal = (-1, -1)
with open("input", "r") as f:
    for i, line in enumerate(f.read().strip().split("\n")):
        if line.find("S") >= 0:
            line = line.replace("S", "a")
        if line.find("E") >= 0:
            goal = (i + 1, line.find("E") + 1)
            line = line.replace("E", "z")
        height_map.append([ord(letter) - 97 for letter in line])

height_map = np.array(height_map)
height_map = np.pad(
    height_map, ((1, 1), (1, 1)), "constant", constant_values=30
)
starts = []
for row in range(height_map.shape[0]):
    for col in range(height_map.shape[1]):
        if height_map[row, col] == 0:
            starts.append((row, col))

shortest_distances = {}
for start in starts:
    path_queue = PriorityQueue()
    path_queue.put((0, start))

    known_distances = {start: 0}
    known_paths = {}

    while not path_queue.empty():
        energy, coords = path_queue.get()
        # print(f"Now looking at {coords} with energy {energy}")
        if coords == goal:
            shortest_distances[start] = known_distances[goal]
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

print(f"Shortest path to goal from any starting point at level a "
      f"takes {min(shortest_distances.values())} steps.")
