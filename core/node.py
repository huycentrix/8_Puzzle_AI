class Node:
    """
    Lớp Node: Đại diện cho một nút trong cây tìm kiếm.
    Lưu trữ trạng thái hiện tại, mối quan hệ với node cha và các chỉ số chi phí.
    """
    def __init__(self, state, parent=None, action=None, cost=0.0, heuristic=0.0):
        # Trạng thái hiện tại của trò chơi (ma trận 3x3 dạng tuple) [cite: 117]
        self.state = state
        
        # Node cha dẫn đến node này (dùng để truy vết lại đường đi khi tìm thấy đích) [cite: 116]
        self.parent = parent
        
        # Hành động di chuyển ô trống để đạt đến trạng thái này (ví dụ: 'UP', 'DOWN') [cite: 116]
        self.action = action
        
        # g(n): Chi phí thực tế từ trạng thái bắt đầu đến node hiện tại [cite: 117]
        self.g = cost
        
        # h(n): Giá trị Heuristic (ước lượng chi phí từ node hiện tại đến đích) [cite: 117]
        self.h = heuristic
        
        # f(n) = g(n) + h(n): Tổng chi phí ước tính (ưu tiên hàng đầu trong A* và IDA*) [cite: 117]
        self.f = self.g + self.h

    def __lt__(self, other):
        """
        Định nghĩa phép so sánh "nhỏ hơn" (<) giữa hai node.
        Giúp Priority Queue (heapq) tự động sắp xếp và lấy ra node có f thấp nhất. 
        """
        return self.f < other.f

    def __eq__(self, other):
        """
        Định nghĩa phép so sánh bằng (==).
        Hai node được coi là trùng nhau nếu chúng có cùng trạng thái (state). 
        """
        return self.state == other.state

    def __hash__(self):
        """
        Hàm băm giúp lưu trữ node vào trong Set hoặc Dictionary 
        """
        return hash(self.state)