import re
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


def find_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


sensors = []
# calculate corners of sensor range, add .5 to avoid lines forming
with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        coords = list(map(int, re.findall("(-?[0-9]+)", line)))
        distance = find_distance(coords[:2], coords[2:]) + .5
        sensors.append([
            [coords[0] + distance, coords[1]],
            [coords[0], coords[1] + distance],
            [coords[0] - distance, coords[1]],
            [coords[0], coords[1] - distance]
        ])

map_max = 4000000  # 20

tunnel_map = Polygon([(0, 0), (0, map_max), (map_max, map_max), (map_max, 0)])
for sen in sensors:
    tunnel_map = tunnel_map.difference(Polygon(sen))

if isinstance(tunnel_map, type(Polygon())):
    if tunnel_map.area <= 1:
        print("Polygon cutting was a success!")
        print(f"Beacon location: {tunnel_map.centroid}")
        tuning_freq = int(tunnel_map.centroid.xy[0][0] * 4000000
                       + tunnel_map.centroid.xy[1][0])
        print(f"Beacon tuning frequency: {tuning_freq}")
