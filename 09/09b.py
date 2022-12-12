from time import sleep
from math import copysign


class Rope:
    def __init__(self, knots=2):
        self.rope_current = [[0, 0] for i in range(knots)]
        self.tail_visited = [(0, 0)]

    def move(self, direction: str, distance: int):
        x, y = 0, 0
        if direction == "U": y = -1
        if direction == "D": y = 1
        if direction == "L": x = -1
        if direction == "R": x = 1
        for i in range(distance):
            # print(f"{direction}, {i+1}/{distance}")
            self.rope_current[0][0] += x
            self.rope_current[0][1] += y
            for k in range(1, len(self.rope_current)):
                if abs(self.rope_current[k-1][0] - self.rope_current[k][0]) > 1:
                    self.rope_current[k][0] += int(copysign(
                        1,
                        self.rope_current[k-1][0] - self.rope_current[k][0]
                    ))
                    if abs(self.rope_current[k-1][1] - self.rope_current[k][1]) > 0:
                        self.rope_current[k][1] += int(copysign(
                            1,
                            self.rope_current[k-1][1] - self.rope_current[k][1]
                        ))
                if abs(self.rope_current[k-1][1] - self.rope_current[k][1]) > 1:
                    self.rope_current[k][1] += int(copysign(
                        1,
                        self.rope_current[k-1][1] - self.rope_current[k][1]
                    ))
                    if abs(self.rope_current[k-1][0] - self.rope_current[k][0]) > 0:
                        self.rope_current[k][0] += int(copysign(
                            1,
                            self.rope_current[k-1][0] - self.rope_current[k][0]
                        ))
            if tuple(self.rope_current[-1]) not in self.tail_visited:
                self.tail_visited.append(tuple(self.rope_current[-1]))
            # print(k, self.rope_current)
            # self.show_map()
            # sleep(.2)

    def show_map(self):
        x_values, y_values = list(zip(*self.rope_current))
        for j in range(min(y_values) - 2, max(y_values) + 2):
            for i in range(min(x_values) - 2, max(x_values) + 2):
                o = "."
                for a, k in enumerate(self.rope_current):
                    if k[0] == i and k[1] == j:
                        o = str(a)
                print(o, end="")
            print("")


with open("input", "r") as f:
    head_moves = [
        (x[0], int(x[2:]))
        for x in f.read().strip().split("\n")
    ]

rope = Rope(10)
for mov in head_moves:
    rope.move(*mov)

print(f"Unique locations visited by the tail: {len(rope.tail_visited)}")
