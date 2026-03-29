import time
from collections import deque
from core.search_base import BaseSearch, SearchResult
from core.node import Node


class BFS(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        start_node = Node(state=self.start_state, cost=0)
        frontier = deque([start_node])
        explored = {self.start_state}

        while frontier:
            current = frontier.popleft()
            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, is_goal=True, extra={"cost": current.g})
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            generated_children = []
            for state in self.puzzle.get_neighbors(current.state):
                if state not in explored:
                    explored.add(state)
                    neighbor = Node(state, current, cost=current.g + 1)
                    frontier.append(neighbor)
                    generated_children.append(neighbor)

            self.record_step(
                result,
                current,
                frontier=list(frontier),
                children=generated_children,
                extra={"cost": current.g},
            )

        result.processing_time = time.time() - start_time
        return result
