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

for i, step in enumerate(result.steps):
    print(f"\n===== Step {i+1} =====")

    print("Current:")
    for row in step["current"]:
        print(row)

    print("h(current) =", step["h"])

    if step["is_goal"]:
        print("GOAL FOUND!")

    print("\nFrontier:")
    for node in step["frontier"]:
        print("State:")
        for row in node["state"]:
            print(row)
        print("h =", node["h"])
        print("------")

print("Path:", result.path)
print("Steps:", len(result.path))