import re
from queue import PriorityQueue
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


def open_valves(time_left: int, curr_1: str, curr_2: str,
                opened: frozenset) -> int:
    if time_left <= 0:
        return 0
    offen = len(opened)
    if offen == valve_count:
        return 0
    # extremely rudimentary pruning
    elif time_left < 16 and offen <= 1:
        return 0
    elif time_left < 10 and offen <= 8:
        return 0
    state_hash = hash(frozenset((time_left, curr_1, curr_2, opened)))
    if state_hash in memo_cache:
        return memo_cache[state_hash]
    time_left -= 1
    best_release = 0
    for next_room_1 in connections[curr_1]:
        for next_room_2 in connections[curr_2]:
            new_release = open_valves(time_left, next_room_1,
                                      next_room_2, opened)
            if new_release > best_release:
                best_release = new_release

    if curr_1 in flow_rates and curr_1 not in opened:
        opened_new = set(opened)
        opened_new.add(curr_1)
        profit = time_left * flow_rates[curr_1]
        for next_room_2 in connections[curr_2]:
            new_release = open_valves(time_left, curr_1,
                                      next_room_2, frozenset(opened_new))
            new_release += profit
            if new_release > best_release:
                best_release = new_release

    if curr_2 in flow_rates and curr_2 not in opened:
        opened_new = set(opened)
        opened_new.add(curr_2)
        profit = time_left * flow_rates[curr_2]
        for next_room_1 in connections[curr_1]:
            new_release = open_valves(time_left, next_room_1,
                                      curr_2, frozenset(opened_new))
            new_release += profit
            if new_release > best_release:
                best_release = new_release

    if (curr_1 in flow_rates and curr_2 in flow_rates
            and curr_1 not in opened and curr_2 not in opened
            and curr_1 != curr_2):
        opened_new = set(opened)
        opened_new.add(curr_1)
        opened_new.add(curr_2)
        profit = time_left * (flow_rates[curr_1] + flow_rates[curr_2])
        new_release = open_valves(time_left, curr_1,
                                  curr_2, frozenset(opened_new))
        new_release += profit
        if new_release > best_release:
            best_release = new_release

    memo_cache[state_hash] = best_release
    return best_release


flow_rates = {}
connections = {}

with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        valve = line[6:8]
        rate = int(line.split(" ")[4].split("=")[1][:-1])
        goes_to = re.findall("[A-Z]{2}", line.split(";")[1])
        if rate > 0:
            flow_rates[valve] = rate
        connections[valve] = goes_to

valve_count = len(flow_rates)
memo_cache = {}

start_time = time.time()
print(open_valves(26, "AA", "AA", frozenset()))
print(f"{time.time() - start_time}s")
