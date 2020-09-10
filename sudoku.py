import time, copy

# Sudoku Solver
# Written by Alex Beals
# December 16, 2016

grid = []

# Prints out a formatted version of the current grid
def printGrid(grid):
	for row_index,row in enumerate(grid):
		rowString = ""
		if row_index % 3 == 0 and row_index != 0:
			print("------|-------|-------")
		for index,element in enumerate(row):
			if index % 3 == 0 and index != 0:
				rowString += "| "
			if element == 0:
				rowString += "_ "
			else:
				rowString += str(element) + " "
		print(rowString)

# Prints out a much larger version of the current grid (empty squares contain the possibilities in the corner, '?' in the bottom right
# means there are more than four current possibilities)
def printExpandedGrid(grid):
	a = {}
	for r in range(0,9):
		for c in range(0,9):
			l = findPossible(r,c,grid)
			if len(l) > 4:
				l = l[:3]
				l.append("?")
			a[(r,c)] = l

	for r in range(0,9):
		row1 = ""
		row2 = ""
		row3 = ""
		for c in range(0,9):
			l = a[(r,c)]
			if c % 3 == 0 and c != 0:
				row1 += " # "
				row2 += " # "
				row3 += " # "
			elif c != 0:
				row1 += "|"
				row2 += "|"
				row3 += "|"

			if len(l) == 0:
				row1 += "     "
				row2 += "  " + str(grid[r][c]) + "  "
				row3 += "     "
			elif len(l) == 1:
				row1 += str(l[0]) + "    "
				row2 += "     "
				row3 += "     "
			elif len(l) >= 2:
				row1 += str(l[0]) + "   " + str(l[1])
				row2 += "     "
				if len(l) == 2:
					row3 += "     "
				elif len(l) == 3:
					row3 += str(l[2]) + "    "
				elif len(l) == 4:
					row3 += str(l[2]) + "   " + str(l[3])
		if r % 3 == 0 and r != 0:
			print("##########################################################")
		elif r != 0:
			print("------------------#-------------------#------------------")
		print(row1)
		print(row2)
		print(row3)

# This finds all possible values for a square by eliminating those in the box that
# it's in, the row, and the column (naive)
def findPossible(r_i, c_i, grid):
	if grid[r_i][c_i] == 0:
		possible = list(range(1,10))
		# Row
		for c in range(0,9):
			e = grid[r_i][c]
			if e != 0 and e in possible:
				possible.remove(e)
		# Col
		for r in range(0,9):
			e = grid[r][c_i]
			if e != 0 and e in possible:
				possible.remove(e)
		# Box
		for r in range(0+r_i//3*3,r_i//3*3+3):
			for c in range(0+c_i//3*3,c_i//3*3+3):
				e = grid[r][c]
				if e != 0 and e in possible:
					possible.remove(e)
		return possible
	else:
		return []

# This returns all elements in a given box
def box(grid,r_i,c_i):
	elems = list(range(1,10))
	for r in range(r_i*3,r_i*3+3):
		for c in range(c_i*3,c_i*3+3):
			e = grid[r][c]
			if e != 0 and e in elems:
				elems.remove(e)
	return elems

# This attempts to find the/a next move
# Silent determines if it prints out the move it makes (not done for 'complete')
# Depth determines if it's allowed to try guessing (if depth < 3)
# Finish if it should be allowed to make any move possible (complete)
def nextMove(grid,silent=False,depth=0,finish=False):
	foundMove = False
	# Easy iteration through all spots, checking if clearly only one
	for r_i in range(0,9):
		for c_i in range(0,9):
			possible = findPossible(r_i,c_i,grid)
			if len(possible) == 1:
				if not foundMove:
					if not silent:
						print("(" + str(r_i+1) + "," + str(c_i+1) + ") -> " + str(possible[0]) + "  [Only possible]")
					grid[r_i][c_i] = possible[0]
					foundMove = True

	# Check by number
	if not foundMove:
		for n in range(1,10):
			# Check by row
			if not foundMove:
				for r_i in range(0,9):
					m = []
					for c_i in range(0,9):
						if n in findPossible(r_i,c_i,grid):
							m.append((r_i,c_i))
					if len(m) == 1 and not foundMove:
						if not silent:
							print("(" + str(m[0][0]+1) + "," + str(m[0][1]+1) + ") -> " + str(n) + "  [Only in row]")
						grid[m[0][0]][m[0][1]] = n
						foundMove = True

			# Check by column
			if not foundMove:
				for c_i in range(0,9):
					m = []
					for r_i in range(0,9):
						if n in findPossible(r_i,c_i,grid):
							m.append((r_i,c_i))
					if len(m) == 1 and not foundMove:
						if not silent:
							print("(" + str(m[0][0]+1) + "," + str(m[0][1]+1) + ") -> " + str(n) + "  [Only in column]")
						grid[m[0][0]][m[0][1]] = n
						foundMove = True

			# Check by box
			if not foundMove:
				for b_r in range(0,3):
					for b_c in range(0,3):
						b = box(grid,b_r,b_c)
						if n in b:
							m = []
							for r in range(b_r*3,b_r*3+3):
								for c in range(b_c*3,b_c*3+3):
									if n in findPossible(r,c,grid):
										m.append((r,c))
							if len(m) == 1 and not foundMove:
								if not silent:
									print("(" + str(m[0][0]+1) + "," + str(m[0][1]+1) + ") -> " + str(n) + "  [Only in box]")
								grid[m[0][0]][m[0][1]] = n
								foundMove = True

	# Guessing clause (not a very pretty fallback)
	if not foundMove and depth < 2:
		for r_i in range(0,9):
			for c_i in range(0,9):
				if not foundMove:
					possible = findPossible(r_i,c_i,grid)
					for i in possible:
						if not foundMove and testPossible(grid,r_i,c_i,i,depth+1,finish):
							if not silent:
								print(depth)
								print("(" + str(r_i+1) + "," + str(c_i+1) + ") -> " + str(i) + "  [Guessing and checking]")
							grid[r_i][c_i] = i
							foundMove = True

	return foundMove

# This checks if the grid is finished
def hasMoves(grid):
	return any(0 in row for row in grid)
	# for row in grid:
	# 	print(row)
	# return False

# This attempts to complete the grid by continually calling nextMove until it gets stuck or succeeds
def complete(grid,depth=0):
	moved = True
	while hasMoves(grid) and moved:
		moved = nextMove(grid,True,depth,True)
	return not hasMoves(grid)

# Checks if it can find a solution given a grid, and then a row-column pair with a value to try.
# If it finds a solution and finish is true, then it sets the grid to the solution so as to speed it up.
def testPossible(grid,r,c,n,depth,finish):
	dup = copy.deepcopy(grid)
	dup[r][c] = n
	if complete(dup,depth):
		if finish:
			for r in range(0,9):
				for c in range(0,9):
					grid[r][c] = dup[r][c]
		return True
	else:
		return False

def isValid(grid):
	# Check that all rows contain no repeats
	for row in grid:
		found = []
		for i in row:
			if i in found:
				return False
			if i != 0:
				found.append(i)

	# Check that all columns contain no repeats
	for c in range(0,9):
		found = []
		for r in range(0,9):
			i = grid[r][c]
			if i in found:
				return False
			if i != 0:
				found.append(i)

	return True


# The UI, with options for entering grids, finding next moves, printing the current grid, finishing the grid, and printing out
# possible values for a row and column index
def call_from_main(data):
	grid = []
	if len(grid) == 0:
		tempGrid = []

		# data = ""
		# while len(data) != 81:
		tempGrid = []
			# data = str(input("Type in the grid, going left to right row by row, 0 = empty: "))
		if len(data) != 81:
			print("Not 81 characters.")
		else:
			for row in range(0,9):
				r = []
				for col in range(0,9):
					r.append(int(data[row*9+col]))
				tempGrid.append(r)
			# if not isValid(tempGrid):
			# 	data = ""
			# 	print("Invalid grid.")
			# 	printGrid(tempGrid)

		if (not isValid(tempGrid)):
			print("Invalid grid.")
			exit()
		grid = tempGrid

	# Initialize variables
	time1 = 0

	# c = input("Controls:\n\t'Enter': Display the next move\n\t'p': Print the current grid (small)\n\t'g': Print the current grid (large)\n\t'c': Complete the grid (or attempt to)\n\t'(r,c)': Prints the possible options for that row, column\n")
	c = "c"
	while hasMoves(grid) and (len(c) == 0 or c == "p" or c == "c" or c == "g" or c[0] == "("):
		if c == "p":
			printGrid(grid)
		elif c == "g":
			printExpandedGrid(grid)
		elif c == "c":
			time1 = time.time()
			if not complete(grid):
				print("Failed to complete.  Please improve algorithm. :)")
				#break
		elif len(c) > 0 and c[0] == "(":
			print(findPossible(int(c[1])-1,int(c[3])-1,grid))
		else:
			nextMove(grid)

		if hasMoves(grid):
			c = input("Controls:\n\t'Enter': Display the next move\n\t'p': Print the current grid (small)\n\t'g': Print the current grid (large)\n\t'c': Complete the grid (or attempt to)\n\t'(r,c)': Prints the possible options for that row, column\n")
		else:
			time2 = time.time()
			print(grid)
			# printGrid(grid)
			if time1 != 0:
				print("Solved in %0.2fs!" % (time2-time1))
			else:
				print("Solved!")
	return grid