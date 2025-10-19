from typing import List, Tuple, Callable
from rush_hour_puzzle import RushHourPuzzle

class Node:
    def __init__(self,state: RushHourPuzzle,
                 parent = None,
                 action = None, # action consists of id veh, direction
                 g: int = 0):  
        self.state = state
        self.parent = parent
        self.action = action
        # g is path cost (number of moves from root)
        self.g = g
        # f is used by A* (g + heuristic)
        self.f = None

    def getPath(self) -> List[RushHourPuzzle]:
        #returns list of states from root (first) to this node (last).

        path = []
        node = self
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()  # because we collected from current to the root
        return path

    def getSolution(self) -> List[Tuple[str, str]]:
        
        #Returns list of actions from root to this node.
        #The root's action is typically None and will be ignored.
       
        actions = []
        node = self
        while node is not None:
            if node.action is not None:
                actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions

    def setF(self, heuristic: Callable[[RushHourPuzzle], int]):

        h = heuristic(self.state)
        self.f = self.g + h
    
    def __lt__(self, other):
        return self.f < other.f

