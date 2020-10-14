def LoadFromFile(filepath):
	file = open(filepath, "r")

	#why do i need to keep track of dimensions?
	dimensions = file.read(0)
	next(file)

	listrep = []
	for i in file:
		i = i.rstrip()
		y = i.split("\t")

		listrep.append(y)


	return listrep

	file.close()	

def DebugPrint(state):
	for line in state:
		for num in line:
			print(num + "\t", end = '')
		print("\n")


def main():
	gamestate = (LoadFromFile("npuzzledata.txt"))
	DebugPrint(gamestate)

main()