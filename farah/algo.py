from collections import deque
from rush_hour_puzzle import RushHourPuzzle
from node import Node

def bfs(initial_state: RushHourPuzzle):    
    # Create initial node
    root = Node(state=initial_state, parent=None, action=None, g=0)
    
    # Check if already at goal
    if root.state.isGoal():
        return root
    
    # Initialize data structures
    open_queue = deque([root])
    closed = set()  # Only track states not nodes
    
    # For tracking performance
    nodes_expanded = 0
    
    # Main loop
    while open_queue:
        # Get next node (FIFO - shallowest first)
        current = open_queue.popleft()
        nodes_expanded += 1
        
        # Skip if already explored (can happen if we add same state from different parents)
        if current.state in closed:
            continue
            
        # Mark as explored NOW (after skipping duplicates)
        closed.add(current.state)
        
        # Get all possible moves from current state
        for action, successor_state in current.state.successorFunction():
            
            # Skip if already explored
            if successor_state in closed:
                continue
            
            # Create child node
            child = Node(
                state=successor_state,
                parent=current,
                action=action,
                g=current.g + 1
            )
            
            # Check if goal BEFORE adding to queue
            if child.state.isGoal():
                print(f"Solution found! Nodes expanded: {nodes_expanded}")
                print(f"Solution depth: {child.g} moves")
                return child
            
            # Add to queue
            open_queue.append(child)
    
    # No solution found
    print(f"No solution exists. Nodes expanded: {nodes_expanded}")
    return None