#!/usr/bin/python3

# AOC 2023 Day 3 solution, part I: ######
# Completed 6865 iterations in 59.96s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     35.10μs    34.78μs   1.95μs
# Execute  8.70ms     8.66ms    118.39μs
# Total    8.73ms     8.70ms    118.96μs

# AOC 2023 Day 3 solution, part II: ########
# Completed 10243 iterations in 59.93s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     35.36μs    35.21μs   1.46μs
# Execute  5.82ms     5.81ms    39.44μs
# Total    5.85ms     5.85ms    39.61μs

import typing
from typing import Generator
from re import Pattern as CompiledRegex
from re import finditer, Match
from re import compile as regex_compile
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(3)

NUMBER_REGEX = regex_compile('\d+')
GEAR_SYMBOL_REGEX = regex_compile(r'\*')

def is_adjacent(line_numb: int, match: Match, x_symb: int) -> bool:
	'''Given a symbol in line 1(one) and column x_symb,
	and number in line line_numb with position given by match;
		Return whether or not they are adjacent to each other.'''
	# If symbol and number are in the same line.
	if line_numb == 1:
		if (match.start() - 1 == x_symb) or (match.end() == x_symb):
			return True
	# If number is in the line above or the line below of the symbol.
	else:
		if (x_symb >= match.start()-1) and (x_symb <= match.end()):
			return True
	return False

def slide_window_and_match(input_: str, pattern: CompiledRegex, lines: int = 3) -> Generator[tuple, None, None]:
	'''Generator that feeds input_ string as a sliding window of 3(lines) lines,
	as well as providing regex matches in this window.'''

	window = []
	window_of_matches = []
	for i, line in enumerate(input_.split('\n')):
		# Skip empty lines.
		if line.strip() == '':
			continue

		# Remove 1 line at the beginning of the window if not one of the first lines.
		# Yield a window.
		if i >= lines:
			yield window, tuple( chain_matches_from_window(window_of_matches) )
			window = window[1:]
			window_of_matches = window_of_matches[1:]

		# Append 1 line to the window.
		window.append(line)
		window_of_matches.append(tuple( pattern.finditer(line) ))

	# Yield last window.
	yield window, tuple( chain_matches_from_window(window_of_matches) )

def chain_matches_from_window(window_of_matches: list) -> Generator[tuple, None, None]:
	'''Chain a "window" of match-generators into a single generator.'''
	for i, generator in enumerate(window_of_matches):
		# From a generator of matches, for each line...
		for value in generator:
			# ...yield value(a match), as well as the line number.
			yield i, value

@arparse_and_time_wrapper
def solve(input_: str, flags: dict) -> int:

	# Cheat around edge cases by adding a line of "......" at the beginning and end.
	input_ = '.' * input_.find('\n') + '\n' + \
			 input_ + \
			 '.' * input_.find('\n')

	running_sum = 0

	# Slide a window with a width of 3 lines over the input.
	# Find numbers in that window using regex.
	for last_three_lines, number_matches  in slide_window_and_match(input_, NUMBER_REGEX):
		top_line, middle_line, bottom_line = last_three_lines

		# Solve part II of the puzzle.
		if flags['fix']:
			# For each "*"(gear) symbol in middle line.
			for gear_symbol_match in GEAR_SYMBOL_REGEX.finditer(middle_line):
				# Find adjacent numbers.
				adjacent_matches = [int(match[1].group(0)) for match in number_matches if is_adjacent(*match, gear_symbol_match.start())]
				# If there are exactly two, add their product to the answer.
				if len(adjacent_matches) == 2:
					running_sum += adjacent_matches[0] * adjacent_matches[1]

		# Solve part I of the puzzle.
		else:
			# Find column-positions of all symbols in the middle line.
			symbol_positions = tuple( (i for i, char in enumerate(middle_line) if (char != '.') and not char.isdigit()) )

			# For each number in the 3-line window, check if they are adjacent to at least 1 symbol.
			for match in number_matches:
				for i in symbol_positions:
					# If that number IS adjacent to a symbol, add it to the sum.
					if is_adjacent(*match, i):
						running_sum += int(match[1].group(0))
						break
	return running_sum

if __name__ == '__main__':
	solve()
