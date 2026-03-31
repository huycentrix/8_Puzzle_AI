# algorithms/astar.py
import heapq
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class AStarSearch(BaseSearch):
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        # Calculate heuristic
        h_start = self.puzzle.heuristic(self.start_state)

        # Build the start node
        start_node = Node(
            state=self.start_state,
            cost=0,
            heuristic=h_start
        )

        frontier = []
        heapq.heappush(frontier, start_node)

        # best_g: dict lưu chi phí g(n) tốt nhất đã biết tới mỗi trạng thái.
        best_g = {self.start_state: 0}

        while frontier:
            # Always pick the node with the smallest g
            current = heapq.heappop(frontier)

            # Lazy-deletion guard
            if current.g > best_g.get(current.state, float('inf')):
                continue
            
            # Mark this state
            result.explored_nodes.append(current.state)

            # Goal test
            if current.state == self.goal_state:
                result.steps.append({
                    "current": current.state,
                    "g": current.g,
                    "h": current.h,
                    "f": current.f,
                    "action": current.action, # Thêm action để hiển thị Log
                    "frontier": [],
                    "is_goal": True
                })
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break
            
            # Expand neighbours
            # Sửa đổi: include_actions=True và unpack thêm biến action
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                # g_new: actual cost of reaching neighborly status
                # Cost = 1
                g_new = current.g + 1

                # Better road to state
                if g_new < best_g.get(state, float('inf')):
                    best_g[state] = g_new          # Update best g 
                    h_new = self.puzzle.heuristic(state)
                    neighbor = Node(
                        state=state,
                        parent=current,
                        action=action,             # Lưu hành động vào Node
                        cost=g_new,                # g(neighbor)
                        heuristic=h_new            # h(neighbor)
                    )
                    # f(neighbor) = g_new + h_new 
                    heapq.heappush(frontier, neighbor)

            # Save step snapshot for visualisation
            result.steps.append({
                "current": current.state,
                "g": current.g,
                "h": current.h,
                "f": current.f,
                "action": current.action, # Thêm action để hiển thị Log
                "frontier": [
                    {"state": node.state, "g": node.g, "h": node.h, "f": node.f}
                    for node in frontier
                ],
                "is_goal": False
            })
        
        result.processing_time = time.time() - start_time
        return result