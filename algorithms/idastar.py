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
        if node.f > f_limit:
            return None, node.f
    
        if node.state == self.goal_state:
            result.steps.append({
                "current": node.state,
                "g": node.g,
                "h": node.h,
                "f": node.f,
                "f_limit": f_limit,
                "action": node.action, # Thêm action cho Log
                "frontier": [],
                "is_goal": True
            })
            return node, f_limit

        min_limit = float('inf')
        successors = []
        
        # Sửa đổi: include_actions=True và unpack action
        for state, action in self.puzzle.get_neighbors(node.state, include_actions=True):
            h_val = self.puzzle.heuristic(state)
            # Truyền action vào Node
            child_node = Node(state, node, action=action, cost=node.g + 1, heuristic=h_val)
            successors.append(child_node)

        result.steps.append({
            "current": node.state,
            "g": node.g,
            "h": node.h,
            "f": node.f,
            "f_limit": f_limit,
            "action": node.action, # Thêm action cho Log
            "frontier": [{"state": n.state, "g": n.g, "h": n.h, "f": n.f} for n in successors],
            "is_goal": False
        })

        for child in successors:
            if child.state not in path:
                path.add(child.state)
                res, new_limit = self.dfs_contour(child, f_limit, path, result)
                if res is not None:
                    return res, f_limit
                if new_limit < min_limit:
                    min_limit = new_limit
                path.remove(child.state) 

        return None, min_limit