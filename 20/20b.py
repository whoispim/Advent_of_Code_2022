with open("input", "r") as f:
    code = [int(x) for x in f.read().strip().split("\n")]

code = [x*811589153 for x in code]
indices = [i for i in range(len(code))]
code_max = len(code) - 1

for cycle in range(10):
    for i in range(len(code)):
        current_pos = indices.index(i)
        move_code = code.pop(current_pos)
        move_index = indices.pop(current_pos)
        new_place = (current_pos + move_code - 1) % code_max + 1
        code.insert(new_place, move_code)
        indices.insert(new_place, move_index)

index_zero = code.index(0)
n1000 = code[(index_zero + 1000) % len(code)]
n2000 = code[(index_zero + 2000) % len(code)]
n3000 = code[(index_zero + 3000) % len(code)]
print(f"Number at pos 1000 after 0: {n1000}")
print(f"Number at pos 2000 after 0: {n2000}")
print(f"Number at pos 3000 after 0: {n3000}")
print(f"Sum: {sum([n1000, n2000, n3000])}")
