import time
import threading
from queue import PriorityQueue


class ParkAnswer:
    def __init__(self, board):
        self.rowsAvailable = list(range(0, len(board)))
        self.columnsAvailable = list(range(0, len(board[0])))
        self.colorsAvailable = set()
        self.placedTrees = []
        self.board = board
        for i in self.rowsAvailable:
            for j in self.columnsAvailablej:
                self.colorsAvailable.add(board[i][j])

    def placeTree(self, row, column):
        self.rowsAvailable.remove(row)
        self.columnsAvailable.remove(column)
        self.colorsAvailable.remove(self.board[row][column])
        self.placedTrees.append((row, column))

    def isGoal(self):
        return len(self.colorsAvailable) == 0

    def getAnswer(self):
        return self.placedTrees

    def __copy__(self):
        cpy = type(self)()
        cpy.rowsAvailable = self.rowsAvailable.copy()
        cpy.columnsAvailable = self.columnsAvailable.copy()
        cpy.colorsAvailable = self.colorsAvailable.copy()
        cpy.placedTrees = self.placedTrees.copy()
        cpy.board = self.board
        return cpy


availableActions = PriorityQueue()


def heuristic(action):
    return 0


def getActions(board, partialAnswer):
    for i in partialAnswer[1].rowsAvailable:
        for j in partialAnswer[1].columnsAvailable:
            if board[i][j] in partialAnswer[1].colorsAvailable:
                newAction = partialAnswer[1].copy()
                newAction.placeTree(i, j)
                availableActions.put((heuristic(newAction) + partialAnswer[0] + 1, newAction))


def loadfile(fileName):
    board = []
    with open(fileName, 'r') as file:
        row = file.readline()
        while row:
            board.append(list(row))
            row = file.readline()
    return board


def main():
    start_time = time.time()
    board = loadfile("park1")
    blankAnswer = ParkAnswer(board)
    getActions(blankAnswer)
    # while True:
        


if __name__ == "__main__":
    main()
