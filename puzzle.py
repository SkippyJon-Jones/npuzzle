import copy

def LoadFromFile(filepath):
	file = open(filepath, "r")
	n = file.read(1)
	n = int(n)
	next(file)

	listrep = []
	for i in file:
		i = i.rstrip()
		y = i.split("\t")
		if (len(y) > n):
			return None
		listrep.append(y)

	if(len(listrep) > n):
		return Non

	return listrep

	file.close()	

def DebugPrint(state):
	for line in state:
		for num in line:
			print(num + "\t", end = '')
		print("\n")

def computeNeighbors(state):
	locationOfSpace = []

	listnum = 0
	elementnum = 0
	for list in state:
		for element in list:
			if (element == "*"):
				locationOfSpace.append(listnum)
				locationOfSpace.append(elementnum)
			elementnum += 1
		listnum += 1
		elementnum = 0

	returnlist = []

	rowOfSpace, colOfSpace = locationOfSpace

	if(rowOfSpace > 0):
		returnlist.append(computeVerticalState(state,locationOfSpace, -1))

	if(rowOfSpace < len(state) - 1):
		returnlist.append(computeVerticalState(state, locationOfSpace, 1))

	if(colOfSpace > 0):
		returnlist.append(computeHorizontalState(state, locationOfSpace, -1))

	if (colOfSpace < len(state) - 1):
		returnlist.append(computeHorizontalState(state, locationOfSpace, 1))

	return returnlist


def computeVerticalState(state, locationOfSpace, pos):
	tempstate = copy.deepcopy(state)
	row, col = locationOfSpace

	num = tempstate[row + pos][col]
	tempstate[row][col] = num
	tempstate[row + pos][col] = "*"
	returnlist1 = [num, tempstate]
	return returnlist1

def computeHorizontalState(state, locationOfSpace, pos):
	tempstate = copy.deepcopy(state)
	row, col = locationOfSpace

	num = tempstate[row][col + pos]
	tempstate[row][col] = num
	tempstate[row][col + pos] = "*"
	returnlist2 = [num, tempstate]
	return returnlist2

def IsGoal(state):
	i = 1
	positionOfSpace = (len(state) ** 2) 
	for row in state:
		for element in row:
			if(i == positionOfSpace and element == "*"):
				return True
			if(element == "*"):
				return False
			if (int(element) != i):
				return False
			i = i +1

def BFS(state):
	frontier = [state]
	discovered = set(map(tuple, flatten(state)))

	parents = {map(tuple, flatten(state)): None}

	while frontier:
		current_state = frontier.pop(0)

		discovered.add(map(tuple, flatten(current_state)))

		if IsGoal(current_state):
			tiles = []
			print(parents[map(tuple, flatten(current_state))])
			currentkey = parents[current_state]
			while currentkey != None:
				tiles.append(currentkey)
				currentkey = tuple(currentkey).get()
			return tiles
		for neighbor in computeNeighbors(current_state):
			# print("x")
			if (map(tuple, neighbor)) not in discovered:
				print("y")
				frontier.append(neighbor[1])
				discovered.add((map(tuple, flatten(neighbor))))	
				parents[map(tuple, flatten(neighbor))] = current_state

def flatten(state):
	list2d = []
	list = []
	for row in state:
		for element in row:
			list.append(element)
	list2d.append(list)
	return list2d


def main():

	gamestate = (LoadFromFile("npuzzledata.txt"))
	print(gamestate)
	print("\n")
	DebugPrint(gamestate)
	print("\n")

	print(BFS(gamestate))
	# print(IsGoal(gamestate))
	#print(computeNeighbors(gamestate))
	#print(computeNeighbors(gamestate))

	# list = computeNeighbors(gamestate)
	# DebugPrint(gamestate)
	# print("\n")
	# for x in list:
	# 	DebugPrint(x[1])
	# 	print("\n")

main()