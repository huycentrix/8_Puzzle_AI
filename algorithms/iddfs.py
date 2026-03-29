import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node


class IDDFSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()
        limit = 0

        while True:
            found_node, is_cutoff = self.dls(Node(self.start_state), limit, {self.start_state}, result, limit)

            if found_node:
                result.path, result.path_cost = self.extract_path(found_node)
                result.success = True
                break

            if not is_cutoff:
                break

            limit += 1

        result.processing_time = time.time() - start_time
        return result

    def dls(self, node, limit, path, result, current_iteration):
        result.explored_nodes.append(node.state)

        if node.state == self.goal_state:
            self.record_step(
                result,
                node,
                is_goal=True,
                extra={"limit": limit, "iteration": current_iteration},
            )
            return node, False

        if limit <= 0:
            return None, True

        cutoff_occurred = False
        successors = []

        for next_state in self.puzzle.get_neighbors(node.state):
            if next_state not in path:
                successors.append(Node(state=next_state, parent=node, cost=node.g + 1))

        self.record_step(
            result,
            node,
            frontier=successors,
            children=successors,
            extra={"limit": limit, "iteration": current_iteration},
        )

        for child in successors:
            path.add(child.state)
            found, shifted_cutoff = self.dls(child, limit - 1, path, result, current_iteration)
            if found:
                return found, False
            if shifted_cutoff:
                cutoff_occurred = True
            path.remove(child.state)

        return None, cutoff_occurred
