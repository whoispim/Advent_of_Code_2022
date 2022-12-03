# A: Rock
# B: Paper
# C: Scissors

# X: Rock
# Y: Paper
# z: Scissors

# Play as Rock:     1
# Play as Paper:    2
# Play as Scissors: 3

# Loss: 0
# Draw: 3
# Win:  6

def game_score(you: str, me: str) -> int:
    return score_dict[me] + result_dict[you][me]


score_dict = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

result_dict = {
    "A": {
        "X": 3,
        "Y": 6,
        "Z": 0
    },
    "B": {
        "X": 0,
        "Y": 3,
        "Z": 6
    },
    "C": {
        "X": 6,
        "Y": 0,
        "Z": 3
    }
}

total_score = 0
with open("input", "r") as f:
    for line in f.readlines():
        total_score += game_score(line[0], line[2])

print(f"Total score for 02a: {total_score}")
