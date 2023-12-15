input_ = ""
while True:
	try:
		input_ += input()
	except:
		break

def hsh(s):
	x = 0
	for char in s:
		x += ord(char)
		x *= 17
		x %= 256
	return x

def parse(step):
	if step[-1] == "-":
		return {
			'label': step[:-1],
			'op': '-',
			'r': step
		}
	else:
		a, b = step.split('=')
		return {
			'label': a,
			'op': '=',
			'FL': int(b),
			'r': step
		}

class Box:
	def __init__(self):
		self.inside = []

	def is_empty(self):
		return self.inside == []

	def __str__(self):
		reprs = []
		for step in self.inside:
			reprs.append( f"[{step['label']} {step['FL']}]" )
		return " ".join(reprs)

	def equals(self, step):
		for i, step2 in enumerate(self.inside):
			if step2['label'] == step['label']:
				self.inside[i] = step
				return
		self.inside.append( step )

	def dash(self, step):
		new_inside = []
		for step2 in self.inside:
			if step2['label'] == step['label']:
				continue
			new_inside.append(step2)
		self.inside = new_inside

class HASHMAP:
	def __init__(self):
		self.boxes = [Box() for i in range(256)]

	def stp(self, step):
		if step['op'] == "=":
			self.boxes[ hsh(step['label']) ].equals(step)
		if step['op'] == "-":
			self.boxes[ hsh(step['label']) ].dash(step)
	
	def focusing_power(self):
		fp = 0
		for i, box in enumerate(self.boxes, 1):
			for j, lens in enumerate(box.inside, 1):
				fp += i * j * lens["FL"]
		return fp
		

inp = input_.split(',')

#print(sum([hsh(s) for s in inp]))

inp = [parse(step) for step in inp]

hashmap = HASHMAP()

for step in inp:
	hashmap.stp(step)
	#print(f'After "{step["r"]}":')
	for i, box in enumerate(hashmap.boxes):
		if not box.is_empty():
			#print(f'Box {i}:', box)
			pass
	#print()

print(f"Focusing power: {hashmap.focusing_power()}")
