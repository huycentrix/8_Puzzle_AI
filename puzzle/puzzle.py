class Puzzle:
    """
    Lớp Puzzle: Mô hình hóa logic bài toán 8-puzzle.
    Bao gồm các phương thức xác định trạng thái láng giềng, tính toán Heuristic 
    và kiểm tra tính khả thi của bài toán.
    """
    def __init__(self, goal_state):
        # Lưu trữ trạng thái đích để so sánh và tính toán khoảng cách
        self.goal = goal_state

    def get_neighbors(self, state):
        """
        Tìm tất cả các trạng thái có thể đạt được từ trạng thái hiện tại
        bằng cách di chuyển ô trống (số 0) lên, xuống, trái, phải.
        """
        neighbors = []

        # Bước 1: Xác định tọa độ (x, y) của ô trống (giá trị 0) trong lưới 3x3
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    x, y = i, j

        # Bước 2: Liệt kê các hướng di chuyển có thể (Lên, Xuống, Trái, Phải)
        moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        for nx, ny in moves:
            # Kiểm tra xem tọa độ mới có nằm trong phạm vi lưới 3x3 không
            if 0 <= nx < 3 and 0 <= ny < 3:
                # Tạo bản sao của trạng thái hiện tại (chuyển tuple sang list để chỉnh sửa)
                new_state = [list(row) for row in state]
                
                # Hoán đổi vị trí của ô trống với ô số ở vị trí mới
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                
                # Chuyển ngược lại thành tuple của tuple để có thể băm (hashable) 
                # và đưa vào tập hợp 'visited' hoặc 'path'.
                neighbors.append(tuple(tuple(r) for r in new_state))

        return neighbors

    def heuristic(self, state):
        """
        Hàm Heuristic: Manhattan Distance (Khoảng cách Manhattan).
        Tính tổng khoảng cách di chuyển tối thiểu của từng ô số từ vị trí 
        hiện tại đến vị trí đích (không tính ô trống).
        """
        dist = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                # Chỉ tính toán cho các ô có số (bỏ qua ô trống)
                if val != 0:
                    # Tìm vị trí đúng của giá trị 'val' trong trạng thái đích
                    for x in range(3):
                        for y in range(3):
                            if self.goal[x][y] == val:
                                # Công thức: |x1 - x2| + |y1 - y2|
                                dist += abs(i - x) + abs(j - y)
        return dist

    def is_solvable(self, state):
        """
        Kiểm tra tính giải được của trạng thái bắt đầu.
        Dựa trên nguyên lý: Số cặp nghịch thế (Inversions).
        Với lưới 3x3, bài toán giải được khi tổng số cặp nghịch thế là số chẵn.
        """
        # Bước 1: Trải phẳng ma trận thành list 1D và loại bỏ ô trống (số 0)
        flat_list = [item for row in state for item in row if item != 0]
    
        inversions = 0
        # Bước 2: Đếm số cặp (a, b) sao cho a đứng trước b nhưng a > b
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1
                
        # Bước 3: Nếu tổng số nghịch thế là số chẵn, bài toán có lời giải
        return inversions % 2 == 0