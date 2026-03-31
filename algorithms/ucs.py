import heapq
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class UniformCostSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        start_node = Node(
            state=self.start_state,
            parent=None,
            cost=0
        )

        frontier = []
        heapq.heappush(frontier, start_node)
        visited = {}

        while frontier:
            current = heapq.heappop(frontier)
            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                result.steps.append({
                    "current": current.state,
                    "g": current.g,
                    "action": current.action, # Thêm action cho Log
                    "frontier": [],
                    "is_goal": True
                })
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break
                
            if current.state in visited and visited[current.state] < current.g:
                continue

            visited[current.state] = current.g

            # Sửa đổi: include_actions=True và unpack thêm biến action
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                step_cost = 1
                new_g = current.g + step_cost

                if state not in visited or new_g < visited.get(state, float('inf')):
                    neighbor = Node(
                        state=state,
                        parent=current,
                        action=action, # Truyền action vào Node
                        cost=new_g
                    )
                    heapq.heappush(frontier, neighbor)

            result.steps.append({
                "current": current.state,
                "g": current.g,
                "action": current.action, # Thêm action cho Log
                "frontier": [{"state": node.state, "g": node.g} for node in frontier],
                "is_goal": False
            })
        
        result.processing_time = time.time() - start_time
        return result