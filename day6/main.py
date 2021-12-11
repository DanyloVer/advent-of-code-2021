import re
import numpy as np
from tqdm import tqdm


# -- defining fish class
class LanternFish:
    def __init__(self, count_down_age, count_members):
        self.count_down_age = count_down_age
        self.count_members = count_members

    def add_a_member(self):
        self.count_members += 1

    def live_a_day(self):
        give_a_birth = False
        if self.count_down_age == 0:
            give_a_birth = True
            self.count_down_age = 6
        else:
            self.count_down_age -= 1
        return give_a_birth


# def main():
# ====== preparing input ======
with open('adventofcode/day6/inputtxt') as file:
    lines = file.readlines()

# -- getting initial population
initial_data = [int(num) for num in lines[0].split(',')]
population = []
for age in set(initial_data):
    count_members = len([el for el in initial_data if el==age])
    population.append(LanternFish(count_down_age=age, count_members=count_members))

print(f'Initial population statistics:')
for generation in population:
    print(f'Age: {generation.count_down_age} members {generation.count_members}')

# -- going over days
for day in tqdm(range(1, 300+1)):
    new_borne = []
    for generation in population:
        give_a_birth = generation.live_a_day()
        if give_a_birth:
            new_borne.append(LanternFish(count_down_age=8, count_members=generation.count_members))
    population.extend(new_borne)

    # add up same populations
    existing_ages = set([generation.count_down_age for generation in population])

    agg_population = []
    for age in existing_ages:
        count_members = np.array([generation.count_members for generation in population if generation.count_down_age == age]).sum()
        agg_population.append(LanternFish(count_down_age=age, count_members=count_members))
    population = agg_population

    # print statistics
    print(f'Final {len(population)} populations statistics for day {day}:')
    for generation in population:
        print(f'Age: {generation.count_down_age} members {generation.count_members}')

population_members = 0
for generation in population:
    population_members += generation.count_members
print(f"Total members: {population_members}")
# if __name__ == '__main__':
#     main()