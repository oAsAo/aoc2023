class Empty(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.is_round = True # Duck typing support.

	def __str__(self):
		return '.'

	def __bool__(self):
		return False

class Rock(object):
	def __init__(self, x, y, is_round):
		self.x = x
		self.y = y
		self.is_round = is_round
	
	def __str__(self):
		if self.is_round:
			return "O"
		else:
			return "#"
	
	def __bool(self):
		return True

class Platform(object):
	def __init__(self, *args):
		self.grid = []
		self.width = 0
		self.height = 0
		#self.rocks = []

		if len(args) > 0:
			if isinstance(args[0], str):
				self._from_string(args[0])
				return
			if isinstance(args[0], Platform):
				self._copy(args[0])
				return
		raise ValueError('Could not initialize Platform from given arguments.')
	
	def _from_string(self, string):
		lines = string.split('\n')[:-1]
		self.width = len(lines[0])
		self.height = len(lines)
		for y in range(self.height):
			self.grid.append([])
			for x in range(self.width):
				element = Empty(x, y)
				if lines[y][x] == "O":
					element = Rock(x, y, is_round=True)
					#self.rocks.append(element)
				elif lines[y][x] == "#":
					element = Rock(x, y, is_round=False)
					#self.rocks.append(element)
				self.grid[-1].append(element)
		print('Initialized Platform from string.')
		print(self)

	def _copy(self, platform):
		self.width = platform.width
		self.height = platform.height
		for y in range(self.height):
			self.grid.append([])
			for x in range(self.width):
				element = None
				if platform.grid[y][x]:
					element = Rock(x, y, platform.grid[y][x].is_round)
				else:
					element = Empty(x, y)
				self.grid[-1].append(element)
		print('Initialized Platform from Platform.')
		print(self)

	
	def __str__(self):
		repr = ''
		for line in self.grid:
			for element in line:
				repr += str(element)	
			repr += '\n'
		return repr
	
	def rows(self):
		for row in self.grid:
			yield row

	def columns(self):
		for x in range(self.width):
			col = []
			for y in range(self.height):
				col.append(self.grid[y][x])
			yield col
	
	def tilt(self, direction="N"):
		direction = direction.upper()
		if direction == 'N':
			for col in self.columns():
				obstacle_position = -1
				for el in col:
					if isinstance(el, Rock):
						if el.is_round:
							self._move_rock(el.x, el.y, el.x, obstacle_position + 1)
						obstacle_position = el.y
		elif direction == 'S':
			for col in self.columns():
				obstacle_position = self.height
				for el in col[::-1]:
					if isinstance(el, Rock):
						if el.is_round:
							self._move_rock(el.x, el.y, el.x, obstacle_position - 1)
						obstacle_position = el.y
		elif direction == 'E':
			for row in self.rows():
				obstacle_position = -1
				for el in row:
					if isinstance(el, Rock):
						if el.is_round:
							self._move_rock(el.x, el.y, obstacle_position + 1, el.y)
						obstacle_position = el.x
		elif direction == 'W':
			for row in self.rows():
				obstacle_position = self.width
				for el in row[::-1]:
					if isinstance(el, Rock):
						if el.is_round:
							self._move_rock(el.x, el.y, obstacle_position - 1, el.y)
						obstacle_position = el.x
		else:
			raise ValueError(f'Invalid compass heading: {direction}')

	def _move_rock(self, x1, y1, x2, y2):
		rock = self.grid[y1][x1]
		self.grid[y1][x1] = Empty(x1, y1)
		rock.x = x2
		rock.y = y2
		self.grid[y2][x2] = rock
	
	def calc_load(self, direction='N'):
		direction = direction.upper()
		total = 0
		for row in self.grid:
			for el in row:
				if isinstance(el, Rock) and el.is_round:
					if direction == 'N':
						total += self.height - el.y
					elif direction == 'S':
						total += el.y + 1
					elif direction == 'W':
						total += self.width - el.x
					elif direction == 'E':
						total += el.x + 1
					else:
						raise ValueError(f'Invalid compass heading: {direction}')
		return total
					
					


input_ = ''
while True:
	try:
		line = input()
	except:
		break
	input_ += line + '\n'

platform = Platform(input_)

platform.tilt('N')
print(platform)

print(f'Load = {platform.calc_load("N")}')

#platform_copy = Platform(platform)
