import time
import copy


class Answer:
    def getAnswer(self):
        pass

    def __copy__(self):
        pass


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


class Solver:
    def loadFile(self, fileName, numInputSplits):
        with open(fileName, 'r') as file:
            rawInput = file.read().split('\n', numInputSplits)
            rawInput[numInputSplits] = rawInput[numInputSplits].split('\n')
        return rawInput

    def getActions(self, partialAnswer):
        pass

    def isGoal(self, partialAnswer):
        pass

    def depthFirstSolve(self):
        possibleActions = self.getActions(self.blankAnswer) # possibleActions will be a list
        answer = None
        actionsExpanded = 0
        startTime = time.time()
        endTime = startTime

        while len(possibleActions) > 0:
            testAnswer = possibleActions.pop()
            actionsExpanded += 1
            if self.isGoal(testAnswer):
                answer = testAnswer.getAnswer()
                endTime = time.time()
                break
            possibleActions += self.getActions(testAnswer)

        if answer is None:
            print("No answer found")
        else:
            print(answer)
            print("Found in {} seconds with {} actions checked".format(endTime-startTime, actionsExpanded))


class ParkSolver(Solver):
    def __init__(self, fileName):
        self.treesPerColor, self.board = super().loadFile(fileName, 1)
        self.blankAnswer = ParkAnswer(self.treesPerColor, self.board)

    def getActions(self, partialAnswer):
        availableActions = []
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if partialAnswer.rowsAvailable[i] > 0 and partialAnswer.columnsAvailable[j] > 0:
                    if partialAnswer.colorsAvailable[self.board[i][j]] > 0:
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
    solver = ParkSolver("puzzles/parks/1")
    solver.depthFirstSolve()


if __name__ == "__main__":
    main()
