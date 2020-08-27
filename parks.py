import copy
from base import Answer, Solver


class ParkAnswer(Answer):
    def __init__(self, trees_per_color=1, board=None):
        if board is None: #used for copy function
            return
        self.placed_trees = []

        self.rows_available = []
        self.columns_available = []
        for _ in board: # Boards are square so no need for second loop
            self.rows_available.append(trees_per_color)
            self.columns_available.append(trees_per_color)

        self.colors_available = dict()
        for row in board:
            for item in row:
                self.colors_available[item] = trees_per_color

    def place_tree(self, row, column, color):
        self.rows_available[row] -= 1
        self.columns_available[column] -= 1
        self.colors_available[color] -= 1
        self.placed_trees.append((row, column))

    def get_answer(self):
        return self.placed_trees

    def __copy__(self):
        cpy = type(self)()
        cpy.rows_available = self.rows_available.copy()
        cpy.columns_available = self.columns_available.copy()
        cpy.colors_available = self.colors_available.copy()
        cpy.placed_trees = self.placed_trees.copy()
        return cpy


class ParkSolver(Solver):
    def __init__(self, fileName):
        self.trees_per_color, self.board = super().load_file(fileName, 1)
        self.trees_per_color = int(self.trees_per_color)
        blank_answer = ParkAnswer(self.trees_per_color, self.board)
        self.color_frequencies = dict()
        for row in self.board:
            for color in row:
                if color in self.color_frequencies:
                    self.color_frequencies[color] += 1
                else:
                    self.color_frequencies[color] = 1
        self.generate_base_answer(blank_answer)
        self.always_invalid_placements = set()
        color_frequencies_modified = copy.copy(self.color_frequencies)
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                neighbor_colors = dict()
                for i in range(row-1, row+2):
                    if i < 0 or i >= len(self.board):
                        continue
                    for j in range(column-1, column+2):
                        if j < 0 or j >= len(self.board[i]):
                            continue
                        if i == row and j == column:
                            continue
                        color = self.board[i][j]
                        if color in neighbor_colors:
                            neighbor_colors[color] += 1
                        else:
                            neighbor_colors[color] = 1
                for color in neighbor_colors:
                    if self.color_frequencies[color] - neighbor_colors[color] < self.trees_per_color:
                        # print(color_frequencies_modified[color], neighbor_colors[color], self.trees_per_color)
                        # print(row, column, color)
                        # print()
                        if (row, column) not in self.always_invalid_placements:
                            self.always_invalid_placements.add((row, column))
                            color_frequencies_modified[self.board[row][column]] -= 1
        self.color_frequencies = color_frequencies_modified
        # print(self.color_frequencies)


    def generate_base_answer(self, blank_answer):
        if self.trees_per_color == 1:
            for color in self.color_frequencies:
                if self.color_frequencies[color] != 1:
                    continue
                will_break = False
                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if self.board[i][j] == color:
                            blank_answer.place_tree(i, j, color)
                            will_break = True
                            break
                    if will_break:
                        break
        elif self.trees_per_color == 2: # improve the base starting answer for some larger puzzles
            for color in self.color_frequencies:
                if self.color_frequencies[color] != 3 or blank_answer.colors_available[color] == 0:
                    continue
                for i in range(len(self.board)):
                    for j in range(len(self.board)):
                        if self.board[i][j] != color:
                            continue
                        if (i < len(self.board)-1 and j < len(self.board)-1) and (self.board[i+1][j] == color and self.board[i][j+1] == color):
                            blank_answer.place_tree(i+1, j, color)
                            blank_answer.place_tree(i, j+1, color)
                            break
                        blank_answer.place_tree(i, j, color)
                        if i < len(self.board) - 2 and self.board[i+2][j] == color:
                            blank_answer.place_tree(i+2, j, color)
                        elif j < len(self.board) - 2 and self.board[i][j+2] == color:
                            blank_answer.place_tree(i, j+2, color)
                        elif (i < len(self.board)-1 and j > 0) and self.board[i+1][j-1] == color:
                            blank_answer.place_tree(i+1, j-1, color)
                        elif (i < len(self.board)-1 and j < len(self.board)-1) and self.board[i+1][j+1] == color:
                            blank_answer.place_tree(i+1, j+1, color)
                        else:
                            print("ERROR: Parks: blank_answer optimization found potential for optimization, but couldn't find exact position")
                        break
        self.base_answer = blank_answer

    def unsolved_heuristic(self, partial_answer):
        things_unsolved = len(self.board) * 3 # same number of rows, columns, and colors for square board
        for color in partial_answer.colors_available:
            if partial_answer.colors_available[color] == 0:
                things_unsolved -= 1
        for i in range(len(self.board)):
            if partial_answer.rows_available[i] == 0:
                things_unsolved -= 1
            if partial_answer.columns_available[i] == 0:
                things_unsolved -= 1
        return things_unsolved * len(partial_answer.placed_trees)

    def color_heuristic(self, partial_answer):
        heuristic_value = 0
        if len(partial_answer.placed_trees) == 0:
            return 0
        for color in self.color_frequencies:
            heuristic_value += self.color_frequencies[color] * partial_answer.colors_available[color]
        return heuristic_value / len(partial_answer.placed_trees)

    def recent_heuristic(self, partial_answer):
        most_recent_row, most_recent_column = partial_answer.placed_trees[-1]
        # most_recent_color = self.board[most_recent_row][most_recent_column]
        new_color_freq = copy.copy(self.color_frequencies)
        invalid_placements = copy.copy(self.always_invalid_placements)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if partial_answer.rows_available[i] == 0 or partial_answer.columns_available[j] == 0:
                    if (i, j) not in invalid_placements:
                        invalid_placements.add((i, j))
                        new_color_freq[self.board[i][j]] -= 1
        for tree in partial_answer.placed_trees:
            for i in range(tree[0]-1, tree[0]+2):
                if i < 0 or i >= len(self.board):
                    continue
                for j in range(tree[1]-1, tree[1]+2):
                    if j < 0 or j >= len(self.board[i]):
                        continue
                    if (i, j) not in invalid_placements:
                        invalid_placements.add((i, j))
                        new_color_freq[self.board[i][j]] -= 1

        for color in new_color_freq:
            if new_color_freq[color] < partial_answer.colors_available[color]:
                return float('inf')

        return -1 * (new_color_freq[color] + len(partial_answer.placed_trees) * len(self.board) * len(self.board))

    def heuristic(self, partial_answer):
        # return self.unsolved_heuristic(partial_answer) # Works better than color heuristic
        return self.recent_heuristic(partial_answer)
        # return False

    # Used in conjunction with getActions to ensure the only returned answers use the most likely guesses
    def get_minimal_colors(self, partial_answer):
        new_color_freq = copy.copy(self.color_frequencies) # Check that most recent was placed correctly
        invalid_placements = copy.copy(self.always_invalid_placements)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if partial_answer.rows_available[i] == 0 or partial_answer.columns_available[j] == 0:
                    if (i, j) not in invalid_placements:
                        invalid_placements.add((i, j))
                        new_color_freq[self.board[i][j]] -= 1
        for tree in partial_answer.placed_trees:
            for i in range(tree[0]-1, tree[0]+2):
                if i < 0 or i >= len(self.board):
                    continue
                for j in range(tree[1]-1, tree[1]+2):
                    if j < 0 or j >= len(self.board[i]):
                        continue
                    if (i, j) not in invalid_placements:
                        invalid_placements.add((i, j))
                        new_color_freq[self.board[i][j]] -= 1
        minimal_colors = []
        minimal_color_frequency = len(self.board) * len(self.board) + 1
        for color in new_color_freq:
            if partial_answer.colors_available[color] == 0:
                continue
            if new_color_freq[color] < minimal_color_frequency:
                minimal_colors = [color]
                minimal_color_frequency = new_color_freq[color]
            elif new_color_freq[color] == minimal_color_frequency:
                minimal_colors.append(color)
        return minimal_colors

    def get_actions(self, partial_answer):
        minimal_colors = self.get_minimal_colors(partial_answer)
        # print(minimal_colors)
        available_actions = []
        for i in range(len(self.board)):
            if partial_answer.rows_available[i] == 0:
                continue
            for j in range(len(self.board[i])):
                if partial_answer.columns_available[j] == 0 or partial_answer.colors_available[self.board[i][j]] == 0:
                    continue
                if self.board[i][j] not in minimal_colors:
                    continue
                neighbor_exists = False
                for tree_row, tree_column in partial_answer.placed_trees:
                    if abs(tree_row - i) <= 1 and abs(tree_column-j) <= 1:
                        neighbor_exists = True
                        break
                if not neighbor_exists:
                    new_action = copy.copy(partial_answer)
                    new_action.place_tree(i, j, self.board[i][j])
                    if self.recent_heuristic(new_action) != float('inf'):
                        available_actions.append(new_action)
        return available_actions

    def is_goal(self, partial_answer):
        for color in partial_answer.colors_available:
            if partial_answer.colors_available[color] > 0:
                return False
        return True


def main():
    solver = ParkSolver("puzzles/parks/1")
    solver.all_solve()
    # solver.all_solve(breadth=False, heuristic=False)


if __name__ == "__main__":
    main()
