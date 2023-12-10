#!/usr/bin/python3

# AOC 2023 Day 10 solution, part I: ####
# Completed 723 iterations in 1m 0s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     114.97μs   107.24μs  28.74μs
# Execute  82.95ms    81.46ms   16.68ms
# Total    83.07ms    81.58ms   16.69ms

# AOC 2023 Day 10 solution, part II: ###
# Completed 7 iterations in 1m 3s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     106.25μs   107.80μs  15.61μs
# Execute  9.04s      9.18s     259.10ms
# Total    9.04s      9.18s     259.10ms

from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY
from cmath import phase
from math import isclose, tau

SETDAY(10)

class Tile(object):
	'''Is used by Grid implementation to represent the data in its each individual tile.'''
	def __init__(self, char, position):
		self._character = char
		self.neighbours = []
		self.position = position
		self.is_part_of_main_loop = None
		self.is_enclosed_by_main_loop = None

	def is_ground(self):
		'''Check if this tile is a ground tile.'''
		return self._character == '.'

	def _append_neighbour_if_exists(self, neighbour):
		'''Append "neigbour" to the list of neighbours if it isn't None. Internal use.'''
		if neighbour is not None:
			self.neighbours.append(neighbour)

class Grid(object):
	def __init__(self, input_):
		self._tiles = [[]]
		self.width = 0
		self.height = 0
		self.start_tile = None
		self.parse_from_input(input_)
		self.main_loop = self.get_main_loop()
		self.tiles_enclosed_by_main_loop = None

	def mark_tiles_inside_main_loop(self):
		'''Initializes all Tile.is_enclosed_by_main_loop to be True if the tile is enclosed by the main loop
		and to be False if it's outside of the main loop. Tiles that are part of the loop remain set to None.'''
		self.tiles_enclosed_by_main_loop = 0
		for y in range(self.height):
			for x in range(self.width):
				this_tile = self._tiles[y][x]
				# Skip tiles that are part of main loop.
				if this_tile.is_part_of_main_loop:
					continue
				north_tile = None if y <= 0 else self._tiles[y-1][ x ]
				west_tile  = None if x <= 0 else self._tiles[ y ][x-1]

				# If this tile is next to a tile that is known to be inside or known to be outside,
				# we can skip some expensive calculations by marking it to be the same.
				# Look at the tile to the west(left) of this tile.
				if west_tile is not None:
					if not west_tile.is_ground():
						if west_tile.is_enclosed_by_main_loop is True:
							this_tile.is_enclosed_by_main_loop = True
							self.tiles_enclosed_by_main_loop += 1
							continue
						if west_tile.is_enclosed_by_main_loop is False:
							this_tile.is_enclosed_by_main_loop = False
							continue
				
				# Look at the tile to the north(top) of this tile.
				if north_tile is not None:
					if not north_tile.is_ground():
						if north_tile.is_enclosed_by_main_loop is True:
							this_tile.is_enclosed_by_main_loop = True
							self.tiles_enclosed_by_main_loop += 1
							continue
						if north_tile.is_enclosed_by_main_loop is False:
							this_tile.is_enclosed_by_main_loop = False
							continue

				# If we have to, calculate whether this tile is enclosed using "winding number".
				if self.is_inside(this_tile, self.main_loop):
					this_tile.is_enclosed_by_main_loop = True
					self.tiles_enclosed_by_main_loop += 1
				else:
					this_tile.is_enclosed_by_main_loop = False

	def parse_from_input(self, input_):
		self._tiles = []
		starting_position = None

		# Fill the _tiles array with Tile objects, without yet properly initiating them.
		for y, line in enumerate(input_.split('\n')):
			# Skip lines that only contain whitespace.
			if line.strip() == '':
				continue

			# Append a new row to the 2d array of Tile-s.
			self._tiles.append([])
			for x, char in enumerate(line):
				new_tile = Tile(char, (x, y))
				# Record the position of the starting tile.
				if char == 'S':
					self.start_tile = new_tile
					starting_position = (x, y)
				# Append a new Tile entry to the last row of 2d array.
				self._tiles[-1].append(new_tile)

		# Figure out width and height of the grid.
		height = len(self._tiles)
		width = len(self._tiles[0])
		self.width, self.height = width, height

		# "Initiate" all the Tile-s except starting position.
		for y in range(self.height):
			for x in range(self.width):
				tile = self._tiles[y][x]

				# Skip ground Tile-s.
				if tile.is_ground():
					continue

				# Skip starting position for now.
				if (x, y) == starting_position:
					continue

				# Add neigbours that this kind of pipe should have to the neigbours list.
				north_tile = None if y <= 0        else self._tiles[y-1][ x ]
				south_tile = None if y >= height-1 else self._tiles[y+1][ x ]
				west_tile  = None if x <= 0        else self._tiles[ y ][x-1]
				east_tile  = None if x >= width-1  else self._tiles[ y ][x+1]
				if tile._character == '|':
					tile._append_neighbour_if_exists(north_tile)
					tile._append_neighbour_if_exists(south_tile)
				if tile._character == '-':
					tile._append_neighbour_if_exists(west_tile)
					tile._append_neighbour_if_exists(east_tile)
				if tile._character == 'L':
					tile._append_neighbour_if_exists(north_tile)
					tile._append_neighbour_if_exists(east_tile)
				if tile._character == 'J':
					tile._append_neighbour_if_exists(north_tile)
					tile._append_neighbour_if_exists(west_tile)
				if tile._character == '7':
					tile._append_neighbour_if_exists(south_tile)
					tile._append_neighbour_if_exists(west_tile)
				if tile._character == 'F':
					tile._append_neighbour_if_exists(south_tile)
					tile._append_neighbour_if_exists(east_tile)

		# Figure out starting Tile by analyzing Tile-s next to it.
		x, y = starting_position
		north_tile = None if y <= 0        else self._tiles[y-1][ x ]
		south_tile = None if y >= height-1 else self._tiles[y+1][ x ]
		west_tile  = None if x <= 0        else self._tiles[ y ][x-1]
		east_tile  = None if x >= width-1  else self._tiles[ y ][x+1]

		# Figure out in which directions starting pipe is connected.
		# Also connect the starting tile in those directions.
		start_has_north_connection = False
		if north_tile is not None:
			if self.start_tile in north_tile.neighbours:
				start_has_north_connection = True
				self.start_tile.neighbours.append(north_tile)
		start_has_south_connection = False
		if south_tile is not None:
			if self.start_tile in south_tile.neighbours:
				start_has_south_connection = True
				self.start_tile.neighbours.append(south_tile)
		start_has_west_connection = False
		if west_tile is not None:
			if self.start_tile in west_tile.neighbours:
				start_has_west_connection = True
				self.start_tile.neighbours.append(west_tile)
		start_has_east_connection = False
		if east_tile is not None:
			if self.start_tile in east_tile.neighbours:
				start_has_east_connection = True
				self.start_tile.neighbours.append(east_tile)

		# Figure out which character should the starting pipe be represented with.
		# Not strictly necessary, but why not.
		if start_has_north_connection and start_has_south_connection:
			self.start_tile._character = '|'
		if start_has_east_connection and start_has_west_connection:
			self.start_tile._character = '-'
		if start_has_north_connection and start_has_east_connection:
			self.start_tile._character = 'L'
		if start_has_north_connection and start_has_west_connection:
			self.start_tile._character = 'J'
		if start_has_south_connection and start_has_west_connection:
			self.start_tile._character = '7'
		if start_has_south_connection and start_has_east_connection:
			self.start_tile._character = 'F'

	def get_main_loop(self):
		'''Return a list of all tiles belonging to the main loop.'''
		main_loop_tiles = [self.start_tile]
		last_visited_tile = self.start_tile
		tile = self.start_tile.neighbours[0]
		# Navigate the main loop and record tiles we visit.
		while tile is not self.start_tile:
			tile.is_part_of_main_loop = True
			main_loop_tiles.append(tile)
			# Don't go in the direction we came from. Go in the opposite direction.
			if last_visited_tile is tile.neighbours[0]:
				last_visited_tile = tile
				tile = tile.neighbours[1]
			else:
				last_visited_tile = tile
				tile = tile.neighbours[0]
		return main_loop_tiles

	def is_inside(self, this_tile, loop):
		'''Check if a tile is inside a loop by calculating the winding number(https://en.wikipedia.org/wiki/Winding_number).'''
		total_angle_difference = 0

		# Follow the main loop. The main loop can be seen as a closed path.
		# Each two tiles next to each other along those path can be seen as a line segment in.
		prev_loop_tile = loop[-1]
		for loop_tile in loop:
			# Project each line segment onto the unit circle by projecting start and end point separately.
			start = complex(*prev_loop_tile.position) - complex(*this_tile.position)
			end   = complex(*loop_tile.position)      - complex(*this_tile.position)
			start_angle = phase(start) % tau
			end_angle =   phase( end ) % tau

			# Figure out (signed) length of this projection...
			d_angle = (tau + end_angle - start_angle) % tau
			if d_angle > 0.5*tau:
				d_angle -= tau
			# ...and add it to a total.
			total_angle_difference += d_angle

			prev_loop_tile = loop_tile

		# Calculate the winding number.
		winding_number = (total_angle_difference / tau) % 2

		# If winding number is 1, this point(tile) is inside the loop.
		if isclose(winding_number, 1, rel_tol=0.1):
			return True
		else:
			return False



def solve(input_, flags):
	# Make a Grid object from input.
	area_sketch = Grid(input_)
	# Get the main loop in that grid(ad a list of Tile-s).
	main_loop = area_sketch.main_loop
	# If solving Part I.
	if not flags['fix']:
		# You get to the most distant point of a loop if you follow it for half of its length.
		max_distance = (len(main_loop) + 1) // 2
		return max_distance
	# If solving Part II.
	else:
		# Calculate number of tiles enclosed by the main loop.
		area_sketch.mark_tiles_inside_main_loop()
		return area_sketch.tiles_enclosed_by_main_loop


if __name__ == '__main__':
	solve = arparse_and_time_wrapper(solve)
	solve()
