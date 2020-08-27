import copy
import heapq
import time

class Answer:
    def get_answer(self):
        pass

    def __copy__(self):
        pass

    def __lt__(self, other): # Heuristic tiebreaker
        return False


class Solver:
    def load_file(self, file_name, num_input_splits):
        with open(file_name, 'r') as file:
            raw_data = file.read().split('\n', num_input_splits)
            raw_data[num_input_splits] = raw_data[num_input_splits].split('\n')
        return raw_data

    # uses blank_answer to generate self.base_answer that has required places already filled in
    # should be called at the end of __init__
    def generate_base_answer(self, blank_answer):
        pass

    def get_actions(self, partial_answer):
        pass

    # checks if the given partial_answer is a final answer
    def is_goal(self, partial_answer):
        pass

    # returns a number to be used in the priority queue for ordering
    # return float('inf') to indicate a partial_answer to throw out that shouldn't be used
    def heuristic(self, partial_answer):
        pass

    def depth_first_solve(self, sort_answer=False):
        possible_actions = self.get_actions(self.base_answer) # possible_actions will be a list
        answer = None
        actions_expanded = 0
        start_time = time.time()
        end_time = start_time

        while len(possible_actions) > 0:
            test_answer = possible_actions.pop()
            actions_expanded += 1
            if self.is_goal(test_answer):
                answer = test_answer.get_answer()
                end_time = time.time()
                break
            possible_actions += self.get_actions(test_answer)

        if answer is None:
            print("No answer found")
        else:
            if sort_answer:
                answer.sort()
            print(answer)
            print("Found in {} seconds with {} actions checked".format(end_time-start_time, actions_expanded))

    def breadth_first_solve(self, sort_answer=False):
        possible_actions = self.get_actions(self.base_answer) # possible_actions will be a list
        answer = None
        actions_expanded = 0
        start_time = time.time()
        end_time = start_time

        while len(possible_actions) > 0:
            test_answer = possible_actions.pop(0)
            actions_expanded += 1
            if self.is_goal(test_answer):
                answer = test_answer.get_answer()
                end_time = time.time()
                break
            possible_actions += self.get_actions(test_answer)

        if answer is None:
            print("No answer found")
        else:
            if sort_answer:
                answer.sort()
            print(answer)
            print("Found in {} seconds with {} actions checked".format(end_time-start_time, actions_expanded))

    def heuristic_solve(self, sort_answer=False):
        possible_actions = self.get_actions(self.base_answer) # possible_actions will be a list
        answer = None
        actions_expanded = 0
        start_time = time.time()
        end_time = start_time

        possible_action_heap = []
        for action in possible_actions:
            action_tuple = (self.heuristic(action), action)
            if action_tuple[0] != float('inf'):
                heapq.heappush(possible_action_heap, action_tuple)
        # print()
        # print()

        while len(possible_action_heap) > 0:
            # for answer in possible_action_heap:
            #   print(answer[0], answer[1].placed_trees)
            # if actions_expanded > 25:
            #   return
            test_answer = heapq.heappop(possible_action_heap)[1]
            # print("Chosen Action:", test_answer.placed_trees)
            actions_expanded += 1
            # if len(test_answer.placed_trees) > 10:
            #   print(actions_expanded, len(test_answer.placed_trees), test_answer.placed_trees)
            if self.is_goal(test_answer):
                answer = test_answer.get_answer()
                end_time = time.time()
                break
            possible_actions = self.get_actions(test_answer)
            for action in possible_actions:
                action_tuple = (self.heuristic(action), action)
                if action_tuple[0] != float('inf'):
                    # print(action_tuple[0], action_tuple[1].placed_trees)
                    heapq.heappush(possible_action_heap, action_tuple)
            # print()
            # print()

        if answer is None:
            print("No answer found")
        else:
            if sort_answer:
                answer.sort()
            print(answer)
            print("Found in {} seconds with {} actions checked".format(end_time-start_time, actions_expanded))

    def all_solve(self, depth=True, breadth=True, heuristic=True):
        if depth:
            print("Depth First:")
            self.depth_first_solve(sort_answer=True)
            print()
        if breadth:
            print("Breadth First:")
            self.breadth_first_solve(sort_answer=True)
            print()
        if heuristic:
            print("Heuristic:")
            self.heuristic_solve(sort_answer=True)
            print()
