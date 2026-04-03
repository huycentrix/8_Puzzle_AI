# Lab 1 - Search Algorithms
GroupID: 1 <br>
Group Members:
- Đoàn Thế Việt (24127590)
- Võ Minh Huy (24127405)
- Nguyễn Thanh Toàn (24127559)
- Cao Hải Vy (24127598)
- Nguyễn Lâm Thảo Trang (24127566)
## 1. Project description
This project implements and visualizes eight classic search algorithms for solving the 8-puzzle problem, a well-known sliding puzzle in artificial intelligence.
### 1.1. Implemented Algorithms:
- Uninformed Search: BFS, DFS, UCS, IDDFS, Bidirectional Search.
- Informed Search: A, Greedy Best-First Search, IDA.
### 1.2. Heuristic Functions (for informed algorithms):
- Manhattan Distance.
- Misplaced Tiles (Hamming Distance).
- Euclidean Distance.
### 1.3. Key Features:
- Graphical User Interface (GUI) built with PySide6 (Qt for Python) and QML.
- Two display modes: Puzzle Setup (animation mode) and Search Tree (tree visualization mode).
- Real-time visualization of the search process with step-by-step playback.
- Performance metrics: processing time, path cost, explored nodes, frontier peak, solution depth.
- Solvability checking using inversion count algorithm.
- Random puzzle generation with guaranteed solvability.
## 2. Directory structure
8_Puzzle_AI/ <br>				
├── PuzzleUI/				# Full QML interface and bridge source code <br>
│   ├── PuzzleUIContent			# UI components (.qml) <br>
│   │   ├── fonts <br>
│   │   ├── images <br>
│   │   ├── AnimationScreen.qml <br>
│   │   ├── App.qml <br>
│   │   ├── ConfigPanel.qml <br>
│   │   ├── ControlPanel.qml <br>
│   │   ├── LogList.qml <br>
│   │   ├── MaterialIcon.qml <br>
│   │   ├── MetricsPanel.qml <br>
│   │   ├── PuzzleGrid.qml <br>
│   │   ├── PuzzleNode.qml <br>
│   │   ├── SearchTreeScreen.qml <br>
│   │   ├── SideButton.qml <br>
│   │   ├── StartStateDialog.qml <br>
│   ├── Python				# main.py and bridge.py <br>
│   │   ├── bridge.py <br>
│   │   ├── main.py <br>
│   │   ├── pyproject.toml <br>
│   ├── qtquickcontrols2.conf <br>
├── algorithms/          			# Contains 8 search algorithms <br>                                          
│   ├── __init__.py <br>
│   ├── astar.py <br>
│   ├── bfs.py <br>
│   ├── bidirectional.py <br>
│   ├── dfs.py <br>
│   ├── greedy.py <br>
│   ├── idastar.py <br>
│   ├── iddfs.py <br>
│   ├── ucs.py <br>
├── core/						# Defines Node and BaseSearch class <br>
│   ├── __init__.py <br>
│   ├── node.py <br>
│   ├── search_base.py <br>
├── puzzle/					# Board logic and feasibility checking <br>
│   ├── __init__.py <br>
│   ├── puzzle.py <br>
├── .gitignore/ <br>
└── README.md/ <br>
## 3. How to build and run
### 3.1. Requirements
- PythoN (3.10 or later).
- PySide6 (6.6.0 or later).
### 3.2. Installation
- Clone the repository (or download the source code):
```bash
git clone https://github.com/huycentrix/8_Puzzle_AI.git
cd 8_Puzzle_AI
```
- Install dependencies (PySide6):
```bash
pip install PySide6
```
### 3.3. Run the program
- Navigate to the Python backend directory:
```bash
cd PuzzleUI/Python
``` 
- Run the main application:
```bash
python main.py
```
- The GUI window will appear, ready for interaction.
## 4. Usage guide
### 4.1. Select mode (Sidebar)
- Puzzle Setup: Animation mode – watch the puzzle being solved step by step.
- Search Tree: Tree visualization mode – explore the search tree with f, g, h values.
### 4.2. Configure the puzzle
- Edit Start State: Click on any cell to edit directly, or use the "Edit Start State" dialog.
- Randomize: Generate a random solvable puzzle.
- Reset: Restore default start state [1, 2, 3, 4, 0, 6, 7, 5, 8].
### 4.3. Select algorithm and heuristic
- Algorithm dropdown: Choose from 8 search algorithms.
- Heuristic dropdown (for A*, GBFS, IDA*): Select Manhattan Distance, Misplaced Tiles, or Euclidean Distance.
- Speed slider: Adjust playback speed (0.5x – 4.0x).
### 4.4. Run search
- Click Run Search to start the selected algorithm.
- Click Stop to interrupt the search.
### 4.5. Observe results
- Metrics panel: View processing time, path cost, explored nodes, frontier peak, solution depth.
- Execution log: See timestamped step-by-step log.
- Search tree (Search Tree mode): Nodes display puzzle state with f, g, h values; edges connect parent-child nodes.
- Animation (Puzzle Setup mode): Tiles slide to show the solution path.