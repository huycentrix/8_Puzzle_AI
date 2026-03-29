from PySide6.QtCore import QObject, QTimer, Signal, Slot

from algorithms.astar import AStarSearch
from algorithms.bfs import BFS
from algorithms.bidirectional import BidirectionalSearch
from algorithms.dfs import DFS
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.idastar import IDAStarSearch
from algorithms.iddfs import IDDFSearch
from algorithms.ucs import UniformCostSearch


class PuzzleBridge(QObject):
    searchReset = Signal()
    stepUpdated = Signal("QVariantMap")
    searchFinished = Signal("QVariantMap")
    searchError = Signal(str)

    def __init__(self, puzzle_class):
        super().__init__()
        self.PuzzleClass = puzzle_class
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_step)
        self.canvas_width = 6000
        self.level_height = 250
        self.reset_runtime()

    def reset_runtime(self):
        self.all_steps = []
        self.path_ids = []
        self.current_step_idx = 0
        self.node_positions = {}
        self.rendered_children = {}
        self.summary = {}

    def state_key(self, flat_state):
        return ",".join(str(item) for item in flat_state)

    def flatten_state(self, state):
        return [item for row in state for item in row]

    def create_solver(self, method, start_state, goal_state, puzzle_logic):
        mapping = {
            "A* Search": AStarSearch,
            "Breadth-First Search (BFS)": BFS,
            "Depth-First Search (DFS)": DFS,
            "Uniform Cost Search (UCS)": UniformCostSearch,
            "Greedy Best-First Search (GBFS)": GreedyBestFirstSearch,
            "Iterative Deepening Search (IDDFS)": IDDFSearch,
            "Iterative Deepening A* (IDA*)": IDAStarSearch,
            "Bidirectional Search": BidirectionalSearch,
        }
        if method not in mapping:
            raise ValueError(f"Unsupported method: {method}")
        return mapping[method](start_state, goal_state, puzzle_logic)

    def ensure_node_position(self, node_info, parent_key=""):
        node_key = self.state_key(node_info["flat_state"])
        if node_key in self.node_positions:
            return node_key, *self.node_positions[node_key]

        depth = node_info.get("depth", 0)
        if parent_key and parent_key in self.node_positions:
            parent_x, parent_y = self.node_positions[parent_key]
            siblings = self.rendered_children.setdefault(parent_key, [])
            if node_key not in siblings:
                siblings.append(node_key)
            sibling_index = siblings.index(node_key)
            sibling_count = len(siblings)
            spacing = 200
            x = int(parent_x - ((sibling_count - 1) * spacing) / 2 + sibling_index * spacing)
            y = int(parent_y + self.level_height)
        else:
            x = int(self.canvas_width // 2)
            y = 90

        self.node_positions[node_key] = (x, y)
        return node_key, x, y

    def place_children_symmetrically(self, parent_key, children_info):
        if not parent_key or parent_key not in self.node_positions or not children_info:
            return

        parent_x, parent_y = self.node_positions[parent_key]
        spacing = 115
        total = len(children_info)
        start_x = parent_x - ((total - 1) * spacing) / 2
        y = int(parent_y + self.level_height)

        ordered_keys = []
        for index, child_info in enumerate(children_info):
            child_key = self.state_key(child_info["flat_state"])
            x = int(start_x + index * spacing)
            self.node_positions[child_key] = (x, y)
            ordered_keys.append(child_key)

        self.rendered_children[parent_key] = ordered_keys

    def build_visual_node(self, node_info, status, parent_key="", is_goal=False):
        node_key, x, y = self.ensure_node_position(node_info, parent_key)
        return {
            "id": node_key,
            "parentId": parent_key,
            "flatState": node_info["flat_state"],
            "g": node_info.get("g", 0),
            "h": node_info.get("h", 0),
            "f": node_info.get("f", 0),
            "depth": node_info.get("depth", 0),
            "status": "path" if is_goal else status,
            "x": x,
            "y": y,
        }

    @Slot(list, int, result="QVariantList")
    def randomize_state(self, goal_list, moves=40):
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))
        puzzle_logic = self.PuzzleClass(goal_state)
        randomized = puzzle_logic.randomize(goal_state, moves)
        return self.flatten_state(randomized)

    @Slot(list, list, result=bool)
    def is_solvable_state(self, start_list, goal_list):
        start_state = tuple(tuple(start_list[i:i + 3]) for i in range(0, 9, 3))
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))
        puzzle_logic = self.PuzzleClass(goal_state)
        return puzzle_logic.is_solvable(start_state)

    @Slot()
    def stop_playback(self):
        self.timer.stop()

    @Slot(str, list, list, float, str)
    def start_search(self, method, start_list, goal_list, speed, heuristic_name):
        self.timer.stop()
        self.reset_runtime()
        self.searchReset.emit()

        start_state = tuple(tuple(start_list[i:i + 3]) for i in range(0, 9, 3))
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))
        puzzle_logic = self.PuzzleClass(goal_state, heuristic_name)

        if not puzzle_logic.is_solvable(start_state):
            self.searchError.emit("Initial state is not solvable for the selected 8-puzzle goal.")
            return

        solver = self.create_solver(method, start_state, goal_state, puzzle_logic)
        result = solver.search()

        self.all_steps = result.steps
        self.path_ids = [self.state_key(self.flatten_state(state)) for state in result.path]
        self.node_positions[self.state_key(start_list)] = (self.canvas_width // 2, 90)
        self.summary = {
            "success": result.success,
            "algorithm": method,
            "heuristic": heuristic_name,
            "pathIds": self.path_ids,
            "pathCost": result.path_cost,
            "solutionDepth": max(0, len(result.path) - 1),
            "exploredCount": len(result.explored_nodes),
            "frontierPeak": result.frontier_peak,
            "processingTimeMs": round(result.processing_time * 1000.0, 3),
            "stepCount": len(result.steps),
            "startState": start_list,
            "goalState": goal_list,
        }

        if not self.all_steps:
            self.searchFinished.emit(self.summary)
            return

        interval = max(80, int(1000 / max(speed, 0.1)))
        self.timer.start(interval)

    def show_next_step(self):
        if self.current_step_idx >= len(self.all_steps):
            self.timer.stop()
            self.searchFinished.emit(self.summary)
            return

        step = self.all_steps[self.current_step_idx]
        parent_key = ""
        if step.get("parent_state"):
            parent_key = self.state_key(self.flatten_state(step["parent_state"]))

        current_node = self.build_visual_node(
            step["current_node"],
            "explored",
            parent_key,
            step.get("is_goal", False),
        )
        self.place_children_symmetrically(current_node["id"], step.get("children", []))
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
