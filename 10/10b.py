def draw(cyc, x):
    if x-1 <= cyc <= x+1:
        print("#", end="")
    else:
        print(" ", end="")
    if cycle >= 39:
        print("")


with open("input", "r") as f:
    commands = f.read().strip().split("\n")

cycle = 0
X = 1

for com in commands:
    draw(cycle, X)
    cycle = (cycle + 1) % 40
    if com[0] == "a":
        draw(cycle, X)
        cycle = (cycle + 1) % 40
        X += int(com[5:])

