class Puzzle:
    """
    Lớp Puzzle: Mô hình hóa logic bài toán 8-puzzle.
    Bao gồm các phương thức xác định trạng thái láng giềng, tính toán Heuristic 
    và kiểm tra tính khả thi của bài toán.
    """
    def __init__(self, goal_state):
        # Lưu trữ trạng thái đích để so sánh và tính toán khoảng cách
        self.goal = goal_state

    def get_neighbors(self, state, include_actions=False):
        neighbors = []
        x, y = 0, 0

        # Xác định tọa độ ô trống
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    x, y = i, j
        moves = [
            (x-1, y, "Move Up"), 
            (x+1, y, "Move Down"), 
            (x, y-1, "Move Left"), 
            (x, y+1, "Move Right")
        ]

        for nx, ny, action_label in moves:
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [list(row) for row in state]
                tile_value = new_state[nx][ny]
                
                # Hoán đổi vị trí
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                final_state = tuple(tuple(r) for r in new_state)

                if include_actions:
                    # Trả về kèm hành động nếu yêu cầu
                    neighbors.append((final_state, f"{action_label} (Tile {tile_value})"))
                else:
                    # Trả về chỉ trạng thái (giống hệt hàm cũ)
                    neighbors.append(final_state)

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