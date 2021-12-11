import numpy as np


class Octopus:
    def __init__(self, energy_level=None, population=None):
        self.energy_level = energy_level
        self.neighbours = []
        self.is_flashed = False
        self.population = population

    def increase_energy_level(self):
        if not self.is_flashed:
            self.energy_level += 1
            if self.energy_level > 9:
                self.is_flashed = True
                self.population.flashes += 1
                self.energy_level = 0
                for neighbour in self.neighbours:
                    neighbour.increase_energy_level()


class Population:
    def __init__(self, init_data):
        self.ordered = []
        self.all = []
        self.flashes = 0
        self.min = None
        self.max = None
        for line in init_data:
            row = []
            for energy_level in line:
                row.append(Octopus(energy_level=energy_level, population=self))
            self.ordered.append(row)

        cnt_rows = len(self.ordered)
        for i, row in enumerate(self.ordered):
            cnt_cols = len(row)
            for j, octopus in enumerate(row):
                neighbours_indexes = [
                    (r, c) for r in range(i-1, i+1+1) for c in range(j-1, j+1+1)
                    if all([r >= 0, c >= 0, r < cnt_rows, c < cnt_cols, r != i or c != j])
                ]
                for coordinates in neighbours_indexes:
                    r, c = coordinates
                    octopus.neighbours.append(self.ordered[r][c])
                self.all.append(octopus)

    def live_a_day(self):
        for octopus in self.all:
            octopus.is_flashed = False
        for octopus in self.all:
            octopus.increase_energy_level()
        self.set_statistics()

    def set_statistics(self):
        self.min = np.array([octopus.energy_level for octopus in self.all]).min()
        self.max = np.array([octopus.energy_level for octopus in self.all]).max()


def day11(is_test=False):
    # ====== preparing input ======
    file_name = 'testinput' if is_test else 'inputtxt'
    with open(file_name) as file:
        lines = file.readlines()
    lines = [[int(_) for _ in line.replace('\n', '')] for line in lines]

    population = Population(init_data=lines)
    task_1(population, is_test)
    population = Population(init_data=lines)
    task_2(population, is_test)


def task_1(population, is_test):
    test_output = 1656
    for day in range(100):
        population.live_a_day()
    task_output = population.flashes
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_2: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_2: The result is {task_output}')


def task_2(population, is_test):
    test_output = 195
    step = 0
    while True:
        step += 1
        population.live_a_day()
        if population.min == population.max == 0:
            break
    task_output = step
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_2: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_2: The result is {task_output}')

if __name__ == '__main__':
    day11(is_test=True)
    day11()