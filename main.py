from puzzle.puzzle import Puzzle
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.idastar import IDAStarSearch

start = (
    (8,6,7),
    (2,5,4),
    (3,0,1)
)

goal = (
    (1,2,3),
    (4,5,6),
    (7,8,0)
)

puzzle = Puzzle(goal)

if not puzzle.is_solvable(start):
    print("Error: Unsolvenable problem!")
else:

    # algo = IDAStarSearch(start, goal, puzzle)
    # result = algo.search()

    # # in step-by-step
    # for i, step in enumerate(result.steps):
    #     print(f"\n===== Step {i+1} =====")

    #     print("Current:")
    #     for row in step["current"]:
    #         print(row)

    #     print(f"g={step['g']}, h={step['h']}, f={step['f']}, f_limit={step['f_limit']}")

    #     if step["is_goal"]:
    #         print("GOAL FOUND!")

    #     print("\nFrontier (successors):")
    #     for node in step["frontier"]:
    #         print("State:")
    #         for row in node["state"]:
    #             print(row)

    #         print(f"g={node['g']}, h={node['h']}, f={node['f']}")

    #         # highlight nếu bị cắt
    #         if node["f"] > step["f_limit"]:
    #             print("CUT OFF (f > f_limit)")

    #         print("------")

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

    print("\nFinal Path:", result.path)
    print("Steps:", len(result.path) - 1)

