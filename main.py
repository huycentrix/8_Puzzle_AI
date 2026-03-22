from puzzle.puzzle import Puzzle
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.ucs import UniformCostSearch

def main():
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

    print("Select Algorithm:")
    print("1. Breadth-First Search (BFS)")
    print("2. Depth-First Search (DFS)")
    print("3. Uniform Cost Search (UCS)")
    print("4. A* Search")
    print("5. Iterative Deepening Depth-First Search (IDDFS)")
    print("6. Bidirectional Search")
    print("7. Greedy Best-First Search (GBFS)")
    print("8. Iterative Deepening A* (IDA*)")

    while True:
        try:
            choice = input("\nEnter your choice: ").strip()
            if choice in ['1', '2','3','4','5','6','7','8']:
                break
            else:
                print("Invalid input. Please enter from 1 to 8.")
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            return

    puzzle = Puzzle(goal)

    if choice == '1':
        print("1")

    elif choice == '3':
        algo = UniformCostSearch(start, goal, puzzle)
        result = algo.search()

        for i, step in enumerate(result.steps):
            print(f"\n===== Step {i+1} =====")

            print("Current:")
            for row in step["current"]:
                print(row)

            print("g(current) =", step["g"])      

            if step["is_goal"]:
                print("GOAL FOUND!")

            print("\nFrontier:")
            for node in step["frontier"]:
                print("State:")
                for row in node["state"]:
                    print(row)
                print("g =", node["g"])           
                print("------")

        print("\n========== RESULT ==========")
        print("Path found :", result.success)
        print("Path cost  :", result.path_cost)
        print("Total steps:", len(result.path))
        print("Time (s)   :", round(result.processing_time, 6))
        print("\nSolution path:")
        for i, state in enumerate(result.path):
            print(f"  Move {i}:")
            for row in state:
                print("   ", row)

    elif choice == '7':
        print("RUNNING GREEDY BEST-FIRST SEARCH (GBFS)")
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")