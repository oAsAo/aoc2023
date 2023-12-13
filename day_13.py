pattern = []

def f(pattern):
	width = len(pattern[0])
	height = len(pattern)
	for x in range(1, width):
		diff = 0
		for line in pattern:
			if x < width-x:
				left = line[0:x]
			else:
				left = line[2*x-width:x]
			right = line[x:2*x]
			right = right[::-1]
			left = int( left.replace(".", "0").replace("#", "1"), 2)
			right = int( right.replace(".", "0").replace("#", "1"), 2)
			diff += list(bin(left ^ right)[2:]).count("1")
		if diff == 1:
			return x
	return 0

def transpose(pattern):
	width = len(pattern[0])
	height = len(pattern)
	transpose = []
	for row in range(width):
		k = [pattern[col][row] for col in range(height)]
		transpose.append( "".join(k) )
	return transpose

def pr(pattern, refl, tr=False):
	a = ""
	for line in pattern:
		a += line[:refl]+"|"+line[refl:] + "\n"
	
	if tr:
		b = a.split('\n')[:-1]
		b = [list(e) for e in b]
		a = "\n".join(["".join([b[i][j] for i in range(len(b))]).replace("|", "-") for j in range(len(b[0]))])
	print(a)

def process_pattern(pattern):
	a = f(pattern)
	tr = transpose(pattern)
	b = f(tr)
	return 100*b + a

sum = 0
while True:
	try:
		line = input()
	except:
		break
	if line.strip() == '':
		sum += process_pattern(pattern)
		pattern = []
		continue
	pattern.append(line)
sum += process_pattern(pattern)
print(sum)
