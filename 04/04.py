def fully_contains(a1, a2, b1, b2):
    if (b1 <= a1 <= b2
            and b1 <= a2 <= b2):
        return True
    if (a1 <= b1 <= a2
            and a1 <= b2 <= a2):
        return True
    return False


def partly_contains(a1, a2, b1, b2):
    if (b1 <= a1 <= b2
            or b1 <= a2 <= b2):
        return True
    if (a1 <= b1 <= a2
            or a1 <= b2 <= a2):
        return True
    return False


assignments = []

with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        elf1, elf2 = line.split(",")
        assignments.append([
            list(map(int, elf1.split("-"))),
            list(map(int, elf2.split("-")))
        ])

fully_contained_sum = 0
partly_contained_sum = 0

for ass in assignments:
    if fully_contains(*ass[0], *ass[1]):
        fully_contained_sum += 1
    if partly_contains(*ass[0], *ass[1]):
        partly_contained_sum += 1

print(f"Number of pairs fully contained in one another: {fully_contained_sum}")
print(f"Number of pairs partly contained in one another: {partly_contained_sum}")
