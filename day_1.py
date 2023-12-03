#!/usr/bin/python3

# AOC 2023 Day 1 solution, part I: #####
# Completed 43725 iterations in 59.69s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     34.15μs    32.44μs   123.98μs
# Execute  1.33ms     1.31ms    173.07μs
# Total    1.37ms     1.34ms    217.36μs

# AOC 2023 Day 1 solution, part II: #####
# Completed 13593 iterations in 59.89s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     38.42μs    35.77μs   15.00μs
# Execute  4.37ms     4.32ms    109.47μs
# Total    4.41ms     4.35ms    114.33μs


from re import compile as regex_compile
from re import finditer
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(1)

TOKEN_TO_VALUE_TABLE = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

TOKENS_LIST = list(TOKEN_TO_VALUE_TABLE.keys())
TOKENS_PATTERN = regex_compile(f'(?=({"|".join(TOKENS_LIST)}))')

@arparse_and_time_wrapper
def solve(input_: str, flags: dict) -> int:
    running_sum = 0
    for line in input_.split('\n'):
        if line.strip() == '':
            continue
        if flags['fix']:
            tokens = [match.group(1) for match in TOKENS_PATTERN.finditer(line)]
            first_digit = TOKEN_TO_VALUE_TABLE[tokens[0]]
            last_digit = TOKEN_TO_VALUE_TABLE[tokens[-1]]
        else:
            for char in line:
                if char.isdigit():
                    first_digit = int(char)
                    break
            for char in line[::-1]:
                if char.isdigit():
                    last_digit = int(char)
                    break
        running_sum += 10*first_digit + last_digit
    return running_sum

if __name__ == '__main__':
    solve()
