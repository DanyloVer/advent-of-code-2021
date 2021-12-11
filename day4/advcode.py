import re
from tqdm import tqdm

# ====== preparing input ======
with open('inputtxt') as file:
    lines = file.readlines()

# -- getting game numbers
bingo_numbers = [int(num) for num in lines[0].replace('\n', '').split(',')]

# -- preparing empty ticket shells
n_of_tickets = len([el for el in lines[2:] if el == '\n'])+1
bingo_tickets_stats = [{"no": n, "numbers": [], "columns": [], "rows": []} for n in range(n_of_tickets)]

# -- getting rows
counter = 0
for el in lines[2:]:
    if el == '\n':
        counter += 1
        continue
    else:
        single_row = re.findall(r"\d+", el)

    bingo_tickets_stats[counter]["no"] = counter
    bingo_tickets_stats[counter]["rows"].append(single_row)

# -- getting columns
for idx, ticket_stats in enumerate(bingo_tickets_stats):
    for col_no in range(len(ticket_stats["rows"][0])):
        column = []
        for row in ticket_stats["rows"]:
            column.append(row[col_no])
        bingo_tickets_stats[idx]["columns"].append(column)

# -- getting numbers
for idx, ticket_stats in enumerate(bingo_tickets_stats):
    ticket_numbers = []
    for row in ticket_stats["rows"]:
        for el in row:
            ticket_numbers.append(el)

    bingo_tickets_stats[idx]["numbers"]=ticket_numbers

# -- the logic
passed_nums = []
winner = None
win_sum = None
for bingo_num in tqdm(bingo_numbers):
    passed_nums.append(bingo_num)
    if len(bingo_tickets_stats) == 0:
        print('No more tickets')
        break
    if len(passed_nums) < len(bingo_tickets_stats[0]["rows"][0]):
        continue
    for ticket_stats in bingo_tickets_stats:
        for row, column in zip(ticket_stats["rows"], ticket_stats["columns"]):
            if any([all(int(num) in passed_nums for num in row), all(int(num) in passed_nums for num in column)]):
                winner = ticket_stats["no"]
                win_sum = sum([int(num) for num in ticket_stats["numbers"] if int(num) not in passed_nums])*bingo_num
                print(winner)
                print(win_sum)
                bingo_tickets_stats = [
                    ticket_stats for ticket_stats in bingo_tickets_stats if ticket_stats["no"] != winner
                ]
    #             break
    #     if winner: break
    # if winner: break



