import numpy as np


def next_step(curr, direct):
    row, col = curr
    move_row, move_col = 0, 0
    if direct == 0:
        move_col = 1
    elif direct == 1:
        move_row = 1
    elif direct == 2:
        move_col = -1
    else:
        move_row = -1
    while True:
        row = (row + move_row) % board.shape[0]
        col = (col + move_col) % board.shape[1]
        if board[row, col] >= 0:
            break
    return row, col


with open("22/input", "r") as f:
    board_string, moves_string = f.read().strip("\n").split("\n\n")

board_string_lines = board_string.split("\n")
board = np.full(
    (len(board_string_lines), max(len(x) for x in board_string_lines)), fill_value=-1
)

for i, row in enumerate(board_string_lines):
    for j, col in enumerate(row):
        if col == ".":
            board[i, j] = 5
        elif col == "#":
            board[i, j] = 6

dists = []
turns = []

i = 0
dist = ""
for i, _ in enumerate(moves_string):
    char = moves_string[i]
    if char.isnumeric():
        dist += char
        continue
    dists.append(int(dist))
    dist = ""
    if char == "L":
        turns.append(-1)
    else:
        turns.append(1)
dists.append(int(dist))
turns.append(0)

direction = 0
curr_coords = (0, np.where(board[0] == 5)[0][0])

plotdict = {
    5: ".",
    6: "#",
    0: ">",
    1: "v",
    2: "<",
    3: "^",
    -1: " ",
}

for dist, turn in zip(dists, turns):
    for i in range(dist):
        board[curr_coords] = direction
        next_coords = next_step(curr_coords, direction)
        if board[next_coords] < 6:
            curr_coords = next_coords
        else:
            break
    direction = (direction + turn) % 4

for row in board:
    for col in row:
        print(plotdict[col], end="")
    print("")

print(
    f"Final state: {curr_coords[0]+1}, {curr_coords[1]+1}, {plotdict[direction]}"
)
score = 1000 * (curr_coords[0]+1) + 4 * (curr_coords[1]+1) + direction
print(f"Final password: {score}")

# 149139 too high
# 149135 too low