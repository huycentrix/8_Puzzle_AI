from collections import deque

from core.node import Node
from core.search_base import BaseSearch, SearchResult


class BidirectionalSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        queue_start = deque([Node(self.start_state, cost=0)])
        queue_goal = deque([Node(self.goal_state, cost=0)])
        visited_start = {self.start_state: queue_start[0]}
        visited_goal = {self.goal_state: queue_goal[0]}

        while queue_start and queue_goal:
            intersection = self.expand_level(queue_start, visited_start, visited_goal, result, "Start ->")
            if intersection:
                self.combine_path(intersection, visited_start, visited_goal, result)
                break

            intersection = self.expand_level(queue_goal, visited_goal, visited_start, result, "<- Goal")
            if intersection:
                self.combine_path(intersection, visited_start, visited_goal, result)
                break

        result.finish()
        return result

    def expand_level(self, queue, visited_mine, visited_other, result, direction):
        current = queue.popleft()
        result.explored_nodes.append(current.state)

        children = []
        for next_state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
            if next_state in visited_mine:
                continue
            child = Node(state=next_state, parent=current, action=action, cost=current.g + 1)
            visited_mine[next_state] = child
            queue.append(child)
            children.append(child)
            if next_state in visited_other:
                self.record_step(result, current, queue, children, False, {"direction": direction})
                return next_state

        self.record_step(result, current, queue, children, False, {"direction": direction})
        return None

    # def combine_path(self, intersection_state, visited_start, visited_goal, result):
    #     node_start = visited_start[intersection_state]
    #     path_start, _ = self.extract_path(node_start)

    #     node_goal = visited_goal[intersection_state]
    #     path_goal, _ = self.extract_path(node_goal)

    #     result.path = path_start + path_goal[::-1][1:]
    #     result.path_cost = len(result.path) - 1
    #     result.success = True
    def combine_path(self, intersection_state, visited_start, visited_goal, result):
        node_start = visited_start[intersection_state]
        node_goal = visited_goal[intersection_state]

        prev = node_start

        current = node_goal.parent

        while current:
            new_node = Node(
                state=current.state,
                parent=prev,
                action=current.action,
                cost=prev.g + 1
            )
            prev = new_node
            current = current.parent

        self.mark_success(result, prev)