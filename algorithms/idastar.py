from core.node import Node
from core.search_base import BaseSearch, SearchResult


class IDAStarSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        root = Node(self.start_state, cost=0, heuristic=self.puzzle.heuristic(self.start_state))
        threshold = root.f

        while True:
            found_node, next_threshold = self.search_contour(root, threshold, {root.state}, result)
            if found_node is not None:
                self.mark_success(result, found_node)
                break
            if next_threshold == float("inf"):
                break
            threshold = next_threshold

        result.finish()
        return result

    def search_contour(self, node, threshold, path_states, result):
        if node.f > threshold:
            return None, node.f

        result.explored_nodes.append(node.state)

        if node.state == self.goal_state:
            self.record_step(result, node, [], [], True, {"f_limit": threshold})
            return node, threshold

        minimum_exceeded = float("inf")
        children = []
        for state in self.puzzle.get_neighbors(node.state):
            if state in path_states:
                continue
            children.append(
                Node(
                    state=state,
                    parent=node,
                    cost=node.g + 1,
                    heuristic=self.puzzle.heuristic(state),
                )
            )

        self.record_step(result, node, children, children, False, {"f_limit": threshold})

        for child in children:
            path_states.add(child.state)
            found_node, next_threshold = self.search_contour(child, threshold, path_states, result)
            if found_node is not None:
                return found_node, threshold
            minimum_exceeded = min(minimum_exceeded, next_threshold)
            path_states.remove(child.state)

        return None, minimum_exceeded
