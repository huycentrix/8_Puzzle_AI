import time
from collections import deque
from core.search_base import BaseSearch, SearchResult
from core.node import Node


class BidirectionalSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        queue_start = deque()
        queue_goal = deque()
        visited_start = {}
        visited_goal = {}

        start_node = Node(self.start_state, cost=0)
        goal_node = Node(self.goal_state, cost=0)

        queue_start.append(start_node)
        queue_goal.append(goal_node)
        visited_start[self.start_state] = start_node
        visited_goal[self.goal_state] = goal_node

        while queue_start and queue_goal:
            intersection = self.expand_level(queue_start, visited_start, visited_goal, result, "Start")
            if intersection:
                return self.combine_path(intersection, visited_start, visited_goal, result, start_time)

            intersection = self.expand_level(queue_goal, visited_goal, visited_start, result, "Goal")
            if intersection:
                return self.combine_path(intersection, visited_start, visited_goal, result, start_time)

        result.processing_time = time.time() - start_time
        return result

    def expand_level(self, queue, visited_mine, visited_other, result, direction):
        current = queue.popleft()
        result.explored_nodes.append(current.state)
        generated_children = []

        for next_state in self.puzzle.get_neighbors(current.state):
            if next_state not in visited_mine:
                new_node = Node(state=next_state, parent=current, cost=current.g + 1)
                visited_mine[next_state] = new_node
                queue.append(new_node)
                generated_children.append(new_node)

                if next_state in visited_other:
                    self.record_step(
                        result,
                        current,
                        frontier=list(queue),
                        children=generated_children,
                        extra={"direction": direction},
                    )
                    return next_state

        self.record_step(
            result,
            current,
            frontier=list(queue),
            children=generated_children,
            extra={"direction": direction},
        )
        return None

    def combine_path(self, intersection_state, visited_start, visited_goal, result, start_time):
        node_start_side = visited_start[intersection_state]
        path_start, _ = self.extract_path(node_start_side)

        node_goal_side = visited_goal[intersection_state]
        path_goal, _ = self.extract_path(node_goal_side)

        result.path = path_start + path_goal[::-1][1:]
        result.path_cost = len(result.path) - 1
        result.success = True
        result.processing_time = time.time() - start_time
        self.record_step(result, node_start_side, is_goal=True)
        return result
