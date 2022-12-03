elves = []

with open("input", "r") as f:
    for elf in f.read().strip().split("\n\n"):
        elves.append(list(map(int, elf.split("\n"))))

elves_sum = [sum(elf) for elf in elves]
elves_sum.sort()

print(f"There are {len(elves_sum)} elves in this expedition.\n"
      f"The biggest ration carried amounts to {elves_sum[-1]} calories.\n"
      f"The biggest three amount to {sum(elves_sum[-3:])}.")
