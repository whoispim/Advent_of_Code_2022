import re


def find_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


sensors = []
with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        coords = list(map(int, re.findall("(-?[0-9]+)", line)))
        sensors.append([coords[:2], coords[2:]])

x_range = [0, 0]
for sen in sensors:
    sen.append(find_distance(*sen))
    # buffer x_range for sensor distance
    x_range[0] = min(x_range[0], sen[0][0] - sen[2], sen[1][0])
    x_range[1] = max(x_range[1], sen[0][0] + sen[2], sen[1][0])

# beware, this solution has _very_ poor performance!

target_row = 2000000
illegal_spots = 0
for x in range(x_range[0], x_range[1]+1):
    for sen in sensors:
        if (find_distance(sen[0], [x, target_row]) <= sen[2]
                and find_distance(sen[1], [x, target_row]) > 0):
            illegal_spots += 1
            break

print(f"Row {target_row} contains {illegal_spots} spots where a beacon "
      f"cannot be present.")
