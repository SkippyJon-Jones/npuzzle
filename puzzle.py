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
			for stategoal in states:
				if (i < len(states)):
					tiles.append(getTile(stategoal, states[i]))
					i = i + 1

			tiles.reverse()

			return tiles

		for neighbor in computeNeighbors(current_state):
			if neighbor[1] not in discovered:
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state
	return None


def BidirectionalSearch(state):
	goalstate = getGoalState(state)

	frontier = [state]
	frontierGoal = [goalstate]

	discovered = set(state)
	discoveredGoal = set(goalstate)

	parents = {state: None}
	parentsGoal = {goalstate: None}

	while frontier or frontierGoal:
		current_state = frontier.pop(0)
		current_stateGoal = frontierGoal.pop(0)

		discovered.add(current_state)
		discoveredGoal.add(current_stateGoal)

		intersection = discovered.intersection(discoveredGoal)

		if(len(intersection) > 0):
			print(intersection)
			current_state = intersection.pop()
			current_stateGoal = current_state
			states = []
			states.append(current_state)
			tiles = []

			currentkey = parents[current_state]

			while currentkey != None:
				states.append(currentkey)
				currentkey = parents[currentkey]

			i = 1
			for prevstate in states:
				if (i < len(states)):
					tiles.append(getTile(prevstate, states[i]))
					i = i + 1

			tiles.reverse()

			statesgoal = []
			statesgoal.append(current_stateGoal)
			tilesgoal = []

			currentkeygoal = parentsGoal[current_stateGoal]

			while currentkeygoal != None:
				statesgoal.append(currentkeygoal)
				currentkeygoal = parentsGoal[currentkeygoal]

			j = 1
			for prevstategoal in statesgoal:
				if (j < len(statesgoal)):
					tilesgoal.append(getTile(prevstategoal, statesgoal[j]))
					j = j + 1



			for x in tilesgoal:
				tiles.append(x)


			return tiles

		for neighbor in computeNeighbors(current_state):
			if neighbor[1] not in discovered:
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state

		for neighbor in computeNeighbors(current_stateGoal):
			if neighbor[1] not in discoveredGoal:
				frontierGoal.append(neighbor[1])
				discoveredGoal.add(neighbor[1])	
				parentsGoal[neighbor[1]] = current_stateGoal


def getGoalState(state):
	tempstate = list(map(list, copy.deepcopy(state)))
	i = 1
	row = 0
	col = 0
	for originalrow in tempstate:
		for element in originalrow:
			if(i == (len(tempstate) ** 2)):
				tempstate[row][col] = "*"
			else:
				tempstate[row][col] = str(i)
				i += 1
			col += 1
		col = 0
		row += 1

	tuplestate = tuple(map(tuple, tempstate))

	return tuplestate


def DFS(state):
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
			for stategoal in states:
				if (i < len(states)):
					tiles.append(getTile(stategoal, states[i]))
					i = i + 1

			tiles.reverse()

			return tiles

		for neighbor in computeNeighbors(current_state):
			if neighbor[1] not in discovered:
				frontier.insert(0, neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state
	return None



def getTile(state1, state2):
	for neighbor in computeNeighbors(state1):
		if neighbor[1] == state2:
			return neighbor[0]

def swapTiles(tiles, state):
	newstate = copy.deepcopy(state)
	for tile in tiles:
		for neighbor in computeNeighbors(newstate):
			if neighbor[0] == tile:
				newstate = neighbor[1]
	return newstate


def main():

	gamestate = (LoadFromFile("npuzzledata.txt"))
	print(gamestate)
	print("\n")
	# DebugPrint(gamestate)
	# print("\n")
	# print(getGoalState(gamestate))
	print(BidirectionalSearch(gamestate))

	# list = ['1', '2', '3', '8', '6', '4', '5', '1', '7', '5', '1', '7', '2', '3', '8', '6', '7', '8', '6', '7', '4', '1', '5', '2', '3', '6', '8', '5', '2', '3', '6']
	# print(swapTiles(list, gamestate))
	# print(DFS(gamestate))
	# print(BFS(gamestate))
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