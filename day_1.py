#!/usr/bin/python3
from re import compile as regex_compile
from re import finditer
import argparse

DEFAULT_PATH = '/home/debian/Code/aoc_2023/inputs/day_1.txt'

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

def parse_cli_arguments():
    argument_parser = argparse.ArgumentParser(description='Solve Advent of Code 2023 day 1 puzzle.')
    argument_parser.add_argument('input_files', type=argparse.FileType('r'), default=[open(DEFAULT_PATH, 'r'),], nargs='*')
    argument_parser.add_argument('-s', '--sum', action='store_true',
            help='If this flag is set and multiple files are passed as inputs, sum across files.')
    argument_parser.add_argument('-f', '--fix', action='store_true',
            help='If this flag is set, apply a "fix" to solve second part of the puzzle.')

    return argument_parser.parse_args()

def solution_first(path=DEFAULT_PATH):
    with open(path, 'r') as file_:
        running_sum = 0
        for line in file_:
            for char in line:
                if char.isdigit():
                    first_digit = char
                    break
            for char in line[::-1]:
                if char.isdigit():
                    last_digit = char
                    break
            running_sum += int(first_digit +
                               last_digit)
    return running_sum

def solution_fixed(path=DEFAULT_PATH):
    with open(path, 'r') as file_:
        running_sum = 0
        for line in file_:
            tokens = [match.group(1) for match in TOKENS_PATTERN.finditer(line)]
            first_digit = TOKEN_TO_VALUE_TABLE[tokens[0]]
            last_digit = TOKEN_TO_VALUE_TABLE[tokens[-1]]
            running_sum += 10*first_digit + last_digit
    return running_sum

if __name__ == '__main__':
    args = parse_cli_arguments()
    relevant_solver = solution_fixed if args.fix else solution_first
    if args.sum:
        print(sum((relevant_solver(f.name) for f in args.input_files)))
    else:
        for f in args.input_files:
            path = f.name
            print(relevant_solver(path))
