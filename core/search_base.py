from abc import ABC, abstractmethod
import time
from core.node import Node

class SearchResult:
    """
    Lớp lưu trữ kết quả sau khi thực hiện thuật toán tìm kiếm.
    """
    def __init__(self):
        # Danh sách các trạng thái tạo thành đường đi từ Start đến Goal [cite: 118]
        self.path = []
        
        # Danh sách tất cả các trạng thái đã bị lấy ra khỏi Frontier (đã duyệt) [cite: 118]
        self.explored_nodes = []
        
        # Tổng chi phí đường đi (trong 8-puzzle thường là số bước di chuyển) [cite: 118]
        self.path_cost = 0.0
        
        # Thời gian thực thi thuật toán (tính bằng giây) [cite: 118]
        self.processing_time = 0.0
        
        # Trạng thái tìm kiếm thành công hay thất bại [cite: 118]
        self.success = False
        
        # Lưu trữ chi tiết từng bước (current node, frontier,...) để minh họa thuật toán [cite: 118]
        self.steps = []


class BaseSearch(ABC):
    """
    Lớp cơ sở trừu tượng (Abstract Base Class) cho tất cả các thuật toán tìm kiếm.
    """
    def __init__(self, start_state, goal_state):
        # Trạng thái bắt đầu của bài toán 
        self.start_state = start_state
        
        # Trạng thái đích cần đạt tới 
        self.goal_state = goal_state

    def extract_path(self, node):
        """
        Truy vết ngược từ node đích về node cha để lấy toàn bộ lộ trình.
        """
        path = []
        # Lưu lại chi phí thực tế g(n) tại node cuối cùng 
        cost = node.g 
        
        # Di chuyển ngược từ đích về gốc dựa trên tham chiếu 'parent'
        while node:
            path.append(node.state)
            node = node.parent
            
        # Đảo ngược danh sách để có thứ tự từ Start -> Goal 
        return path[::-1], cost

    @abstractmethod
    def search(self):
        """
        Phương thức trừu tượng buộc các lớp con (BFS, DFS, A*,...) phải tự định nghĩa 
        logic tìm kiếm riêng. 
        """
        pass