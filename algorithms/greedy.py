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
        # Khởi tạo đối tượng lưu trữ kết quả cuối cùng
        result = SearchResult()
        start_time = time.time()

        # Tạo node bắt đầu. 
        # Với Greedy, chi phí thực tế (cost/g) không quan trọng nên thường đặt bằng 0.
        start_node = Node(
            state=self.start_state,
            heuristic=self.puzzle.heuristic(self.start_state)
        )

        # Frontier: Sử dụng Priority Queue  
        # heapq sẽ dựa vào hàm __lt__ trong lớp Node để lấy node có f (hoặc h) nhỏ nhất.
        frontier = []
        heapq.heappush(frontier, start_node)

        # Visited: Tập hợp lưu các trạng thái đã xét để tránh rơi vào vòng lặp vô tận.
        visited = set()

        while frontier:
            # Lấy node "hứa hẹn nhất" (h nhỏ nhất) ra khỏi hàng đợi
            current = heapq.heappop(frontier)

            # Ghi nhận trạng thái này đã được khám phá (phục vụ thống kê/báo cáo)
            result.explored_nodes.append(current.state)
            
            # Kiểm tra xem trạng thái hiện tại đã là đích (Goal) chưa
            if current.state == self.goal_state:
                # Lưu bước cuối cùng vào danh sách các bước thực hiện
                result.steps.append({
                    "current": current.state,
                    "h": current.h,
                    "frontier": [],
                    "is_goal": True
                })
                
                # Trích xuất đường đi từ đích ngược về gốc và lưu kết quả
                result.path, result.path_cost = self.extract_path(current)
                result.success = True
                break

            # Đánh dấu trạng thái hiện tại đã xử lý xong
            visited.add(current.state)

            # Duyệt qua các trạng thái láng giềng (các cách di chuyển ô trống khả thi)
            for state in self.puzzle.get_neighbors(current.state):
                if state not in visited:
                    # Tính toán giá trị ước lượng từ trạng thái này đến đích
                    h = self.puzzle.heuristic(state)
                    # Tạo node mới. Lưu ý: cost=0 vì Greedy không quan tâm độ dài quãng đường đã đi.
                    neighbor = Node(state, current, cost=0, heuristic=h)
                    # Thêm vào hàng đợi ưu tiên để xét ở các bước tiếp theo
                    heapq.heappush(frontier, neighbor)

            # LƯU DỮ LIỆU TỪNG BƯỚC: Phục vụ cho việc hiển thị trên GUI hoặc Video Demo
            result.steps.append({
                "current": current.state,
                "h": current.h,
                # Chụp lại trạng thái của Frontier tại thời điểm này
                "frontier": [{"state": node.state, "h": node.h} for node in frontier],
                "is_goal": False
            })

        # Tính tổng thời gian thực thi thuật toán
        result.processing_time = time.time() - start_time
        return result