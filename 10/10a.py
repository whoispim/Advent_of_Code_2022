# Find the signal strength during the
# 20th, 60th, 100th, 140th, 180th, and 220th cycles

with open("input", "r") as f:
    commands = f.read().strip().split("\n")

i_cycles = [20, 60, 100, 140, 180, 220]
cycle = 0
X = 1
i_signal_strengths = []

for com in commands:
    cycle += 1
    if cycle in i_cycles:
        i_signal_strengths.append(cycle * X)
    if com[0] == "a":
        cycle += 1
        if cycle in i_cycles:
            i_signal_strengths.append(cycle * X)
        X += int(com[5:])

print(i_signal_strengths)
print(f"Sum of interesting signal strengths: {sum(i_signal_strengths)}")
