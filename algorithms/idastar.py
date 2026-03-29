import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node


class IDAStarSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        root = Node(
            state=self.start_state,
            cost=0,
            heuristic=self.puzzle.heuristic(self.start_state),
        )
        f_limit = root.f

        while True:
            solution, new_limit = self.dfs_contour(root, f_limit, {root.state}, result)

            if solution is not None:
                result.path, result.path_cost = self.extract_path(solution)
                result.success = True
                break

            if new_limit == float("inf"):
                break

            f_limit = new_limit

        result.processing_time = time.time() - start_time
        return result

    def dfs_contour(self, node, f_limit, path, result):
        if node.f > f_limit:
            return None, node.f

        if node.state == self.goal_state:
            self.record_step(result, node, is_goal=True, extra={"f_limit": f_limit})
            return node, f_limit

        min_limit = float("inf")
        successors = []

        for state in self.puzzle.get_neighbors(node.state):
            successors.append(
                Node(
                    state=state,
                    parent=node,
                    cost=node.g + 1,
                    heuristic=self.puzzle.heuristic(state),
                )
            )

        self.record_step(result, node, frontier=successors, children=successors, extra={"f_limit": f_limit})

        for child in successors:
            if child.state not in path:
                path.add(child.state)
                res, new_limit = self.dfs_contour(child, f_limit, path, result)
                if res is not None:
                    return res, f_limit
                if new_limit < min_limit:
                    min_limit = new_limit
                path.remove(child.state)

        return None, min_limit
