import time
import copy

class Answer:
	def getAnswer(self):
		pass

	def __copy__(self):
		pass


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
