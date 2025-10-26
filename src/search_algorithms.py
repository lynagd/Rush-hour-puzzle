from collections import deque
import heapq
from node import Node
from rush_hour_puzzle import RushHourPuzzle 

def BFS(initial_state, max_nodes=100000):
    """Best BFS implementation combining all good features."""
    
    open_list = deque()
    closed_set = set()
    open_set = set()
    
    init_node = Node(initial_state, None, None)
    
    if initial_state.isGoal():
        print("BFS: Initial state is goal!")
        return init_node, 0
    
    # Use canonical_key for reliability
    init_key = initial_state.canonical_key()
    open_list.append(init_node)
    open_set.add(init_key)
    
    steps = 0
    
    while open_list:
        # Progress every 1000 nodes
        if steps > 0 and steps % 1000 == 0:
            print(f"BFS: {steps} nodes | open list size: {len(open_list)}")
        
        current = open_list.popleft()
        current_key = current.state.canonical_key()
        
        open_set.discard(current_key)
        closed_set.add(current_key)
        steps += 1
        
        # Safety limit
        if steps > max_nodes:
            print(f"BFS: Max nodes ({max_nodes}) reached. Try A*!")
            return None, steps
        
        for action, successor_state in current.state.successorFunction():
            child = Node(successor_state, current, action)
            child_key = successor_state.canonical_key()
            
            if child_key in closed_set or child_key in open_set:
                continue
            
            if successor_state.isGoal():
                print(f"BFS: Solution in {steps} steps!")
                return child, steps
            
            open_list.append(child)
            open_set.add(child_key)
    
    print("BFS: No solution found!")
    return None, steps

def heuristic_h1(state):
    """
    Heuristic 1: Distance from red car 'X' to the exit.
    """
    # Find the red car 'X'
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            # Use same exit as isGoal: leftmost x position for X should be board_width - 2
            target_x = state.board_width - 2
            current_x = vehicle['x']
            
            # Distance to exit (number of left/right moves needed)
            distance = target_x - current_x
            return max(0, distance)  # Never negative
    
    return 0


def heuristic_h2(state):
    """
    Heuristic 2: h1 + number of blocking vehicles.
    """
    h1 = heuristic_h1(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if not red_car:
        return h1
    
    # Count blocking vehicles (using a set to avoid double-counting)
    blocking_vehicles = set()
    red_y = red_car['y']
    # right-end index of red car (first cell to the right is red_x_end)
    red_x_end = red_car['x'] + red_car['length']
    # check every cell to the board edge (cells that must be cleared)
    for x in range(red_x_end, state.board_width):
        cell = state.board[red_y][x]
        if cell != '.' and cell != '#' and cell != 'X':
            blocking_vehicles.add(cell)
    
    return h1 + len(blocking_vehicles)


def heuristic_h3(state):
    """
    Heuristic 3: Enhanced heuristic considering blocking vehicles 
    and their mobility (proposed third heuristic).
    
    This heuristic adds penalties for:
    - Vehicles blocking the red car (h2)
    - Vehicles that are harder to move (blocked themselves)
    - Secondary blockers (vehicles blocking the primary blockers)
    """
    h2_value = heuristic_h2(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if not red_car:
        return h2_value
    
    # Additional penalty for deeply blocked vehicles
    penalty = 0
    red_y = red_car['y']
    red_x_end = red_car['x'] + red_car['length']
    target_x = state.board_width - 1
    
    # Find all blocking vehicles
    blocking_vehicle_ids = set()
    for x in range(red_x_end, target_x):
        if x < state.board_width:
            cell = state.board[red_y][x]
            if cell != '.' and cell != '#' and cell != 'X':
                blocking_vehicle_ids.add(cell)
    
    # Check blocking vehicles and their mobility
    for blocking_id in blocking_vehicle_ids:
        # Find this blocking vehicle
        for vehicle in state.vehicles:
            if vehicle['id'] == blocking_id:
                if vehicle['orientation'] == 'V':
                    # Vertical vehicle blocking horizontal path
                    # Check if it can move up or down
                    can_move_up = (vehicle['y'] > 0 and 
                                 state.board[vehicle['y'] - 1][vehicle['x']] == '.')
                    can_move_down = (vehicle['y'] + vehicle['length'] < state.board_height and 
                                   state.board[vehicle['y'] + vehicle['length']][vehicle['x']] == '.')
                    
                    if not (can_move_up or can_move_down):
                        # Vehicle is stuck, add higher penalty
                        penalty += 3
                    elif not can_move_up or not can_move_down:
                        # Vehicle can only move one direction
                        penalty += 1
                
                elif vehicle['orientation'] == 'H':
                    # Horizontal vehicle blocking (shouldn't happen but check anyway)
                    can_move_left = (vehicle['x'] > 0 and 
                                   state.board[vehicle['y']][vehicle['x'] - 1] == '.')
                    can_move_right = (vehicle['x'] + vehicle['length'] < state.board_width and 
                                    state.board[vehicle['y']][vehicle['x'] + vehicle['length']] == '.')
                    
                    if not (can_move_left or can_move_right):
                        penalty += 3
                    elif not can_move_left or not can_move_right:
                        penalty += 1
                break
    
    return h2_value + penalty

##changed 
def A_star(initial_state, heuristic_function=heuristic_h1):
    """
    A* Search algorithm following the course pseudocode (Figure 1.29).
    Uses a heuristic function to guide the search.
    
    Parameters:
    - initial_state: RushHourPuzzle instance
    - heuristic_function: Function to estimate cost to goal
    
    Returns:
    - goal_node: Node containing the goal state, or None
    - steps: Number of nodes expanded
    """
    # Open: priorityQueue /* Ordered queue by f */
    open_list = []
    
    # Closed: set for O(1) lookup
    closed_set = set()
    
    # For tracking nodes in open list (for efficient lookup and updates)
    open_dict = {}  # Maps state_hash -> node
    
    # Counter to break ties in priority queue (ensures FIFO for equal f-values)
    counter = 0
    
    # init_node <- Node (s, None, None)
    init_node = Node(initial_state, None, None)
    
    # init_node.f <- h(init_node)
    init_node.setF(heuristic_function)
    
    # if (isGoal(init_node.state)) then return init_node
    if initial_state.isGoal():
        print("A*: Initial state is goal!")
        return init_node, 0
    
    # Open.insert(init_node)
    heapq.heappush(open_list, (init_node.f, counter, init_node))
    counter += 1
    open_dict[hash(init_node.state)] = init_node
    
    steps = 0
    
    # while (not Open.empty()) do
    while open_list:
        # Show progress every 1000 nodes
        if steps > 0 and steps % 1000 == 0:
            print(f"A*: Expanded {steps} nodes, open list size: {len(open_list)}")
        
        # current <- Open.dequeue() /* Remove node with lowest f */
        _, _, current = heapq.heappop(open_list)
        current_hash = hash(current.state)
        
        # Skip if this state was already processed (can happen with duplicates in heap)
        if current_hash in closed_set:
            continue
        
        # Remove from open_dict
        if current_hash in open_dict:
            del open_dict[current_hash]
        
        # if (isGoal(current.state)) then return current
        if current.state.isGoal():
            print(f"A*: Solution found in {steps} steps!")
            return current, steps
        
        # Closed.add(current)
        closed_set.add(current_hash)
        steps += 1
        
        # for each (action, successor) in successorsFn(current.state) do
        for action, successor_state in current.state.successorFunction():
            # child <- Node (successor, current, action)
            child = Node(successor_state, current, action)
            
            # child.f <- child.g + h(child)
            child.setF(heuristic_function)
            
            child_hash = hash(child.state)
            
            # Skip if already in closed set
            if child_hash in closed_set:
                continue
            
            # if (child.state not in Open) then
            if child_hash not in open_dict:
                # Open.insert(child)
                heapq.heappush(open_list, (child.f, counter, child))
                counter += 1
                open_dict[child_hash] = child
            
            # else if (child.state in Open with a higher value of f) then
            else:
                old_node = open_dict[child_hash]
                # Replace if we found a better path
                if child.g < old_node.g:
                    # Update the existing node with better path
                    old_node.g = child.g
                    old_node.parent = child.parent
                    old_node.action = child.action
                    old_node.setF(heuristic_function)
                    
                    # Add updated node back to heap
                    # (old entry still in heap but will be skipped due to closed set check)
                    heapq.heappush(open_list, (old_node.f, counter, old_node))
                    counter += 1
    
    # return None
    print("A*: No solution found!")
    return None, steps