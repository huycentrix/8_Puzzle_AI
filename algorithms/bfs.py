# algorithms/bfs.py
import time
from collections import deque
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class BFS(BaseSearch):
    """
    Thuật toán Breadth-First Search (BFS).
    Chiến lược: Duyệt theo từng mức độ sâu (level by level) bằng hàng đợi (Queue - FIFO).
    Đảm bảo luôn tìm được đường đi ngắn nhất trong bài toán có chi phí các bước bằng nhau.
    """
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        # Khởi tạo node gốc. BFS quan tâm đến số bước (cost), heuristic có thể bỏ qua.
        start_node = Node(state=self.start_state, cost=0)
        
        # Frontier: Sử dụng deque để tối ưu thao tác popleft() O(1)
        frontier = deque([start_node])
        
        # Explored: Dùng Set để lưu các trạng thái đã sinh ra, tránh trùng lặp
        explored = set([self.start_state])

        while frontier:
            # Lấy node cũ nhất ra khỏi hàng đợi (FIFO)
            current = frontier.popleft()
            
            # Ghi nhận trạng thái đã được khám phá
            result.explored_nodes.append(current.state)

            # Kiểm tra xem trạng thái hiện tại đã là đích chưa
            if current.state == self.goal_state:
                result.steps.append({
                    "current": current.state,
                    "cost": current.g,
                    "action": current.action, # Thêm action để hiển thị Log
                    "frontier": [],
                    "is_goal": True
                })
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            # Duyệt qua các trạng thái láng giềng
            # Sửa đổi: include_actions=True và unpack thêm biến action
            for state, action in self.puzzle.get_neighbors(current.state, include_actions=True):
                if state not in explored:
                    # Đánh dấu đã duyệt ngay khi sinh ra để giảm tải cho Frontier
                    explored.add(state)
                    # Tạo node con với chi phí tăng lên 1 (mỗi bước đi tốn 1 cost)
                    neighbor = Node(state, current, action=action, cost=current.g + 1)
                    frontier.append(neighbor)

            # LƯU DỮ LIỆU TỪNG BƯỚC phục vụ GUI / Video Demo
            result.steps.append({
                "current": current.state,
                "cost": current.g,
                "action": current.action, # Thêm action để hiển thị Log
                # Lưu lại trạng thái của Frontier.
                "frontier": [{"state": node.state, "cost": node.g} for node in frontier],
                "is_goal": False
            })

        result.processing_time = time.time() - start_time
        return result