import copy
import math

def LoadFromFile(filepath):
	file = open(filepath, "r")
	n = file.read(1)
	n = int(n)
	next(file)

	listrep = []

	# creates a 2d list representation of the input data
	for i in file:
		i = i.rstrip()
		y = i.split("\t")

		# checks ot see if each line is too long
		if (len(y) > n):
			return None

		listrep.append(y)

	# checks to see if there are too many lines
	if(len(listrep) > n):
		return None

	# converts the 2d list rep to a tuple of tuples
	tuplerep = tuple(map(tuple, listrep))
	return tuplerep

	file.close()	

# prints the current gamestate as a representation of how it
#  would look in the actual game
def DebugPrint(state):
	for line in state:
		for num in line:
			print(num + "\t", end = '')
		print("\n")

def computeNeighbors(state):
	locationOfSpace = []


	listnum = 0
	elementnum = 0

	# loops through the whole gamestate to find the 
	#  coordinates  of the space
	for list in state:
		for element in list:
			if (element == "*"):
				locationOfSpace.append(listnum)
				locationOfSpace.append(elementnum)
			elementnum += 1
		listnum += 1
		elementnum = 0

	
	# list representaion of neighbor states
	returnlist = []

	# unpacks the coordinates to do tests within this function
	rowOfSpace, colOfSpace = locationOfSpace

	# series of if statements to check if there is a possible neighbor 
	#  	in the up, down, right, or left direction
	if(rowOfSpace > 0):
		returnlist.append(computeVerticalState(state,locationOfSpace, -1))

	if(rowOfSpace < len(state) - 1):
		returnlist.append(computeVerticalState(state, locationOfSpace, 1))

	if(colOfSpace > 0):
		returnlist.append(computeHorizontalState(state, locationOfSpace, -1))

	if (colOfSpace < len(state) - 1):
		returnlist.append(computeHorizontalState(state, locationOfSpace, 1))

	# converts the list rep to a tuple rep
	tuplelist = tuple(returnlist)

	return tuplelist

# finds the neighboring state that requires moving
 # a tile from the left or the right
def computeVerticalState(state, locationOfSpace, pos):
	# creates a completely new copy of the current state as a list
	tempstate = list(map(list, copy.deepcopy(state)))

	row, col = locationOfSpace

	# series of steps to switch the space and the 
	#  tile in the specified direction
	num = tempstate[row + pos][col]
	tempstate[row][col] = num
	tempstate[row + pos][col] = "*"

	# converts the list rep of the state to a tuple rep
	tuplestate = tuple(map(tuple, tempstate))

	# returns both the neigboring gamestate and the tiles that was moved
	returntuple = (num, tuplestate)

	return returntuple

# finds the neighboring state that requires moving
 # a tile from above or below
def computeHorizontalState(state, locationOfSpace, pos):
	# creates a completely new copy of the current state as a list
	tempstate = list(map(list, copy.deepcopy(state)))
	row, col = locationOfSpace

	# series of steps to switch the space and the 
	#  tile in the specified direction
	num = tempstate[row][col + pos]
	tempstate[row][col] = num
	tempstate[row][col + pos] = "*"

	# converts the list rep of the state to a tuple rep
	tuplestate = tuple(map(tuple, tempstate))

	# returns both the neigboring gamestate and the tiles that was moved
	returntuple = (num, tuplestate)

	return returntuple

def IsGoal(state):
	i = 1
	# finds where the space should be in a winning gamestate
	positionOfSpace = (len(state) ** 2) 
	for row in state:
		for element in row:
			# series of checks to determine if the gamestate qualfies as being
			#  the "winning state"
			if(i == positionOfSpace and element == "*"):
				return True
			if(element == "*"):
				return False
			if (int(element) != i):
				return False
			i = i + 1

# searching for the shortest amount of tiles to move
#  in order to achieve a winning gamestate
def BFS(state):
	frontier = [state]
	discovered = set(state)

	parents = {state: None}

	while frontier:
		# pops the front element of the frontier to search
		current_state = frontier.pop(0)

		discovered.add(current_state)

		# if the current state is the goal state, it returns the tiles
		#  moved in order to get to this current state
		if IsGoal(current_state):
			states = []
			states.append(current_state)
			tiles = []

			currentkey = parents[current_state]

			# backtracks through the parents to find the states that
			#  were passed through on the way to this current state
			while currentkey != None:
				states.append(currentkey)
				currentkey = parents[currentkey]

			# from the series of states, finds the series of tiles
			#  from each state to the next
			i = 1
			for stategoal in states:
				if (i < len(states)):
					tiles.append(getTile(stategoal, states[i]))
					i = i + 1

			# puts the list of tiles into the correct order
			tiles.reverse()

			return tiles

		# loops through the neighbors of the current state
		for neighbor in computeNeighbors(current_state):
			# if the current state hasn't already been considered,
			#  adds it to the list of states to explore and keeps
			#  	track of the "parent" state
			if neighbor[1] not in discovered:
				# adds the neighboring state to the
				#  BACK of the frontier list
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state
	return None

# searching for any series of tiles to get to
#  a winning game state. Similar process to BFS.
def DFS(state):
	frontier = [state]
	discovered = set(state)

	parents = {state: None}

	while frontier:
		# pops the front element of the frontier to search
		current_state = frontier.pop(0)

		discovered.add(current_state)

		# backtracks through the parents to find the states that
			#  were passed through on the way to this current state
		if IsGoal(current_state):
			states = []
			states.append(current_state)
			tiles = []

			currentkey = parents[current_state]

			# backtracks through the parents to find the states that
			#  were passed through on the way to this current state
			while currentkey != None:
				states.append(currentkey)
				currentkey = parents[currentkey]

			# from the series of states, finds the series of tiles
			#  from each state to the next
			i = 1
			for stategoal in states:
				if (i < len(states)):
					tiles.append(getTile(stategoal, states[i]))
					i = i + 1

			# puts the list of tiles into the correct order
			tiles.reverse()

			return tiles

		# loops through the neighbors of the current state
		for neighbor in computeNeighbors(current_state):
			# if the current state hasn't already been considered,
			#  adds it to the list of states to explore and keeps
			#  	track of the "parent" state
			if neighbor[1] not in discovered:
				# adds the neighboring state to the
				#  FRONT of the frontier list
				frontier.insert(0, neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state
	return None

# runs to BFS searches in sync with eachother,
#  searching from the goal state and the original
#  game state
def BidirectionalSearch(state):

	goalstate = getGoalState(state)

	# creates two of each data structure for the 
	#  two simulataneous searches
	frontier = [state]
	frontierGoal = [goalstate]

	discovered = set(state)
	discoveredGoal = set(goalstate)

	parents = {state: None}
	parentsGoal = {goalstate: None}

	while frontier or frontierGoal:
		# pops the current state of both frontier lists
		current_state = frontier.pop(0)
		current_stateGoal = frontierGoal.pop(0)

		discovered.add(current_state)
		discoveredGoal.add(current_stateGoal)

		# checks to see if the two sets of the two searhces
		#  have any common elemnents
		intersection = discovered.intersection(discoveredGoal)
		if(len(intersection) > 0):

			# set both of the current states to this common element
			current_state = intersection.pop()
			current_stateGoal = current_state


			states = []
			states.append(current_state)
			tiles = []

			currentkey = parents[current_state]

			# backtracks from the current state to the original
			#  game state
			while currentkey != None:
				states.append(currentkey)
				currentkey = parents[currentkey]

			# finds the series of tiles from the series of states
			i = 1
			for prevstate in states:
				if (i < len(states)):
					tiles.append(getTile(prevstate, states[i]))
					i = i + 1

			# reverses the tiles into the correct order
			tiles.reverse()



			statesgoal = []
			statesgoal.append(current_stateGoal)
			tilesgoal = []

			currentkeygoal = parentsGoal[current_stateGoal]

			# backtracks from the current state to the goal state
			while currentkeygoal != None:
				statesgoal.append(currentkeygoal)
				currentkeygoal = parentsGoal[currentkeygoal]

			# finds the series of tiles from the series of states
			j = 1
			for prevstategoal in statesgoal:
				if (j < len(statesgoal)):
					tilesgoal.append(getTile(prevstategoal, statesgoal[j]))
					j = j + 1

			# Note: the tiles are already in the correct order for the
			#  goal state because the search was originally done backwards

			# combines both series of tiles into one list
			for x in tilesgoal:
				tiles.append(x)


			return tiles

		# loops through the neighbors of both game states back to back
		for neighbor in computeNeighbors(current_state):
			# if the current state hasn't already been considered,
			#  adds it to the list of states to explore and keeps
			#  	track of the "parent" state
			if neighbor[1] not in discovered:
				# adds the neighboring state to the
				#  FRONT of the frontier list
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state

		for neighbor in computeNeighbors(current_stateGoal):
			# if the current state hasn't already been considered,
			#  adds it to the list of states to explore and keeps
			#  	track of the "parent" state
			if neighbor[1] not in discoveredGoal:
				# adds the neighboring state to the
				#  FRONT of the frontier list
				frontierGoal.append(neighbor[1])
				discoveredGoal.add(neighbor[1])	
				parentsGoal[neighbor[1]] = current_stateGoal


# constructs the goal/winning state for a given state
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

# gets the tile needed to get from one state to another
#  returning None if it is not possible
def getTile(state1, state2):
	for neighbor in computeNeighbors(state1):
		if neighbor[1] == state2:
			return neighbor[0]

# Swaps a tile in a given state and then returns
#  the new state
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


	
main()