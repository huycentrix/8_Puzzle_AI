import heapq
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class GreedyBestFirstSearch(BaseSearch):
    """
    Thuật toán Greedy Best-First Search (GBFS).
    Chiến lược: Luôn chọn mở rộng trạng thái có giá trị Heuristic h(n) thấp nhất 
    (được ước lượng là gần đích nhất) mà không quan tâm đến chi phí đã đi g(n).
    """
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        start_node = Node(
            state=self.start_state,
            heuristic=self.puzzle.heuristic(self.start_state)
        )

        frontier = []
        heapq.heappush(frontier, start_node)
        visited = set()

        while frontier:
            current = heapq.heappop(frontier)
            result.explored_nodes.append(current.state)
            
            if current.state == self.goal_state:
                result.steps.append({
                    "current": current.state,
                    "h": current.h,
                    "action": current.action, # Thêm action cho Log
                    "frontier": [],
                    "is_goal": True
                })
                
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            visited.add(current.state)

            # Sửa đổi: include_actions=True và unpack thêm biến action
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                if state not in visited:
                    h = self.puzzle.heuristic(state)
                    # Truyền action vào Node
                    neighbor = Node(state, current, action=action, cost=0, heuristic=h)
                    heapq.heappush(frontier, neighbor)

            result.steps.append({
                "current": current.state,
                "h": current.h,
                "action": current.action, # Thêm action cho Log
                "frontier": [{"state": node.state, "h": node.h} for node in frontier],
                "is_goal": False
            })

        result.processing_time = time.time() - start_time
        return result