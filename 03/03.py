priorities = {
    l: n + 1
    for n, l in enumerate(
        list(
            map(
                chr,
                list(range(ord("a"), ord("z") + 1))
                + list(range(ord("A"), ord("Z") + 1)),
            )
        )
    )
}

backpacks = []

with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        split = len(line) // 2
        backpacks.append([line[:split], line[split:]])

priority_sum = 0
for pack in backpacks:
    for item in pack[0]:
        if item in pack[1]:
            break
    priority_sum += priorities[item]

print(f"Sum of the priorities of items present in both compartments: {priority_sum}")

priority_sum = 0
for i in range(0, len(backpacks)-2, 3):
    for item in backpacks[i][0] + backpacks[i][1]:
        if (item in backpacks[i+1][0] + backpacks[i+1][1]
                and item in backpacks[i+2][0] + backpacks[i+2][1]):
            break
    priority_sum += priorities[item]

print(f"Sum of the priorities of items present in a triplets backpacks: {priority_sum}")