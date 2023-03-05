import numpy as np

with open("23/input", "r") as f:
    elves_strings = f.read().strip().replace(".", "0").replace("#", "1").split("\n")
    elves = np.array([list(x) for x in elves_strings], dtype=int)


direction_coordinates = [
    ((-1, 0), (-1, -1), (-1, 1)),
    ((1, 0), (1, -1), (1, 1)),
    ((0, -1), (-1, -1), (1, -1)),
    ((0, 1), (-1, 1), (1, 1)),
]

round_number = 0
while True:
    start_elves = elves
    round_number += 1
    elves = np.pad(elves, pad_width=1, mode="constant", constant_values=0)
    elf_proposals = {}
    for i in range(1, elves.shape[0] - 1):
        for j in range(1, elves.shape[1] - 1):
            if elves[i, j] == 1:
                if np.sum(elves[i - 1 : i + 2, j - 1 : j + 2]) > 1:
                    for direction in direction_coordinates:
                        neighbours = 0
                        for position in direction:
                            neighbours += elves[i + position[0], j + position[1]]
                        if neighbours == 0:
                            elf_proposals[(i, j)] = (
                                i + direction[0][0],
                                j + direction[0][1],
                            )
                            break

    seen = set()
    multi_proposed = [x for x in elf_proposals.values() if x in seen or seen.add(x)]
    elf_proposals = {k: v for k, v in elf_proposals.items() if v not in multi_proposed}
    for k in elf_proposals.keys():
        elves[k] = 0
        elves[elf_proposals[k]] = 1

    while True:
        trimmed_elves = elves
        if np.sum(trimmed_elves[0, :]) == 0:
            trimmed_elves = trimmed_elves[1:, :]
        if np.sum(trimmed_elves[-1, :]) == 0:
            trimmed_elves = trimmed_elves[:-1, :]
        if np.sum(trimmed_elves[:, 0]) == 0:
            trimmed_elves = trimmed_elves[:, 1:]
        if np.sum(trimmed_elves[:, -1]) == 0:
            trimmed_elves = trimmed_elves[:, :-1]
        if np.all(trimmed_elves == elves):
            break
        elves = trimmed_elves

    if np.all(elves == start_elves):
        break
    direction_coordinates = direction_coordinates[1:] + direction_coordinates[0:1]

empty_spaces = elves.shape[0] * elves.shape[1] - np.sum(elves)

print("Equilibrium achieved!")
print(
    f"There are {empty_spaces} empty spaces on the elf grid after {round_number} moves"
)
