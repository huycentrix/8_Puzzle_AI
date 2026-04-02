from core.node import Node
from core.search_base import BaseSearch, SearchResult


class IDDFSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        limit = 0

        while True:
            found_node, is_cutoff = self.dls(
                Node(self.start_state, cost=0),
                limit,
                {self.start_state},
                result,
                limit,
            )

            if found_node:
                self.mark_success(result, found_node)
                break

            if not is_cutoff:
                break

            limit += 1

        result.finish()
        return result

    def dls(self, node, limit, path, result, current_iteration):
        result.explored_nodes.append(node.state)

        if node.state == self.goal_state:
            self.record_step(
                result,
                node,
                [],
                [],
                True,
                {"limit": limit, "iteration": current_iteration},
            )
            return node, False

        if limit <= 0:
            return None, True

        cutoff_occurred = False
        children = []
        for next_state, action in self.puzzle.get_neighbors(node.state, include_actions=True):
            if next_state in path:
                continue
            children.append(Node(state=next_state, parent=node, action=action, cost=node.g + 1))

        self.record_step(
            result,
            node,
            children,
            children,
            False,
            {"limit": limit, "iteration": current_iteration},
        )

        for child in children:
            path.add(child.state)
            found, shifted_cutoff = self.dls(child, limit - 1, path, result, current_iteration)
            if found:
                return found, False
            if shifted_cutoff:
                cutoff_occurred = True
            path.remove(child.state)

        return None, cutoff_occurred
