import heapq
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class UniformCostSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        # Build the start node
        start_node = Node(
            state=self.start_state,
            parent=None,
            cost=0
        )

        frontier = []
        heapq.heappush(frontier, start_node)

        visited = {}

        while frontier:
            # Always pick the node with the smallest g
            current = heapq.heappop(frontier)
            result.explored_nodes.append(current.state)

            # Goal test
            if current.state == self.goal_state:
                result.steps.append({
                    "current": current.state,
                    "g": current.g,
                    "frontier": [],
                    "is_goal": True
                })
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break
                
            # Lazy-deletion guard
            # Skip any stale copy whose cost is higher than what we've recorded.
            if current.state in visited and visited[current.state] < current.g:
                continue

            # Mark this state as settled at the current (cheapest known) cost
            visited[current.state] = current.g

            # Expand neighbours
            for state in self.puzzle.get_neighbors(current.state):

                step_cost = 1  # every tile move costs 1
                new_g = current.g + step_cost   # total cost to reach child

                # Only push if this path is strictly cheaper than any known path
                if state not in visited or new_g < visited.get(state, float('inf')):
                    neighbor = Node(
                        state=state,
                        parent=current,
                        cost=new_g          # g is the only ordering key
                    )
                    heapq.heappush(frontier, neighbor)

            # Save step snapshot for visualisation
            result.steps.append({
                "current": current.state,
                "g": current.g,
                "frontier": [
                    {"state": node.state, "g": node.g}
                    for node in frontier
                ],
                "is_goal": False
            })
        
        result.processing_time = time.time() - start_time
        return result