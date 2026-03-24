from puzzle.puzzle import Puzzle
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.idastar import IDAStarSearch
from algorithms.ucs import UniformCostSearch
from algorithms.astar import AStarSearch
from algorithms.iddfs import IDDFSearch
from algorithms.bidirectional import BidirectionalSearch

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
        print("RUNNING UCS")
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
    elif choice == '4':
        print("RUNNING A* SEARCH")
        algo = AStarSearch(start, goal, puzzle)
        result = algo.search()

        for i, step in enumerate(result.steps):
            print(f"\n===== Step {i+1} =====")

            print("Current:")
            for row in step["current"]:
                print(row)

            print(f"g(n) = {step['g']},  h(n) = {step['h']},  f(n) = {step['f']}")

            if step["is_goal"]:
                print("GOAL FOUND!")

            print("\nFrontier:")
            for node in step["frontier"]:
                print("State:")
                for row in node["state"]:
                    print(row)
                print(f"g = {node['g']},  h = {node['h']},  f = {node['f']}")
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
    
    elif choice == '5':
        print("RUNNING IDDFS (Iterative Deepening Depth-First Search)")
        algo = IDDFSearch(start, goal, puzzle)
        result = algo.search()

        current_iter = -1 #bien theo doi vong lap hien tai
        step_in_iter = 0  #bien step rieng cho moi iteration

        for i, step in enumerate(result.steps):
            #kiem tra xem co thuoc iteration moi khong
            if step["iteration"] != current_iter:
                current_iter = step["iteration"]
                print(f"\n" + "="*40)
                print(f"   STARTING ITERATION WITH LIMIT: {current_iter}")
                print("="*40)
            else:
                step_in_iter += 1 

            print(f"\n>> Iteration {current_iter} - Step {step_in_iter}:")
            print("Current State:")
            for row in step["current"]:
                print(row)
            print(f"Depth remaining: {step['limit']}")

            if step["is_goal"]:
                print("GOAL FOUND!")

            #in frontier neu khong phai node la cua limit
            if step["frontier"]:
                print("\nFrontier (Successors):")
                for node in step["frontier"]:
                    print(f"  {node['state']}")
                print("------")

        print("\n========== RESULT ==========")
        print("Path found :", result.success)
        print("Path cost  :", result.path_cost)
        print("Total nodes explored:", len(result.explored_nodes))
        print("Time (s)   :", round(result.processing_time, 6))
        
        if result.success:
            print("\nSolution path:")
            for i, state in enumerate(result.path):
                print(f"  Step {i}:")
                for row in state:
                    print("   ", row)

    elif choice == '6':
        print("RUNNING BIDIRECTIONAL SEARCH (Start <-> Goal)")
        algo = BidirectionalSearch(start, goal, puzzle)
        result = algo.search()

        #in dien bien tim kiem, gioi han 20
        for i, step in enumerate(result.steps[:20]): 
            print(f"\n===== Step {i+1} =====")
            print(f"Direction: {step.get('direction', 'Intersection')}") 
            print("Current State:")
            for row in step["current"]:
                print(row)
            
            if step.get("is_goal"):
                print("INTERSECTION FOUND!") 

        if len(result.steps) > 20:
            print(f"\n... and {len(result.steps) - 20} more steps ...")

        #ket qua
        print("\n" + "="*20 + " RESULT " + "="*20)
        print(f"Path found      : {result.success}") 
        print(f"Total path cost : {result.path_cost} steps") 
        print(f"Nodes explored  : {len(result.explored_nodes)}") 
        print(f"Execution time  : {round(result.processing_time, 6)} (s)") 
        
        if result.success:
            print("\nFull Solution Path (Start -> Intersection -> Goal):") 
            for i, state in enumerate(result.path):
                print(f"  Step {i}:")
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
        print("Steps:", len(result.path) - 1)

    elif choice == '8':
        algo = IDAStarSearch(start, goal, puzzle)
        result = algo.search()

        # in step-by-step
        for i, step in enumerate(result.steps):
            print(f"\n===== Step {i+1} =====")

            print("Current:")
            for row in step["current"]:
                print(row)

            print(f"g={step['g']}, h={step['h']}, f={step['f']}, f_limit={step['f_limit']}")

            if step["is_goal"]:
                print("GOAL FOUND!")

            print("\nFrontier (successors):")
            for node in step["frontier"]:
                print("State:")
                for row in node["state"]:
                    print(row)

                print(f"g={node['g']}, h={node['h']}, f={node['f']}")

                # highlight nếu bị cắt
                if node["f"] > step["f_limit"]:
                    print("CUT OFF (f > f_limit)")

                print("------")
        print("\nFinal Path:", result.path)
        print("Steps:", len(result.path) - 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")