import math
import random


class Puzzle:
    def __init__(self, goal_state, heuristic_name="Manhattan Distance"):
        self.goal = goal_state
        self.heuristic_name = heuristic_name
        self.goal_positions = {}
        for row in range(3):
            for col in range(3):
                self.goal_positions[self.goal[row][col]] = (row, col)

    def get_neighbors(self, state):
        zero_row = zero_col = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] == 0:
                    zero_row, zero_col = row, col
                    break

        neighbors = []
        for next_row, next_col in (
            (zero_row - 1, zero_col),
            (zero_row + 1, zero_col),
            (zero_row, zero_col - 1),
            (zero_row, zero_col + 1),
        ):
            if 0 <= next_row < 3 and 0 <= next_col < 3:
                board = [list(r) for r in state]
                board[zero_row][zero_col], board[next_row][next_col] = board[next_row][next_col], board[zero_row][zero_col]
                neighbors.append(tuple(tuple(r) for r in board))
        return neighbors

    def heuristic(self, state):
        if self.heuristic_name == "Misplaced Tiles":
            return self.misplaced_tiles(state)
        if self.heuristic_name == "Euclidean Distance":
            return self.euclidean_distance(state)
        return self.manhattan_distance(state)

    def manhattan_distance(self, state):
        distance = 0
        for row in range(3):
            for col in range(3):
                value = state[row][col]
                if value == 0:
                    continue
                goal_row, goal_col = self.goal_positions[value]
                distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def misplaced_tiles(self, state):
        count = 0
        for row in range(3):
            for col in range(3):
                value = state[row][col]
                if value != 0 and value != self.goal[row][col]:
                    count += 1
        return count

    def euclidean_distance(self, state):
        distance = 0.0
        for row in range(3):
            for col in range(3):
                value = state[row][col]
                if value == 0:
                    continue
                goal_row, goal_col = self.goal_positions[value]
                distance += math.hypot(row - goal_row, col - goal_col)
        return distance

    def is_solvable(self, state):
        flat = [item for row in state for item in row if item != 0]
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions % 2 == 0

    def randomize(self, start_state=None, moves=40):
        state = start_state or self.goal
        current = state
        previous = None
        for _ in range(max(1, moves)):
            neighbors = self.get_neighbors(current)
            if previous in neighbors and len(neighbors) > 1:
                neighbors = [candidate for candidate in neighbors if candidate != previous]
            previous = current
            current = random.choice(neighbors)
        return current
