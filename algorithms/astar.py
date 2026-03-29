import heapq
from itertools import count

from core.node import Node
from core.search_base import BaseSearch, SearchResult


class AStarSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        sequence = count()
        start = Node(self.start_state, cost=0, heuristic=self.puzzle.heuristic(self.start_state))
        frontier = [(start.f, start.h, next(sequence), start)]
        best_cost = {self.start_state: 0}

        while frontier:
            _, _, _, current = heapq.heappop(frontier)
            if current.g > best_cost.get(current.state, float("inf")):
                continue

            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, [entry[3] for entry in frontier], [], True)
                self.mark_success(result, current)
                break

            children = []
            for state in self.puzzle.get_neighbors(current.state):
                new_cost = current.g + 1
                if new_cost >= best_cost.get(state, float("inf")):
                    continue
                child = Node(
                    state=state,
                    parent=current,
                    cost=new_cost,
                    heuristic=self.puzzle.heuristic(state),
                )
                best_cost[state] = new_cost
                heapq.heappush(frontier, (child.f, child.h, next(sequence), child))
                children.append(child)

            self.record_step(result, current, [entry[3] for entry in frontier], children)

        result.finish()
        return result
