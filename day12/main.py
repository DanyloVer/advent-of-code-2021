import numpy as np
from copy import copy
import datetime


class Cave:
    def __init__(self, name: str = None):
        self.name = name
        self.is_big = name == name.upper()
        self.connections = []


class CaveSystem:
    def __init__(self, init_data: list = None):
        self.caves_by_name = {}
        self.caves = []
        self.paths = None
        self.paths_str = None
        for cave1, cave2 in init_data:
            for cave in [cave1, cave2]:
                if cave not in self.caves_by_name:
                    self.caves_by_name[cave] = Cave(name=cave)
            for cave_from, cave_to in [(cave1, cave2), (cave2, cave1)]:
                self.caves_by_name[cave_from].connections.append(self.caves_by_name[cave_to])
        for cave_name in self.caves_by_name.keys():
            self.caves.append(self.caves_by_name[cave_name])

    @staticmethod
    def stringify_paths(paths):
        return ['->'.join([cave.name for cave in path['caves']]) for path in paths]

    def set_paths(self, paths: list = None, small_caves_limit=1, final_output=None):
        if final_output is None:
            final_output = []
        if paths is None:
            start_point = self.caves_by_name['start']
            paths = []
            for connection in start_point.connections:
                paths.append({'caves': [start_point, connection], "small_caves_limit": small_caves_limit})
        new_paths = []
        for path in paths:

            if path['caves'][-1].name == 'end':
                new_path = {'caves': copy(path['caves']), "small_caves_limit": copy(path["small_caves_limit"])}
                final_output.append(new_path)
            else:
                for connection in path['caves'][-1].connections:
                    new_path = {'caves': copy(path['caves']), "small_caves_limit": copy(path["small_caves_limit"])}
                    if connection.name == 'start':
                        continue

                    cnt_cave = 0 if connection.is_big else len([cave.name for cave in path['caves'] if cave.name == connection.name])

                    if cnt_cave >= new_path["small_caves_limit"]:
                        continue
                    if cnt_cave == 1:
                        new_path["small_caves_limit"] = 1
                    new_path['caves'].append(connection)
                    if new_path not in new_paths and new_path not in final_output:
                        if connection.name == 'end':
                            final_output.append(new_path)
                        else:
                            new_paths.append(new_path)
        print(datetime.datetime.now(), len(final_output), len(new_paths))
        if len([path for path in new_paths if path not in paths]) == 0:
            self.paths = final_output
            self.paths_str = self.stringify_paths(final_output)
            return self.paths_str
        else:
            return self.set_paths(paths=new_paths, final_output=final_output)


def day12(is_test: bool = False):
    # ====== preparing input ======
    file_name = 'testinput' if is_test else 'inputtxt'
    with open(file_name) as file:
        lines = file.readlines()
    lines = [line.replace('\n', '').split('-') for line in lines]

    cave_system = CaveSystem(init_data=lines)
    cave_system.set_paths()
    task_1(cave_system, is_test)
    cave_system.set_paths(small_caves_limit=2)
    task_2(cave_system, is_test)


def task_1(cave_system, is_test):
    test_output = 10
    task_output = len([path for path in cave_system.paths if path['caves'][-1].name == 'end'])
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_1: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_1: The result is {task_output}')


def task_2(cave_system, is_test):
    test_output = 36
    task_output = len([path for path in cave_system.paths if path['caves'][-1].name == 'end'])
    if is_test:
        is_passed = task_output == test_output
        print(f'Task_2: {"GC! ^_^:" if is_passed else "Sorry :(" } the result {task_output} {"=" if is_passed else "!="} {test_output} (expected)')
    else:
        print(f'Task_2: The result is {task_output}')


if __name__ == '__main__':
    day12(is_test=True)
    day12()