#!/usr/bin/python3

# AOC 2023 Day 4 solution, part I: #####
# Completed 16159 iterations in 59.89s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     36.32μs    35.79μs   2.27μs
# Execute  3.67ms     3.63ms    263.22μs
# Total    3.71ms     3.67ms    263.48μs

# AOC 2023 Day 4 solution, part II: #######
# Completed 15326 iterations in 59.89s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     38.09μs    36.39μs   12.02μs
# Execute  3.87ms     3.84ms    89.20μs
# Total    3.91ms     3.88ms    93.73μs

from re import finditer
from re import compile as regex_compile
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(4)

NUMBER_PATTERN = regex_compile('\d+')


def split_into_lines(input_: str) -> list:
	'''Splits input into array of lines, while discarding empty(white-space only) lines.'''
	lines = []
	for line in input_.split('\n'):
		# Skip empty lines.
		if line.strip() == '':
			continue

		lines.append(line)
	return lines


def count_matches_in_line(card: str) -> int:
	'''For a given line, return an int - how many numbers on that card are in the winning set.'''

	# Discard "Card N:" part of the string by finding ":".
	card = card[card.find(':') + 1:]
	# Separate into winning numbers and numbers you have.
	winning, have = card.split('|')
	# Convert winning numbers from a string to a set.
	winning_set = set( (int(regex_match.group(0)) for regex_match in NUMBER_PATTERN.finditer(winning)) )

	match_count = 0
	# Iterate over numbers you have...
	for regex_match in NUMBER_PATTERN.finditer(have):
		number = int(regex_match.group(0))

		# ...and count matches.
		if number in winning_set:
			match_count += 1

	return match_count


@arparse_and_time_wrapper
def solve(input_: str, flags: dict) -> int:

	solution = 0
	lines = split_into_lines(input_)
	if flags['fix']:
		# i-th position in this array signifies number of cards with "card number" of (i+1).
		# Initiate to all 1(ones)-s, since there is only 1 copy of each card to begin with.
		number_of_copies = [1 for i in range( len(lines) )]

	for card_number, line in enumerate(lines, 1):
		match_count = count_matches_in_line(line)
		# If solving part I.
		if not flags['fix']:
			# Add correct number of "points" to the solution.
			solution += 0 if (match_count == 0) else 2**(match_count-1)

		# If solving part II.
		else:
			# Add copies of cards you won (due to cards with card number "card_number").
			for i in range(1, match_count + 1):
				number_of_copies[card_number + i - 1] += number_of_copies[card_number - 1]

			# Add number of cards with card number "card_number" to the solution.
			solution += number_of_copies[card_number - 1]

	return solution


if __name__ == '__main__':
	solve()
