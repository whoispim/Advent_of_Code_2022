class Rope:
    def __init__(self):
        self.head_current = (0, 0)
        self.tail_current = (0, 0)
        self.tail_visited = [(0, 0)]

    def move(self, direction: str, distance: int):
        x, y = 0, 0
        if direction == "U": y = -1
        if direction == "D": y = 1
        if direction == "L": x = -1
        if direction == "R": x = 1
        for i in range(distance):
            self.head_current = (
                self.head_current[0] + x,
                self.head_current[1] + y
            )
            if abs(self.tail_current[0] - self.head_current[0]) > 1:
                self.tail_current = (
                    self.tail_current[0] + x,
                    self.head_current[1]
                )
            if abs(self.tail_current[1] - self.head_current[1]) > 1:
                self.tail_current = (
                    self.head_current[0],
                    self.tail_current[1] + y
                )
            if self.tail_current not in self.tail_visited:
                self.tail_visited.append(self.tail_current)


with open("input", "r") as f:
    head_moves = [
        (x[0], int(x[2:]))
        for x in f.read().strip().split("\n")
    ]

rope = Rope()
for mov in head_moves:
    rope.move(*mov)

print(f"Unique locations visited by the tail: {len(rope.tail_visited)}")
