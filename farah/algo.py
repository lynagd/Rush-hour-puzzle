import heapq
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

def a_star(initial_state: RushHourPuzzle, heuristic):
    """
    A* Search algorithm for Rush Hour puzzle.
    
    A* uses f = g + h to prioritize nodes:
    - g: actual cost from start (number of moves)
    - h: estimated cost to goal (heuristic)
    - f: total estimated cost
    
    """
    
    # Create initial node
    init_node = Node(state=initial_state, parent=None, action=None, g=0)
    init_node.setF(heuristic)
    
    # Check if already at goal
    if init_node.state.isGoal():
        return init_node
    
    # Priority queue: stores (f_value, counter, node)
    # counter ensures FIFO order for nodes with same f value
    open_heap = []
    counter = 0
    heapq.heappush(open_heap, (init_node.f, counter, init_node))
    counter += 1
    
    # Track states in open list with their best f value for fast lookup
    open_dict = {initial_state: init_node.f}
    
    # Closed set: states we've fully explored
    closed = set()
    
    # For tracking performance
    nodes_expanded = 0
    max_queue_size = 1
    
    # Main loop
    while open_heap:
        # Track max queue size for statistics
        max_queue_size = max(max_queue_size, len(open_heap))
        
        # Get node with lowest f value (priority queue)
        f_val, _, current = heapq.heappop(open_heap)
        
        # Remove from open tracking dictionary
        if current.state in open_dict:
            del open_dict[current.state]
        
        nodes_expanded += 1
        
        # Skip if already explored
        if current.state in closed:
            continue
        
        # Check if goal
        if current.state.isGoal():
            print(f"A* Solution found! Nodes expanded: {nodes_expanded}")
            print(f"Solution depth: {current.g} moves")
            print(f"Max queue size: {max_queue_size}")
            return current
        
        # Mark as explored
        closed.add(current.state)
        
        # Generate successors
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
            child.setF(heuristic)
            
            # Check if this state is already in open with a better or equal path
            if successor_state in open_dict:
                if child.f >= open_dict[successor_state]:
                    # We already have a better or equal path to this state
                    continue
                # If we get here, this new path is better
                # The old node will be skipped when popped (by closed check)
            
            # Add to open list
            heapq.heappush(open_heap, (child.f, counter, child))
            open_dict[successor_state] = child.f
            counter += 1
    
    # No solution found
    print(f"No solution exists. Nodes expanded: {nodes_expanded}")
    return None