import copy
import math

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
		return None

	tuplerep = tuple(map(tuple, listrep))
	return tuplerep

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

	tuplelist = tuple(returnlist)
	return tuplelist


def computeVerticalState(state, locationOfSpace, pos):
	tempstate = list(map(list, copy.deepcopy(state)))
	row, col = locationOfSpace

	num = tempstate[row + pos][col]
	tempstate[row][col] = num
	tempstate[row + pos][col] = "*"

	tuplestate = tuple(map(tuple, tempstate))

	returntuple = (num, tuplestate)
	return returntuple

def computeHorizontalState(state, locationOfSpace, pos):
	tempstate = list(map(list, copy.deepcopy(state)))
	row, col = locationOfSpace

	num = tempstate[row][col + pos]
	tempstate[row][col] = num
	tempstate[row][col + pos] = "*"

	tuplestate = tuple(map(tuple, tempstate))

	returntuple = (num, tuplestate)
	return returntuple

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
			i = i + 1

def BFS(state):
	frontier = [state]
	discovered = set(state)

	parents = {state: None}

	while frontier:
		current_state = frontier.pop(0)

		discovered.add(current_state)

		if IsGoal(current_state):
			states = []
			states.append(current_state)
			tiles = []

			currentkey = parents[current_state]

			while currentkey != None:
				states.append(currentkey)
				currentkey = parents[currentkey]

			i = 1
			for state in states:
				if (i <=len(states)):
					tiles.append(getTile(state, states[i]))

			return tiles

		for neighbor in computeNeighbors(current_state):
			if neighbor[1] not in discovered:
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state


def getTile(state1, state2):
	for neighbor in computeNeighbors(state1):
		if neighbor[1] == state2:
			return neighbor[0]

	return "too long"
# def get_key(val, parents):
#     for key, value in parents.items(): 
#          if val == value: 
#              return key
  
#     return None
# def flatten(state):
# 	list2d = []
# 	list = []
# 	for row in state:
# 		for element in row:
# 			list.append(element)
# 	list2d.append(list)
# 	return list2d



# def flattenNieghbor(nieghborstate):
# 	state = nieghborstate[1]
# 	tile = nieghborstate.pop(0)
# 	list = []
# 	list2d = []
# 	list.append(tile)
# 	for row in state:
# 		for element in row:
# 			list.append(element)

# 	list2d.append(list)	
# 	return list2d

# def unflatten(list):
# 	length = math.sqrt(len(list))
# 	list2d = []
# 	individuallist = []
# 	i = 0
# 	for element in list:
# 		if(i == length):
# 			i = 0
# 			list2d.append(individuallist)
# 			individuallist.clear()
# 		else:
# 			individuallist.append(element)
# 	print(list2d)
# 	return list2d

def main():

	gamestate = (LoadFromFile("npuzzledata.txt"))
	print(gamestate)
	print("\n")
	# DebugPrint(gamestate)
	# print("\n")

	print(BFS(gamestate))
	# print(IsGoal(gamestate))
	# print(computeNeighbors(gamestate))
	#print(computeNeighbors(gamestate))

	# list = computeNeighbors(gamestate)
	# DebugPrint(gamestate)
	# print("\n")
	# for x in list:
	# 	DebugPrint(x[1])
	# 	print("\n")

main()