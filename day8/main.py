import re
from tqdm import tqdm
import numpy as np

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# ====== preparing input ======
with open('adventofcode/day8/inputtxt') as file:
    lines = file.readlines()

signals =[{"pattern": line[0].split(' '), "output":line[1].split(' ')} for line in [raw_line.replace('\n', '').split(' | ') for raw_line in lines]]

# -- sort inputs
signals_sorted = []
for signal in signals:
    pattern = []
    output = []
    for entry in signal['pattern']:
        pattern.append(''.join(sorted(entry)))
    for entry in signal['output']:
        output.append(''.join(sorted(entry)))
    signals_sorted.append({"pattern": pattern, "output": output})

# -- count 1, 4, 7, or 8 in the output
count = 0
for signal in signals_sorted:
    for entry in signal['output']:
        if len(entry) in [2,4,3,7]:
            count += 1
print(f'Count 1, 4, 7, or 8 is {count}')


def recognize_pattern(pattern):
    #     pattern = signals_sorted[0]['pattern']
    decoded_numbers = {str(i): '' for i in range(10)}
    # -- find 1,4,7,8
    pattern_new = []
    for entry in pattern:
        if len(entry) == 2:
            decoded_numbers['1'] = entry
        elif len(entry) == 3:
            decoded_numbers['7'] = entry
        elif len(entry) == 4:
            decoded_numbers['4'] = entry
        elif len(entry) == 7:
            decoded_numbers['8'] = entry
        else:
            pattern_new.append(entry)
    pattern = pattern_new

    diff_4_and_1 = ''.join([n for n in decoded_numbers['4'] if n not in decoded_numbers['1']])

    pattern_new = []
    for entry in pattern:
        if len(entry) == 6 and not all([symb in entry for symb in decoded_numbers['1']]):  # -- find 6
            decoded_numbers['6'] = entry
        elif len(entry) == 6 and all([symb in entry for symb in decoded_numbers['4']]):  # -- find 6
            decoded_numbers['9'] = entry
        elif len(entry) == 5 and all([symb in entry for symb in decoded_numbers['1']]):
            decoded_numbers['3'] = entry
        elif len(entry) == 5 and all([symb in entry for symb in diff_4_and_1]):
            decoded_numbers['5'] = entry
        elif len(entry) == 5 and not all([symb in entry for symb in diff_4_and_1]):
            decoded_numbers['2'] = entry
        else:
            decoded_numbers['0'] = entry
    pattdiff_4_and_1 = ''.join([n for n in decoded_numbers['4'] if n not in decoded_numbers['1']])

    pattern_new = []
    for entry in pattern:
        if len(entry) == 6 and not all([symb in entry for symb in decoded_numbers['1']]):  # -- find 6
            decoded_numbers['6'] = entry
        elif len(entry) == 6 and all([symb in entry for symb in decoded_numbers['4']]):  # -- find 6
            decoded_numbers['9'] = entry
        elif len(entry) == 5 and all([symb in entry for symb in decoded_numbers['1']]):
            decoded_numbers['3'] = entry
        elif len(entry) == 5 and all([symb in entry for symb in diff_4_and_1]):
            decoded_numbers['5'] = entry
        elif len(entry) == 5 and not all([symb in entry for symb in diff_4_and_1]):
            decoded_numbers['2'] = entry
        else:
            decoded_numbers['0'] = entry
    # pattern = pattern_newern = pattern_new
    return {decoded_numbers[k]: int(k) for k in decoded_numbers}


# -- decode
print('Signals')
final_numbers = []
for signal in signals_sorted:
    decode_key = recognize_pattern(signal['pattern'])
    numeric_output = ''
    for symbol in signal['output']:
        numeric_output += str(decode_key[symbol])
    final_numbers.append(int(numeric_output))

print(f"The final sum is {np.array(final_numbers).sum()}")



