import heapq
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node


class AStarSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        start_node = Node(
            state=self.start_state,
            cost=0,
            heuristic=self.puzzle.heuristic(self.start_state),
        )

        frontier = []
        heapq.heappush(frontier, start_node)
        best_g = {self.start_state: 0}

        while frontier:
            current = heapq.heappop(frontier)
            if current.g > best_g.get(current.state, float("inf")):
                continue

            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, is_goal=True)
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            generated_children = []
            for state in self.puzzle.get_neighbors(current.state):
                g_new = current.g + 1
                if g_new < best_g.get(state, float("inf")):
                    best_g[state] = g_new
                    neighbor = Node(
                        state=state,
                        parent=current,
                        cost=g_new,
                        heuristic=self.puzzle.heuristic(state),
                    )
                    heapq.heappush(frontier, neighbor)
                    generated_children.append(neighbor)

            self.record_step(result, current, frontier=list(frontier), children=generated_children)

        result.processing_time = time.time() - start_time
        return result
