import numpy as np
from copy import copy
import datetime
from pprint import pprint


class WordLetter:
    def __init__(self, symbol):
        self.symbol = symbol
        self.next_letter: WordLetter = None


class Word:
    def __init__(self, initial_sequence: str, transformation_rules: dict):
        self.letters = WordLetter(initial_sequence[0])
        self.transformation_rules = transformation_rules
        working_letter = self.letters
        for _ in initial_sequence[1:]:
            working_letter.next_letter = WordLetter(_)
            working_letter = working_letter.next_letter
        self.initial_letters = copy(self.letters)

    def perform_transformation(self):
        working_letter = self.letters
        while working_letter.next_letter:
            letter_pair = working_letter.symbol + working_letter.next_letter.symbol
            in_letter = self.transformation_rules.get(letter_pair)
            if in_letter:
                insertion = WordLetter(in_letter)
                insertion.next_letter = working_letter.next_letter
                working_letter.next_letter = insertion
                working_letter = insertion.next_letter
            else:
                working_letter = working_letter.next_letter

    def do_transformation_series(self, n):
        for i in range(n):
            self.perform_transformation()
            print(i, self.get_statistics())

    def get_statistics(self):
        statistics_dict = {}
        working_letter = self.letters
        while True:
            if working_letter.symbol in statistics_dict:
                statistics_dict[working_letter.symbol] += 1
            else:
                statistics_dict[working_letter.symbol] = 1
            working_letter = working_letter.next_letter
            if working_letter is None:
                break
        return statistics_dict


def day_runner(is_test: bool = False):
    # ====== preparing input ======
    file_name = 'testinput' if is_test else 'inputtxt'
    with open(file_name) as file:
        lines = file.read().splitlines()

    initial_sequence = lines[0]
    transformation_rules = dict(k_v.split(" -> ") for k_v in lines[2:] if k_v)

    task_1(initial_sequence, transformation_rules, is_test)
    task_2(initial_sequence, transformation_rules, is_test)


def task_1(initial_sequence, transformation_rules, is_test):
    test_output = 1588
    word = Word(initial_sequence=initial_sequence, transformation_rules=transformation_rules)
    word.do_transformation_series(10)
    statistics = word.get_statistics()
    min_val = min(statistics.values())
    max_val = max(statistics.values())

    task_output = max_val - min_val
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_1: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_1: The result is {task_output}')


def task_2(initial_sequence, transformation_rules, is_test):
    test_output = 2188189693529
    word = Word(initial_sequence=initial_sequence, transformation_rules=transformation_rules)
    word.do_transformation_series(40)
    statistics = word.get_statistics()
    min_val = min(statistics.values())
    max_val = max(statistics.values())

    task_output = max_val - min_val
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_1: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_1: The result is {task_output}')


def main():
    day_runner(is_test=True)
    day_runner()


if __name__ == '__main__':
    main()