class WordLetterPair:
    def __init__(self, symbol_pair):
        self.symbol = symbol_pair


class Word:
    def __init__(self, initial_sequence: str, transformation_rules: dict):
        self.transformation_rules = transformation_rules
        self.letter_pairs = {}
        for a, b in zip(initial_sequence[:-1], initial_sequence[1:]):
            letter_pair = a+b
            if letter_pair in self.letter_pairs:
                self.letter_pairs[letter_pair] += 1
            else:
                self.letter_pairs[letter_pair] = 1

        self.letters = {}
        for _ in initial_sequence:
            if _ in self.letters:
                self.letters[_] += 1
            else:
                self.letters[_] = 1

    def perform_transformation(self):
        new_letter_pairs = {}
        for lp, freq in self.letter_pairs.items():
            in_letter = self.transformation_rules.get(lp)
            if in_letter:
                if in_letter in self.letters:
                    self.letters[in_letter] += freq
                else:
                    self.letters[in_letter] = freq

                pair_a = lp[0]+in_letter
                if pair_a in new_letter_pairs:
                    new_letter_pairs[pair_a] += freq
                else:
                    new_letter_pairs[pair_a] = freq

                pair_b = in_letter + lp[1]
                if pair_b in new_letter_pairs:
                    new_letter_pairs[pair_b] += freq
                else:
                    new_letter_pairs[pair_b] = freq
            else:
                if lp in new_letter_pairs:
                    new_letter_pairs[lp] += freq
                else:
                    new_letter_pairs[lp] = freq
        self.letter_pairs = new_letter_pairs

    def do_transformation_series(self, n):
        for i in range(n):
            self.perform_transformation()
            # print(i, self.get_statistics())

    def get_statistics(self):
        return self.letters


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
        print(f'Task_2: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_2: The result is {task_output}')


def main():
    day_runner(is_test=True)
    day_runner()


if __name__ == '__main__':
    main()