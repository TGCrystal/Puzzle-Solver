from base import Answer, Solver
import copy


class ParkAnswer(Answer):
	def __init__(self, treesPerColor='1', board=None):
		if board is None: #used for copy function
			return
		treesPerColor = int(treesPerColor)
		self.placedTrees = []

		self.rowsAvailable = dict()
		self.columnsAvailable = dict()
		for i in range(0, len(board)): # Boards are square so no need for second loop
			self.rowsAvailable[i] = treesPerColor
			self.columnsAvailable[i] = treesPerColor

		self.colorsAvailable = dict()
		for i in self.rowsAvailable:
			for j in self.columnsAvailable:
				self.colorsAvailable[board[i][j]] = treesPerColor

	def placeTree(self, row, column, color):
		self.rowsAvailable[row] -= 1
		self.columnsAvailable[column] -= 1
		self.colorsAvailable[color] -= 1
		self.placedTrees.append((row, column))

	def getAnswer(self):
		return self.placedTrees

	def __copy__(self):
		cpy = type(self)()
		cpy.rowsAvailable = self.rowsAvailable.copy()
		cpy.columnsAvailable = self.columnsAvailable.copy()
		cpy.colorsAvailable = self.colorsAvailable.copy()
		cpy.placedTrees = self.placedTrees.copy()
		return cpy


class ParkSolver(Solver):
	def __init__(self, fileName):
		self.treesPerColor, self.board = super().loadFile(fileName, 1)
		self.blankAnswer = ParkAnswer(self.treesPerColor, self.board)
		self.colorFrequencies = dict()
		for row in self.board:
			for color in row:
				if color in self.colorFrequencies:
					self.colorFrequencies[color] += 1
				else:
					self.colorFrequencies[color] = 1

		if self.treesPerColor == 1:
			for color in self.colorFrequencies:
				if self.colorFrequencies[color] != 1:
					continue
				willBreak = False
				for i in range(len(self.board)):
					for j in range(len(self.board)):
						if self.board[i][j] == color:
							self.blankAnswer.placeTree(i, j, color)
							willBreak = True
							break
					if willBreak:
						break
		elif self.treesPerColor == 2: # improve the base starting answer for some larger puzzles
			for color in self.colorFrequencies:
				if self.colorFrequencies[color] != 3 or self.blankAnswer.colorsAvailable[color] == 0:
					continue
				for i in range(len(self.board)):
					for j in range(len(self.board)):
						if self.board[i][j] != color:
							continue
						if ( i<len(self.board)-1 and j<len(self.board)-1 ) and ( self.board[i+1][j]==color and self.board[i][j+1]==color ):
							self.blankAnswer.placeTree(i+1, j, color)
							self.blankAnswer.placeTree(i, j+1, color)
							break
						self.blankAnswer.placeTree(i, j, color)
						if i < len(self.board) - 2 and self.board[i+2][j] == color:
							self.blankAnswer.placeTree(i+2, j, color)
						elif j < len(self.board) - 2 and self.board[i][j+2] == color:
							self.blankAnswer.placeTree(i, j+2, color)
						elif ( i<len(self.board)-1 and j>0 ) and self.board[i+1][j-1] == color:
							self.blankAnswer.placeTree(i+1, j-1, color)
						elif ( i<len(self.board)-1 and j<len(self.board)-1 ) and self.board[i+1][j+1] == color:
							self.blankAnswer.placeTree(i+1, j+1, color)
						else:
							print("ERROR: Parks: blankAnswer optimization found potential for optimization, but couldn't find exact position")
						break

	def unsolvedHeuristic(self, partialAnswer):
		thingsUnsolved = len(self.board) * 3 # same number of rows, columns, and colors for square board
		for color in partialAnswer.colorsAvailable:
			if partialAnswer.colorsAvailable[color] == 0:
				thingsUnsolved -= 1
		for i in partialAnswer.rowsAvailable:
			if partialAnswer.rowsAvailable[i] == 0:
				thingsUnsolved -= 1
			if partialAnswer.columnsAvailable[i] == 0:
				thingsUnsolved -= 1
		return thingsUnsolved * len(partialAnswer.placedTrees)

	def colorHeuristic(self, partialAnswer):
		heuristicValue = 0
		if len(partialAnswer.placedTrees) == 0:
			return 0
		for color in self.colorFrequencies:
			heuristicValue += self.colorFrequencies[color] * partialAnswer.colorsAvailable[color]
		return heuristicValue / len(partialAnswer.placedTrees)

	def heuristic(self, partialAnswer):
		return self.unsolvedHeuristic(partialAnswer) # Works better than color heuristic
		# return False

	def getActions(self, partialAnswer):
		availableActions = []
		for i in range(0, len(self.board)):
			for j in range(0, len(self.board[i])):
				if partialAnswer.rowsAvailable[i] == 0 or partialAnswer.columnsAvailable[j] == 0 or partialAnswer.colorsAvailable[self.board[i][j]] == 0:
					continue
				neighborExists = False
				for treeRow, treeColumn in partialAnswer.placedTrees:
					if abs(treeRow - i) <= 1 and abs(treeColumn-j) <= 1:
						neighborExists = True
						break
				if not neighborExists:
					newAction = copy.copy(partialAnswer)
					newAction.placeTree(i, j, self.board[i][j])
					availableActions.append(newAction)
		return availableActions

	def isGoal(self, partialAnswer):
		for color in partialAnswer.colorsAvailable:
			if partialAnswer.colorsAvailable[color] > 0:
				return False
		return True


def main():
	solver = ParkSolver("puzzles/parks/41")
	solver.heuristicSolve()


if __name__ == "__main__":
	main()
