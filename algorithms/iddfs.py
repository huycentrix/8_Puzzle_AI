import time
from core.search_base import BaseSearch, SearchResult
from core.node import Node

class IDDFSearch(BaseSearch):
    """
    Iterative Deepening Depth-First Search (IDDFS): DFS voi depth-limit tang dan
    """
    def __init__(self, start_state, goal_state, puzzle):
        super().__init__(start_state, goal_state)
        self.puzzle = puzzle
    
    def search(self):
        result = SearchResult()
        start_time = time.time()
        limit = 0

        while True:
            found_node , is_cutoff = self.dls(Node(self.start_state), limit, {self.start_state}, result, limit)
            
            #tim thay dich -> lay ra path 
            if found_node:
                result.path, result.path_cost = self.extract_path(found_node)
                result.success = True
                break
            
            #khong tim thay + duyet het cay + toi da limit -> vo nghiem
            if not is_cutoff:
                break

            #cutoff -> tang depth
            limit += 1

        result.processing_time = time.time() - start_time
        return result

    def dls(self, node, limit, path, result, current_iteration):
        result.explored_nodes.append(node.state)
        
        if node.state == self.goal_state:
            result.steps.append({
                "current": node.state,
                "limit": limit,
                "iteration": current_iteration,
                "action": node.action, # Thêm action cho Log
                "frontier": [],
                "is_goal": True
            })
            return node, False

        if limit <= 0:
            return None, True

        cutoff_occurred = False
        successors = []
        
        # Sửa đổi: include_actions=True và unpack action
        for next_state, action in self.puzzle.get_neighbors(node.state, include_actions=True):
            if next_state not in path:
                # Truyền action vào Node
                child = Node(state=next_state, parent=node, action=action, cost=node.g + 1)
                successors.append(child)

        result.steps.append({
            "current": node.state,
            "limit": limit,
            "iteration": current_iteration,
            "action": node.action, # Thêm action cho Log
            "frontier": [{"state": n.state} for n in successors],
            "is_goal": False
        })

        for child in successors:
            path.add(child.state)
            found, shifted_cutoff = self.dls(child, limit - 1, path, result, current_iteration)
            if found:
                return found, False
            if shifted_cutoff:
                cutoff_occurred = True
            path.remove(child.state) 

        return None, cutoff_occurred