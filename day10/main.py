import re
from tqdm import tqdm
import numpy as np


class Chunk:
    def __init__(self, open_sign=None, close_sign=None, parent_chunk=None):
        self.open_sign = open_sign
        self.close_sign = close_sign
        self.offsprings = []
        self.parent_chunk = parent_chunk
    # def add_offspring(self):
    #     self.offsprings.append(Chunk())
    #     return self.offsprings[-1]


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


MAPPING = DotDict({"pairs": ['()', '[]', '{}', '<>']})
MAPPING.open_symbols = [i[0] for i in MAPPING.pairs]
MAPPING.close_symbols = [i[1] for i in MAPPING.pairs]
MAPPING.get_match = {k: v for i in MAPPING.pairs for k, v in [(i[0], i[1]), (i[1], i[0])]}
MAPPING.get_task_1_price = {')': 3, ']': 57, '}': 1197, '>': 25137}
MAPPING.get_task_2_price = {')': 1, ']': 2, '}': 3, '>': 4}


def day10(is_test=False):
    # ====== preparing input ======
    file_name = 'testinput' if is_test else 'inputtxt'
    with open(file_name) as file:
        lines = file.readlines()
    lines = [[char for char in line.replace('\n', '')] for line in lines]

    task_1(lines, is_test)
    task_2(lines, is_test)


def task_1(lines, is_test):
    test_output = 26397
    chunks = []
    for line in lines:
        chunks.append(pars_line(line))
    syntax_scores = []
    for chunk in chunks:
        syntax_scores.append(get_syntax_score(chunk))
    syntax_sum = np.array(syntax_scores).sum()
    if is_test:
        is_passed = syntax_sum == test_output
        print(f'Task_1: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {syntax_sum} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_1: The result is {syntax_sum}')


def task_2(lines, is_test):
    test_output = 288957
    chunks = []
    for line in lines:
        chunks.append(pars_line(line))
    completion_scores = []
    for chunk in chunks:
        completion_score = get_completion_score(chunk)
        if completion_score is not None:
            completion_scores.append(completion_score)
    task_output = int(np.median(completion_scores))
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_2: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_2: The result is {task_output}')


def get_completion_score(chunk: Chunk):
    completion_score = 0
    completion_string = get_completion_string(chunk)
    if completion_string is None:
        return None
    else:
        for sign in completion_string:
            completion_score = completion_score * 5 + MAPPING.get_task_2_price[sign]
    return completion_score


def get_completion_string(chunk: Chunk, completion_str=''):
    if completion_str is None:
        return None
    if chunk.close_sign is not None:
        if MAPPING.get_match[chunk.open_sign] != chunk.close_sign:
            completion_str = None
            return completion_str
    elif chunk.open_sign is not None:
        completion_str = MAPPING.get_match[chunk.open_sign] + completion_str

    for offspring in chunk.offsprings[::-1]:
        completion_str = get_completion_string(chunk=offspring, completion_str=completion_str) #+ completion_str
    return completion_str


def get_syntax_score(chunk: Chunk, syntax_score=0):
    if syntax_score > 0:
        return 0
    if chunk.close_sign is not None:
        if MAPPING.get_match[chunk.open_sign] != chunk.close_sign:
            syntax_score += MAPPING.get_task_1_price[chunk.close_sign]
            return syntax_score
    for offspring in chunk.offsprings:
        syntax_score += get_syntax_score(chunk=offspring, syntax_score=syntax_score)
        if syntax_score > 0:
            return syntax_score
    return syntax_score


def pars_line(line):
    working_chunk = Chunk()
    parent = working_chunk
    for _ in line:
        if _ in MAPPING.open_symbols:
            offspring = Chunk(open_sign=_, parent_chunk=working_chunk)
            # if parent is None:
            #     parent = offspring
            # if working_chunk is not None:
            working_chunk.offsprings.append(offspring)
            working_chunk = offspring
        elif _ in MAPPING.close_symbols:
            working_chunk.close_sign = _
            working_chunk = working_chunk.parent_chunk
    return parent


if __name__ == '__main__':
    day10(is_test=True)
    day10()
