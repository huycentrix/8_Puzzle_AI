from puzzle.puzzle import Puzzle
from algorithms.greedy import GreedyBestFirstSearch

start = (
    (1,2,3),
    (4,0,6),
    (7,5,8)
)

goal = (
    (1,2,3),
    (4,5,6),
    (7,8,0)
)

puzzle = Puzzle(goal)

algo = GreedyBestFirstSearch(start, goal, puzzle)
result = algo.search()

print("Path:", result.path)
print("Steps:", len(result.path))