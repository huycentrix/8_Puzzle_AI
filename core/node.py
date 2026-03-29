class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = cost
        self.h = heuristic
        self.f = self.g + self.h

    @property
    def depth(self):
        return self.g

    def __lt__(self, other):
        return (self.f, self.h, self.g) < (other.f, other.h, other.g)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)
