import heapq
from itertools import count

from core.node import Node
from core.search_base import BaseSearch, SearchResult


class GreedyBestFirstSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        sequence = count()
        start = Node(self.start_state, cost=0, heuristic=self.puzzle.heuristic(self.start_state))
        frontier = [(start.h, next(sequence), start)]
        visited = set()

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.state in visited:
                continue

            visited.add(current.state)
            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, [entry[2] for entry in frontier], [], True)
                self.mark_success(result, current)
                break

            children = []
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                if state in visited:
                    continue
                child = Node(
                    state=state,
                    parent=current,
                    action=action,
                    cost=current.g + 1,
                    heuristic=self.puzzle.heuristic(state),
                )
                heapq.heappush(frontier, (child.h, next(sequence), child))
                children.append(child)

            self.record_step(result, current, [entry[2] for entry in frontier], children)

        result.finish()
        return result
