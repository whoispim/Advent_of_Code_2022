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


packets = [[[2]], [[6]]]
with open("input", "r") as f:
    for pack in f.read().strip().replace("\n\n", "\n").split("\n"):
        if re.match("^[0-9,\[\]]*$", pack):
            packets.append(eval(pack))

all_sorted = False
while not all_sorted:
    all_sorted = True
    for i in range(len(packets)-1):
        if not compare_pairs(packets[i], packets[i+1]):
            all_sorted = False
            pack = packets[i]
            packets[i] = packets[i+1]
            packets[i+1] = pack
# for pack in packets:
#     print(pack)

print(f"Pairs have been sorted. Decoder key is "
      f"{(packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)}")
