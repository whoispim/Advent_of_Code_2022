import numpy as np


def check_surfaces(lav, x_, y_, z_):
    exposed = 0
    for x_offset in [-1, 1]:
        if lav[x_ + x_offset, y_, z_] == 0:
            exposed += 1
    for y_offset in [-1, 1]:
        if lav[x_, y_ + y_offset, z_] == 0:
            exposed += 1
    for z_offset in [-1, 1]:
        if lav[x_, y_, z_ + z_offset] == 0:
            exposed += 1
    return exposed


with open("input", "r") as f:
    dots = []
    for line in f.read().strip().split("\n"):
        dots.append(list(map(lambda x: int(x) + 1, line.split(","))))

lava = np.zeros((
    max([x[0] for x in dots]) + 2,
    max([x[1] for x in dots]) + 2,
    max([x[2] for x in dots]) + 2
))

for dot in dots:
    lava[dot[0], dot[1], dot[2]] = 1

exposed_surfaces = 0
for dot in dots:
    exposed_surfaces += check_surfaces(lava, *dot)

print(f"Exposed surface units: {exposed_surfaces}")
