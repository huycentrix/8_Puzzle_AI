# algorithms/dfs.py
import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class DFS(BaseSearch):
    """
    Thuật toán Depth-First Search (DFS).
    Chiến lược: Đi sâu nhất có thể vào một nhánh trước khi quay lui (Backtracking).
    Sử dụng ngăn xếp (Stack - LIFO). Không đảm bảo tìm được đường đi ngắn nhất.
    """
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        start_node = Node(state=self.start_state, cost=0)
        
        # Frontier: Sử dụng list như một Stack
        frontier = [start_node]
        visited = set()

        while frontier:
            # Lấy node mới nhất vừa được đưa vào (LIFO)
            current = frontier.pop()
            
            # Nếu node này đã được duyệt qua một đường khác nhanh hơn, bỏ qua
            if current.state in visited:
                continue

            # Đánh dấu đã duyệt khi rút ra khỏi stack
            visited.add(current.state)
            result.explored_nodes.append(current.state)

            if current.state == self.goal_state:
                result.steps.append({
                    "current": current.state,
                    "cost": current.g,
                    "frontier": [],
                    "is_goal": True
                })
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            # Sinh các trạng thái láng giềng.
            # Dùng reversed() để khi đẩy vào Stack, các hành động ưu tiên (ví dụ UP, LEFT) 
            # sẽ nằm ở đỉnh Stack và được pop ra trước.
            neighbors = self.puzzle.get_neighbors(current.state)
            for state in reversed(neighbors):
                if state not in visited:
                    neighbor = Node(state, current, cost=current.g + 1)
                    frontier.append(neighbor)

            # LƯU DỮ LIỆU TỪNG BƯỚC phục vụ GUI / Video Demo
            result.steps.append({
                "current": current.state,
                "cost": current.g,
                "frontier": [{"state": node.state, "cost": node.g} for node in frontier],
                "is_goal": False
            })

        result.processing_time = time.time() - start_time
        return result
