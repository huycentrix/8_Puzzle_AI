from PySide6.QtCore import QObject, Slot, Signal, QTimer

from algorithms.astar import AStarSearch
from algorithms.bfs import BFS
from algorithms.bidirectional import BidirectionalSearch
from algorithms.dfs import DFS
from algorithms.greedy import GreedyBestFirstSearch
from algorithms.idastar import IDAStarSearch
from algorithms.iddfs import IDDFSearch
from algorithms.ucs import UniformCostSearch


class PuzzleBridge(QObject):
    stepUpdated = Signal("QVariantMap")
    searchReset = Signal()
    searchFinished = Signal(bool, list)

    def __init__(self, puzzle_class):
        super().__init__()
        self.PuzzleClass = puzzle_class
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_step)
        self.all_steps = []
        self.path_ids = []
        self.current_step_idx = 0
        self.canvas_width = 8000
        self.level_height = 250
        self.node_positions = {}
        self.rendered_children = {}

    def state_key(self, flat_state):
        return ",".join(str(item) for item in flat_state)

    def flatten_state(self, state):
        return [item for row in state for item in row]

    def ensure_node_position(self, node_info, parent_key=""):
        node_key = self.state_key(node_info["flat_state"])
        if node_key in self.node_positions:
            x, y = self.node_positions[node_key]
            return node_key, x, y

        if parent_key and parent_key in self.node_positions:
            parent_x, parent_y = self.node_positions[parent_key]
            sibling_bucket = self.rendered_children.setdefault(parent_key, [])
            if node_key not in sibling_bucket:
                sibling_bucket.append(node_key)

            child_count = max(len(sibling_bucket), 1)
            child_index = sibling_bucket.index(node_key)
            spacing = 220
            start_x = parent_x - ((child_count - 1) * spacing) / 2
            x = int(start_x + child_index * spacing)
            y = parent_y + self.level_height
        else:
            x = self.canvas_width // 2
            y = 100

        self.node_positions[node_key] = (x, y)
        return node_key, x, y

    def build_visual_node(self, node_info, status, parent_key="", is_goal=False):
        node_key, x, y = self.ensure_node_position(node_info, parent_key)
        return {
            "id": node_key,
            "parentId": parent_key,
            "flatState": node_info["flat_state"],
            "g": node_info.get("g", 0),
            "h": node_info.get("h", 0),
            "f": node_info.get("f", 0),
            "status": "path" if is_goal else status,
            "x": x,
            "y": y,
            "isGoal": is_goal,
        }

    def create_solver(self, method, start_state, goal_state, puzzle_logic):
        if method == "A* Search":
            return AStarSearch(start_state, goal_state, puzzle_logic)
        if method == "Breadth-First Search (BFS)":
            return BFS(start_state, goal_state, puzzle_logic)
        if method == "Depth-First Search (DFS)":
            return DFS(start_state, goal_state, puzzle_logic)
        if method == "Uniform Cost Search (UCS)":
            return UniformCostSearch(start_state, goal_state, puzzle_logic)
        if method == "Greedy Best-First Search (GBFS)":
            return GreedyBestFirstSearch(start_state, goal_state, puzzle_logic)
        if method == "Iterative Deepening Search (IDDFS)":
            return IDDFSearch(start_state, goal_state, puzzle_logic)
        if method == "Iterative Deepening A* (IDA*)":
            return IDAStarSearch(start_state, goal_state, puzzle_logic)
        if method == "Bidirectional Search":
            return BidirectionalSearch(start_state, goal_state, puzzle_logic)
        raise ValueError(f"Unsupported method: {method}")

    @Slot(str, list, list, float)
    def start_search(self, method, start_list, goal_list, speed):
        start_state = tuple(tuple(start_list[i:i + 3]) for i in range(0, 9, 3))
        goal_state = tuple(tuple(goal_list[i:i + 3]) for i in range(0, 9, 3))

        puzzle_logic = self.PuzzleClass(goal_state)
        solver = self.create_solver(method, start_state, goal_state, puzzle_logic)

        result = solver.search()
        self.all_steps = result.steps
        self.path_ids = [self.state_key(self.flatten_state(state)) for state in result.path]
        self.current_step_idx = 0
        self.node_positions = {}
        self.rendered_children = {}
        self.searchReset.emit()

        start_key = self.state_key(start_list)
        self.node_positions[start_key] = (self.canvas_width // 2, 100)

        interval = max(1, int(1000 / max(speed, 0.1)))
        self.timer.start(interval)

    def show_next_step(self):
        if self.current_step_idx >= len(self.all_steps):
            self.timer.stop()
            self.searchFinished.emit(True, self.path_ids)
            return

        step = self.all_steps[self.current_step_idx]
        current_info = step["current_node"]
        parent_key = ""
        if step.get("parent_state"):
            parent_key = self.state_key(self.flatten_state(step["parent_state"]))

        current_node = self.build_visual_node(
            current_info,
            "explored",
            parent_key=parent_key,
            is_goal=step.get("is_goal", False),
        )

        children_nodes = []
        for child_info in step.get("children", []):
            children_nodes.append(
                self.build_visual_node(child_info, "frontier", parent_key=current_node["id"])
            )

        payload = {
            "stepNumber": self.current_step_idx + 1,
            "nodesExpanded": len(children_nodes),
            "currentNode": current_node,
            "children": children_nodes,
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
