from queue import LifoQueue
import re

with open("input_festive", "r") as f:
    stack_input, crane_input = f.read().strip("\n").split("\n\n")

stacks = []
for i, row in enumerate(stack_input.split("\n")[0:-1][::-1]):
    for j in range((len(row) + 1) // 4):
        if i == 0:
            stacks.append(LifoQueue())
        item = row[j * 4 + 1]
        if item != " ":
            stacks[j].put(row[j * 4 + 1])

crane = [
    tuple(map(int, re.split("move | from | to ", a)[1:]))
    for a in crane_input.split("\n")
]

crane_buffer = LifoQueue()
for move in crane:
    amount = move[0]
    stack_from = move[1] - 1
    stack_to = move[2] - 1
    for i in range(amount):
        crane_buffer.put(stacks[stack_from].get())
    while not crane_buffer.empty():
        stacks[stack_to].put(crane_buffer.get())

print(
    f"Crates in top of stack after {len(crane)} "
    f"operations using CrateMover 9001: ",
    end=""
)
for stack in stacks:
    print(stack.get(), end="")
print()
