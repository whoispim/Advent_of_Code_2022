import numpy as np
from queue import Queue


def find_air(lav):
    air = set()
    air.add((0, 0, 0))
    air_queue = Queue()
    air_queue.put((0, 0, 0))
    while not air_queue.empty():
        cx, cy, cz = air_queue.get()
        for x_offset in [-1, 1]:
            xo = max(0, cx + x_offset)
            xo = min(lav.shape[0]-1, xo)
            if lav[xo, cy, cz] == 0:
                if (xo, cy, cz) not in air:
                    air.add((xo, cy, cz))
                    air_queue.put((xo, cy, cz))
        for y_offset in [-1, 1]:
            yo = max(0, cy + y_offset)
            yo = min(lav.shape[1]-1, yo)
            if lav[cx, yo, cz] == 0:
                if (cx, yo, cz) not in air:
                    air.add((cx, yo, cz))
                    air_queue.put((cx, yo, cz))
        for z_offset in [-1, 1]:
            zo = max(0, cz + z_offset)
            zo = min(lav.shape[2]-1, zo)
            if lav[cx, cy, zo] == 0:
                if (cx, cy, zo) not in air:
                    air.add((cx, cy, zo))
                    air_queue.put((cx, cy, zo))
    return air


def check_all_surfaces(air, x_, y_, z_):
    exposed = 0
    for x_offset in [-1, 1]:
        if (x_ + x_offset, y_, z_) in air:
            exposed += 1
    for y_offset in [-1, 1]:
        if (x_, y_ + y_offset, z_) in air:
            exposed += 1
    for z_offset in [-1, 1]:
        if (x_, y_, z_ + z_offset) in air:
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
outside_air = find_air(lava)
for dot in dots:
    exposed_surfaces += check_all_surfaces(outside_air, *dot)

print(f"Outside-air-exposed surface units: {exposed_surfaces}")
