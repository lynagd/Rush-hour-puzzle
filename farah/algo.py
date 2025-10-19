from collections import deque
from rush_hour_puzzle import RushHourPuzzle
from node import Node

def bfs(initial_state: RushHourPuzzle):
    
    root = Node(state=initial_state, parent=None, action=None, g=0)
    
    # if (isGoal(init_node.state)) then return init_node
    if root.state.isGoal():
        return root
    
    # Open: queue (FIFO list)
    open_queue = deque([root])
    
    # Additional: Track states in Open for fast lookup (optimization)
    open_set = {initial_state}
    
    # Closed: list
    closed = set()
    
    # For tracking performance
    nodes_expanded = 0
    
    # while (not Open.empty()) do
    while open_queue:
        
        # current <- Open.dequeue()
        current = open_queue.popleft()
        open_set.remove(current.state)  # Remove from tracking set
        nodes_expanded += 1
        
        # Closed.add(current)
        closed.add(current.state)
        
        # for each (action, successor) in successorsFn(current.state) do
        for action, successor_state in current.state.successorFunction():
            
            # child <- Node (successor, current, action)
            child = Node(
                state=successor_state,
                parent=current,
                action=action,
                g=current.g + 1
            )
            
            # if (isGoal(child.state)) then return child
            if child.state.isGoal():
                print(f"Solution found! Nodes expanded: {nodes_expanded}")
                print(f"Solution depth: {child.g} moves")
                return child
            
            # if (child.state not in Closed and not in Open) then
            if child.state not in closed and child.state not in open_set:
                # Open.enqueue(child)
                open_queue.append(child)
                open_set.add(child.state)  # Track it
    
    # return None
    print(f"No solution exists. Nodes expanded: {nodes_expanded}")
    return None