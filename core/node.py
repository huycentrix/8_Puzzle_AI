class Node:
    def __init__(self, state, parent=None, action=None, cost=0.0, heuristic=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        
        self.g = cost
        self.h = heuristic
        self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)