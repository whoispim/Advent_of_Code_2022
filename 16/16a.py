import re
from queue import PriorityQueue
import itertools
import time


def find_shortest_connections(start, cons):
    path_queue = PriorityQueue()
    path_queue.put((0, start))

    known_distances = {start: 0}
    known_paths = {}

    while not path_queue.empty():
        dist, room = path_queue.get()
        dist += 1
        for next_room in cons[room]:
            if (next_room not in known_distances
                    or known_distances[next_room] > dist):
                known_distances[next_room] = dist
                known_paths[next_room] = room
                path_queue.put((dist, next_room))
    return known_distances


def open_valves(time_left: int, current_room: str, opened: set) -> int:
    if time_left <= 0:
        return 0

    best_release = 0
    opened = opened.copy()
    opened.add(current_room)
    for next_room in flow_rates:
        if next_room not in opened:
            new_time = time_left - distances[current_room][next_room] - 1
            profit = new_time * flow_rates[next_room]
            best_release = max(
                best_release,
                profit + open_valves(new_time, next_room, opened)
            )

    return best_release


flow_rates = {"AA": 0}
connections = {}

with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        valve = line[6:8]
        rate = int(line.split(" ")[4].split("=")[1][:-1])
        goes_to = re.findall("[A-Z]{2}", line.split(";")[1])
        if rate > 0:
            flow_rates[valve] = rate
        connections[valve] = goes_to

distances = {
    key: find_shortest_connections(key, connections)
    for key in connections.keys()
}

start_time = time.time()
print(open_valves(30, "AA", set()))
print(f"{time.time() - start_time}s")
