from core.node import Node
from core.search_base import BaseSearch, SearchResult


class DFS(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        frontier = [Node(self.start_state)]
        visited = set()

        while frontier:
            current = frontier.pop()
            if current.state in visited:
                continue

            visited.add(current.state)
            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, frontier, [], True)
                self.mark_success(result, current)
                break

            children = []
            for state in reversed(self.puzzle.get_neighbors(current.state)):
                if state in visited:
                    continue
                child = Node(state=state, parent=current, cost=current.g + 1)
                frontier.append(child)
                children.append(child)

            self.record_step(result, current, frontier, children)

        result.finish()
        return result
