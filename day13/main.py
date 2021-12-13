import numpy as np
from copy import copy
import datetime
from pprint import pprint


class Paper:
    def __init__(self, lines):
        self.dotes = [[int(i) for i in line.replace('\n', '').split(',')] for line in lines if ',' in line]
        self.instructions = [line.replace('\n', '').replace('fold along ', '').split('=') for line in lines if '=' in line]
        self.max_x = np.array([x for x, y in self.dotes]).max()
        self.max_y = np.array([y for x, y in self.dotes]).max()
        self.matrix = [[0 for x in range(self.max_x+1)] for y in range(self.max_y+1)]

        for x, y in self.dotes:
            self.matrix[y][x] = 1

    def print_matrix(self):
        print('\n')
        for row in self.matrix:
            print(''.join(['.' if _ == 0 else '#' for _ in row]))
        print('\n')

    def fold_matrix(self, instruction):
        axis, no = instruction
        no = int(no)
        new_matrix = []
        if axis == 'y':
            up_part = self.matrix[:no]
            bottom_part = self.matrix[no+1:]
            bottom_part = bottom_part[::-1]
            if len(up_part) > len(bottom_part):
                for i in range(len(up_part)-len(bottom_part)):
                    row = [0 for j in up_part[0]]
                    bottom_part.insert(0, row)

            for idy, y in enumerate(up_part):
                row = []
                for idx, x in enumerate(y):
                    row.append(1 if x == 1 or bottom_part[idy][idx] == 1 else 0)
                new_matrix.append(row)
        else:
            new_matrix = []
            left_part = [row[:no] for row in self.matrix]
            right_part = [row[no+1:] for row in self.matrix]
            right_part = [row[::-1] for row in right_part]
            for idy, y in enumerate(left_part):
                row = []
                for idx, x in enumerate(y):
                    row.append(1 if x == 1 or right_part[idy][idx] == 1 else 0)
                new_matrix.append(row)

        self.matrix = new_matrix


def day13(is_test: bool = False):
    # ====== preparing input ======
    file_name = 'testinput' if is_test else 'inputtxt'
    with open(file_name) as file:
        lines = file.readlines()

    paper = Paper(lines=lines)
    task_1(paper, is_test)
    paper = Paper(lines=lines)
    task_2(paper, is_test)


def task_1(paper: Paper, is_test):
    test_output = 17
    for instruction in paper.instructions:
        paper.fold_matrix(instruction)
        break

    task_output = np.array(paper.matrix).sum()
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_1: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_1: The result is {task_output}')


def task_2(paper, is_test):
    test_output = 16
    for instruction in paper.instructions:
        print(instruction)
        paper.fold_matrix(instruction)
    paper.print_matrix()

    task_output = np.array(paper.matrix).sum()
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_1: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_1: The result is {task_output}')


if __name__ == '__main__':
    day13(is_test=True)
    day13()