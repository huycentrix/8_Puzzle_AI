from core.node import Node
from core.search_base import BaseSearch, SearchResult


class IDDFSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        depth_limit = 0

        while True:
            found_node, cutoff = self.depth_limited_search(
                Node(self.start_state, cost=0),
                depth_limit,
                {self.start_state},
                result,
                depth_limit,
            )
            if found_node is not None:
                self.mark_success(result, found_node)
                break
            if not cutoff:
                break
            depth_limit += 1

        result.finish()
        return result

    def depth_limited_search(self, node, depth_limit, path_states, result, iteration):
        result.explored_nodes.append(node.state)

        if node.state == self.goal_state:
            self.record_step(result, node, [], [], True, {"limit": depth_limit, "iteration": iteration})
            return node, False

        if depth_limit == 0:
            return None, True

        children = []
        for state in self.puzzle.get_neighbors(node.state):
            if state in path_states:
                continue
            children.append(Node(state=state, parent=node, cost=node.g + 1))

        self.record_step(
            result,
            node,
            children,
            children,
            False,
            {"limit": depth_limit, "iteration": iteration},
        )

        cutoff_occurred = False
        for child in children:
            path_states.add(child.state)
            found_node, cutoff = self.depth_limited_search(child, depth_limit - 1, path_states, result, iteration)
            if found_node is not None:
                return found_node, False
            cutoff_occurred = cutoff_occurred or cutoff
            path_states.remove(child.state)

        return None, cutoff_occurred
