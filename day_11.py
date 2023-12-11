#!/usr/bin/python3

# AOC 2023 Day 11 solution, part I: #######
# Completed 1005 iterations in 1m 0s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     36.54μs    34.29μs   10.09μs
# Execute  59.69ms    59.57ms   744.81μs
# Total    59.73ms    59.61ms   751.89μs

# AOC 2023 Day 11 solution, part II: ############
# Completed 895 iterations in 1m 0s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     53.59μs    37.85μs   27.96μs
# Execute  67.04ms    65.94ms   1.94ms
# Total    67.09ms    65.99ms   1.96ms


from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(11)

EXPANSION_FACTOR = 2

def parse(input_):
	'''Parse input and return three lists.
	First - with 0-indexed (x, y) coordinates of each galaxy.
	Second - a list of booleans that tell whether or not each -column- is empty.
	Third - a list of booleans that tell whether or not each -row- is empty.'''
	lines = input_.split('\n')
	galaxies = []
	# Initiate are_columns_empty to correct size (width), all presumed to be True.
	are_columns_empty = [True for i in range( len(lines[0]) )]
	are_rows_empty = []
	for y, line in enumerate(lines):
		# Skip lines that only contain whitespace.
		if line.strip() == '':
			continue
		# Append a True to are_rows_empty to get correct height by the end of loop.
		are_rows_empty.append(True)
		for x, char in enumerate(line):
			# If we find a galaxy, then this row and column are definetely not
			# empty, and we also append it to the list of galaxies.
			if char == '#':
				galaxies.append( (x, y) )
				are_rows_empty[-1] = False
				are_columns_empty[x] = False
	return galaxies, are_columns_empty, are_rows_empty

def expand(galaxies, are_columns_empty, are_rows_empty):
	'''Take results from parse(), and calculate positions of
	the galaxies in the "expanded universe".'''
	new_galaxies = []
	for galaxy in galaxies:
		x, y = galaxy
		x_new, y_new = x, y
		for i, is_column_empty in enumerate(are_columns_empty):
			if i >= x:
				break
			if is_column_empty:
				x_new += (EXPANSION_FACTOR - 1)
		for i, is_row_empty in enumerate(are_rows_empty):
			if i >= y:
				break
			if is_row_empty:
				y_new += (EXPANSION_FACTOR - 1)
		new_galaxies.append( (x_new, y_new) )
	return new_galaxies

def distance(p1, p2):
	'''Calculate taxicab distance(https://en.wikipedia.org/wiki/Taxicab_geometry)
	between two points (in this case galaxies).'''
	return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])

def solve(input_, flags):
	global EXPANSION_FACTOR
	# Choose how much bigger to make each empty line.
	# Depends on whether we are solving Part I or II.
	if flags['fix']:
		EXPANSION_FACTOR = 1_000_000
	else:
		EXPANSION_FACTOR = 2
	
	universe = parse(input_)
	expanded_galaxies = expand(*universe)

	# This is kinda stupid but i literally just calculate distance between each pair of galaxies.
	# Also conveniently distance from a galaxy to itself is 0, so no special cases.
	sum_of_distances = 0
	for galaxy_A in expanded_galaxies:
		for galaxy_B in expanded_galaxies:
			sum_of_distances += distance(galaxy_A, galaxy_B)

	# For some reason puzzle actually wants half of the answer.
	# Obviously there's double cover, but i think it should count.
	return sum_of_distances // 2


if __name__ == '__main__':
	solve = arparse_and_time_wrapper(solve)
	solve()
