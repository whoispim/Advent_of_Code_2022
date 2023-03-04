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
    sec = sector_map[curr]
    new_row = row + move_row
    new_col = col + move_col
    if (new_row < 0 or new_row == board.shape[0]
        or new_col < 0 or new_col == board.shape[1]
        or sector_map[new_row, new_col] == 0):
        new_row, new_col, direct = edge_transfer(new_row, new_col, direct, sec)

    return (new_row, new_col), direct


def edge_transfer(row, col, direct, sec):
    old_row = row % cube_size[0]
    old_col = col % cube_size[1]
    new_row = old_row
    new_col = old_col
    if sec == 1:
        if direct == 2:
            sec = 4
            direct = 0
            new_row = cube_size[0] - 1 - old_row
            new_col = 0
        elif direct == 3:
            sec = 6
            direct = 0
            new_row = old_col
            new_col = 0
    elif sec == 2:
        if direct == 0:
            sec = 5
            direct = 2
            new_row = cube_size[0] - 1 - old_row
            new_col = cube_size[1] - 1
        if direct == 1:
            sec = 3
            direct = 2
            new_row = old_col
            new_col = cube_size[1] - 1
        if direct == 3:
            sec = 6
            direct = 3
            new_row = cube_size[0] - 1
            new_col = old_col
    elif sec == 3:
        if direct == 0:
            sec = 2
            direct = 3
            new_row = cube_size[0] - 1
            new_col = old_row
        elif direct == 2:
            sec = 4
            direct = 1
            new_row = 0
            new_col = old_row
    elif sec == 4:
        if direct == 2:
            sec = 1
            direct = 0
            new_row = cube_size[0] - 1 - old_row
            new_col = 0
        elif direct == 3:
            sec = 3
            direct = 0
            new_row = old_col
            new_col = 0
    elif sec == 5:
        if direct == 0:
            sec = 2
            direct = 2
            new_row = cube_size[0] - 1 - old_row
            new_col = cube_size[1] - 1
        elif direct == 1:
            sec = 6
            direct = 2
            new_row = old_col
            new_col = cube_size[1] - 1
    elif sec == 6:
        if direct == 0:
            sec = 5
            direct = 3
            new_row = cube_size[0] - 1
            new_col = old_row
        elif direct == 1:
            sec = 2
            direct = 1
            new_row = 0
            new_col = old_col
        elif direct == 2:
            sec = 1
            direct = 1
            new_row = 0
            new_col = old_row
            
    
    if sec == 1:
        row = new_row
        col = new_col + cube_size[1]
    elif sec == 2:
        row = new_row
        col = new_col + cube_size[1] * 2
    elif sec == 3:
        row = new_row + cube_size[0]
        col = new_col + cube_size[1]
    elif sec == 4:
        row = new_row + cube_size[0] * 2
        col = new_col
    elif sec == 5:
        row = new_row + cube_size[0] * 2
        col = new_col + cube_size[1]
    elif sec == 6:
        row = new_row + cube_size[0] * 3
        col = new_col
    return row, col, direct


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

cube_size = (board.shape[0] // 4, board.shape[1] // 3)
sector_map = np.concatenate(
    (
        np.concatenate(
            (
                np.full(cube_size, fill_value=0),
                np.full(cube_size, fill_value=1),
                np.full(cube_size, fill_value=2),
            ),
            axis=1,
        ),
        np.concatenate(
            (
                np.full(cube_size, fill_value=0),
                np.full(cube_size, fill_value=3),
                np.full(cube_size, fill_value=0),
            ),
            axis=1,
        ),
        np.concatenate(
            (
                np.full(cube_size, fill_value=4),
                np.full(cube_size, fill_value=5),
                np.full(cube_size, fill_value=0),
            ),
            axis=1,
        ),
        np.concatenate(
            (
                np.full(cube_size, fill_value=6),
                np.full(cube_size, fill_value=0),
                np.full(cube_size, fill_value=0),
            ),
            axis=1,
        ),
    ),
    axis=0,
)

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
        next_coords, next_direct = next_step(curr_coords, direction)
        if board[next_coords] < 6:
            curr_coords = next_coords
            direction = next_direct
        else:
            break
    direction = (direction + turn) % 4

for row in board:
    for col in row:
        print(plotdict[col], end="")
    print("")

print(f"Final state: {curr_coords[0]+1}, {curr_coords[1]+1}, {plotdict[direction]}")
score = 1000 * (curr_coords[0] + 1) + 4 * (curr_coords[1] + 1) + direction
print(f"Final password: {score}")
