#!/usr/bin/python3

# AOC 2023 Day 2 solution, part I: ####
# Completed 34824 iterations in 59.75s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     31.73μs    31.02μs   85.74μs
# Execute  1.68ms     1.68ms    20.48μs
# Total    1.72ms     1.71ms    89.60μs

# AOC 2023 Day 2 solution, part II: #####
# Completed 29350 iterations in 59.77s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     33.26μs    31.81μs   9.16μs
# Execute  2.00ms     1.97ms    61.58μs
# Total    2.04ms     2.00ms    64.77μs


import typing
from re import compile as regex_compile
from re import finditer
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(2)

# Contents of the bag to check possibility against in the Part I.
BAG_CONTENTS = {
	'red': 12,
	'green': 13,
	'blue': 14
}

# Python list containing names of colors, e.g. ['red', 'green', 'blue'].
LIST_OF_COLORS = list(BAG_CONTENTS.keys()) 

# Regex pattern to match individual color-count entries from the input.
ENTRY_PATTERN = regex_compile(f'(\d+) (red|green|blue)')


def parse_input_str_to_array(input_: str) -> list:
	array = []
	for game in input_.split('\n'):
		# Skip lines that contain only whitespace.
		if game.strip() == '':
			continue

		# For each parsed "game", append a line to the array.
		array.append([])

		# Discard "Game N:" part of the string by finding ":".
		game_results = game[game.find(':') + 1:]

		for round_ in game_results.split(';'):
			# Initiate to all 0s.
			pulled_out_this_round = {color: 0 for color in LIST_OF_COLORS}
			for entry in ENTRY_PATTERN.finditer(round_):
				# Set pulled_out_this_round[parsed color name] = parsed count.
				pulled_out_this_round[entry.group(2)] = int(entry.group(1))
			# Append parsed round results in the last row of the array.
			array[-1].append(pulled_out_this_round)

	return array


def is_game_possible_if_bag_contains(game: list, bag_contents: dict) -> bool:
	for round_results in game:
		for color in LIST_OF_COLORS:
			if round_results[color] > bag_contents[color]:
				return False
	return True


def calculate_min_contents_of_bag(game: list) -> dict:
	# Initiate to all 0s.
	min_bag_contents = {color: 0 for color in LIST_OF_COLORS}
	# Iterate over each color.
	for color in LIST_OF_COLORS:
		# For each color, set round_results[color] to max value of all rounds.
		for round_results in game:
			min_bag_contents[color] = max(min_bag_contents[color], round_results[color])
	# Return minimal bag contents for the game to be possible.
	return min_bag_contents


def calclate_power_of_a_set_of_cubes(bag_contents: dict) -> int:
	# Init to 1(one) since this is a product.
	power = 1
	# Calculate product of all color-counts.
	for color in LIST_OF_COLORS:
		power *= bag_contents.get(color, 0)
	return power

@arparse_and_time_wrapper
def solve(input_: str, flags: dict) -> int:
	answer = 0
	array = parse_input_str_to_array(input_)
	for id_, game in enumerate(array, 1):
		if flags['fix']:
			min_contents = calculate_min_contents_of_bag(game)
			power = calclate_power_of_a_set_of_cubes(min_contents)
			answer += power
		elif is_game_possible_if_bag_contains(game, BAG_CONTENTS):
			answer += id_
	return answer


if __name__ == '__main__':
	solve()
