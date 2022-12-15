import numpy as np


def drop_sand():
    sand_coord = [0, 500]
    while True:
        if ceiling[sand_coord[0], sand_coord[1]] == 2:
            return False
        # print(sand_coord)
        if ceiling[sand_coord[0]+1, sand_coord[1]] == 0:
            sand_coord[0] += 1
        elif ceiling[sand_coord[0]+1, sand_coord[1]-1] == 0:
            sand_coord[0] += 1
            sand_coord[1] -= 1
        elif ceiling[sand_coord[0]+1, sand_coord[1]+1] == 0:
            sand_coord[0] += 1
            sand_coord[1] += 1
        else:
            ceiling[sand_coord[0], sand_coord[1]] = 2
            return True


rock_paths = []
with open("input", "r") as f:
    for path in f.read().strip().split("\n"):
        coords = []
        for coord in path.split(" -> "):
            coords.append(tuple(map(int, coord.split(",")))[::-1])
        rock_paths.append(coords)

max_right = max(
    [item for sublist in rock_paths for item in sublist],
    key=lambda x: x[1]
)[1]
max_down = max(
    [item for sublist in rock_paths for item in sublist],
    key=lambda x: x[0]
)[0]

ceiling = np.zeros((max_down+3, max_right+max_down))

for path in rock_paths:
    for i in range(len(path)-1):
        y_minmax = sorted([path[i][0], path[i+1][0]])
        x_minmax = sorted([path[i][1], path[i+1][1]])
        for y in range(y_minmax[0], y_minmax[1] + 1):
            for x in range(x_minmax[0], x_minmax[1] + 1):
                ceiling[y, x] = 1

ceiling[-1, :] = 1

grains = 0
while True:
    grains += 1
    if not drop_sand():
        break

print(f"{grains-1} grains of sand came to rest.")
