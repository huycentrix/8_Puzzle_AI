from core.node import Node
from core.search_base import BaseSearch, SearchResult


class IDAStarSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        root = Node(
            state=self.start_state,
            cost=0,
            heuristic=self.puzzle.heuristic(self.start_state),
        )
        f_limit = root.f
        iteration = 0

        while True:
            solution, new_limit = self.dfs_contour(root, f_limit, {root.state}, result, iteration)

            if solution is not None:
                self.mark_success(result, solution)
                break

            if new_limit == float("inf"):
                break

            f_limit = new_limit
            iteration += 1

        result.finish()
        return result

    def dfs_contour(self, node, f_limit, path, result, iteration):
        if node.f > f_limit:
            return None, node.f

        result.explored_nodes.append(node.state)

        if node.state == self.goal_state:
            self.record_step(
                result,
                node,
                [],
                [],
                True,
                {"f_limit": f_limit, "iteration": iteration},
            )
            return node, f_limit

        min_limit = float("inf")
        children = []
        for state, action in self.puzzle.get_neighbors(node.state, include_actions=True):
            child = Node(
                state=state,
                parent=node,
                action=action,
                cost=node.g + 1,
                heuristic=self.puzzle.heuristic(state),
            )
            children.append(child)

        self.record_step(
            result,
            node,
            children,
            children,
            False,
            {"f_limit": f_limit, "iteration": iteration},
        )

        for child in children:
            if child.state in path:
                continue
            path.add(child.state)
            found, new_limit = self.dfs_contour(child, f_limit, path, result, iteration)
            if found is not None:
                return found, f_limit
            if new_limit < min_limit:
                min_limit = new_limit
            path.remove(child.state)

        return None, min_limit
