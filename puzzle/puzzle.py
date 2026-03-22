class Puzzle:
    def __init__(self, goal_state):
        self.goal = goal_state

    def get_neighbors(self, state):
        neighbors = []

        # tìm ô trống
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    x, y = i, j

        moves = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

        for nx, ny in moves:
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [list(row) for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(tuple(tuple(r) for r in new_state))

        return neighbors

    def heuristic(self, state):
        # Manhattan Distance
        dist = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val != 0:
                    for x in range(3):
                        for y in range(3):
                            if self.goal[x][y] == val:
                                dist += abs(i-x) + abs(j-y)
        return dist