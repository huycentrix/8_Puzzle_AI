import heapq
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class GreedyBestFirstSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        start_node = Node(
            state=self.start_state,
            heuristic=self.puzzle.heuristic(self.start_state)
        )

        frontier = []
        heapq.heappush(frontier, start_node)

        visited = set()

        while frontier:
            current = heapq.heappop(frontier)

            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            visited.add(current.state)

            for state in self.puzzle.get_neighbors(current.state):
                if state not in visited:
                    h = self.puzzle.heuristic(state)
                    neighbor = Node(state, current, cost=0, heuristic=h)
                    heapq.heappush(frontier, neighbor)

        result.processing_time = time.time() - start_time
        return result