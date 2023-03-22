def snafu2dec(snafu_num):
    dec = 0
    for i, snaf in enumerate(reversed(snafu_num)):
        dec += snaf * 5**i
    return dec


def dec2snafu(dec_num):
    snaf_dict = {2: "=", 1: "-", 0: "0", -1: "1", -2: "2"}
    snaf_str = ""
    # find biggest possible power of 5
    power = 0
    while True:
        if abs(dec_num * 2) < 5**power:
            break
        power += 1

    for p in reversed(range(power)):
        neo_num = dec_num
        neo_snaf = 0
        for i in (2, 1, -1, -2):
            if abs(dec_num + (5**p * i)) < abs(neo_num):
                neo_num = dec_num + (5**p * i)
                neo_snaf = i
        dec_num = neo_num
        snaf_str += snaf_dict[neo_snaf]
    return snaf_str


with open("25/input", "r") as f:
    snafu_nums = f.read().strip().split("\n")

for i, num in enumerate(snafu_nums):
    new_num = []
    for digit in num:
        if digit.isnumeric():
            new_num.append(int(digit))
        elif digit == "-":
            new_num.append(-1)
        elif digit == "=":
            new_num.append(-2)
    snafu_nums[i] = new_num

dec_nums = [snafu2dec(snafu) for snafu in snafu_nums]
dec_sum = sum(dec_nums)
print(f"Decimal sum of all that snafu is          {dec_sum}")

print(f"Turning that back into snafu makes it     {dec2snafu(dec_sum)}")
