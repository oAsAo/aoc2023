#!/usr/bin/python3

# AOC 2023 Day 6 solution, part I: ######
# Completed 1190655 iterations in 52.79s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     26.82μs    26.07μs   5.59μs
# Execute  17.52μs    16.98μs   4.30μs
# Total    44.34μs    43.05μs   7.57μs

# AOC 2023 Day 6 solution, part II: ########
# Completed 1318639 iterations in 51.89s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     26.89μs    26.12μs   4.67μs
# Execute  12.46μs    12.06μs   3.15μs
# Total    39.35μs    38.19μs   6.02μs


from re import finditer
from re import compile as regex_compile
from math import isqrt
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(6)

NUMBER_PATTERN = regex_compile('\d+')

def solve(input_: str, flags: dict) -> int:
	# Init to 1(one) because we are multiplying.
	answer = 1

	# For Part II, ignore spaces.
	if flags['fix']:
		input_ = input_.replace(' ', '')
	# First line are durations. Second line are records.
	race_durations, records = input_.split('\n')[:2]
	race_durations = [int(match.group(0)) for match in NUMBER_PATTERN.finditer(race_durations)]
	records = [int(match.group(0)) for match in NUMBER_PATTERN.finditer(records)]
	# Pair-up corresponding durations and records.
	race_pairs = [(duration, records[i]) for i, duration in enumerate(race_durations)]

	# For each race recorded in the input.
	for duration, record in race_pairs:
		# The question is asking to count all integer x=length of time to hold button for,
		# 	such that x(duration-x) > r. Turning that into an equality and simplifying,
		# 	we get the quadratic equation x^2 - duration*x + records = 0.
		# Length of the range of solutions to original inequality in REAL numbers
		# 	is given by the square root of it's determinant D:
		D = duration * duration - 4 * record
		# However, we are looking for the answer in integers, so we 1.use isqrt() function
		# 	which is basically y = floor(sqrt(x)), but bypassing floats.
		sqrt = isqrt(D)

		# This value is no further than 1 away from the correct answer, and we can find
		# 	the correct answer by adding a correction term that is either 1, 0, or -1.
		# We will need to check whether D was a perfect square or not, which we can do like this:
		is_exact = (sqrt * sqrt == D)
		# Then the equation for the correction term is:
		correction = int(not is_exact) - int(is_exact^(sqrt%2 == 0)^(duration%2 == 0))
		# ...proving that this equation is correct is left as an exercise for the reader.

		# Finally, we multiply answer variable by the number of ways to win this race.
		answer *= (sqrt + correction)

	return answer

if __name__ == '__main__':
	solve = arparse_and_time_wrapper(solve)
	solve()
