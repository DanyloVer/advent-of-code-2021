import re
import numpy as np
from tqdm import tqdm


# ====== preparing input ======
with open('adventofcode/day7/inputtxt') as file:
    lines = file.readlines()

# -- getting initial positions
initial_data = np.array([int(num) for num in lines[0].split(',')])
# initial_data.sort()

possible_positions = range(initial_data.min(),initial_data.max()+1,1)

fuel_costs = []
for position in tqdm(possible_positions):
    fuel_costs.append([position, np.array([(1+abs(crab_position-position))/2*abs(crab_position-position) for crab_position in initial_data]).sum()])

minimum_fuel_costs = np.array([point_stat[1] for point_stat in fuel_costs]).min()
optimal_points = [point_stat[0] for point_stat in fuel_costs if point_stat[1] == minimum_fuel_costs]

print(f"Minimum fuel costs {minimum_fuel_costs} in positions {optimal_points}")


