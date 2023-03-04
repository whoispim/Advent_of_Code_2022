def operate(monk1, monk2, op):
    if op == "+":
        return monk1 + monk2
    if op == "-":
        return monk1 - monk2
    if op == "*":
        return monk1 * monk2
    if op == "/":
        return monk1 / monk2


def rev_operate(monk1, monk2, op, pos):
    if op == "+":
        return monk1 - monk2
    if op == "*":
        return monk1 / monk2
    if op == "-":
        if pos == 1:
            return monk1 + monk2
        return monk2 - monk1
    if op == "/":
        if pos == 1:
            return monk1 * monk2
        return monk2 / monk1


def get_number(monk):
    if monk == "humn":
        print("HUMAN FOUND BEEP BOOP")
        return 0, True
    if monk in numbers:
        return numbers[monk], False

    targ1, targ2, op = operations[monk]
    num1, humn1 = get_number(targ1)
    num2, humn2 = get_number(targ2)
    if not (humn1 or humn2):
        return operate(num1, num2, op), False

    if humn1:
        human_ops.append((num2, op, 1))
        return num2, True
    if humn2:
        human_ops.append((num1, op, 2))
        return num1, True


def get_humn(monk):
    path_1, is_human_1 = get_number(operations["root"][0])
    path_2, is_human_2 = get_number(operations["root"][1])

    if is_human_1:
        non_human = path_2
    else:
        non_human = path_1
    print(f"Path without human actor results in {int(non_human)}")
    print(f"Calculating {len(human_ops)} operations on human side")

    for opera in human_ops[::-1]:
        non_human = rev_operate(non_human, *opera)

    print(f"Human should have yelled: {int(non_human)}")


with open("21/input", "r") as f:
    numbers = {}
    operations = {}
    for line in f.read().strip().split("\n"):
        monkey, thing = line.split(": ")
        if thing.isdigit():
            numbers[monkey] = int(thing)
        else:
            target1, op, target2 = thing.split(" ")
            operations[monkey] = (target1, target2, op)
    operations["root"] = operations["root"][:2]
    del numbers["humn"]

human_ops = []

get_humn("root")
