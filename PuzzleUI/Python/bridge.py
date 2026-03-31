import random
import threading
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer, QMetaObject, Qt, Q_ARG
import datetime
from algorithms.bfs import BFS
from algorithms.astar import AStarSearch
from algorithms.dfs import DFS
from algorithms.ucs import UniformCostSearch
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.iddfs import IDDFSearch
from algorithms.idastar import IDAStarSearch
from algorithms.bidirectional import BidirectionalSearch
from puzzle.puzzle import Puzzle

class PuzzleBridge(QObject):
    # Các tín hiệu thông báo cho QML cập nhật giao diện
    puzzleModelChanged = Signal()
    metricsChanged = Signal()
    newLogEntry = Signal(int, str, str)
    def __init__(self):
        super().__init__()
        # Trạng thái mặc định (1D list cho QML)
        self._puzzle_model = [1, 2, 3, 4, 0, 5, 7, 8, 6]
        
        # Các thông số đo lường (Metrics)
        self._total_steps = 0
        self._nodes_expanded = 0
        self._solution_depth = 0
        self._processing_time = "0 ms"
        # Dữ liệu phục vụ Animation
        self._solution_steps = []
        self._current_idx = 0
        
        # Timer điều khiển tốc độ phát lại (Playback)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_to_next_step)

    # --- PROPERTIES (Để QML đọc dữ liệu) ---

    @Property(list, notify=puzzleModelChanged)
    def puzzleModel(self):
        return self._puzzle_model
    @Property(str, notify=metricsChanged)
    def processingTime(self):
        return self._processing_time
    @Property(int, notify=metricsChanged)
    def totalSteps(self):
        return self._total_steps

    @Property(int, notify=metricsChanged)
    def nodesExpanded(self):
        return self._nodes_expanded

    @Property(int, notify=metricsChanged)
    def solutionDepth(self):
        return self._solution_depth

    # --- SLOTS (Để QML gọi lệnh) ---
    @Slot()
    def shufflePuzzle(self):
        """Xáo trộn bàn cờ bằng cách sinh mảng ngẫu nhiên và kiểm tra inversions"""
        self.animation_timer.stop()
        
        goal_state_2d = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
        puzzle = Puzzle(goal_state_2d)
        
        # Tạo danh sách các số từ 0-8
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        while True:
            # 1. Trộn ngẫu nhiên mảng
            random.shuffle(numbers)
            
            # 2. Chuyển list 1D thành tuple 2D để kiểm tra bằng logic của bạn
            temp_state = tuple(tuple(numbers[i:i+3]) for i in range(0, 9, 3))
            
            # 3. Sử dụng hàm is_solvable trong puzzle.py
            if puzzle.is_solvable(temp_state):
                # Nếu giải được, cập nhật model và thoát vòng lặp
                self._puzzle_model = list(numbers)
                break

        # Cập nhật giao diện và reset thông số
        self.puzzleModelChanged.emit()
        self._total_steps = 0
        self._nodes_expanded = 0
        self._solution_depth = 0
        self._processing_time = "0 ms"
        self.metricsChanged.emit()

    @Slot(list, str, float)
    def startSolve(self, current_list, algo_name, speed):
        """
        Khởi chạy thuật toán trong một luồng riêng để tránh treo UI.
        """
        # Dừng timer cũ nếu đang chạy
        self.animation_timer.stop()
        
        # Chạy thuật toán trong Thread riêng
        thread = threading.Thread(target=self._run_algorithm, args=(current_list, algo_name, speed))
        thread.daemon = True
        thread.start()

    def _run_algorithm(self, current_list, algo_name, speed):
        # 1. Chuẩn bị dữ liệu
        start_state = tuple(tuple(current_list[i:i+3]) for i in range(0, 9, 3))
        goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
        puzzle = Puzzle(goal_state)
        
        # 2. Lựa chọn thuật toán
        if algo_name == "A* Search":
            algo = AStarSearch(start_state, goal_state, puzzle)
        elif algo_name == "Breadth-First Search":
            algo = BFS(start_state, goal_state, puzzle)
        elif algo_name == "Depth-First Search":
            algo = DFS(start_state, goal_state, puzzle)
        elif algo_name == "Uniform Cost Search":
            algo = UniformCostSearch(start_state, goal_state, puzzle)
        elif algo_name == "Greedy Search":
            algo = GreedyBestFirstSearch(start_state, goal_state, puzzle)
        elif algo_name == "IDDFS":
            algo = IDDFSearch(start_state, goal_state, puzzle)
        elif algo_name == "IDA* Search":
            algo = IDAStarSearch(start_state, goal_state, puzzle)
        elif algo_name == "Bidirectional Search":
            algo = BidirectionalSearch(start_state, goal_state, puzzle)
        else:
            algo = AStarSearch(start_state, goal_state, puzzle)
        result = algo.search()
        
        if result.success:
            # Cập nhật thông số Metrics ban đầu
            self._solution_steps = result.steps
            self._total_steps = len(result.path) - 1
            self._nodes_expanded = len(result.explored_nodes)
            self._solution_depth = self._total_steps
            self._current_idx = 0
            self._processing_time = f"{result.processing_time * 1000:.2f} ms"
            # Thông báo cho QML cập nhật bảng Metrics Ledger
            self.metricsChanged.emit()
            
            # 4. Tính toán tốc độ và khởi chạy Timer (Quay về luồng chính UI)
            interval = int(500 / speed)
            QMetaObject.invokeMethod(self.animation_timer, "start", 
                                   Qt.QueuedConnection, Q_ARG(int, interval))

    def update_to_next_step(self):
        if self._current_idx < len(self._solution_steps):
            # 1. Lấy dữ liệu của bước hiện tại
            step_data = self._solution_steps[self._current_idx]
            
            # 2. Cập nhật trạng thái bàn cờ để Grid trượt
            state_2d = step_data["current"]
            self._puzzle_model = [item for row in state_2d for item in row]
            self.puzzleModelChanged.emit()

            # 3. CẬP NHẬT METRICS TRỰC TIẾP TẠI ĐÂY
            # Lấy cost (g) của node hiện tại làm Total Steps
            # self._total_steps = step_data.get("cost", 0)
            action = step_data.get("action", "Initial State")
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            self.newLogEntry.emit(self._current_idx + 1, action, current_time)
            # Giả định mỗi bước tương ứng với một node được lấy ra khỏi Frontier
            self._nodes_expanded = self._current_idx + 1 
            
            # Phát tín hiệu để QML cập nhật lại các con số trên màn hình
            self.metricsChanged.emit()
            
            self._current_idx += 1
        else:
            self.animation_timer.stop()

    @Slot()
    def stopSolve(self):
        """Dừng quá trình animation"""
        self.animation_timer.stop()