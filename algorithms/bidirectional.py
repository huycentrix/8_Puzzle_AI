from collections import deque

from core.node import Node
from core.search_base import BaseSearch, SearchResult


class BidirectionalSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_queue = deque([Node(self.start_state, cost=0)])
        goal_queue = deque([Node(self.goal_state, cost=0)])
        start_visited = {self.start_state: start_queue[0]}
        goal_visited = {self.goal_state: goal_queue[0]}

        while start_queue and goal_queue:
            meeting_state = self.expand_one_side(start_queue, start_visited, goal_visited, result, "forward")
            if meeting_state is not None:
                self.combine_paths(meeting_state, start_visited, goal_visited, result)
                break

            meeting_state = self.expand_one_side(goal_queue, goal_visited, start_visited, result, "backward")
            if meeting_state is not None:
                self.combine_paths(meeting_state, start_visited, goal_visited, result)
                break

        result.finish()
        return result

    def expand_one_side(self, queue, own_visited, other_visited, result, direction):
        current = queue.popleft()
        result.explored_nodes.append(current.state)

        children = []
        for state in self.puzzle.get_neighbors(current.state):
            if state in own_visited:
                continue
            child = Node(state=state, parent=current, cost=current.g + 1)
            own_visited[state] = child
            queue.append(child)
            children.append(child)
            if state in other_visited:
                self.record_step(result, current, queue, children, False, {"direction": direction})
                return state

        self.record_step(result, current, queue, children, False, {"direction": direction})
        return None

    def combine_paths(self, meeting_state, start_visited, goal_visited, result):
        start_path, _ = self.extract_path(start_visited[meeting_state])
        goal_path, _ = self.extract_path(goal_visited[meeting_state])
        result.path = start_path + list(reversed(goal_path[:-1]))
        result.path_cost = len(result.path) - 1
        result.success = True
        self.record_step(result, start_visited[meeting_state], [], [], True, {"direction": "meeting"})
