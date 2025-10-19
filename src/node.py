class Node:
    """
    This class represents a node in the search tree.
    Each node contains a state, parent reference, action, and costs.
    """
    
    def __init__(self, state, parent=None, action=None):
        """
        Initialize a node in the search tree.
        
        Parameters:
        - state: RushHourPuzzle instance representing the state
        - parent: Reference to parent node
        - action: Action that led to this state (vehicle_id, direction)
        """
        self.state = state      # The puzzle state
        self.parent = parent    # Parent node
        self.action = action    # Action that created this node
        self.g = 0              # Path cost from initial state
        self.f = 0              # Fitness function for A* (f = g + h)
        
        # Calculate g (path cost)
        if parent:
            self.g = parent.g + 1  # Each step costs 1
        else:
            self.g = 0  # Initial state has cost 0
    
    def getPath(self):
        """
        Returns the sequence of states from initial state to current state.
        Traces back from current node to root using parent references.
        
        Returns: List of RushHourPuzzle states
        """
        path = []
        current_node = self
        
        # Trace back from current node to initial node
        while current_node is not None:
            path.append(current_node.state)
            current_node = current_node.parent
        
        # Reverse to get path from initial to current
        path.reverse()
        return path
    
    def getSolution(self):
        """
        Returns the sequence of actions from initial state to current state.
        
        Returns: List of actions (vehicle_id, direction) tuples
        """
        actions = []
        current_node = self
        
        # Trace back and collect actions
        while current_node.parent is not None:
            actions.append(current_node.action)
            current_node = current_node.parent
        
        # Reverse to get actions in correct order
        actions.reverse()
        return actions
    
    def setF(self, heuristic_function):
        """
        Calculate the fitness function f for A* algorithm.
        f = g + h
        where g is the path cost and h is the heuristic value.
        
        Parameters:
        - heuristic_function: Function that takes a state and returns h value
        """
        h = heuristic_function(self.state)
        self.f = self.g + h
    
    def __lt__(self, other):
        """
        Less than comparison for priority queue in A*.
        Compares based on f value.
        """
        return self.f < other.f
    
    def __eq__(self, other):
        """
        Check if two nodes have the same state.
        """
        if not isinstance(other, Node):
            return False
        return self.state == other.state
    
    def __hash__(self):
        """
        Hash function based on state.
        """
        return hash(self.state)