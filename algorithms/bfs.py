from collections import deque

from core.node import Node
from core.search_base import BaseSearch, SearchResult


class BFS(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        frontier = deque([Node(self.start_state, cost=0)])
        visited = {self.start_state}

        while frontier:
            current = frontier.popleft()
            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, frontier, [], True)
                self.mark_success(result, current)
                break

            children = []
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                if state in visited:
                    continue
                visited.add(state)
                child = Node(state=state, parent=current, action=action, cost=current.g + 1)
                frontier.append(child)
                children.append(child)

            self.record_step(result, current, frontier, children)

        result.finish()
        return result
