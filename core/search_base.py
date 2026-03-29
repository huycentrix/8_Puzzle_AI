from abc import ABC, abstractmethod
from time import perf_counter


class SearchResult:
    def __init__(self):
        self.path = []
        self.explored_nodes = []
        self.path_cost = 0
        self.processing_time = 0.0
        self.success = False
        self.steps = []
        self.frontier_peak = 0
        self.start_time = perf_counter()

    def finish(self):
        self.processing_time = perf_counter() - self.start_time


class BaseSearch(ABC):
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def extract_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path, len(path) - 1

    def serialize_state(self, state):
        return [item for row in state for item in row]

    def node_snapshot(self, node):
        return {
            "state": node.state,
            "flat_state": self.serialize_state(node.state),
            "g": node.g,
            "h": node.h,
            "f": node.f,
            "depth": node.depth,
        }

    def record_step(self, result, current, frontier=None, children=None, is_goal=False, extra=None):
        frontier = list(frontier or [])
        children = list(children or [])
        result.frontier_peak = max(result.frontier_peak, len(frontier))
        step = {
            "current_node": self.node_snapshot(current),
            "parent_state": current.parent.state if current.parent else None,
            "frontier": [self.node_snapshot(node) for node in frontier],
            "children": [self.node_snapshot(node) for node in children],
            "frontier_count": len(frontier),
            "explored_count": len(result.explored_nodes),
            "is_goal": is_goal,
        }
        if extra:
            step.update(extra)
        result.steps.append(step)

    def mark_success(self, result, node):
        result.path, result.path_cost = self.extract_path(node)
        result.success = True

    @abstractmethod
    def search(self):
        raise NotImplementedError
