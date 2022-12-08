import numpy as np

forest = np.genfromtxt("input", dtype=int, delimiter=1)

forest = np.pad(forest, ((1, 1), (1, 1)), "constant", constant_values=-1)
visible = np.zeros(forest.shape)

for i in range(1, forest.shape[0]):
    for j in range(1, forest.shape[1]):
        if all(forest[i, :j] < forest[i, j]):
            visible[i, j] = 1
        if forest[i, j] == 9:
            break

    for j in range(forest.shape[1]-2, 0, -1):
        if all(forest[i, j+1:] < forest[i, j]):
            visible[i, j] = 1
        if forest[i, j] == 9:
            break

for j in range(1, forest.shape[1]):
    for i in range(1, forest.shape[0]):
        if all(forest[:i, j] < forest[i, j]):
            visible[i, j] = 1
        if forest[i, j] == 9:
            break

    for i in range(forest.shape[0]-2, 0, -1):
        if all(forest[i+1:, j] < forest[i, j]):
            visible[i, j] = 1
        if forest[i, j] == 9:
            break

print(f"There are {int(np.sum(visible))} trees visible from the outside.")

forest = forest[1:-1, 1:-1]
scenic = np.zeros(forest.shape)
for i in range(1, forest.shape[0]-1):
    for j in range(1, forest.shape[1]-1):
        a = [0, 0, 0, 0]
        x = 1
        while True:
            if i + x > forest.shape[0] - 1:
                break
            a[0] += 1
            if forest[i, j] <= forest[i+x, j]:
                break
            x += 1
        x = 1
        while True:
            if j + x > forest.shape[1] - 1:
                break
            a[1] += 1
            if forest[i, j] <= forest[i, j+x]:
                break
            x += 1
        x = 1
        while True:
            if i - x < 0:
                break
            a[2] += 1
            if forest[i, j] <= forest[i-x, j]:
                break
            x += 1
        x = 1
        while True:
            if j - x < 0:
                break
            a[3] += 1
            if forest[i, j] <= forest[i, j-x]:
                break
            x += 1
        scenic[i, j] = np.prod(a)

print(f"The highest possible scenic value™ for any tree is "
      f"{int(np.max(scenic))} at "
      f"{np.unravel_index(scenic.argmax(), scenic.shape)}.")
