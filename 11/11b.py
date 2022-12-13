def monkey_do(op):
    if op[23:] == "* old":
        return lambda x: x * x
    modifier = int(op[25:])
    if op[23] == "*":
        return lambda x: x * modifier
    if op[23] == "+":
        return lambda x: x + modifier


def monkey_test(test, if_true, if_false):
    test = int(test[21:])
    if_true = int(if_true[29:])
    if_false = int(if_false[30:])
    # print(if_true, if_false)
    def actual_test(num):
        if num % test == 0:
            return if_true
        return if_false
    return actual_test


with open("input", "r") as f:
    monkeys_raw = f.read().strip().split("\n\n")

monkeys = []
anti_worrier = 1

for monk in monkeys_raw:
    _, items_raw, op_raw, test_raw, if_true_raw, if_false_raw = monk.split("\n")
    monkeys.append([
        list(map(int, items_raw[18:].split(", "))),
        monkey_do(op_raw),
        monkey_test(test_raw, if_true_raw, if_false_raw)
    ])
    # use least common multiple to keep the numbers manageable
    anti_worrier *= int(test_raw[21:])


monkey_activism = [0 for i in range(len(monkeys))]
round_number = 0
while round_number < 10000:
    for i, monkey in enumerate(monkeys):
        while len(monkey[0]) > 0:
            item = monkey[0].pop(0)
            item = monkey[1](item)
            # item = item // 3
            target = monkey[2](item)
            item = item % anti_worrier
            monkeys[target][0].append(item)
            monkey_activism[i] += 1
    round_number += 1
    # print(f"----------------------Round {round_number}")
    # for mo in monkeys:
    #     print(mo[0])

print(f"Monkey activity: {monkey_activism}")
monkey_activism.sort()
print(f"Monkey business of top 2 monkey activists: "
      f"{monkey_activism[-2] * monkey_activism[-1]}")
