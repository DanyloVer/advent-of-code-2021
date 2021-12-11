import re
from tqdm import tqdm
import numpy as np
from local_utils import get_list

def get_basin(input, row_id, col_id, basin=None, real_new_points=None):
    if basin is None:
        basin = []
        current_value = get_list(input, row_id, col_id)
        central_point = {'val': current_value, 'row': row_id, 'col': col_id}
        basin.append(central_point)

    if real_new_points is None:
        real_new_points = basin

    new_points = []
    for point in real_new_points:
        for side in ['left', 'above', 'right', 'behind']:
            new_points.extend(gotodircetion(input, side, point, basin))

    real_new_points = [point for point in new_points if point not in basin]
    if len(real_new_points) == 0:
        basin.extend(real_new_points)
        return basin
    else:
        return get_basin(input, row_id, col_id, basin=basin, real_new_points=real_new_points)


def gotodircetion(input, side, point, output=None):
    if output is None:
        output = []
    if side == 'left':
        col_delta = -1
        row_delta = 0
    elif side == 'above':
        col_delta = 0
        row_delta = 1
    elif side == 'right':
        col_delta = 1
        row_delta = 0
    elif side == 'behind':
        col_delta = 0
        row_delta = -1

    next_val = get_list(input, point['row'] + row_delta, point['col'] + col_delta)
    new_basin_point = {'val': next_val, 'row': point['row'] + row_delta, 'col': point['col'] + col_delta}
    if 9 > next_val > point['val'] and new_basin_point not in output:
        output.append(new_basin_point)
        return gotodircetion(input, side, new_basin_point, output)
    else:
        return output


def task_2(input):
    basins = []
    for row_id, row in enumerate(input):
        for col_id, val in enumerate(row):
            left = get_list(input, row_id, col_id-1)  # left
            right = get_list(input, row_id, col_id+1)  # right
            above = get_list(input, row_id+1, col_id)  # above
            behind = get_list(input, row_id-1, col_id)  # behind
            neighbors = [left, right, above, behind]
            # print(val,neighbors, row_id, col_id)
            if val < np.array(neighbors).min():
                basin = get_basin(input, row_id, col_id)
                # basin.append({'val': val, 'row': row_id, 'col': col_id})
                basins.append(basin)
                # print(basin)
    basins_stats = []
    for idx, basin in enumerate(basins):
        basins_stats.append({"basin_idx": idx, "size": len(basin)})

    basins_stats.sort(key=lambda x: x["size"], reverse=True)
    top_3_basins = basins_stats[:3]
    print(top_3_basins)
    print(f"Total risk level is {np.array([x['size'] for x in top_3_basins]).prod()}")



def task_1(input):
    risk_levels = []
    for row_id, row in enumerate(input):
        for col_id, val in enumerate(row):
            neighbors = []
            neighbors.append(get_list(input, row_id, col_id - 1))  # left
            neighbors.append(get_list(input, row_id, col_id + 1))  # right
            neighbors.append(get_list(input, row_id + 1, col_id))  # above
            neighbors.append(get_list(input, row_id - 1, col_id))  # behind
            # print(val, neighbors, row_id, col_id)
            if val < np.array(neighbors).min():
                risk_levels.append(val + 1)

    print(f"Total risk level is {np.array(risk_levels).sum()}")


def main(is_test=False):
    # ====== preparing input ======
    with open('testinput' if is_test else 'inputtxt') as file:  # adventofcode/day9/inputtxt
        lines = file.readlines()

    input = [[int(num) for num in line.replace('\n', '')] for line in lines]

    task_1(input)
    task_2(input)


if __name__ == '__main__':
    main(is_test=False)