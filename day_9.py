#!/usr/bin/python3

# AOC 2023 Day 9 solution, part I: ##########
# Completed 5034 iterations in 59.97s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     40.61μs    36.72μs   14.92μs
# Execute  11.87ms    11.73ms   313.72μs
# Total    11.91ms    11.76ms   319.02μs
# 
# AOC 2023 Day 9 solution, part II: ###
# Completed 4842 iterations in 59.96s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     50.13μs    37.80μs   21.94μs
# Execute  12.33ms    12.21ms   339.39μs
# Total    12.38ms    12.25ms   354.41μs

from re import finditer
from re import compile as regex_compile
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(9)

NUMBER_PATTERN = regex_compile('-?([0-9])+')

def is_zero(sequence: list) -> bool:
	'''Return True if and only if list contains only zeros.'''
	if sum( (abs(number) for number in sequence) ) == 0:
		return True
	else:
		return False

def forward_difference(sequence: list) -> list:
	'''Calculate the first order forward difference(https://en.wikipedia.org/wiki/Finite_difference) of a sequence.'''
	dsequence = []
	for i in range(len(sequence) - 1):
		dsequence.append( sequence[i+1] - sequence[i] )
	return dsequence

def extrapolate(sequence: list) -> int:
	'''Use calculus of finite differences to predict next value in a list of integers.'''
	# Calculate higher and higher forward differences until highest of them is a sequence of 0-s.
	differences = [sequence]
	while not is_zero(differences[-1]):
		differences.append( forward_difference(differences[-1]) )

	# Extrapolate the highest-degree difference by adding a zero to it.
	differences[-1].append(0)
	# Extrapolate the rest(including 0-th degree aka the original sequence) of them.
	for i in range(len(differences)-2, -1, -1):
		differences[i].append(differences[i][-1] + differences[i+1][-1])

	# Return the newly extrapolated value.
	return differences[0][-1]

def solve(input_: str, flags: dict) -> int:
	answer = 0
	for line in input_.split('\n'):
		# Skip lines that only contain whitespace.
		if line.strip() == '':
			continue
		# Parse each line into a list of integers.
		sequence = [int(num.group(0)) for num in NUMBER_PATTERN.finditer(line)]
		# Solve part I.
		if not flags['fix']:
			answer += extrapolate(sequence)
		# Solve part II.
		else:
			# Flip sequence before extrapolating.
			answer += extrapolate(sequence[::-1])
	return answer


if __name__ == '__main__':
	solve = arparse_and_time_wrapper(solve)
	solve()