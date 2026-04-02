import heapq
from itertools import count

from core.node import Node
from core.search_base import BaseSearch, SearchResult


class UniformCostSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        sequence = count()
        start = Node(self.start_state, cost=0)
        frontier = [(start.g, next(sequence), start)]
        best_cost = {self.start_state: 0}

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.g > best_cost.get(current.state, float("inf")):
                continue

            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                self.record_step(result, current, [entry[2] for entry in frontier], [], True)
                self.mark_success(result, current)
                break

            children = []
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                new_cost = current.g + 1
                if new_cost >= best_cost.get(state, float("inf")):
                    continue
                child = Node(state=state, parent=current, action=action, cost=new_cost)
                best_cost[state] = new_cost
                heapq.heappush(frontier, (child.g, next(sequence), child))
                children.append(child)

            self.record_step(result, current, [entry[2] for entry in frontier], children)

        result.finish()
        return result
