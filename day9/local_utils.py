def get_list(list, row, column):
    if any([row<0, column<0]):
        return 9
    else:
        try:
            return list[row][column]
        except IndexError:
            return 9