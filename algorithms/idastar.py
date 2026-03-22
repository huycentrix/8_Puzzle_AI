import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class IDAStarSearch(BaseSearch):
    """
    Thuật toán IDA* (Iterative Deepening A*).
    Chiến lược: Sử dụng tìm kiếm theo chiều sâu (DFS) giới hạn bởi giá trị f = g + h.
    Nếu không tìm thấy đích trong ngưỡng f_limit hiện tại, ngưỡng sẽ được tăng lên
    bằng giá trị f nhỏ nhất đã bị vượt qua ở lần lặp trước.
    """
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        # Khởi tạo đối tượng lưu trữ kết quả 
        result = SearchResult()
        start_time = time.time()

        # Tạo node gốc từ trạng thái bắt đầu 
        root = Node(
            state=self.start_state,
            cost=0,
            heuristic=self.puzzle.heuristic(self.start_state)
        )

        # Ngưỡng f ban đầu được đặt bằng giá trị f của node gốc
        f_limit = root.f

        while True:
            # Thực hiện DFS giới hạn bởi f_limit. 
            # {root.state} đóng vai trò là 'path' để kiểm tra chu trình trên nhánh hiện tại.
            solution, new_limit = self.dfs_contour(root, f_limit, {root.state}, result)

            # Nếu tìm thấy đích (solution khác None)
            if solution is not None:
                # Trích xuất đường đi và chi phí từ node đích 
                result.path, result.path_cost = self.extract_path(solution)
                result.success = True
                break

            # Nếu new_limit không đổi (vô cùng), nghĩa là đã duyệt hết không gian mà không thấy đích
            if new_limit == float('inf'):
                break

            # Cập nhật ngưỡng f mới: là giá trị f nhỏ nhất vượt ngưỡng cũ ở lần duyệt vừa rồi
            f_limit = new_limit  

        # Ghi nhận thời gian thực thi tổng cộng 
        result.processing_time = time.time() - start_time
        return result

    def dfs_contour(self, node, f_limit, path, result):
        """
        Hàm đệ quy thực hiện tìm kiếm theo chiều sâu giới hạn bởi f_limit.
        Trả về: (node_đích, f_ngưỡng_mới)
        """
        # Nếu f của node hiện tại vượt quá ngưỡng cho phép, dừng nhánh này 
        # và trả về f để làm căn cứ cập nhật f_limit mới 
        if node.f > f_limit:
            return None, node.f
    
        # Kiểm tra trạng thái đích
        if node.state == self.goal_state:
            # Lưu bước cuối cùng vào danh sách steps để hiển thị 
            result.steps.append({
                "current": node.state,
                "g": node.g,
                "h": node.h,
                "f": node.f,
                "f_limit": f_limit,
                "frontier": [],
                "is_goal": True
            })
            return node, f_limit

        # Giá trị nhỏ nhất trong số các node bị vượt ngưỡng ở nhánh này
        min_limit = float('inf')
    
        # Mở rộng các trạng thái kế tiếp (successors)
        successors = []
        for state in self.puzzle.get_neighbors(node.state):
            h_val = self.puzzle.heuristic(state)
            # Tạo node con với chi phí g tăng thêm 1 
            child_node = Node(state, node, cost=node.g + 1, heuristic=h_val)
            successors.append(child_node)

        # Lưu thông tin bước hiện tại phục vụ yêu cầu GUI và so sánh 
        result.steps.append({
            "current": node.state,
            "g": node.g,
            "h": node.h,
            "f": node.f,
            "f_limit": f_limit,
            # Frontier ở đây là danh sách các node con của node hiện tại
            "frontier": [{"state": n.state, "g": n.g, "h": n.h, "f": n.f} for n in successors],
            "is_goal": False
        })

        # Duyệt qua từng node con theo phong cách DFS
        for child in successors:
            # Kiểm tra tránh quay lại trạng thái đã nằm trong đường dẫn hiện tại (chu trình)
            if child.state not in path:
                path.add(child.state) # Đánh dấu đã thăm trên nhánh này
            
                # Gọi đệ quy xuống sâu hơn
                res, new_limit = self.dfs_contour(child, f_limit, path, result)
            
                # Nếu tìm thấy đích ở nhánh con, trả về ngay lập tức
                if res is not None:
                    return res, f_limit
            
                # Cập nhật giá trị ngưỡng nhỏ nhất cho lần lặp IDA* tiếp theo
                if new_limit < min_limit:
                    min_limit = new_limit
            
                # Quay lui (Backtrack): Xóa trạng thái khỏi đường dẫn để các nhánh khác có thể dùng lại
                path.remove(child.state) 

        return None, min_limit