def operate(monk1, monk2, op):
    if op == "+":
        return lambda monk1, monk2: monk1 + monk2
    if op == "-":
        return lambda monk1, monk2: monk1 - monk2
    if op == "*":
        return lambda monk1, monk2: monk1 * monk2
    if op == "/":
        return lambda monk1, monk2: monk1 // monk2


def get_root(monk):
    if monk in numbers:
        return numbers[monk]
    targ1, targ2, op = operations[monk]
    num1 = get_root(targ1)
    num2 = get_root(targ2)
    return op(num1, num2)


with open("21/input", "r") as f:
    numbers = {}
    operations = {}
    for line in f.read().strip().split("\n"):
        monkey, thing = line.split(": ")
        if thing.isdigit():
            numbers[monkey] = int(thing)
        else:
            target1, op, target2 = thing.split(" ")
            operations[monkey] = (target1, target2, operate(target1, target2, op))

monkey_root = get_root("root")
print(f"The monkey named root finally yells {monkey_root}")
