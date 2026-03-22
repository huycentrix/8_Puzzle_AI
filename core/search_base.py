from abc import ABC, abstractmethod
import time
from core.node import Node

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

    @abstractmethod
    def search(self):
        pass