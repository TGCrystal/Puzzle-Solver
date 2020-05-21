import copy
import heapq
import time

class Answer:
	def getAnswer(self):
		pass

	def __copy__(self):
		pass

	def __lt__(self, other): # Heuristic tiebreaker
		return False


class Solver:
	def loadFile(self, fileName, numInputSplits):
		with open(fileName, 'r') as file:
			rawInput = file.read().split('\n', numInputSplits)
			rawInput[numInputSplits] = rawInput[numInputSplits].split('\n')
		return rawInput

	# uses blankAnswer to generate self.baseAnswer that has required places already filled in
	# should be called at the end of __init__
	def generateBaseAnswer(self, blankAnswer):
		pass

	def getActions(self, partialAnswer):
		pass

	# checks if the given partialAnswer is a final answer
	def isGoal(self, partialAnswer):
		pass

	# returns a number to be used in the priority queue for 
	def heuristic(self, partialAnswer):
		pass

	def depthFirstSolve(self, sortAnswer=False):
		possibleActions = self.getActions(self.baseAnswer) # possibleActions will be a list
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
			if sortAnswer:
				answer.sort()
			print(answer)
			print("Found in {} seconds with {} actions checked".format(endTime-startTime, actionsExpanded))

	def breadthFirstSolve(self, sortAnswer=False):
		possibleActions = self.getActions(self.baseAnswer) # possibleActions will be a list
		answer = None
		actionsExpanded = 0
		startTime = time.time()
		endTime = startTime

		while len(possibleActions) > 0:
			testAnswer = possibleActions.pop(0)
			actionsExpanded += 1
			if self.isGoal(testAnswer):
				answer = testAnswer.getAnswer()
				endTime = time.time()
				break
			possibleActions += self.getActions(testAnswer)

		if answer is None:
			print("No answer found")
		else:
			if sortAnswer:
				answer.sort()
			print(answer)
			print("Found in {} seconds with {} actions checked".format(endTime-startTime, actionsExpanded))

	def heuristicSolve(self, sortAnswer=False):
		possibleActions = self.getActions(self.baseAnswer) # possibleActions will be a list
		answer = None
		actionsExpanded = 0
		startTime = time.time()
		endTime = startTime

		possibleActionHeap = []
		for action in possibleActions:
			actionTuple = (self.heuristic(action), action)
			heapq.heappush(possibleActionHeap, actionTuple)

		while len(possibleActionHeap) > 0:
			testAnswer = heapq.heappop(possibleActionHeap)[1]
			actionsExpanded += 1
			if self.isGoal(testAnswer):
				answer = testAnswer.getAnswer()
				endTime = time.time()
				break
			possibleActions = self.getActions(testAnswer)
			for action in possibleActions:
				actionTuple = (self.heuristic(action), action)
				heapq.heappush(possibleActionHeap, actionTuple)

		if answer is None:
			print("No answer found")
		else:
			if sortAnswer:
				answer.sort()
			print(answer)
			print("Found in {} seconds with {} actions checked".format(endTime-startTime, actionsExpanded))

	def allSolve(self, depth=True, breadth=True, heuristic=True):
		if depth:
			print("Depth First:")
			self.depthFirstSolve(sortAnswer=True)
			print()
		if breadth:
			print("Breadth First:")
			self.breadthFirstSolve(sortAnswer=True)
			print()
		if heuristic:
			print("Heuristic:")
			self.heuristicSolve(sortAnswer=True)
			print()
