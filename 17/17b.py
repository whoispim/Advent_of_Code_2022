import numpy as np


def next_rock():
    while True:
        for y, rock in enumerate(rock_types):
            yield rock, y


def next_gas():
    while True:
        for i, direction in enumerate(gas):
            yield direction, i


def blow_rock(the_rock):
    direction, cyc = next(gas_gen)
    if direction == ">":
        if np.all(the_rock[:, -1] == 0):
            the_rock = np.roll(the_rock, shift=1)
    else:
        if np.all(the_rock[:, 0] == 0):
            the_rock = np.roll(the_rock, shift=-1)
    return the_rock, cyc


def drop_rocks(number_of_rocks):
    global gas_gen, chamber
    rock_gen = next_rock()
    gas_gen = next_gas()
    chamber = np.ones((1, 7))
    for j in range(number_of_rocks):
        a_rock, rock_t = next(rock_gen)
        rock_height = a_rock.shape[0]
        # trim zero-rows, add spacer
        chamber = chamber[~np.all(chamber == 0, axis=1)]
        chamber = np.concatenate((np.zeros((3 + rock_height, 7)),
                                  chamber))
        fall = 0
        while True:
            blown_rock, cycle = blow_rock(a_rock)
            # can't be blown into walls
            if np.all(np.add(blown_rock,
                             chamber[fall:fall + rock_height, :]) <= 1):
                a_rock = blown_rock
            if np.any(np.add(a_rock,
                             chamber[fall + 1:fall + 1 + rock_height, :]) == 2):
                chamber = np.concatenate((
                    chamber[:fall, :],
                    np.add(a_rock, chamber[fall:fall + rock_height, :]),
                    chamber[fall + rock_height:, :]
                ))
                break
            else:
                fall += 1
    chamber = chamber[~np.all(chamber == 0, axis=1)]
    return chamber.shape[0] - 1


rock_types = []
with open("rock_types", "r") as f:
    for rock in f.read().strip().split("\n\n"):
        r = []
        for line in rock.replace("#", "1").replace(".", "0").split("\n"):
            r.append(list(line))
        rock_types.append(np.array(r, dtype=int))

with open("input", "r") as f:
    gas = f.read().strip()

# checking for repeating patterns in stack size difference after 10000 rocks:
# the first 183 rocks show no pattern
# following height changes have a phase length of 1745
phases_needed = 1000000000000 // 1745
after_phases = 1000000000000 % 1745 - 183
height1 = drop_rocks(183)
print(f"Stack height after 183 rocks is {height1}")
height2 = drop_rocks((183 + 1745))
height_phase = height2 - height1
print(f"Stack height of 1745-rock-phase is {height_phase}")
height3 = drop_rocks((183 + 1745 + after_phases))
height_post = height3 - height2
print(f"Stack height of post-phase {after_phases} rocks is {height_post}")
print(f"Phases needed to reach 1000000000000 rocks: {phases_needed}")
height_final = (height1
                + phases_needed * height_phase
                + height_post)
print(f"Final height is {height_final}")