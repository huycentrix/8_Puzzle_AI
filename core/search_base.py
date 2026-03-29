from abc import ABC, abstractmethod
import time


class SearchResult:
    def __init__(self):
        self.path = []
        self.explored_nodes = []
        self.path_cost = 0.0
        self.processing_time = 0.0
        self.success = False
        self.steps = []


class BaseSearch(ABC):
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def extract_path(self, node):
        path = []
        cost = node.g

        while node:
            path.append(node.state)
            node = node.parent

        return path[::-1], cost

    def serialize_state(self, state):
        return [item for row in state for item in row]

    def node_snapshot(self, node):
        return {
            "state": node.state,
            "flat_state": self.serialize_state(node.state),
            "g": getattr(node, "g", 0),
            "h": getattr(node, "h", 0),
            "f": getattr(node, "f", getattr(node, "g", 0) + getattr(node, "h", 0)),
        }

    def record_step(self, result, current, frontier=None, children=None, is_goal=False, extra=None):
        step = {
            "current_node": self.node_snapshot(current),
            "parent_state": current.parent.state if current.parent else None,
            "frontier": [self.node_snapshot(node) for node in (frontier or [])],
            "children": [self.node_snapshot(node) for node in (children or [])],
            "is_goal": is_goal,
        }
        if extra:
            step.update(extra)
        result.steps.append(step)

    @abstractmethod
    def search(self):
        pass
