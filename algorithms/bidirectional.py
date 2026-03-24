import time
from collections import deque
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class BidirectionalSearch(BaseSearch):
    """
    Bidirectional Search: chay BFS tu ca 2 start_state -> X và X <- goal_state
    """
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle

    def search(self):
        result = SearchResult()
        start_time = time.time()

        #queue cho 2 chieu (frontier)
        queue_start = deque()
        queue_goal = deque()

        #visited: {state: node} truy vet duong di
        visited_start = {}
        visited_goal = {}

        start_node = Node(self.start_state, cost=0)
        goal_node = Node(self.goal_state, cost=0)

        #dua vao queue, danh dau
        queue_start.append(start_node)
        queue_goal.append(goal_node)
        visited_start[self.start_state] = start_node
        visited_goal[self.goal_state] = goal_node

        while queue_start and queue_goal:
            #mo rong tu phia start
            intersection = self.expand_level(queue_start, visited_start, visited_goal, result, "Start ->")
            if intersection:
                return self.combine_path(intersection, visited_start, visited_goal, result, start_time)

            #mo rong tu phia goal
            intersection = self.expand_level(queue_goal, visited_goal, visited_start, result, "<- Goal")
            if intersection:
                return self.combine_path(intersection, visited_start, visited_goal, result, start_time)

        result.processing_time = time.time() - start_time
        return result

    def expand_level(self, queue, visited_mine, visited_other, result, direction):
        """
        Mo rong 1 lop BFS
        """
        current = queue.popleft()
        result.explored_nodes.append(current.state)
        
        #luu cho GUI
        result.steps.append({
            "current": current.state,
            "direction": direction,
            "is_goal": False
        })        

        for next_state in self.puzzle.get_neighbors(current.state): #lay state frontier
            if next_state not in visited_mine:
                #tao node moi, luu visited
                new_node = Node(state=next_state, parent=current, cost=current.g + 1)
                visited_mine[next_state] = new_node
                queue.append(new_node)

                #kiem tra co giao nhau?
                if next_state in visited_other:
                    return next_state 
        return None

    def combine_path(self, intersection_state, visited_start, visited_goal, result, start_time):
        """
        Noi duong di khi thay giao diem
        """
        #start_state -> X 
        node_start_side = visited_start[intersection_state]
        path_start, _ = self.extract_path(node_start_side)

        #X <- goal_state
        node_goal_side = visited_goal[intersection_state]
        path_goal, _ = self.extract_path(node_goal_side)
        
        #ghep start_state -> X + X <- goal_state (đảo lại) va bo node X trung
        result.path = path_start + path_goal[::-1][1:]
        result.path_cost = len(result.path) - 1 
        result.success = True
        result.processing_time = time.time() - start_time
        result.steps.append({"current": intersection_state, "is_goal": True})

        return result
