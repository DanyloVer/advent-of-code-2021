import re
import numpy as np

# ====== preparing input ======
with open('adventofcode/day5/inputtxt') as file:
    lines = file.readlines()

# -- get vectors
vectors = [[[int(num) for num in re.findall(r"\d+", dot)] for dot in vector.split('->')] for vector in lines]

# -- filter out non horizontal and non vertical
vectors = [
    np.array(vector) for vector in vectors if any([
        vector[0][0] == vector[1][0],  # vertical
        vector[0][1] == vector[1][1],  # horizontal
        abs(vector[0][0] - vector[1][0]) == abs(vector[0][1] - vector[1][1])  # diagonal
    ])
]

# -- create empty map
board_size = np.array([vector_m.max() for vector_m in vectors]).max()
print(f'Map size is {board_size}x{board_size}')
final_map = []
for i in range(board_size+1):
    final_map.append([0 for j in range(board_size+1)])

# -- iterate numbers by vector inputs
for vector in vectors:
    print(vector)
    # -- if x equals then vertical
    if vector[0][0] == vector[1][0]:
        print('Doing column')
        x = vector[0][0]
        min_y = min(vector[0][1], vector[1][1])
        max_y = max(vector[0][1], vector[1][1])
        for y in range(min_y, max_y+1):
            final_map[y][x] += 1
            # print(f"({x},{y})")
    # -- if y equals then horizontal
    if vector[0][1] == vector[1][1]:
        print('Doing row')
        y = vector[1][1]
        min_x = min(vector[0][0], vector[1][0])
        max_x = max(vector[0][0], vector[1][0])
        for x in range(min_x, max_x + 1):
            final_map[y][x] += 1
            # print(f"({x},{y})")
    # -- diagonal
    if abs(vector[0][0] - vector[1][0]) == abs(vector[0][1] - vector[1][1]):
        print('Doing diagonal')
        x1, x2, y1, y2 = (vector[0][0], vector[1][0], vector[0][1], vector[1][1])
        x_sign, y_sign = (1 if x2 > x1 else -1, 1 if y2 > y1 else -1)
        for x, y in zip(range(x1, x2+x_sign, x_sign), range(y1, y2+y_sign, y_sign)):
            final_map[y][x] += 1

# -- count danger zones
count_danger = 0
for row in final_map:
    count_danger += len([num for num in row if num>1])

print(f'The number of danger zones is: {count_danger}')