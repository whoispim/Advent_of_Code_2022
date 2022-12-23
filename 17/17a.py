import numpy as np


def next_rock():
    while True:
        for rock in rock_types:
            yield rock


def next_gas():
    while True:
        for direction in gas:
            yield direction


def blow_rock(the_rock):
    if next(gas_gen) == ">":
        if np.all(the_rock[:, -1] == 0):
            the_rock = np.roll(the_rock, shift=1)
    else:
        if np.all(the_rock[:, 0] == 0):
            the_rock = np.roll(the_rock, shift=-1)
    return the_rock



rock_types = []
with open("rock_types", "r") as f:
    for rock in f.read().strip().split("\n\n"):
        r = []
        for line in rock.replace("#", "1").replace(".", "0").split("\n"):
            r.append(list(line))
        rock_types.append(np.array(r, dtype=int))

with open("input", "r") as f:
    gas = f.read().strip()

rock_gen = next_rock()
gas_gen = next_gas()
chamber = np.ones((1, 7))

for j in range(2022):
    a_rock = next(rock_gen)
    rock_height = a_rock.shape[0]
    # trim zero-rows, add spacer
    chamber = chamber[~np.all(chamber == 0, axis=1)]
    chamber = np.concatenate((np.zeros((3 + rock_height, 7)),
                              chamber))
    fall = 0
    while True:
        blown_rock = blow_rock(a_rock)
        # can't be blown into walls
        if np.all(np.add(blown_rock, chamber[fall:fall+rock_height, :]) <= 1):
            a_rock = blown_rock
        if np.any(np.add(a_rock, chamber[fall+1:fall+1+rock_height, :]) == 2):
            chamber = np.concatenate((
                chamber[:fall, :],
                np.add(a_rock, chamber[fall:fall + rock_height, :]),
                chamber[fall + rock_height:, :]
            ))
            break
        else:
            fall += 1
chamber = chamber[~np.all(chamber == 0, axis=1)]

print(f"Final stack height is {chamber.shape[0] - 1}")
