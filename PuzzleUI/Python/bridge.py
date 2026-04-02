import datetime
import threading

from PySide6.QtCore import QObject, Property, Q_ARG, QMetaObject, Qt, QTimer, Signal, Slot

from algorithms.astar import AStarSearch
from algorithms.bfs import BFS
from algorithms.bidirectional import BidirectionalSearch
from algorithms.dfs import DFS
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.idastar import IDAStarSearch
from algorithms.iddfs import IDDFSearch
from algorithms.ucs import UniformCostSearch
from puzzle.puzzle import Puzzle


class PuzzleBridge(QObject):
    puzzleModelChanged = Signal()
    metricsChanged = Signal()
    newLogEntry = Signal(int, str, str)

    searchReset = Signal()
    stepUpdated = Signal("QVariantMap")
    searchFinished = Signal("QVariantMap")
    searchError = Signal(str)
    treeSearchPrepared = Signal(object)
    treeSearchFailed = Signal(str)

    def __init__(self):
        super().__init__()
        self._puzzle_model = [1, 2, 3, 4, 0, 5, 7, 8, 6]
        self._total_steps = 0
        self._nodes_expanded = 0
        self._solution_depth = 0
        self._processing_time = "0 ms"
        self._solution_steps = []
        self._current_idx = 0

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_to_next_step)

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_step)
        self.canvas_width = 60000
        self.level_height = 180
        self.level_start_x = 160
        self.level_spacing_x = 150
        self.max_visualized_steps = 250
        self._tree_search_running = False
        self.treeSearchPrepared.connect(self._apply_prepared_tree_search)
        self.treeSearchFailed.connect(self._apply_tree_search_error)
        self.reset_runtime()

    def reset_runtime(self):
        self.all_steps = []
        self.path_ids = []
        self.current_step_idx = 0
        self.reset_tree_layout()
        self.summary = {}
        self.current_visual_iteration = None

    def reset_tree_layout(self):
        self.node_positions = {}
        self.level_counts = {}

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

    def state_key(self, flat_state):
        return ",".join(str(item) for item in flat_state)

    def flatten_state(self, state):
        return [item for row in state for item in row]

    def create_solver(self, method, start_state, goal_state, puzzle_logic):
        mapping = {
            "A* Search": AStarSearch,
            "Breadth-First Search": BFS,
            "Breadth-First Search (BFS)": BFS,
            "Depth-First Search": DFS,
            "Depth-First Search (DFS)": DFS,
            "Uniform Cost Search": UniformCostSearch,
            "Uniform Cost Search (UCS)": UniformCostSearch,
            "Greedy Search": GreedyBestFirstSearch,
            "Greedy Best-First Search (GBFS)": GreedyBestFirstSearch,
            "IDDFS": IDDFSearch,
            "Iterative Deepening Search (IDDFS)": IDDFSearch,
            "IDA* Search": IDAStarSearch,
            "Iterative Deepening A* (IDA*)": IDAStarSearch,
            "Bidirectional Search": BidirectionalSearch,
        }
        if method not in mapping:
            raise ValueError(f"Unsupported method: {method}")
        return mapping[method](start_state, goal_state, puzzle_logic)

    def ensure_node_position(self, node_info, node_id):
        if node_id in self.node_positions:
            return node_id, *self.node_positions[node_id]

        depth = int(node_info.get("depth", 0))
        if depth <= 0:
            x = int(self.canvas_width // 2)
            y = 90
        else:
            slot_index = self.level_counts.get(depth, 0)
            x = int(self.level_start_x + slot_index * self.level_spacing_x)
            y = int(90 + depth * self.level_height)
            self.level_counts[depth] = slot_index + 1

        self.node_positions[node_id] = (x, y)
        return node_id, x, y

    def place_children_symmetrically(self, parent_key, children_info):
        child_x_positions = []
        for child_info in children_info:
            child_id = str(child_info["uid"])
            _, child_x, _ = self.ensure_node_position(child_info, child_id)
            child_x_positions.append(child_x)

        if (
            parent_key
            and parent_key in self.node_positions
            and child_x_positions
            and int(children_info[0].get("depth", 1)) == 1
        ):
            _, parent_y = self.node_positions[parent_key]
            centered_parent_x = int(sum(child_x_positions) / len(child_x_positions))
            self.node_positions[parent_key] = (centered_parent_x, parent_y)

    def randomize_easy_state(self, goal_state, heuristic_name="Manhattan Distance"):
        puzzle = Puzzle(goal_state, heuristic_name)
        move_options = [4, 6, 8, 10, 12]
        candidates = []

        for moves in move_options:
            for _ in range(3):
                state = puzzle.randomize(goal_state, moves)
                score = (
                    puzzle.heuristic(state),
                    puzzle.misplaced_tiles(state),
                    moves,
                )
                candidates.append((score, state))

        candidates.sort(key=lambda item: item[0])
        return candidates[0][1]

    def build_visual_node(self, node_info, status, parent_id="", is_goal=False):
        node_key = str(node_info["uid"])
        _, x, y = self.ensure_node_position(node_info, node_key)
        return {
            "id": node_key,
            "parentId": parent_id,
            "stateKey": self.state_key(node_info["flat_state"]),
            "flatState": node_info["flat_state"],
            "g": node_info.get("g", 0),
            "h": node_info.get("h", 0),
            "f": node_info.get("f", 0),
            "depth": node_info.get("depth", 0),
            "status": "path" if is_goal else status,
            "x": x,
            "y": y,
        }

    @Slot()
    def shufflePuzzle(self):
        self.animation_timer.stop()
        goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
        self._puzzle_model = self.flatten_state(self.randomize_easy_state(goal_state))
        self.puzzleModelChanged.emit()
        self._total_steps = 0
        self._nodes_expanded = 0
        self._solution_depth = 0
        self._processing_time = "0 ms"
        self.metricsChanged.emit()

    @Slot(list, int, result="QVariantList")
    def randomize_state(self, goal_list, moves=40):
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))
        randomized = self.randomize_easy_state(goal_state)
        return self.flatten_state(randomized)

    @Slot(list, list, result=bool)
    def is_solvable_state(self, start_list, goal_list):
        start_state = tuple(tuple(start_list[i:i + 3]) for i in range(0, 9, 3))
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))
        puzzle = Puzzle(goal_state)
        return puzzle.is_solvable(start_state)

    @Slot()
    def stop_playback(self):
        self.timer.stop()

    @Slot()
    def stopSolve(self):
        self.animation_timer.stop()

    @Slot(list, str, float, str)
    def startSolve(self, current_list, algo_name, speed, heuristic_name):
        self.animation_timer.stop()
        thread = threading.Thread(target=self._run_animation_algorithm, args=(current_list, algo_name, speed, heuristic_name))
        thread.daemon = True
        thread.start()

    def _run_animation_algorithm(self, current_list, algo_name, speed, heuristic_name):
        start_state = tuple(tuple(current_list[i:i + 3]) for i in range(0, 9, 3))
        goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
        puzzle = Puzzle(goal_state, heuristic_name)
        algo = self.create_solver(algo_name, start_state, goal_state, puzzle)
        result = algo.search()

        if result.success:
            self._solution_steps = result.steps
            self._total_steps = len(result.path) - 1
            self._nodes_expanded = len(result.explored_nodes)
            self._solution_depth = self._total_steps
            self._current_idx = 0
            self._processing_time = f"{result.processing_time * 1000:.2f} ms"
            self.metricsChanged.emit()

            interval = int(500 / max(speed, 0.1))
            QMetaObject.invokeMethod(self.animation_timer, "start", Qt.QueuedConnection, Q_ARG(int, interval))

    def update_to_next_step(self):
        if self._current_idx < len(self._solution_steps):
            step_data = self._solution_steps[self._current_idx]
            state_2d = step_data["current"]
            self._puzzle_model = [item for row in state_2d for item in row]
            self.puzzleModelChanged.emit()

            action = step_data.get("action") or "Initial State"
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.newLogEntry.emit(self._current_idx + 1, action, current_time)
            self._nodes_expanded = self._current_idx + 1
            self.metricsChanged.emit()
            self._current_idx += 1
        else:
            self.animation_timer.stop()

    @Slot(str, list, list, float, str)
    def start_search(self, method, start_list, goal_list, speed, heuristic_name):
        if self._tree_search_running:
            return

        self.timer.stop()
        self.reset_runtime()
        self.searchReset.emit()
        self._tree_search_running = True

        worker = threading.Thread(
            target=self._run_tree_search,
            args=(method, start_list, goal_list, speed, heuristic_name),
        )
        worker.daemon = True
        worker.start()

    def _run_tree_search(self, method, start_list, goal_list, speed, heuristic_name):
        start_state = tuple(tuple(start_list[i:i + 3]) for i in range(0, 9, 3))
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))
        puzzle = Puzzle(goal_state, heuristic_name)

        if not puzzle.is_solvable(start_state):
            self.treeSearchFailed.emit("Initial state is not solvable for the selected 8-puzzle goal.")
            return

        solver = self.create_solver(method, start_state, goal_state, puzzle)
        result = solver.search()
        truncated = len(result.steps) > self.max_visualized_steps
        visual_steps = result.steps[:self.max_visualized_steps]

        payload = {
            "steps": visual_steps,
            "startKey": self.state_key(start_list),
            "summary": {
            "success": result.success,
            "algorithm": method,
            "heuristic": heuristic_name,
            "pathIds": [self.state_key(self.flatten_state(state)) for state in result.path],
            "pathCost": result.path_cost,
            "solutionDepth": max(0, len(result.path) - 1),
            "exploredCount": len(result.explored_nodes),
            "frontierPeak": result.frontier_peak,
            "processingTimeMs": round(result.processing_time * 1000.0, 3),
            "stepCount": len(result.steps),
            "visualizedStepCount": len(visual_steps),
            "renderTruncated": truncated,
            "startState": start_list,
            "goalState": goal_list,
            "speed": speed,
            },
        }
        self.treeSearchPrepared.emit(payload)

    @Slot(object)
    def _apply_prepared_tree_search(self, payload):
        self._tree_search_running = False
        self.all_steps = payload["steps"]
        self.summary = payload["summary"]
        self.path_ids = self.summary["pathIds"]
        self.current_visual_iteration = None
        self.reset_tree_layout()
        if self.all_steps:
            root_uid = str(self.all_steps[0]["current_node"]["uid"])
            self.node_positions[root_uid] = (self.canvas_width // 2, 90)
        self.level_counts[0] = 1

        if not self.all_steps:
            self.searchFinished.emit(self.summary)
            return

        interval = max(80, int(1000 / max(float(self.summary["speed"]), 0.1)))
        self.timer.start(interval)

    @Slot(str)
    def _apply_tree_search_error(self, message):
        self._tree_search_running = False
        self.searchError.emit(message)

    def show_next_step(self):
        if self.current_step_idx >= len(self.all_steps):
            self.timer.stop()
            self.searchFinished.emit(self.summary)
            return

        step = self.all_steps[self.current_step_idx]
        step_iteration = step.get("iteration", None)
        if (
            self.summary.get("algorithm") in {"IDDFS", "IDA* Search"}
            and step_iteration != self.current_visual_iteration
        ):
            self.current_visual_iteration = step_iteration
            self.reset_tree_layout()
            root_uid = str(step["current_node"]["uid"])
            if step["current_node"].get("depth", 0) == 0:
                self.node_positions[root_uid] = (self.canvas_width // 2, 90)
            self.level_counts[0] = 1

        parent_id = ""
        if step["current_node"].get("parent_uid") is not None:
            parent_id = str(step["current_node"]["parent_uid"])

        current_key = str(step["current_node"]["uid"])
        self.place_children_symmetrically(current_key, step.get("children", []))
        current_node = self.build_visual_node(
            step["current_node"],
            "explored",
            parent_id,
            step.get("is_goal", False),
        )
        children = [
            self.build_visual_node(child_info, "frontier", current_node["id"], False)
            for child_info in step.get("children", [])
        ]

        payload = {
            "stepNumber": self.current_step_idx + 1,
            "currentNode": current_node,
            "children": children,
            "frontierCount": step.get("frontier_count", 0),
            "exploredCount": step.get("explored_count", 0),
            "isGoal": step.get("is_goal", False),
            "meta": {
                "direction": step.get("direction", ""),
                "limit": step.get("limit", -1),
                "iteration": step.get("iteration", -1),
                "fLimit": step.get("f_limit", -1),
            },
        }
        self.stepUpdated.emit(payload)
        self.current_step_idx += 1
