import re


def compare_pairs(p1, p2):
    if not (type(p1) == list and type(p2) == list):
        raise Exception("Please use two lists as arguments")
    for el1, el2 in zip(p1, p2):
        if type(el1) == int and type(el2) == int:
            # print(f"{el1} and {el2} are ints")
            if el1 < el2:
                return True
            elif el1 > el2:
                return False
        if type(el1) == list and type(el2) == int:
            # print(f"{el1} is list, {el2} is int")
            result = compare_pairs(el1, [el2])
            if result is not None:
                return result
        if type(el1) == int and type(el2) == list:
            # print(f"{el1} is int, {el2} is list")
            result = compare_pairs([el1], el2)
            if result is not None:
                return result
        if type(el1) == list and type(el2) == list:
            # print(f"{el1} and {el2} both are lists")
            result = compare_pairs(el1, el2)
            if result is not None:
                return result
    # if one pair is used up, return
    if len(p1) < len(p2):
        # print("List 1 is exhausted")
        return True
    elif len(p1) > len(p2):
        # print("List 2 is exhausted")
        return False


pairs = []
with open("input", "r") as f:
    for pair in f.read().strip().split("\n\n"):
        if re.match("^[0-9,\[\]\n]*$", pair):
            pairs.append(list(map(eval, pair.split("\n"))))

right_indices = []
for i, pair in enumerate(pairs):
    if compare_pairs(*pair):
        right_indices.append(i+1)

print(f"Pairs that are in the right order: {right_indices}")
print(f"Sum of indices: {sum(right_indices)}")
