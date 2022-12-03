# A: Rock
# B: Paper
# C: Scissors

# X: Lose
# Y: Draw
# z: Win

# Play as Rock:     1
# Play as Paper:    2
# Play as Scissors: 3

# Loss: 0
# Draw: 3
# Win:  6

def game_score(you: str, goal: str) -> int:
    return result_dict[goal] + score_dict[goal_dict[you][goal]]


score_dict = {
    "A": 1,
    "B": 2,
    "C": 3
}

result_dict = {
    "X": 0,
    "Y": 3,
    "Z": 6
}

goal_dict = {
    "A": {
        "X": "C",
        "Y": "A",
        "Z": "B"
    },
    "B": {
        "X": "A",
        "Y": "B",
        "Z": "C"
    },
    "C": {
        "X": "B",
        "Y": "C",
        "Z": "A"
    }
}

total_score = 0
with open("input", "r") as f:
    for line in f.readlines():
        total_score += game_score(line[0], line[2])

print(f"Total score for 02b: {total_score}")
