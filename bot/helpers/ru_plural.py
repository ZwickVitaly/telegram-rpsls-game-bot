def times_plural(times: int):
    twelve_fourteen = [12, 13, 14]
    two_four = [2, 4]
    if times % 10 in two_four and times % 100 not in twelve_fourteen:
        return "раза"
    return "раз"