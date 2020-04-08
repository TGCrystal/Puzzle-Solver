import time
import threading
from queue import PriorityQueue
import copy


availableActions = PriorityQueue()


class ParkAnswer:
    def __init__(self, board):
        self.rowsAvailable = list(range(0, len(board)))
        self.columnsAvailable = list(range(0, len(board[0])-1)) #-1 to account for \n character
        self.colorsAvailable = set()
        self.placedTrees = []
        self.board = board
        # print(self.rowsAvailable, self.columnsAvailable)
        for i in self.rowsAvailable:
            for j in self.columnsAvailable:
                # print(i, j)
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
        cpy = type(self)(self.board)
        cpy.rowsAvailable = self.rowsAvailable.copy()
        cpy.columnsAvailable = self.columnsAvailable.copy()
        cpy.colorsAvailable = self.colorsAvailable.copy()
        cpy.placedTrees = self.placedTrees.copy()
        cpy.board = self.board
        return cpy

    def __lt__(self, other):
        return True

def heuristic(action):
    return 0


def getActions(partialAnswer):
    for i in partialAnswer[1].rowsAvailable:
        for j in partialAnswer[1].columnsAvailable:
            if partialAnswer[1].board[i][j] in partialAnswer[1].colorsAvailable:
                newAction = copy.copy(partialAnswer[1])
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
    startTime = time.time()
    board = loadfile("park1")
    blankAnswer = ParkAnswer(board)
    threading.Thread(target=getActions, args=((0, blankAnswer),)).start()
    actionsExpanded = 1
    answer = None
    while True:
        testAnswer = availableActions.get()
        actionsExpanded += 1
        if testAnswer[1].isGoal():
            answer = testAnswer[1].getAnswer()
            break
        threading.Thread(target=getActions, args=(testAnswer,)).start()
    print(actionsExpanded, time.time()-startTime)
    print(answer)


if __name__ == "__main__":
    main()
